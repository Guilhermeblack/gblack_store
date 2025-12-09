from django.test import TestCase
from django.core.management import call_command
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from loja.models import Produto, Carrinho, StoreConfig

class AdvancedCartTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.produto = Produto.objects.create(
            nome='Test Product',
            preco=100.00,
            tipo='A',
            estoque=10,
            is_available=True
        )
        StoreConfig.objects.create(cart_expiration_days=3)

    def test_guest_cart_creation_and_stock_reservation(self):
        # 1. Add item as guest
        url = '/api/v1/cart/add_item/'
        guest_id = 'guest-123'
        data = {'product_id': self.produto.id, 'quantity': 2}
        
        response = self.client.post(url, data, format='json', headers={'X-Guest-ID': guest_id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 2. Verify Cart Created
        carrinho = Carrinho.objects.get(session_id=guest_id)
        self.assertEqual(carrinho.items.count(), 1)
        self.assertEqual(carrinho.items.first().quantidade, 2)
        
        # 3. Verify Stock Decremented
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.estoque, 8) # 10 - 2

    def test_stock_restoration_on_remove(self):
        # 1. Add item
        url = '/api/v1/cart/add_item/'
        guest_id = 'guest-123'
        self.client.post(url, {'product_id': self.produto.id, 'quantity': 2}, format='json', headers={'X-Guest-ID': guest_id})
        
        carrinho = Carrinho.objects.get(session_id=guest_id)
        item_id = carrinho.items.first().id
        
        # 2. Remove item
        url_remove = '/api/v1/cart/remove_item/'
        self.client.post(url_remove, {'item_id': item_id}, format='json', headers={'X-Guest-ID': guest_id})
        
        # 3. Verify Stock Restored
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.estoque, 10)

    def test_cart_expiration_cleanup(self):
        # 1. Create expired cart
        guest_id = 'expired-guest'
        carrinho = Carrinho.objects.create(session_id=guest_id)
        # Manually create item and decrement stock
        from loja.models import CartItem
        CartItem.objects.create(carrinho=carrinho, produto=self.produto, quantidade=3)
        self.produto.estoque = 7
        self.produto.save()
        
        # Backdate cart
        expired_date = timezone.now() - timezone.timedelta(days=4)
        Carrinho.objects.filter(id=carrinho.id).update(updated_at=expired_date)
        
        # 2. Run cleanup command
        call_command('cleanup_carts')
        
        # 3. Verify Cart Deleted and Stock Restored
        self.assertFalse(Carrinho.objects.filter(id=carrinho.id).exists())
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.estoque, 10) # 7 + 3
