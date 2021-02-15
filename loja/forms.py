from django import forms
from django.contrib.auth import get_user
from . import models
from cloudinary.models import CloudinaryField

class autForm(forms.ModelForm):

    class Meta:
        model= models.Cliente
        fields = ['nome_log', 'senha']
        name= 'logform'
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'senha'}))
    nome_log = forms.CharField()

#
class cria_usr(forms.ModelForm):

    class Meta:
        model = models.Cliente
        fields = ['cpf', 'email', 'nome', 'senha','senha_rep', 'telefone', 'loja']
        # name= 'cria_usr'
    nome = forms.CharField()
    cpf = forms.CharField()
    telefone = forms.CharField()
    loja = forms.BooleanField()
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'senha'}))
    senha_rep = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'repetir senha'}))
    email = forms.CharField()
# #
# #
class produtoform(forms.ModelForm):

    class Meta:
        model = models.Produto
        fields = ['descricao','img_prod','nome','preco','tipo','estoque']

    # nome = forms.CharField()
    # descricao = forms.TextField(attrs={'rows': 3, 'cols': 10})
    # preco = forms.CharField()
    img_prod = CloudinaryField()
    tipo = forms.ChoiceField(choices=models.Produto.STATUS_CHOICES)

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

