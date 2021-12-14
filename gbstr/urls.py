from django.urls import path, include
from django.contrib import admin
from loja import views

from django.conf import urls, settings
from gbstr import settings
from django.conf.urls.static import static

app_name = 'gbstr'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('conta', views.conta, name='conta'),
    path('prod', views.prod, name='prod'),
    path('pagamento', views.pagamento, name='pagamento'),
    path('', include('pwa.urls')),
    path('logout', views.logoutuser, name='logout'),

    # path('checkout/', include('django_pagarme.urls'))

    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
