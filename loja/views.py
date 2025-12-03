import json
from datetime import date

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from decimal import Decimal
from loja import forms, models
from gbstr import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
import requests
import cloudinary
from pprint import pprint

# Session.objects.all().delete()
def term_condition(request):
    return render(request, 'privacy_policy_gb.html')

def index(request):
    if request.method == 'POST':
        rq = request.POST
        if 'senha_rep' in rq: # Registration
            usr_form = forms.cria_usr(rq)
            if usr_form.is_valid():
                cli = usr_form.save()
                # Create Cart
                models.Carrinho.objects.create(cliente=cli)
                
                login(request, cli)
                messages.info(request, 'Usuário criado com sucesso')
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                for field, errors in usr_form.errors.items():
                    for error in errors:
                        messages.warning(request, f"{field}: {error}")
                return redirect('index')
                
        elif 'nome_log' in rq: # Login
            form = forms.autForm(rq)
            if form.is_valid():
                username = form.cleaned_data['nome_log']
                password = form.cleaned_data['senha']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, 'Bem vindo')
                    return redirect(settings.LOGIN_REDIRECT_URL)
                else:
                    messages.warning(request, 'Usuário ou senha inválidos')
                    return redirect('index')
        
        elif 'email_lead' in rq: # Lead
            cli_ip = obter_ip(request)
            # geoloc = obter_geolocalizacao_ip(cli_ip) # Optional: enable if needed
            
            models.Leads.objects.create(
                email_lead=rq.get('email_lead'),
                ip_lead=cli_ip,
                nome=rq.get('nome_lead'),
                telefone=rq.get('telefone_lead')
            )
            messages.info(request, 'Obrigado pelo interesse!')
            return redirect('index')

    # Context for GET
    pedido = []
    if request.user.is_authenticated:
        try:
            carrinho = request.user.carrinho
            pedido = carrinho.items.all()
        except models.Carrinho.DoesNotExist:
            models.Carrinho.objects.create(cliente=request.user)
            pedido = []

    # Filtra apenas produtos disponíveis
    produtos = models.Produto.objects.filter(is_available=True).order_by('tipo')

    return render(request, 'index.html', {
        'criar': forms.cria_usr(),
        'pedidos': pedido,
        'logar': forms.autForm(),
        'produtos': produtos,
        'prodtipo': models.Produto.STATUS_CHOICES
    })

@login_required(login_url='index')
def logoutuser(request):
    logout(request)
    return redirect('index')

@login_required(login_url='index')
def conta(request):
    if request.method == 'POST':
        rq = request.POST
        if 'lojasim' in rq:
            request.user.loja = True
            request.user.save()
            messages.info(request, 'Agora você é uma loja!')
            return redirect('conta')
            
        elif 'exc_prod' in rq:
            # Logic to exclude product seems weird in original code (exclude(pk=rq['exc_prod'])).
            # Assuming it meant delete.
            try:
                prod = models.Produto.objects.get(pk=rq['exc_prod'])
                prod.delete()
                messages.info(request, 'Produto excluído')
            except models.Produto.DoesNotExist:
                pass
            return redirect('conta')
            
        elif 'tipo' in rq: # Add Product
            if request.FILES:
                prod_form = forms.produtoform(rq, request.FILES)
                if prod_form.is_valid():
                    prod = prod_form.save(commit=False)
                    cloudinary.uploader.upload(request.FILES['img_prod'], folder="gbstr")
                    prod.save()
                    messages.info(request, 'Produto cadastrado')
                else:
                    messages.warning(request, 'Erro ao cadastrar produto')
            return redirect('conta')

    try:
        carrinho = request.user.carrinho
    except models.Carrinho.DoesNotExist:
        carrinho = models.Carrinho.objects.create(cliente=request.user)

    prods = models.Produto.objects.all()
    
    return render(request, 'conta.html', {
        'prod': forms.produtoform(),
        'usuario': request.user,
        'carrinho': carrinho,
        'produtos': prods,
        'prodtipo': models.Produto.STATUS_CHOICES,
        'vendas': request.user.vendas.all().order_by('-created_at')
    })

@login_required(login_url='index')
def prod(request):
    if request.method == 'POST':
        rq = request.POST
        
        if 'add_carrinho' in rq:
            prod_id = rq['add_carrinho']
            prod = get_object_or_404(models.Produto, pk=prod_id)
            
            if prod.estoque <= 0:
                messages.warning(request, 'Estoque indisponível')
                return redirect('index') # Or wherever

            carrinho, _ = models.Carrinho.objects.get_or_create(cliente=request.user)
            
            cart_item, created = models.CartItem.objects.get_or_create(
                carrinho=carrinho,
                produto=prod
            )
            
            if not created:
                cart_item.quantidade += 1
                cart_item.save()
            
            messages.info(request, 'Produto adicionado ao carrinho')
            return redirect('index') # Or stay on page

        # Product editing logic (simplified)
        elif 'proid' in rq:
            pdt = get_object_or_404(models.Produto, pk=rq['proid'])
            if 'pdt_nome' in rq: pdt.nome = rq['pdt_nome']
            if 'pdt_est' in rq: pdt.estoque = int(rq['pdt_est'])
            if 'pdt_des' in rq: pdt.descricao = rq['pdt_des']
            if 'pdt_pre' in rq: pdt.preco = rq['pdt_pre']
            if 'btn_del' in rq: pdt.delete(); return redirect('conta')
            pdt.save()
            return redirect('conta')

    return redirect('index')

def pagamento(request):
    # Deprecated or redirect to new checkout
    return redirect('checkout_payment')

def formata_valor(val):
    valor = str(val).replace('.', '')
    valor = float(valor.replace(',', '.'))
    return valor

def obter_ip(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if not ip:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def obter_geolocalizacao_ip(ip):
    # Placeholder
    return {}