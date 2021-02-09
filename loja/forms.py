from django import forms
from django.contrib.auth import get_user
from . import models

class autForm(forms.ModelForm):

    class Meta:
        model= models.Cliente
        fields = ['email', 'telefone', 'cpf', 'nome', 'senha']
        name= 'logform'
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'senha'}))
    nome = forms.CharField()
    cpf = forms.CharField()
    telefone = forms.CharField()
    email = forms.CharField()
#
class cria_usr(forms.ModelForm):

    class Meta:
        model = models.Cliente
        fields = ['loja', 'nome', 'senha', 'telefone', 'email', 'cpf']
        name= 'cria_usr'
    nome = forms.CharField()
    cpf = forms.CharField()
    telefone = forms.CharField()
    loja = forms.CharField()
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'senha'}))
    email = forms.CharField()
# #
# #
# class produto(forms.ModelForm):
#
#     class Meta:
#         model = models.Produto
#         fields = ['nome','descricao','preco','tipo','img_prod']
#
#     nome = forms.CharField()
#     descricao = forms.CharField()
#     # preco = forms.DecimalField(decimal_places=2)
#     tipo = forms.ChoiceField(choices=(
#         models.Produto.STATUS_CHOICES
#     ))
#
#
# class carrinho(forms.ModelForm):
#
#     class Meta:
#         model = models.Carrinho
#         fields = 'cliente_cli','valor'
#         name= 'logform'

#
#     def __init__(self, *args, **kwargs):
#         super(pedidos, self).__init__(*args, **kwargs)
#         self.fields['produtosPed'].label =''

