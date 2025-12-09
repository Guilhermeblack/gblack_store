from django.contrib import admin
from . import models


@admin.register(models.Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'cpf', 'telefone', 'is_active')
    search_fields = ('username', 'email', 'cpf')
    list_filter = ('is_active', 'loja')


@admin.register(models.Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'preco', 'estoque', 'is_available', 'created_at')
    list_filter = ('tipo', 'is_available')
    search_fields = ('nome', 'descricao')
    list_editable = ('is_available',)


@admin.register(models.FeedPost)
class FeedPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'scheduled_date', 'is_published', 'created_at')
    list_filter = ('is_published', 'scheduled_date')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    date_hierarchy = 'scheduled_date'
    filter_horizontal = ('products',)
    
    fieldsets = (
        ('Conteúdo', {
            'fields': ('title', 'content', 'image')
        }),
        ('Produtos Vinculados', {
            'fields': ('products',),
            'description': 'Selecione os produtos que deseja vincular a este post para sugestão de compra.'
        }),
        ('Publicação', {
            'fields': ('scheduled_date', 'is_published')
        }),
    )


@admin.register(models.ProductDiscount)
class ProductDiscountAdmin(admin.ModelAdmin):
    list_display = ('produto', 'discount_percent', 'start_date', 'end_date', 'is_active', 'is_currently_active')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('produto__nome',)
    list_editable = ('is_active',)
    date_hierarchy = 'start_date'
    
    def is_currently_active(self, obj):
        return obj.is_currently_active()
    is_currently_active.boolean = True
    is_currently_active.short_description = 'Ativo Agora'


admin.site.register(models.Carrinho)
admin.site.register(models.CartItem)
admin.site.register(models.Venda)
admin.site.register(models.ItemVenda)
admin.site.register(models.Address)
admin.site.register(models.PaymentTransaction)
admin.site.register(models.Leads)
