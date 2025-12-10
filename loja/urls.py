from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views
from . import webhook_views

router = DefaultRouter()
router.register(r'products', api_views.ProdutoViewSet, basename='product')
router.register(r'cart', api_views.CarrinhoViewSet, basename='cart')
router.register(r'user', api_views.UserViewSet, basename='user')
router.register(r'address', api_views.AddressViewSet, basename='address')
router.register(r'orders', api_views.VendaViewSet, basename='order')
router.register(r'feed', api_views.FeedViewSet, basename='feed')

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    
    # Webhooks for external services
    path('webhooks/payment/', webhook_views.payment_webhook, name='payment_webhook'),
    path('webhooks/shipping/', webhook_views.shipping_webhook, name='shipping_webhook'),
    path('webhooks/marketplace/<str:marketplace>/', webhook_views.marketplace_webhook, name='marketplace_webhook'),
]
