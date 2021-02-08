from django.db import models
from cloudinary.models import CloudinaryField
from django.utils.timezone import now

class Cliente(models.Model):

    class Meta:
        permissions = [
            ('adicionar_prod', 'Adicionar produto'),
            ('pagar_prod', 'Pagar produtos'),

        ]

        # app_label = 'Cliente'


    id = models.AutoField(primary_key=True),

    nome = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        default='gerente'
    ),
    senha = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    ),
    telefone = models.CharField(
        max_length=20,
        null=False,
        blank=False,

    ),
    email = models.CharField(
        max_length=35,
        null=False,
        blank=False,

    ),
    cpf = models.CharField(
        max_length=16,
        null=False,
        blank=False,

    ),

    objects = models.Manager()

class Produto(models.Model):

    id = models.AutoField(primary_key=True)


    nome = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    descricao = models.TextField(
        max_length=255,
        null=False,
        blank=False
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

    # def __str__(self):
    #     return self.nome

    objects = models.Manager()

class Carrinho(models.Model):

    cliente_cli = models.ForeignKey(
        Cliente,
        null=True,
        on_delete=models.CASCADE,
        related_name="Cliente"
    )

    id = models.AutoField(primary_key=True),



    produto_cli= models.ManyToManyField(Produto, related_name='produto', blank=False)

    valor = models.FloatField(
        default=0.0,
        null=False,
        blank=True

    )

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

    data = models.DateTimeField(auto_now_add=True, blank=True)

    # def __str__(self):
    #     return '{}'.format(self.id)

    objects = models.Manager()



class logform(models.Model):
    senha = models.CharField(
        max_length=80,
        null=False,
        blank=False,
    )
    nome = models.CharField(
        max_length=80,
        null=False,
        blank=False,
    )

