from django.urls import path, include
from django.contrib import admin
from loja import views
from django.conf import urls, settings
from django.conf.urls.static import static

app_name = 'loja'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('', include('pwa.urls')),
    path('conta', views.conta, name='conta'),
    path('pagamento', views.pagamento, name='pagamento'),
    path('logout', views.logoutuser, name='logout'),
    # path('ped', views.ped, name='pedidos'),
    # path('adm', views.adm, name='administrador'),
    # path('profile', views.profile, name='profile'),
    # path('pedidos', views.ped, name='pedidos'),
    # path('sobre', views.sobre, name='sobre'),
    path('checkout/', include('django_pagarme.urls'))
    # path('loguin/', include('urls', namespace='log')),

    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
