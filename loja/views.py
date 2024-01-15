from datetime import date

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from loja import forms,models
from gbstr import settings
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
import validate_docbr as docbr
import requests
from django.contrib.auth.hashers import make_password, check_password, BCryptPasswordHasher, pbkdf2
from django.contrib.auth import logout, login, authenticate, get_user
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import Permission
from pprint import pprint
import cloudinary
from django.views.decorators.csrf import csrf_protect

# Session.objects.all().delete()

def index(request):

    if request.POST:
        rq = request.POST
    # print(' >>>', request.POST)
        pprint(request.POST)
        if 'senha_rep' in rq and rq['senha_rep'] == rq['senha']:
            doc = [(docbr.CPF, rq['cpf'])]
            if docbr.validate_docs(doc):
                # print('validooou')
                password = make_password(rq['senha'], salt=None, hasher='pbkdf2_sha256')
                usr = forms.cria_usr(rq)
                # usr['senha'].value = password
                # pprint(usr)
                # print(usr.errors)
                if usr.is_valid():
                    cli = usr.save()
                    cart = models.Carrinho.objects.create(
                        cliente_cli=cli
                    )
                    cart.save()

                    login(request,cli)
                    print('logou')
                    messages.info(request, ' Usuário criado')
                return redirect(settings.LOGIN_REDIRECT_URL, permanent=True)
            else:
                messages.warning(request, 'CPF/CNPJ inválidos')
                return redirect(settings.LOGIN_REDIRECT_URL, permanent=True)
        elif 'nome_log' in rq:

            try:
                encod = models.Cliente.objects.get(email=rq['nome_log'])
            except ObjectDoesNotExist:
                encod = None

            pprint(encod)
            # print(encod.errors)
            if encod is not None and encod.check_password(rq['senha']):
                login(request, encod)
                messages.info(request, ' Bem vindo')
                return redirect(settings.LOGIN_REDIRECT_URL, permanent=True)
            else:
                messages.info(request, 'Usuário inexistente/Bloqueado')
                return redirect(settings.LOGIN_REDIRECT_URL, permanent=True)
    if request.user.is_authenticated:
        carrinho = models.Carrinho.objects.get(cliente_cli= request.user.id)
        pprint(carrinho.id)
        pedido = models.Tot_ped.objects.filter(carrinho=carrinho.id)
        pprint(pedido)
    else:
        pedido =[]

    if models.Produto.objects.all() is None:
        pdt = []
    else:
        pdt =models.Produto.objects.all().order_by('tipo')

    return render(request,
                  'index.html',
                  {
                    'criar': forms.cria_usr,
                    'pedidos': pedido,
                    'logar': forms.autForm,
                    # 'prod': forms.produtoform,
                    'produtos': pdt,
                    'prodtipo': models.Produto.STATUS_CHOICES
                  })
#

def term_condition(request):
    return redirect('term_cond')

@login_required(login_url='index')
def logoutuser(request):
    logout(request)
    return redirect('index')

