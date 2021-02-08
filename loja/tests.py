from django.contrib.auth.hashers import make_password
from django.test import TestCase

from .views import  index


# importa a funçao ou classe a ser testada

class testRenders(TestCase):

    def testIndex(self):
        if self.client.get(index).status_code == 200:
            return self.assertTemplateUsed('index.html')

#     def testLog(self):
#         if self.client.post(loguin, {
#             'nome':'gerente',
#
#             'senha': make_password('prontoadmin', salt=None, hasher='pbkdf2_sha256')
#         }).status_code == 200:
#             return self.assertTemplateUsed('adm')
#
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
