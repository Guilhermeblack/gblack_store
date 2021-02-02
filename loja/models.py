# class Gerente(models.Model):
#
#     class Meta:
#         permissions = [
#             ('fazer_pedido', 'incluir pedido'),
#             ('ver_feed', 'visualizar o feed'),
#             ('iniciar_movimento', 'iniciar o movimento'),
#             ('fechar_comanda', 'fechar a comanda'),
#             ('abrir_comanda', 'abrir uma nova comanda'),
#             ('controlar_produtos', 'controlar produtos disponiveis')
#         ]
#
#         # app_label = 'gerente'
#
#     def __str__(self):
#         return self.nome
#
#     id = models.AutoField(primary_key=True),
#     nome = models.CharField(
#         max_length=50,
#         null=False,
#         blank=False,
#         default='gerente'
#     ),
#     senha = models.CharField(
#         max_length=50,
#         null=False,
#         blank=False,
#     ),
#     senha_rep = models.CharField(
#         max_length=50,
#         null=False,
#         blank=False,
#
#     ),
#
#     objects = models.Manager()
#
# class Garcom(models.Model):
#     class Meta:
#         permissions = [
#             ('fazer_pedido', 'incluir pedido'),
#             ('pedido_entregue', 'pedido foi entregue'),
#             ('ver_feed', 'visualizar o feed'),
#             ('abrir_comanda', 'abrir uma nova comanda')
#         ]
#
#     def __str__(self):
#         return self.nome
#
#     id = models.AutoField(primary_key=True),
#
#     nome = models.CharField(
#         max_length=50,
#         null=False,
#         blank=False,
#         default="garçom",
#     ),
#     senha = models.CharField(
#         max_length=50,
#         null=False,
#         blank=False,
#     ),
#     senha_rep = models.CharField(
#         max_length=50,
#         null=False,
#         blank=False,
#     ),
#     objects = models.Manager()
#
# class Cozinha(models.Model):
#     class Meta:
#         permissions = [
#             ('pedido_pronto', 'pedido pronto'),
#             ('ver_feed', 'visualizar o feed')
#         ]
#
#     def __str__(self):
#         return self.nome
#
#     id = models.AutoField(primary_key=True),
#
#     nome = models.CharField(
#         max_length=50,
#         null=False,
#         blank=False,
#         default='cheff',
#     )
#     senha = models.CharField(
#         max_length=50,
#         null=False,
#         blank=False,
#     )
#     senha_rep = models.CharField(
#         max_length=50,
#         null=False,
#         blank=False,
#     )
#     objects = models.Manager()
#
#
# class Caixa(models.Model):
#     class Meta:
#         permissions = [
#             ('fechar_comanda', 'fechar a comanda'),
#             ('ver_feed', 'visualizar o feed')
#         ]
#
#     def __str__(self):
#         return self.nome
#
#     id = models.AutoField(primary_key=True),
#
#
#     nome = models.CharField(
#         max_length=50,
#         null=False,
#         blank=False,
#         default='cheff',
#     )
#     senha = models.CharField(
#         max_length=50,
#         null=False,
#         blank=False,
#     )
#     senha_rep = models.CharField(
#         max_length=50,
#         null=False,
#         blank=False,
#     )
#     objects = models.Manager()
#
#
# class Comanda(models.Model):
#
#     id = models.AutoField(primary_key=True)
#
#
#     nome = models.CharField(
#         max_length=50,
#         null=False,
#         blank=False,
#
#     )
#
#     n_mesa = models.IntegerField(
#         null=False,
#         blank=False,
#     )
#
#     valor = models.FloatField(
#         default=0.0,
#         null=False,
#         blank=True
#
#     )
#
#     data = models.DateTimeField(auto_now_add=True, blank=True)
#
#     STATUS_CHOICES = (
#         ("A", "Aberto"),
#         ("F", "Fechado"),
#     )
#     status = models.CharField(
#         max_length=1,
#         choices=STATUS_CHOICES,
#         default="A",
#         blank=True,
#         null=False
#     )
#
#
#     def __str__(self):
#         return ' {}'.format(self.nome)
#
#     objects = models.Manager()
#
#
# class Produtocad(models.Model):
#
#     id = models.AutoField(primary_key=True)
#
#
#     nome = models.CharField(
#         max_length=50,
#         null=False,
#         blank=False
#     )
#     descricao = models.TextField(
#         max_length=255,
#         null=False,
#         blank=False
#     )
#     preco = models.FloatField(
#         null=False,
#         blank=False,
#         default=0.0
#     )
#
#     # pedidoProdutos = models.ManyToManyField(Pedido)
#
#     STATUS_CHOICES = (
#         ("A", "Alimento"),
#         ("B", "Bebida"),
#     )
#     tipo = models.CharField(
#         max_length=1,
#         choices=STATUS_CHOICES,
#         blank=False,
#         null=False
#     )
#
#     img_prod = CloudinaryField()
#
#     def __str__(self):
#         return self.nome
#
#     objects = models.Manager()
#
# class Pedido(models.Model):
#
#     STATUS_CHOICES = (
#         ("P", "Pedido realizado"),
#         ("F", "Fazendo"),
#         ("S", "Saiu para entrega"),
#         ("E", "Foi entregue"),
#         ("C", "Cancelado")
#     )
#
#     STATUS_PGT = (
#         ("P", "Pago"),
#         ("R", "Resto"),
#         ("N", "Não pago")
#     )
#
#
#     comandaref= models.ForeignKey(
#         Comanda,
#         null=True,
#         on_delete=models.CASCADE,
#         related_name="pedidoComanda"
#     )
#
#     id = models.AutoField(primary_key=True)
#
#
#     produtosPed= models.ManyToManyField(Produtocad, related_name='produto', blank=False)
#
#     quantidade = models.IntegerField(
#         null=False,
#         blank=False,
#         default= 1
#     )
#     observacao = models.TextField(
#         max_length=170,
#         null=False,
#         blank=True,
#         default='Sem Observações.',
#
#     )
#
#     status = models.CharField(
#         max_length=1,
#         choices=STATUS_CHOICES,
#         blank=False,
#         null=False,
#         default="P"
#     )
#
#     status_pago = models.CharField(
#         max_length=1,
#         choices=STATUS_PGT,
#         blank=False,
#         null=False,
#         default="N"
#
#     )
#
#     valor = models.FloatField(
#         default=0.0,
#         null=False,
#         blank=True
#
#     )
#
#     data = models.DateTimeField(auto_now_add=True , blank=True)
#
#     def __str__(self):
#         return '{} - {}'.format( self.id, self.comandaref)
#
#     objects = models.Manager()
#
# class pagamentos(models.Model):
#
#     id = models.AutoField(primary_key=True)
#
#
#     pedidored = models.ManyToManyField(Pedido, related_name='pedidored', blank=True)
#
#     STATUS_PGT = (
#         ("F", "fechou comanda"),
#         ("P", "pagou produto"),
#         ("R", "Restante")
#     )
#
#     FORMA_PGT = (
#         ("C", "Cartão"),
#         ("P", "Pix"),
#         ("D", "Dinheiro")
#     )
#
#     formapg = models.CharField(
#         max_length=1,
#         choices=FORMA_PGT,
#         blank=False,
#         null=False,
#         default="D"
#     )
#
#     status = models.CharField(
#         max_length=1,
#         choices=STATUS_PGT,
#         blank=False,
#         null=False,
#         default="R"
#     )
#
#
#     valor = models.FloatField(
#         default=0.0,
#         null=False,
#         blank=True
#     )
#
#     data = models.DateTimeField(auto_now_add=True, blank=True)
#
#     def __str__(self):
#         return '{}'.format(self.id)
#
#     objects = models.Manager()
#
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
#
# class movi(models.Model):
#     STATUS_CHOICES = (
#         ("L", "Ligado"),
#         ("D", "Desligado"),
#     )
#
#     movimento = models.CharField(
#         max_length=1,
#         choices=STATUS_CHOICES,
#         blank=False,
#         null=False
#     )
#     objects = models.Manager()
# # Create your models here.