@login_required(login_url='index')
def conta(request):

    if request.POST:
        rq = request.POST
        pprint(rq)
        if 'lojasim' in rq:
            usr = models.Cliente.objects.get(pk=request.user.id)
            usr.loja = True
            pprint(usr)
            usr.save()
            messages.info(request,' Agora é uma loja')
        elif 'exc_prod' in rq:
            prod = models.Produto.objects.exclude(pk=rq['exc_prod'])

            prod.save()
            messages.info(request,' Excluido')
        elif 'tipo' in rq:
            # rq['img_prod'] = 'gbstr/'+rq['img_prod']
            pprint(request.FILES)
            print('entro pdsadasdkasd´sadas')

            if request.FILES:
                rf = request.FILES
                prod = forms.produtoform(rq,rf)
                pprint(prod)
                print('produto aqqq')
            else:
                prod = forms.produtoform(rq)
            pprint(prod)
            if prod.is_valid():

                cloudinary.uploader.upload(rf['img_prod'], folder="gbstr")
                prod.save()
                print('salvo prod')
                messages.info(request, 'Produto cadastrado')
            else:
                print(prod.errors)
                messages.info(request, 'Produto não cadastrado')
            return redirect(settings.LOGIN_REDIRECT_URL, permanent=True)

    # pprint(client)

    clent = models.Cliente.objects.get(pk=request.user.id)
    cart = models.Carrinho.objects.get(cliente_cli=clent.id)
    prods = models.Produto.objects.all()
    # pprint(clent)
    # pprint(cart)

    # if len(cart) isArray:
    #     cart = [cart]
    # pprint(cart.produto_cli)
    # pprint(prods)
    return render(
        request,
        'conta.html',
        {
            'prod': forms.produtoform,
            # 'userform':forms.cria_usr(),
            'usuario': clent,
            'carrinho': cart,
            # 'totalpedido': models.Tot_ped.objects.all(),
            # 'venda': models.Venda.objects.all(),
            'produtos': prods,
            # 'pagamento': models.Pagamentos.objects.all(),
            'prodtipo': models.Produto.STATUS_CHOICES

        }
    )

def prod(request):

    if request.POST:
        pprint(request.POST)
        rq =request.POST
        if 'proid' in rq:
            pdt = models.Produto.objects.get(pk=rq['proid'])
        if 'add_carrinho' in rq:
            cli = models.Cliente.objects.get(id=request.user.id)

            prod = models.Produto.objects.get(pk=request.POST['add_carrinho'])
            if prod.estoque <=0:
                messages.warning(request, 'estoque indisponível')
                return HttpResponse(prod.estoque)

            prod.estoque -= 1
            prod.save()
            carrinho = models.Carrinho.objects.get(cliente_cli=cli.id)
            pprint(carrinho.produto_cli.all())

            if prod not in carrinho.produto_cli.all():
                carrinho.produto_cli.add(prod)
                ped = models.Tot_ped.objects.create(
                    carrinho=carrinho,
                    produto_carrinho=prod
                )
            else:
                ped = models.Tot_ped.objects.get(produto_carrinho=prod.id)
            carrinho.valor += prod.preco
            carrinho.save()

            ped.quantidade +=1
            ped.save()

            pedido = models.Tot_ped.objects.filter(carrinho= carrinho.id)
            messages.info(request, 'Pedido Feito')
            print('deu tudo')
            return HttpResponse(prod.estoque)

        elif 'pdt_nome' in rq and rq['pdt_nome'] != '':
            pdt.nome = rq['pdt_nome']
            pdt.save()
        elif 'pdt_est' in rq and rq['pdt_est'] != '':
            pprint(rq['pdt_est'])
            pdt.estoque = int(rq['pdt_est'])
            pdt.save()
        elif 'pdt_des' in rq and rq['pdt_des'] != '':
            pprint(rq['pdt_des'])
            pdt.descricao = rq['pdt_des']
            pdt.save()
        elif 'pdt_tipo' in rq and rq['pdt_tipo'] != '':
            pprint(pdt.tipo)
            obj = models.Produto.objects.filter(pk=rq['proid'])
            opc = models.Produto.STATUS_CHOICES
            for p in opc:
                if p[0] == rq['pdt_tipo']:
                    obj.update(tipo=p[0])

        elif 'pdt_pre' in rq and rq['pdt_pre'] != '':
            pdt.preco = rq['pdt_pre']
            pdt.save()
        elif 'btn_del' in rq and rq['btn_del'] != '':
            pdt.delete()
            pdt.save()
        clent = models.Cliente.objects.get(pk=request.user.id)
        cart = models.Carrinho.objects.get(cliente_cli=clent.id)
        prods = models.Produto.objects.all()
        return render(
            request,
            'conta.html',
            {
                'prod': forms.produtoform,
                # 'userform':forms.cria_usr(),
                'usuario': clent,
                'carrinho': cart,
                # 'totalpedido': models.Tot_ped.objects.all(),
                # 'venda': models.Venda.objects.all(),
                'produtos': prods,
                # 'pagamento': models.Pagamentos.objects.all(),
                'prodtipo': models.Produto.STATUS_CHOICES

            }
        )
    return redirect(settings.LOGIN_REDIRECT_URL, permanent=True)  # enviar para as comandas


