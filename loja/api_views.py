from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Produto, Carrinho, CartItem, Cliente, Address, Venda, FeedPost, ItemVenda
from .serializers import (
    ProdutoSerializer, CarrinhoSerializer, CartItemSerializer, 
    ClienteSerializer, AddressSerializer, VendaSerializer, FeedPostSerializer
)

class FeedViewSet(viewsets.ModelViewSet):
    queryset = FeedPost.objects.all().order_by('-scheduled_date')
    serializer_class = FeedPostSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Produto.objects.all()
        return Produto.objects.filter(is_available=True)
    
    @action(detail=True, methods=['get'])
    def related(self, request, pk=None):
        """Retorna produtos relacionados (mesmo tipo)"""
        product = self.get_object()
        related_products = Produto.objects.filter(
            tipo=product.tipo, 
            is_available=True
        ).exclude(id=product.id)[:4]
        serializer = self.get_serializer(related_products, many=True)
        return Response(serializer.data)

class CarrinhoViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny] # Allow guests

    def get_cart(self, request):
        if request.user.is_authenticated:
            carrinho, _ = Carrinho.objects.get_or_create(cliente=request.user)
        else:
            session_id = request.headers.get('X-Guest-ID')
            if not session_id:
                return None
            carrinho, _ = Carrinho.objects.get_or_create(session_id=session_id)
        return carrinho

    def list(self, request):
        carrinho = self.get_cart(request)
        if not carrinho:
            return Response({'items': [], 'total': 0})
        serializer = CarrinhoSerializer(carrinho)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        from django.db import transaction
        
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        # Validate Guest ID if not authenticated
        if not request.user.is_authenticated and not request.headers.get('X-Guest-ID'):
             return Response({'error': 'Guest ID required for guest users'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # Lock product row
                produto = Produto.objects.select_for_update().get(pk=product_id)
                
                if not produto.is_available:
                     return Response({'error': 'Produto indisponível'}, status=status.HTTP_400_BAD_REQUEST)

                if produto.estoque < quantity:
                    return Response({'error': 'Estoque insuficiente'}, status=status.HTTP_400_BAD_REQUEST)
                
                carrinho = self.get_cart(request)
                cart_item, created = CartItem.objects.get_or_create(carrinho=carrinho, produto=produto)
                
                if not created:
                    cart_item.quantidade += quantity
                else:
                    cart_item.quantidade = quantity
                    
                cart_item.save()
                
                # Decrement stock immediately
                produto.estoque -= quantity
                produto.save()
                
                return Response(CarrinhoSerializer(carrinho).data)
        except Produto.DoesNotExist:
            return Response({'error': 'Produto não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        from django.db import transaction
        item_id = request.data.get('item_id')
        
        carrinho = self.get_cart(request)
        if not carrinho:
             return Response({'error': 'Carrinho não encontrado'}, status=status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                item = get_object_or_404(CartItem, pk=item_id, carrinho=carrinho)
                
                # Restore stock
                produto = Produto.objects.select_for_update().get(pk=item.produto.id)
                produto.estoque += item.quantidade
                produto.save()
                
                item.delete()
                return Response(CarrinhoSerializer(carrinho).data)
        except Exception as e:
             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['post'])
    def update_quantity(self, request):
        from django.db import transaction
        item_id = request.data.get('item_id')
        new_quantity = int(request.data.get('quantity', 1))
        
        carrinho = self.get_cart(request)
        if not carrinho:
             return Response({'error': 'Carrinho não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            with transaction.atomic():
                item = get_object_or_404(CartItem, pk=item_id, carrinho=carrinho)
                produto = Produto.objects.select_for_update().get(pk=item.produto.id)
                
                diff = new_quantity - item.quantidade
                
                if diff > 0: # Increasing quantity
                    if produto.estoque < diff:
                        return Response({'error': 'Estoque insuficiente'}, status=status.HTTP_400_BAD_REQUEST)
                    produto.estoque -= diff
                elif diff < 0: # Decreasing quantity
                    produto.estoque += abs(diff)
                
                produto.save()
                
                if new_quantity > 0:
                    item.quantidade = new_quantity
                    item.save()
                else:
                    item.delete()
                    
                return Response(CarrinhoSerializer(carrinho).data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_queryset(self):
        if self.action == 'create':
            return Cliente.objects.all()
        return Cliente.objects.filter(id=self.request.user.id)
        
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(cliente=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(cliente=self.request.user)

class VendaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VendaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Venda.objects.all().order_by('-created_at')
        return Venda.objects.filter(cliente=self.request.user).order_by('-created_at')

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def update_status(self, request, pk=None):
        venda = self.get_object()
        status_venda = request.data.get('status')
        if status_venda:
            venda.status = status_venda
            venda.save()
            return Response(VendaSerializer(venda).data)
        return Response({'error': 'Status not provided'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        """
        Processa o checkout:
        1. Valida endereço
        2. Valida estoque
        3. Cria Venda
        4. Move itens do carrinho para Venda
        5. Processa pagamento (simulado)
        6. Limpa carrinho
        """
        from django.db import transaction
        from .models import PaymentTransaction
        
        address_id = request.data.get('address_id')
        payment_method = request.data.get('payment_method')
        
        if not address_id:
            return Response({'error': 'Endereço não fornecido'}, status=status.HTTP_400_BAD_REQUEST)
            
        if not payment_method:
            return Response({'error': 'Método de pagamento não fornecido'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            address = Address.objects.get(pk=address_id, cliente=request.user)
        except Address.DoesNotExist:
            return Response({'error': 'Endereço inválido'}, status=status.HTTP_400_BAD_REQUEST)
            
        carrinho = get_object_or_404(Carrinho, cliente=request.user)
        if not carrinho.items.exists():
            return Response({'error': 'Carrinho vazio'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            with transaction.atomic():
                # 1. Create Venda
                venda = Venda.objects.create(
                    cliente=request.user,
                    address=address,
                    total=carrinho.get_total(),
                    status='PAID' # Simulating immediate success for now
                )
                
                # 2. Move items from Cart to ItemVenda
                for item in carrinho.items.all():
                    # Valida disponibilidade do produto
                    if not item.produto.is_available:
                        raise Exception(f'Produto {item.produto.nome} não está mais disponível')
                    
                    if item.produto.estoque < item.quantidade:
                        raise Exception(f'Estoque insuficiente para {item.produto.nome}')
                    
                    # Usa preço com desconto se houver
                    preco_atual = item.produto.get_current_price()
                    
                    ItemVenda.objects.create(
                        venda=venda,
                        produto=item.produto,
                        produto_nome=item.produto.nome,
                        preco_unitario=preco_atual,
                        quantidade=item.quantidade
                    )
                    # Decrement stock
                    item.produto.estoque -= item.quantidade
                    item.produto.save()
                
                # 3. Create PaymentTransaction
                PaymentTransaction.objects.create(
                    venda=venda,
                    amount=venda.total,
                    method=payment_method,
                    status='APPROVED',
                    transaction_id=f'SIM-{venda.id}-123456'
                )
                
                # 4. Clear Cart
                carrinho.items.all().delete()
                
                return Response({
                    'success': True,
                    'venda_id': venda.id,
                    'message': 'Pedido realizado com sucesso!'
                })
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
