from django.contrib import admin
from . import models


admin.site.register(models.Cliente)
admin.site.register(models.Produto)
admin.site.register(models.Carrinho)
admin.site.register(models.CartItem)
admin.site.register(models.Venda)
admin.site.register(models.ItemVenda)
admin.site.register(models.Address)
admin.site.register(models.PaymentTransaction)
admin.site.register(models.Leads)