@csrf_protect
def pagamento(request):


    if request.POST:
        print(' >>>', request.POST)
        pass
    clent = models.Cliente.objects.get(pk=request.user.id)
    cart = models.Carrinho.objects.get(cliente_cli=clent.id)
    prods = models.Produto.objects.all()
    pprint(clent)
    pprint(cart)

    # if len(cart) isArray:
    #     cart = [cart]
    pprint(cart.produto_cli)
    pprint(prods)
    return render(
        request,
        'conta.html',
        {
            'prod': forms.produtoform,
            # 'userform':forms.cria_usr(),
            'usuario': clent,
            'carrinho': cart,
            # 'totalpedido': models.Tot_ped.objects.all(),
            # 'venda': models.Venda.objects.all(),
            'produtos': prods,
            # 'pagamento': models.Pagamentos.objects.all(),
            'prodtipo': models.Produto.STATUS_CHOICES

        }
    )
#
#             if user is not None:
#                 login(request, user)
#                 return redirect(settings.LOGIN_REDIRECT_URL, permanent=True)
#
#             messages.error(request, 'Dados inválidos')
#             return render(request, 'loguin.html', {'form': forms.autForm})
#         messages.error(request, 'Formulrio inválido')
#         return render(request, 'loguin.html', {'form': forms.autForm})
#     else:
#         if request.user.is_authenticated:
#             return redirect('profile')
#
#         return render(request, 'loguin.html', {'form': forms.autForm})
#
#
# def profile(request):
#     if request.user.is_authenticated:
#         usr = get_user(request)
#         grupo = request.user.groups.all()
#         print(grupo)
#
#         if 'caixas' in str(grupo):
#             messages.info(request, 'Logado como caixa. \n Data: {}'.format(date.today()))
#             return render(request, 'feed.html', {'pedidos': models.Pedido.objects.all()})  # enviar para as comandas
#
#         elif 'cozinha' in str(grupo):
#             if request.user.has_perm('pedido_pronto'):
#                 messages.info(request, 'Logado como cozinha. \n Data: {}'.format(date.today()))
#                 return render(request, 'feed.html', {'pedidos': models.Pedido.objects.all()})
#
#         elif 'gerente' in str(grupo):
#             return redirect('administrador')
#
#         elif 'garçons' in str(grupo):
#             messages.info(request, 'Bem vindo Garçom. \n Data: {}'.format(date.today()))
#             formComanda = forms.comandas
#             return render(request, 'pedidos.html',
#                           {'newcomanda': formComanda, 'produtos': models.Produtocad.objects.all()})
#         else:
#             messages.info(request, 'Usuário nao identificado. \n Data: {}'.format(date.today()))
#             # return redirect('loguin')
#
#         print(request, "erro nos grupos")
#     return redirect('index')
#
#

