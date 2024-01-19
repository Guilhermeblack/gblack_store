from datetime import date

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from decimal import Decimal, ROUND_DOWN
from loja import forms,models
from gbstr import settings
from loja.widgets import oauth2_client, servico_cobranca
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
import validate_docbr as docbr
import requests
from django.contrib.auth.hashers import make_password, check_password, BCryptPasswordHasher, pbkdf2
from django.contrib.auth import logout, login, authenticate, get_user
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import Permission
from pprint import pprint
import cloudinary
from django.views.decorators.csrf import csrf_protect

# Session.objects.all().delete()
def term_condition(request):
    return render(request, 'privacy_policy_gb.html')


def index(request):

    if request.POST:
        rq = request.POST
    # print(' >>>', request.POST)
        pprint(request.POST)
        if 'senha_rep' in rq and rq['senha_rep'] == rq['senha']:
            doc = [(docbr.CPF, rq['cpf'])]
            if docbr.validate_docs(doc):
                # print('validooou')
                password = make_password(rq['senha'], salt=None, hasher='pbkdf2_sha256')
                usr = forms.cria_usr(rq)
                # usr['senha'].value = password
                # pprint(usr)
                # print(usr.errors)
                if usr.is_valid():
                    cli = usr.save()
                    cart = models.Carrinho.objects.create(
                        cliente_cli=cli
                    )
                    cart.save()

                    login(request,cli)
                    print('logou')
                    messages.info(request, ' Usuário criado')
                return redirect(settings.LOGIN_REDIRECT_URL, permanent=True)
            else:
                messages.warning(request, 'CPF/CNPJ inválidos')
                return redirect(settings.LOGIN_REDIRECT_URL, permanent=True)
        elif 'nome_log' in rq:

            try:
                encod = models.Cliente.objects.get(email=rq['nome_log'])
            except ObjectDoesNotExist:
                encod = None

            pprint(encod)
            # print(encod.errors)
            if encod is not None and encod.check_password(rq['senha']):
                login(request, encod)
                messages.info(request, ' Bem vindo')
                return redirect(settings.LOGIN_REDIRECT_URL, permanent=True)
            else:
                messages.info(request, 'Usuário inexistente/Bloqueado')
                return redirect(settings.LOGIN_REDIRECT_URL, permanent=True)
    if request.user.is_authenticated:
        carrinho = models.Carrinho.objects.get(cliente_cli= request.user.id)
        pprint(carrinho.id)
        pedido = models.Tot_ped.objects.filter(carrinho=carrinho.id)
        pprint(pedido)
    else:
        pedido =[]

    if models.Produto.objects.all() is None:
        pdt = []
    else:
        pdt =models.Produto.objects.all().order_by('tipo')

    return render(request,
                  'index.html',
                  {
                    'criar': forms.cria_usr,
                    'pedidos': pedido,
                    'logar': forms.autForm,
                    # 'prod': forms.produtoform,
                    'produtos': pdt,
                    'prodtipo': models.Produto.STATUS_CHOICES
                  })

@login_required(login_url='index')
def logoutuser(request):
    logout(request)
    return redirect('index')

@login_required(login_url='index')
def conta(request):

    if request.POST:
        rq = request.POST
        pprint(rq)
        if 'lojasim' in rq:
            usr = models.Cliente.objects.get(pk=request.user.id)
            usr.loja = True
            pprint(usr)
            usr.save()
            messages.info(request,' Agora é uma loja')
        elif 'exc_prod' in rq:
            prod = models.Produto.objects.exclude(pk=rq['exc_prod'])

            prod.save()
            messages.info(request,' Excluido')
        elif 'tipo' in rq:
            # rq['img_prod'] = 'gbstr/'+rq['img_prod']
            pprint(request.FILES)
            print('entro pdsadasdkasd´sadas')

            if request.FILES:
                rf = request.FILES
                prod = forms.produtoform(rq,rf)
                pprint(prod)
                print('produto aqqq')
            else:
                prod = forms.produtoform(rq)
            pprint(prod)
            if prod.is_valid():

                cloudinary.uploader.upload(rf['img_prod'], folder="gbstr")
                prod.save()
                print('salvo prod')
                messages.info(request, 'Produto cadastrado')
            else:
                print(prod.errors)
                messages.info(request, 'Produto não cadastrado')
            return redirect(settings.LOGIN_REDIRECT_URL, permanent=True)

    # pprint(client)

    clent = models.Cliente.objects.get(pk=request.user.id)
    cart = models.Carrinho.objects.get(cliente_cli=clent.id)
    prods = models.Produto.objects.all()
    # pprint(clent)
    # pprint(cart)

    # if len(cart) isArray:
    #     cart = [cart]
    # pprint(cart.produto_cli)
    # pprint(prods)
    return render(
        request,
        'conta.html',
        {
            'prod': forms.produtoform,
            # 'userform':forms.cria_usr(),
            'usuario': clent,
            'carrinho': cart,
            # 'totalpedido': models.Tot_ped.objects.all(),
            # 'venda': models.Venda.objects.all(),
            'produtos': prods,
            # 'pagamento': models.Pagamentos.objects.all(),
            'prodtipo': models.Produto.STATUS_CHOICES

        }
    )

