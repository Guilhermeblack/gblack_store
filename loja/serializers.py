from rest_framework import serializers
from .models import Produto, Carrinho, CartItem, Cliente, Address, Venda, ItemVenda, FeedPost, PaymentTransaction

class FeedPostSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    class Meta:
        model = FeedPost
        fields = ['id', 'title', 'content', 'image', 'image_url', 'products', 'scheduled_date', 'is_published', 'created_at']

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def get_products(self, obj):
        from .serializers import ProdutoSerializer
        return ProdutoSerializer(obj.products.all(), many=True).data

class ProdutoSerializer(serializers.ModelSerializer):
    current_price = serializers.DecimalField(source='get_current_price', max_digits=10, decimal_places=2, read_only=True)
    img_prod_url = serializers.SerializerMethodField()

    class Meta:
        model = Produto
        fields = ['id', 'nome', 'descricao', 'preco', 'current_price', 'img_prod', 'img_prod_url', 'tipo', 'estoque', 'is_available']

    def get_img_prod_url(self, obj):
        if obj.img_prod:
            return obj.img_prod.url
        return None

class CartItemSerializer(serializers.ModelSerializer):
    produto = ProdutoSerializer(read_only=True)
    subtotal = serializers.DecimalField(source='get_subtotal', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'produto', 'quantidade', 'subtotal']

class CarrinhoSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(source='get_total', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Carrinho
        fields = ['id', 'items', 'total']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cliente
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'cpf', 'telefone', 'addresses', 'is_staff']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = Cliente(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class ItemVendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemVenda
        fields = ['produto_nome', 'preco_unitario', 'quantidade', 'get_subtotal']

class VendaSerializer(serializers.ModelSerializer):
    items = ItemVendaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Venda
        fields = ['id', 'status', 'total', 'created_at', 'items', 'observacao']

class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = ['id', 'amount', 'method', 'status', 'transaction_id', 'created_at']
