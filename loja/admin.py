from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin


admin.site.register(models.Produto)
admin.site.register(models.Cliente, UserAdmin)
admin.site.register(models.Carrinho)
admin.site.register(models.Tot_ped)
admin.site.register(models.Venda)
admin.site.register(models.Pagamentos)

