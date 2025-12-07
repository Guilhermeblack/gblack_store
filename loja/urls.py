from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

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
]
