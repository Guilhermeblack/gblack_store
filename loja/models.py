from django.db import models
from cloudinary.models import CloudinaryField
from django.utils.timezone import now
from django.utils.translation import ugettext as _
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin,AbstractUser
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

# class User_cria(PermissionsMixin, BaseUserManager):
#
#     def create_user(self, *args, **kwargs):
#         email = kwargs["nome"]
#         email = self.normalize_email(email)
#         password = kwargs["password"]
#         kwargs.pop("password")
#
#         if not email:
#             raise ValueError(_('sem nome válido'))
#
#         user = self.model(**kwargs)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#
#     def create_superuser(self, *args, **kwargs):
#         user = self.create_user(**kwargs)
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user


class Cliente( AbstractUser, PermissionsMixin):

    class Meta:
        permissions = [
            ('adicionar_prod', 'Adicionar produto'),
            ('pagar_prod', 'Pagar produtos'),
            ('uai', 'te4s')
        ]
        # app_label = 'Cliente'

    # groups = models.ManyToManyField(User, related_name='grupos', blank=True)
    # user_permissions = models.ManyToManyField(User, related_name='permissoes', blank=True)
    id = models.AutoField(primary_key=True)
    loja = models.BooleanField(default=False)

    nome = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        unique=True,
        # default='some_val'
    )
    senha = models.CharField(
        max_length=50,
        null=True,
        blank=False,
    )
    telefone = models.CharField(
        max_length=20,
        null=True,
        blank=False,

    )
    email = models.CharField(
        max_length=35,
        null=True,
        blank=False,

    )
    cpf = models.CharField(
        max_length=16,
        null=True,
        blank=False,
        unique=True,

    )
    data = models.DateTimeField(auto_now_add=True, blank=True)
    USERNAME_FIELD = 'nome'
    REQUIRED_FIELDS = ['senha', 'cpf']
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # objects = UserManager()

class Produto(models.Model):

    id = models.AutoField(primary_key=True)


    nome = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    descricao = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    preco = models.FloatField(
        null=False,
        blank=False,
        default=0.0
    )

    img_prod = CloudinaryField()

    STATUS_CHOICES = (
        ("R", "Relogio"),
        ("A", "Acessorio"),
        ("v", "Vesturaio"),
    )
    tipo = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        blank=False,
        null=False
    )
    estoque= models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)])
    data = models.DateTimeField(auto_now_add=True, blank=True)

    # def __str__(self):
    #     return self.nome

    objects = models.Manager()

class Carrinho(models.Model):

    cliente_cli = models.ForeignKey(
        Cliente,
        blank=True,
        on_delete=models.CASCADE,
        related_name="cliente_cli"
    )

    id = models.AutoField(primary_key=True),



    produto_cli= models.ManyToManyField(Produto, related_name='produto', blank=True)

    valor = models.FloatField(
        default=0.0,
        null=False,
        blank=True

    )
    data = models.DateTimeField(auto_now_add=True, blank=True)

    objects = models.Manager()


class Tot_ped(models.Model):


    # def __str__(self):
    #     return self.id

    id = models.AutoField(primary_key=True),
    carrinho = models.ForeignKey(
        Carrinho,
        null=True,
        on_delete=models.CASCADE,
        related_name="carrinho"
    )

    quantidade = models.IntegerField(
        null=False,
        blank=False,
        default=1
    )

    produto_carrinho = models.ForeignKey(
        Produto,
        null=True,
        on_delete=models.CASCADE,
        related_name="prod_carrinho"
    )

    objects = models.Manager()


class Venda(models.Model):

    STATUS_CHOICES = (
        ("P", "Pedido realizado"),
        ("F", "Fazendo"),
        ("S", "Saiu para entrega"),
        ("E", "Foi entregue"),
        ("C", "Cancelado")
    )

    STATUS_PGT = (
        ("P", "Pago"),
        ("R", "Resto"),
        ("N", "Não pago")
    )

    carrinho = models.ForeignKey(
        Carrinho,
        null=True,
        on_delete=models.CASCADE,
        related_name="carrinho_cli"
    )

    id = models.AutoField(primary_key=True)


    produto_cli= models.ManyToManyField(Produto, related_name='produto_cli', blank=False)

    quantidade = models.IntegerField(
        null=False,
        blank=False,
        default= 1
    )
    observacao = models.TextField(
        max_length=170,
        null=False,
        blank=True,
        default='Sem Observações.',

    )

    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        blank=False,
        null=False,
        default="P"
    )

    status_pago = models.CharField(
        max_length=1,
        choices=STATUS_PGT,
        blank=False,
        null=False,
        default="N"

    )

    valor = models.FloatField(
        default=0.0,
        null=False,
        blank=True

    )

    data = models.DateTimeField(auto_now_add=True , blank=True)

    # def __str__(self):
    #     return '{} - {}'.format( self.id, self.carrinho)

    objects = models.Manager()

class Pagamentos(models.Model):

    id = models.AutoField(primary_key=True)


    carrinho_ped = models.ManyToManyField(Carrinho, related_name='carribgo_ped', blank=True)

    STATUS_PGT = (
        ("C", "Completo"),
        ("P", "Processo"),
        ("R", "Recusado")
    )

    FORMA_PGT = (
        ("C", "Cartão"),
        ("P", "Pix"),
        ("D", "Dinheiro")
    )

    formapg = models.CharField(
        max_length=1,
        choices=FORMA_PGT,
        blank=False,
        null=False,
        default="D"
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS_PGT,
        blank=False,
        null=False,
        default="R"
    )


    valor = models.FloatField(
        default=0.0,
        null=False,
        blank=True
    )
    # is_active = models.BooleanField(default=True)
    # is_admin = models.BooleanField(default=False)
    # is_staff = models.BooleanField(default=False)
    data = models.DateTimeField(auto_now_add=True, blank=True)

    # def __str__(self):
    #     return '{}'.format(self.id)

    objects = models.Manager()



# class logform(models.Model):
#     senha = models.CharField(
#         max_length=80,
#         null=False,
#         blank=False,
#     )
#     nome = models.CharField(
#         max_length=80,
#         null=False,
#         blank=False,
#     )

