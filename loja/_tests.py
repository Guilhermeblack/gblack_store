from django.contrib.auth.hashers import make_password
from django.test import TestCase

from . import views, models


# importa a funçao ou classe a ser testada

class testRenders(TestCase):

    def testIndex(self):
        if self.client.get(views.index).status_code == 200:
            return self.assertTemplateUsed('index.html')

    def testCriausr(self):
        if self.client.post(views.index, {
            'nome': 'joao',
            'email':'joao@bolao',
            'senha':'prontoadmin',
            'telefone': '9999-9999',
            'senha_rep':'prontoadmin',
            'cpf':'14407486'

            # 'senha': make_password('prontoadmin', salt=None, hasher='pbkdf2_sha256')
        }).status_code == 200:

            # self.client.force_login(models.Cliente.objects.get_or_create(username='josé')[0])
            return self.assertTemplateUsed('index')
#
    def testLogin(self):
        if self.client.post(views.index, {
            'nome_log': 'joao',
            'senha': 'prontoadmin',

            # 'senha': make_password('prontoadmin', salt=None, hasher='pbkdf2_sha256')
        }).status_code == 200:
            return self.assertTemplateUsed('index')

# class testStatusMovimento(TestCase):
#
#     #teste do ajax
#     def alteraMov(self):
#         if self.movimento == "D":
#             if self.client.post(adm, {
#                 'movimento': "L"
#             }).status_code == 200:
#                 # verificar com alguma mensagem de retorno aqui
#                 return self.assertTemplateUsed('adm');
#
#
#     # cria uma classe que vai receber o TestCase
#     # cria as funções que testarão o retorno da classe ou funçao importada
#
#     # os testes podem ser chamados individualmente, pelo modulo, pelo app, ou test em geral
