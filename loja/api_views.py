from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Produto, Carrinho, CartItem, Cliente, Address, Venda, FeedPost
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
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        products = Produto.objects.filter(is_available=True)[:5]
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

class CarrinhoViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        carrinho, _ = Carrinho.objects.get_or_create(cliente=request.user)
        serializer = CarrinhoSerializer(carrinho)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        produto = get_object_or_404(Produto, pk=product_id)
        
        if produto.estoque < quantity:
            return Response({'error': 'Estoque insuficiente'}, status=status.HTTP_400_BAD_REQUEST)
            
        carrinho, _ = Carrinho.objects.get_or_create(cliente=request.user)
        cart_item, created = CartItem.objects.get_or_create(carrinho=carrinho, produto=produto)
        
        if not created:
            cart_item.quantidade += quantity
        else:
            cart_item.quantidade = quantity
            
        cart_item.save()
        
        return Response(CarrinhoSerializer(carrinho).data)

    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        item_id = request.data.get('item_id')
        carrinho = get_object_or_404(Carrinho, cliente=request.user)
        item = get_object_or_404(CartItem, pk=item_id, carrinho=carrinho)
        item.delete()
        return Response(CarrinhoSerializer(carrinho).data)
        
    @action(detail=False, methods=['post'])
    def update_quantity(self, request):
        item_id = request.data.get('item_id')
        quantity = int(request.data.get('quantity', 1))
        
        carrinho = get_object_or_404(Carrinho, cliente=request.user)
        item = get_object_or_404(CartItem, pk=item_id, carrinho=carrinho)
        
        if quantity > 0:
            item.quantidade = quantity
            item.save()
        else:
            item.delete()
            
        return Response(CarrinhoSerializer(carrinho).data)

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
