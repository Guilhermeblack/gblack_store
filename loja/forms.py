from django import forms
from django.contrib.auth import get_user_model
from . import models
from cloudinary.models import CloudinaryField

User = get_user_model()

class autForm(forms.Form):
    nome_log = forms.CharField(label="Email")
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'senha'}))

class cria_usr(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'senha'}))
    senha_rep = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'repetir senha'}))
    nome = forms.CharField(label="Nome Completo") # We will save this to first_name

    class Meta:
        model = models.Cliente
        fields = ['cpf', 'email', 'telefone']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email'] # Use email as username
        user.first_name = self.cleaned_data['nome']
        user.set_password(self.cleaned_data['senha'])
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        senha_rep = cleaned_data.get("senha_rep")

        if senha and senha_rep and senha != senha_rep:
            self.add_error('senha_rep', "As senhas não conferem")

class produtoform(forms.ModelForm):
    class Meta:
        model = models.Produto
        fields = ['descricao','img_prod','nome','preco','tipo','estoque']

    # nome = forms.CharField()
    # descricao = forms.TextField(attrs={'rows': 3, 'cols': 10})
    # preco = forms.CharField()
    img_prod = CloudinaryField()
    tipo = forms.ChoiceField(choices=models.Produto.STATUS_CHOICES)