#
#
# # @permission_required('ver_feed')
# def feed(request):
#     estado_mov = models.movi.objects.filter(pk=1).values()
#     STATUS_CHOICES = (
#         "Pedido realizado",
#         "Fazendo",
#         "Saiu para entrega",
#         "Foi entregue",
#         "Cancelado"
#     )
#     FORMA_PGT = (
#         "Cartão",
#         # "Pix",
#         "Dinheiro"
#     )
#     if request.POST:
#         # print(request.POST)
#
#         if 'exc_ped' in request.POST:
#             pprint(request.POST)
#             ped = models.Pedido.objects.get(pk=request.POST['exc_ped'])
#             ped.status="C"
#             ped.valor =0
#             # pprint(ped)
#             pprint(ped.produtosPed.all())
#             produto_ped = models.Produtocad.objects.get(pk=ped.produtosPed.all()[0].id)
#
#             comanda = models.Comanda.objects.get(pk=ped.comandaref.id)
#             vll = ped.quantidade *produto_ped.preco
#             print(vll, '  <<< vll')
#             comanda.valor -= vll
#             comanda.save()
#             ped.save()
#             messages.success(request, "{}, Pedido cancelado com sucesso!".format(request.user))
#             return render(request, 'feed.html', {
#
#                 'comandas': models.Comanda.objects.all().order_by('id', 'data'),
#                 'pedidos': models.Pedido.objects.all().order_by('id', 'status'),
#                 'choices': STATUS_CHOICES,
#                 'fpg': FORMA_PGT,
#                 'movi': estado_mov[0]['movimento']
#             })
#
#         if 'stats' in request.POST:
#             print(request.POST)
#             ped= models.Pedido.objects.filter(pk=request.POST['idstat'])
#             pprint(ped)
#             ped.update(status=request.POST['stats'])
#             # ped.save()
#             messages.success(request, "{}, status alterado com sucesso.".format(request.user))
#             return render(request, 'feed.html', {
#
#                 'comandas': models.Comanda.objects.all().order_by('id', 'data'),
#                 'pedidos': models.Pedido.objects.all().order_by('id', 'status'),
#                 'choices': STATUS_CHOICES,
#                 'fpg': FORMA_PGT,
#                 'movi': estado_mov[0]['movimento']
#             })
#
#         if 'comanda_x' in request.POST:
#             # tirar do total da comanda
#
#             pprint(request.POST)
#             formapg = request.POST['fpag']
#             com = models.Comanda.objects.get(pk=int(request.POST['comanda_x']))
#             valo_ped = float(request.POST['valo'])
#
#             if formapg == 'Cartão':
#                 maquina = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True, lookup_class=False)
#                 transacao = django_pagarme.mposandroid.Mpos(maquina , settings.CHAVE_PAGARME_CRIPTOGRAFIA_PUBLICA)
#                 transacao.openConnection()
#                 transacao.initialize()
#                 transacao.payAmount(valo_ped)
#                 transacao.payAmount.PaymentMethod.CreditCard
#
#                 transacao.close('conexão fechada')
#                 transacao.closeConnection()
#             new_status = 'VERIFICADA'
#
#
#             # loop itens
#
#             valo= valo_ped
#             if 'pedi[]' in request.POST:
#                 peed = request.POST['pedi[]']
#                 pprint(peed)
#                 print('entao foi o pedd')
#
#                 if isinstance(peed, str):
#                     pedido_prod = models.Pedido.objects.get(pk=peed)
#                     print('valor comanda maior q 0 e um item')
#                     com.valor -= valo_ped
#                     if valo >= pedido_prod.valor:
#                         if com.valor <= 0:
#                             com.status = "F"
#                             receb = models.pagamentos.objects.create(
#                                 valor=float(valo_ped),
#                                 status="F",
#                                 formapg=formapg
#                             )
#
#                             receb.pedidored.add(pedido_prod)
#
#                             receb.save()
#                             com.save()
#                             new_status = 'FECHADA'
#                             print('valor comanda menor q 0')
#                         valo -= pedido_prod.valor
#                         print('valor paga o produto')
#                         pedido_prod.valor = 0
#                         pedido_prod.status_pago = "P"
#                         receb = models.pagamentos.objects.create(
#                             valor=valo_ped,
#                             status= "P",
#                             formapg=formapg
#                         )
#                         receb.pedidored.add(pedido_prod)
#                         receb.save()
#                         com.save()
#                         pedido_prod.save()
#
#                     else:
#
#                         if valo > 0:
#                             print('valor nao paga produto e maior q 0')
#                             print(valo,'  valoo')
#                             pedido_prod.valor -= valo
#                             print(com.valor,'  comanda valoor')
#                             print(pedido_prod.valor,'  valor do pedido')
#                             pedido_prod.status_pago = "R"
#                             receb = models.pagamentos.objects.create(
#                                 valor=valo_ped,
#                                 status="R",
#                                 formapg=formapg
#                             )
#                             receb.pedidored.add(pedido_prod)
#                             receb.save()
#                             pedido_prod.save()
#                             com.save()
#                             print('passo aqui')
#                     pedido_prod.save()
#                     new_status = 'ATUALIZADA com sucesso'
#
#
#                 elif peed.length > 0:
#                     com.valor -= valo_ped
#                     for num, p in peed:
#                         pedido_prod = models.Pedido.objects.get(pk=p)
#
#                         if valo >= pedido_prod.produtosPed.all()[0].preco:
#                             print('valor do pagamento pagou produto')
#                             valo -= pedido_prod.produtosPed.all()[0].preco
#                             pedido_prod.valor -= valo
#                             pedido_prod.status_pago = "P"
#                             receb = models.pagamentos.objects.create(
#                                 valor=valo_ped,
#                                 status="P",
#                                 formapg=formapg
#                             )
#                             receb.pedidored.add(pedido_prod)
#                             receb.save()
#                             pedido_prod.save()
#                         else:
#                             if valo > 0:
#                                 print('valor do pagamento nao pagou produto mas tem restante pae')
#                                 pdt = models.Produtocad.objects.get(pk=pedido_prod.produtosPed.all()[0].id)
#                                 pprint(pdt)
#                                 res = pdt.preco - valo
#                                 com.valor += res
#                                 pedido_prod.valor -= valo
#                                 pedido_prod.status_pago = "R"
#                                 receb = models.pagamentos.objects.create(
#                                     valor=valo_ped,
#                                     status="R",
#                                     formapg=formapg
#                                 )
#                                 receb.pedidored.add(pedido_prod)
#                                 receb.save()
#                                 pedido_prod.save()
#
#                                 com.save()
#                     new_status = 'ATUALIZADA com sucesso'
#                     pedido_prod.save()
#                     com.save()
#
#                 if com.valor == 0:
#
#                     com.status="F"
#                     if com.valor <= 0:
#                         com.status = "F"
#                         receb = models.pagamentos.objects.create(
#                             valor=valo_ped,
#                             status="F",
#                             formapg=formapg
#                         )
#                         receb.pedidored.add(pedido_prod)
#                         receb.save()
#                         com.save()
#                         new_status = 'FECHADA'
#                     com.save()
#                     new_status = 'FECHADA'
#             else:
#                 new_status = 'Sem pedido Selecionado'
#
#
#             messages.success(request, "{}, Comanda {} .".format(request.user, new_status))
#
#
#             return render(request, 'feed.html', {
#
#                 'comandas': models.Comanda.objects.all().order_by('id', 'data'),
#                 'pedidos': models.Pedido.objects.all().order_by('id', 'status'),
#                 'choices': STATUS_CHOICES,
#                 'fpg': FORMA_PGT,
#                 'movi': estado_mov[0]['movimento']
#             })
#
#     else:
#         messages.success(request, "{}, Data {}".format(request.user, date.today()))
#
#         # pprint(models.Pedido.objects.all().order_by('id'))
#         return render(request, 'feed.html', {
#
#             'comandas': models.Comanda.objects.all().order_by('id', 'data'),
#             'pedidos': models.Pedido.objects.all().order_by('id'),
#             'choices': STATUS_CHOICES,
#             'fpg': FORMA_PGT,
#             'movi': estado_mov[0]['movimento']
#         })
#
#
# def ped(request):
#     estado_mov = models.movi.objects.filter(pk=1).values()
#     formComanda = forms.comandas
#     if request.POST:
#         # print(request.POST)
#
#
#         if 'n_mesa' in request.POST:
#             usr = get_user(request)
#
#             pprint(request.POST)
#
#             # if usr.has_perm('abrir_comanda'):
#             formcom = forms.comandas(request.POST)
#
#             pprint(formcom)
#
#             # criar verificação do numero da comanda se nao esta aberta para nao repetir numero
#
#             # print('tem perm')
#             if formcom.is_valid():
#                 formcom.save()
#                 messages.success(request, "Comanda aberta !")
#                 return render(request, 'pedidos.html',
#                               {'newcomanda': formComanda,
#                                'prod': models.Produtocad.objects.all(),
#                                'movi':estado_mov[0]['movimento'],
#                                'comandas': models.Comanda.objects.filter(status="A"),
#                                'pedido': forms.pedidos
#                                })
#             else:
#                 messages.warning(request, "Formulário inválido!")
#
#                 return render(request, 'pedidos.html',
#                               {'newcomanda': formComanda,
#                                'prod': models.Produtocad.objects.all(),
#                                'movi': estado_mov[0]['movimento'],
#                                'comandas': models.Comanda.objects.filter(status="A"),
#                                'pedido': forms.pedidos
#                                })
#
#         if 'comandaref' in request.POST:
#             # produto = models.Produtocad.objects.get(pk=request.POST['produtosPed'])
#             newped = forms.pedidos(request.POST)
#
#             # jogar campo por campo e jogar o produto depois
#
#             if newped.is_valid():
#
#                 add_comanda = models.Comanda.objects.get(pk=request.POST['comandaref'])
#                 prod = models.Produtocad.objects.get(pk=request.POST['produtosPed'])
#
#                 qnt = int(request.POST['quantidade'])
#                 # print(newped)
#
#                 valu = prod.preco * qnt
#                 newped.cleaned_data['valor'] =float(valu)
#                 newped['valor'].value = valu
#                 print(newped.cleaned_data, '  <<<')
#                 if newped.is_valid():
#                     j= newped.save()
#                     j.save()
#                     ped_val = models.Pedido.objects.get(pk=j.id)
#                     print(ped_val.valor, '  valor q fico d opedido')
#                     ped_val.valor= valu
#                     print(ped_val.valor, '  depois e salv')
#                     ped_val.save()
#
#
#                     # print(newped.cleaned_data['valor'])
#                 add_comanda.valor += valu
#                 add_comanda.save()
#
#                 messages.success(request, "Pedido registrado !")
#                 return render(request, 'pedidos.html',
#                               {'newcomanda': formComanda,
#                                'prod': models.Produtocad.objects.all(),
#                                'movi': estado_mov[0]['movimento'],
#                                'comandas': models.Comanda.objects.filter(status="A"),
#                                'pedido': forms.pedidos
#                                })
#             else:
#                 messages.warning(request, "Dados de registro inválidos !")
#
#                 return render(request, 'pedidos.html',
#                               {'newcomanda': formComanda,
#                                'prod': models.Produtocad.objects.all(),
#                                'movi': estado_mov[0]['movimento'],
#                                'comandas': models.Comanda.objects.filter(status="A"),
#                                'pedido': forms.pedidos
#                                })
#
#
#     else:
#         messages.success(request, "{}, Data {}".format(request.user, date.today()))
#         return render(request, 'pedidos.html', {
#             'newcomanda': formComanda,
#             'prod': models.Produtocad.objects.all(),
#             'comandas': models.Comanda.objects.filter(status= "A"),
#             'movi':estado_mov[0]['movimento'],
#             'pedido': forms.pedidos()
#
#         })
#
#
# @permission_required('gerenciador.iniciar_movimento')
# def adm(request):
#     # print('do adm ', request.user.groups.all()[0])
#     if request.user.has_perm("gerenciador.iniciar_movimento"):
#
#         if request.POST:
#             rq = request.POST
#             pprint(rq)
#             # if 'prod_x' in rq:
#
#             if 'prod_x' in rq:
#
#                 models.Produtocad.objects.filter(pk=request.POST['prod_x']).delete()
#                 estado_mov = models.movi.objects.filter(pk=1).values()
#                 messages.info(request, "Produto deletado com sucesso!")
#                 return render(request, 'adm.html', {'form': forms.produto,
#                                                     'prod': models.Produtocad.objects.all(),
#                                                     'logado': get_user(request),
#                                                     'mov': estado_mov[0]['movimento']
#                                                     })
#
#             if 'movimento' in rq:
#                 # useer = forms.mov(rq)
#
#                 # print(useer)
#                 # if useer.is_valid():
#                 mov_atual = models.movi.objects.all().update(movimento=rq['movimento'])
#                 # print(mov_atual, 'movaq')
#                 # print('nudale', rq['movimento'])
#
#                 if (mov_atual == 1):
#                     if (rq['movimento'] == 'L'):
#
#                         messages.info(request, "Movimento iniciado com sucesso !")
#                         # print('nudale', rq['movimento'])
#                         estado_mov = models.movi.objects.filter(pk=1).values()
#                         # print(estado_mov)
#                         return render(request, 'adm.html', {'form': forms.produto,
#                                                             'prod': models.Produtocad.objects.all(),
#                                                             'logado': get_user(request),
#                                                             'mov': estado_mov[0]['movimento']
#                                                             })
#
#                     elif (rq['movimento'] == 'D'):
#
#
#                         messages.info(request, "Movimento encerrado com sucesso !")
#                         # print('trerrekcheck', rq['movimento'])
#                         estado_mov = models.movi.objects.filter(pk=1).values()
#                         # print(estado_mov)
#                         return render(request, 'adm.html', {'form': forms.produto,
#                                                             'prod': models.Produtocad.objects.all(),
#                                                             'logado': get_user(request),
#                                                             'mov': estado_mov[0]['movimento']
#                                                             })
#                 else:
#                     # messages.error(request, "{}".format('Não foi possível alterar o movimento.'))
#                     rq = models.movi.objects.filter(pk=1).values()
#                     return render(request, 'adm.html', {'form': forms.produto,
#                                                         'prod': models.Produtocad.objects.all(),
#                                                         'logado': get_user(request),
#                                                         'mov': rq[0]['movimento']
#                                                         })
#             if 'tipo' in rq:
#                 if 'img_prod' in request.FILES:
#                     rf= request.FILES
#                 new_prod = forms.produto(rq,rf)
#
#                 if new_prod.is_valid():
#
#
#                     pprint(request.FILES['img_prod'])
#                     cloudinary.uploader.upload(rf['img_prod'], folder="produtos")
#                     new_prod.save()
#                     messages.success(request, "Produto cadastrado !")
#                     return redirect('administrador')
#                 else:
#                     messages.warning(request, "Dados inválidos !")
#
#             if 'relator' in rq:
#
#                 if len(rq) <5 and rq['date_ate'] == '' and rq['date_de'] == '':
#                     messages.warning(request, "Sem dados para conulta !")
#
#                 # comandas
#                 if rq['relator'] == 'relacomanda':
#
#                     result = models.Comanda.objects.all()
#
#                     # filtros
#                     if rq['nmesa_comanda'] != '':
#                         result = result.filter(
#                             n_mesa=rq['nmesa_comanda']
#                         )
#                     if rq['nome_comanda'] != '':
#                         result = result.filter(
#                             nome=rq['nome_comanda']
#                         )
#                     if rq['date_de'] != '':
#                         result = result.exclude(
#                             data =datetime.datetime.strptime(rq['date_de'], '%Y-%m-%dT%H:%M')
#                         )
#
#                     if rq['date_ate'] != '':
#                         result = result.filter(
#                             data =datetime.datetime.strptime(rq['date_ate'], '%Y-%m-%dT%H:%M')
#                         )
#
#                     if 'cat_comanda' in rq and rq['cat_comanda'] != '':
#                         result = result.order_by(rq['cat_comanda'])
#
#                     if 'status_comanda' in rq and rq['status_comanda'] != '':
#                         result = result.filter(status= rq['status_comanda'])
#
#                     # if rq['nmesa_comanda'] == '' and rq['nome_comanda'] == '' and rq['date_de'] == '' and rq['date_ate'] == '':
#                     #     result = models.Comanda.objects.all()
#
#                 # pedidos
#                 elif rq['relator'] == 'relaped':
#                     if len(rq) < 5 and rq['date_ate'] == '' and rq['date_de'] == '':
#                         messages.warning(request, "Sem dados para conulta !")
#                     result = models.Pedido.objects.all()
#                     if rq['date_de'] != '':
#                         result = result.exclude(
#                             data =datetime.datetime.strptime(rq['date_de'], '%Y-%m-%dT%H:%M')
#                         )
#
#                     if rq['date_ate'] != '':
#                         result = result.filter(
#                             data =datetime.datetime.strptime(rq['date_ate'], '%Y-%m-%dT%H:%M')
#                         )
#                     if rq['nmesa_comanda'] != '':
#                         result = result.filter(comandaref__n_mesa__contains = rq['nmesa_comanda'])
#                     if rq['nome_comanda'] != '':
#                         result = result.filter(comandaref__nome__contains = rq['nome_comanda'])
#                     if 'cat_comanda' in rq and rq['cat_comanda'] != '':
#                         result = result.order_by(rq['cat_comanda'])
#                     if 'statsped[]' in rq and rq['statsped[]'] != '':
#                         pprint(rq['statsped[]'])
#                         re = rq.getlist('statsped[]')
#                         pprint(re)
#                         result = result.filter(status__in=rq['statsped[]'])
#                         # for i in re:
#                         #     print('do status', i)
#
#
#
#                 # produtos
#                 elif rq['relator'] == 'relaprod':
#                     if len(rq) < 5 and rq['date_ate'] == '' and rq['date_de'] == '':
#                         messages.warning(request, "Sem dados para conulta !")
#                     result = models.Produtocad.objects.all()
#                     if rq['date_de'] != '':
#                         result = result.exclude(
#                             data =datetime.datetime.strptime(rq['date_de'], '%Y-%m-%dT%H:%M')
#                         )
#
#                     if rq['date_ate'] != '':
#                         result = result.filter(
#                             data =datetime.datetime.strptime(rq['date_ate'], '%Y-%m-%dT%H:%M')
#                         )
#                     if 'selec_produto[]' in rq and rq['selec_produto[]'] != '':
#                         re = rq.getlist('selec_produto[]')
#                         pprint(re)
#                         result = result.filter(pk__in=re)
#                     if 'tipo_prod' in rq and rq['tipo_prod'] != '':
#                         result = result.order_by(rq['tipo_prod'])
#                     if 'cat_comanda' in rq and rq['cat_comanda'] != '':
#                         result = result.filter(tipo__in=rq['cat_comanda'])
#
#
#                 # recebimentos
#                 elif rq['relator'] == 'relareceb':
#                     result = models.pagamentos.objects.all()
#                     if len(rq) < 5 and rq['date_ate'] == '' and rq['date_de'] == '':
#                         messages.warning(request, "Sem dados para conulta !")
#
#                     if rq['date_de'] != '':
#                         result = result.exclude(
#                             data =datetime.datetime.strptime(rq['date_de'], '%Y-%m-%dT%H:%M')
#                         )
#                         pprint(result)
#                         print('nodate')
#                     if rq['date_ate'] != '':
#                         result = result.filter(
#                             data =datetime.datetime.strptime(rq['date_ate'], '%Y-%m-%dT%H:%M')
#                         )
#
#                 req = models.movi.objects.filter(pk=1).values()
#                 print('relatoriopae')
#                 return render(request, 'relatorio.html', {
#                                                     'relatorio': result,
#                                                     'logado': get_user(request),
#                                                     'tp': rq['relator'],
#                                                     'mov': req
#                                                     })
#         else:
#
#
#
#             rq = models.movi.objects.filter(pk=1).values()
#             # estado_mov = models.movi.objects.filter(pk=1)
#             # print(rq)
#             return render(request, 'adm.html', {'form': forms.produto,
#                                                 'prod': models.Produtocad.objects.all(),
#                                                 'logado': get_user(request),
#                                                 'mov': rq[0]['movimento']
#                                                 })
#     else:
#         messages.danger(request, "Você não tem permissão para acessar esta página.")
#         return redirect('index')
# # Create your views here.
