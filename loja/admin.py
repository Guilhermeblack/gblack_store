from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin

class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'nome', 'cpf')}),
        ('Permissions', {'fields': (
            'loja',
            # 'is_admin',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ( 'senha', 'senha2')
            }
        ),
    )

    list_display = ('email', 'nome',)
    list_filter = ('loja','groups')
    search_fields = ('nome',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(models.Produto)
admin.site.register(models.Cliente, UserAdmin)
admin.site.register(models.Carrinho)
admin.site.register(models.Tot_ped)
admin.site.register(models.Venda)
admin.site.register(models.Pagamentos)