def prod(request):

    if request.POST:
        pprint(request.POST)
        rq =request.POST
        if 'proid' in rq:
            pdt = models.Produto.objects.get(pk=rq['proid'])
        if 'add_carrinho' in rq:
            cli = models.Cliente.objects.get(id=request.user.id)

            prod = models.Produto.objects.get(pk=request.POST['add_carrinho'])
            if prod.estoque <=0:
                messages.warning(request, 'estoque indisponível')
                return HttpResponse(prod.estoque)

            prod.estoque -= 1
            prod.save()
            carrinho = models.Carrinho.objects.get(cliente_cli=cli.id)
            pprint(carrinho.produto_cli.all())

            if prod not in carrinho.produto_cli.all():
                carrinho.produto_cli.add(prod)
                ped = models.Tot_ped.objects.create(
                    carrinho=carrinho,
                    produto_carrinho=prod
                )
            else:
                ped = models.Tot_ped.objects.get(produto_carrinho=prod.id)
            carrinho.valor += prod.preco
            carrinho.save()

            ped.quantidade +=1
            ped.save()

            pedido = models.Tot_ped.objects.filter(carrinho= carrinho.id)
            messages.info(request, 'Pedido Feito')
            print('deu tudo')
            return HttpResponse(prod.estoque)

        elif 'pdt_nome' in rq and rq['pdt_nome'] != '':
            pdt.nome = rq['pdt_nome']
            pdt.save()
        elif 'pdt_est' in rq and rq['pdt_est'] != '':
            pprint(rq['pdt_est'])
            pdt.estoque = int(rq['pdt_est'])
            pdt.save()
        elif 'pdt_des' in rq and rq['pdt_des'] != '':
            pprint(rq['pdt_des'])
            pdt.descricao = rq['pdt_des']
            pdt.save()
        elif 'pdt_tipo' in rq and rq['pdt_tipo'] != '':
            pprint(pdt.tipo)
            obj = models.Produto.objects.filter(pk=rq['proid'])
            opc = models.Produto.STATUS_CHOICES
            for p in opc:
                if p[0] == rq['pdt_tipo']:
                    obj.update(tipo=p[0])

        elif 'pdt_pre' in rq and rq['pdt_pre'] != '':
            pdt.preco = rq['pdt_pre']
            pdt.save()
        elif 'btn_del' in rq and rq['btn_del'] != '':
            pdt.delete()
            pdt.save()
        clent = models.Cliente.objects.get(pk=request.user.id)
        cart = models.Carrinho.objects.get(cliente_cli=clent.id)
        prods = models.Produto.objects.all()
        return render(
            request,
            'conta.html',
            {
                'prod': forms.produtoform,
                # 'userform':forms.cria_usr(),
                'usuario': clent,
                'carrinho': cart,
                # 'totalpedido': models.Tot_ped.objects.all(),
                # 'venda': models.Venda.objects.all(),
                'produtos': prods,
                # 'pagamento': models.Pagamentos.objects.all(),
                'prodtipo': models.Produto.STATUS_CHOICES

            }
        )
    return redirect(settings.LOGIN_REDIRECT_URL, permanent=True)  # enviar para as comandas


@csrf_protect
def pagamento(request):


    if request.POST:
        # print(' >>>', request.POST)
        # print(' >>>', request.POST['tipo_pagamento'])

        if request.POST['tipo_pagamento'] == 'pix':
            # pag = widgets get_qrcode(request.POST.valor_pagamento, request.POST.usuario);
            cliente = str(request.POST['usuario'])
            valor = formata_valor(request.POST['valor_pagamento']);

            cob = servico_cobranca.GerencianetService.create_pix_charge(amount=valor, chave_pix='40844509876', cliente=cliente )
            txid = cob.get('txid')
            qr_code = servico_cobranca.GerencianetService.get_qr_code(txid)

            print('qr_code', qr_code)
            response_data = {
                'qr_code': qr_code.get('qrcode'),
                'qr_code_imagem': qr_code.get('imagemQrcode'),
                'qr_code_link': qr_code.get('linkVisualizacao')
            }
            return JsonResponse(response_data)
        else:
            pass
            # pag = widgets get_card(request.POST.valor_pagamento, request.POST.usuario);
        pass




    clent = models.Cliente.objects.get(pk=request.user.id)
    cart = models.Carrinho.objects.get(cliente_cli=clent.id)
    prods = models.Produto.objects.all()

    # if len(cart) isArray:
    #     cart = [cart]
    # pprint(cart.produto_cli)
    # pprint(prods)
    return render(
        request,
        'conta.html',
        {
            'prod': forms.produtoform,
            # 'userform':forms.cria_usr(),
            'usuario': clent,
            'carrinho': cart,
            # 'totalpedido': models.Tot_ped.objects.all(),
            # 'venda': models.Venda.objects.all(),
            'produtos': prods,
            # 'pagamento': models.Pagamentos.objects.all(),
            'prodtipo': models.Produto.STATUS_CHOICES

        }
    )

def formata_valor(val):

    valor = str(val).replace('.', '')
    valor = float(valor.replace(',', '.'))
    valor = f"{valor:.2f}"
    return valor