from django.db import models
from cloudinary.models import CloudinaryField
from django.utils.timezone import now
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

class Cliente(AbstractUser):
    # AbstractUser already has username, email, first_name, last_name, etc.
    # We can add extra fields here.
    
    id = models.BigAutoField(primary_key=True)
    loja = models.BooleanField(default=False)
    
    # Using email as unique identifier is good practice, but AbstractUser uses username by default.
    # We will keep username but enforce email uniqueness.
    email = models.EmailField(unique=True, null=False, blank=False)
    
    cpf = models.CharField(
        max_length=16,
        null=True,
        blank=False,
        unique=True,
    )
    telefone = models.CharField(
        max_length=20,
        null=True,
        blank=False,
    )
    
    # REQUIRED_FIELDS must contain all required fields on top of USERNAME_FIELD
    # USERNAME_FIELD = 'username' (default)
    REQUIRED_FIELDS = ['email', 'cpf']

    def __str__(self):
        return self.username

class Address(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=20)
    complement = models.CharField(max_length=100, blank=True, null=True)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2) # UF
    zip_code = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.street}, {self.number} - {self.city}/{self.state}"

class Produto(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100, null=False, blank=False)
    descricao = models.TextField(null=True, blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    img_prod = CloudinaryField('image', blank=True, null=True)
    
    STATUS_CHOICES = (
        ("R", "Relogio"),
        ("A", "Acessorio"),
        ("V", "Vestuario"),
    )
    tipo = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        blank=False,
        null=False
    )
    estoque = models.IntegerField(validators=[MinValueValidator(0)])
    is_available = models.BooleanField(default=True, verbose_name="Disponível")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_current_price(self):
        """Retorna o preço atual considerando descontos ativos"""
        from django.utils import timezone
        now = timezone.now()
        
        # Busca desconto ativo
        active_discount = self.discounts.filter(
            is_active=True,
            start_date__lte=now,
            end_date__gte=now
        ).first()
        
        if active_discount:
            discount_amount = self.preco * (active_discount.discount_percent / 100)
            return self.preco - discount_amount
        return self.preco

    def __str__(self):
        return self.nome

class StoreConfig(models.Model):
    """Configurações gerais da loja"""
    cart_expiration_days = models.PositiveIntegerField(
        default=3,
        verbose_name="Dias para expiração do carrinho",
        help_text="Número de dias que um item fica reservado no carrinho antes de voltar ao estoque."
    )
    
    class Meta:
        verbose_name = "Configuração da Loja"
        verbose_name_plural = "Configurações da Loja"

    def save(self, *args, **kwargs):
        if not self.pk and StoreConfig.objects.exists():
            # Force singleton
            return
        super().save(*args, **kwargs)

    def __str__(self):
        return "Configuração da Loja"

class Carrinho(models.Model):
    cliente = models.OneToOneField(
        Cliente,
        on_delete=models.CASCADE,
        related_name="carrinho",
        null=True,
        blank=True
    )
    session_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total(self):
        return sum(item.get_subtotal() for item in self.items.all())
        
    def __str__(self):
        if self.cliente:
            return f"Carrinho de {self.cliente.username}"
        return f"Carrinho Visitante {self.session_id}"

class CartItem(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, related_name="items")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    
    def get_subtotal(self):
        return self.produto.get_current_price() * self.quantidade

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"

class Venda(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pendente"),
        ("PAID", "Pago"),
        ("SHIPPED", "Enviado"),
        ("DELIVERED", "Entregue"),
        ("CANCELED", "Cancelado")
    )

    id = models.BigAutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="vendas")
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )
    
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Venda #{self.id} - {self.cliente.username}"

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name="items")
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True)
    produto_nome = models.CharField(max_length=100) # Snapshot in case product is deleted
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2) # Snapshot price
    quantidade = models.PositiveIntegerField()
    
    def get_subtotal(self):
        return self.preco_unitario * self.quantidade

class PaymentTransaction(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ("PIX", "Pix"),
        ("CARD", "Cartão de Crédito"),
        ("BOLETO", "Boleto"),
    )
    STATUS_CHOICES = (
        ("PENDING", "Pendente"),
        ("APPROVED", "Aprovado"),
        ("FAILED", "Falhou"),
    )
    
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    transaction_id = models.CharField(max_length=100, blank=True, null=True) # External ID
    created_at = models.DateTimeField(auto_now_add=True)

class Leads(models.Model):
    id = models.BigAutoField(primary_key=True)
    email_lead = models.EmailField(max_length=70, blank=True, unique=True)
    ip_lead = models.GenericIPAddressField(null=True)
    endereco = models.CharField(max_length=200, null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    nome = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class FeedPost(models.Model):
    """Posts do feed para orientações e novidades sobre produtos"""
    title = models.CharField(max_length=200, verbose_name="Título")
    content = models.TextField(verbose_name="Conteúdo")
    image = CloudinaryField('image', blank=True, null=True)
    products = models.ManyToManyField(
        'Produto',
        blank=True,
        related_name='feed_posts',
        verbose_name="Produtos Vinculados"
    )
    scheduled_date = models.DateTimeField(verbose_name="Data de Publicação")
    is_published = models.BooleanField(default=False, verbose_name="Publicado")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scheduled_date']
        verbose_name = "Post do Feed"
        verbose_name_plural = "Posts do Feed"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """Auto-publica posts cuja data de agendamento já passou"""
        from django.utils import timezone
        if self.scheduled_date <= timezone.now():
            self.is_published = True
        super().save(*args, **kwargs)


class ProductDiscount(models.Model):
    """Descontos programados para produtos"""
    produto = models.ForeignKey(
        Produto, 
        on_delete=models.CASCADE, 
        related_name='discounts',
        verbose_name="Produto"
    )
    discount_percent = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Desconto (%)"
    )
    start_date = models.DateTimeField(verbose_name="Data de Início")
    end_date = models.DateTimeField(verbose_name="Data de Término")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = "Desconto de Produto"
        verbose_name_plural = "Descontos de Produtos"
    
    def __str__(self):
        return f"{self.produto.nome} - {self.discount_percent}% ({self.start_date.strftime('%d/%m/%Y')} - {self.end_date.strftime('%d/%m/%Y')})"
    
    def is_currently_active(self):
        """Verifica se o desconto está ativo no momento"""
        from django.utils import timezone
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date
