from django.urls import path, include
from django.contrib import admin
from loja import views, checkout_views, feed_views

from django.conf import urls, settings
from . import settings
from django.conf.urls.static import static

app_name = 'gbstr'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('conta', views.conta, name='conta'),
    path('prod', views.prod, name='prod'),
    path('pagamento', views.pagamento, name='pagamento'),
    # path('', include('pwa.urls')),
    path('logout', views.logoutuser, name='logout'),
    path('privacy_poli', views.term_condition, name='term_cond'),
    
    # Checkout Routes
    path('checkout/cart/', checkout_views.checkout_cart, name='checkout_cart'),
    path('checkout/address/', checkout_views.checkout_address, name='checkout_address'),
    path('checkout/payment/', checkout_views.checkout_payment, name='checkout_payment'),
    path('checkout/process/', checkout_views.process_payment, name='process_payment'),
    path('checkout/success/', checkout_views.checkout_success, name='checkout_success'),
    
    # Feed Routes
    path('feed/', feed_views.feed_list, name='feed_list'),
    path('feed/<int:pk>/', feed_views.feed_detail, name='feed_detail'),

    # path('checkout/', include('django_pagarme.urls'))

    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
