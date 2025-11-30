from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from . import models, forms
import json

@login_required(login_url='index')
def checkout_cart(request):
    try:
        carrinho = request.user.carrinho
    except models.Carrinho.DoesNotExist:
        carrinho = models.Carrinho.objects.create(cliente=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        item_id = request.POST.get('item_id')
        
        if action == 'update_qty':
            qty = int(request.POST.get('quantity', 1))
            item = get_object_or_404(models.CartItem, id=item_id, carrinho=carrinho)
            if qty > 0:
                item.quantidade = qty
                item.save()
            else:
                item.delete()
        elif action == 'remove':
            item = get_object_or_404(models.CartItem, id=item_id, carrinho=carrinho)
            item.delete()
            
        return redirect('checkout_cart')

    return render(request, 'checkout_cart.html', {'carrinho': carrinho})

@login_required(login_url='index')
def checkout_address(request):
    if request.method == 'POST':
        # Simple address handling for now - creating a new one every time or selecting existing
        # In a real app, we'd have a form to select or add.
        # Here we'll just process the form data to create an address
        
        address = models.Address.objects.create(
            cliente=request.user,
            street=request.POST.get('street'),
            number=request.POST.get('number'),
            complement=request.POST.get('complement'),
            neighborhood=request.POST.get('neighborhood'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            zip_code=request.POST.get('zip_code')
        )
        
        # Store address ID in session to use in next step
        request.session['checkout_address_id'] = address.id
        return redirect('checkout_payment')

    addresses = request.user.addresses.all()
    return render(request, 'checkout_address.html', {'addresses': addresses})

@login_required(login_url='index')
def checkout_payment(request):
    address_id = request.session.get('checkout_address_id')
    if not address_id:
        messages.warning(request, "Por favor, selecione um endereço de entrega.")
        return redirect('checkout_address')
        
    try:
        carrinho = request.user.carrinho
        if not carrinho.items.exists():
             messages.warning(request, "Seu carrinho está vazio.")
             return redirect('checkout_cart')
    except models.Carrinho.DoesNotExist:
        return redirect('index')

    return render(request, 'checkout_payment.html', {
        'carrinho': carrinho,
        'total': carrinho.get_total()
    })

@login_required(login_url='index')
def process_payment(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid method'})
        
    try:
        data = json.loads(request.body)
        payment_method = data.get('method')
        
        carrinho = request.user.carrinho
        address_id = request.session.get('checkout_address_id')
        address = models.Address.objects.get(id=address_id)
        
        with transaction.atomic():
            # 1. Create Venda
            venda = models.Venda.objects.create(
                cliente=request.user,
                address=address,
                total=carrinho.get_total(),
                status='PAID' # Simulating immediate success
            )
            
            # 2. Move items from Cart to ItemVenda
            for item in carrinho.items.all():
                models.ItemVenda.objects.create(
                    venda=venda,
                    produto=item.produto,
                    produto_nome=item.produto.nome,
                    preco_unitario=item.produto.preco,
                    quantidade=item.quantidade
                )
                # Decrement stock
                item.produto.estoque -= item.quantidade
                item.produto.save()
            
            # 3. Create PaymentTransaction
            models.PaymentTransaction.objects.create(
                venda=venda,
                amount=venda.total,
                method=payment_method,
                status='APPROVED',
                transaction_id=f'SIM-{venda.id}-123456'
            )
            
            # 4. Clear Cart
            carrinho.items.all().delete()
            
            return JsonResponse({'success': True, 'redirect_url': '/checkout/success'})
            
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required(login_url='index')
def checkout_success(request):
    return render(request, 'checkout_success.html')
