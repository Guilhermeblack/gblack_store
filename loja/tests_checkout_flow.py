from django.test import TestCase
from django.contrib.auth import get_user_model
from loja.models import Produto, Carrinho, CartItem, Address, Venda, PaymentTransaction
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class CheckoutFlowTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password', email='test@example.com')
        self.client.force_authenticate(user=self.user)
        
        self.produto = Produto.objects.create(
            nome='Test Product',
            preco=100.00,
            tipo='A',
            estoque=10,
            is_available=True,
            img_prod='sample.jpg'
        )
        
        self.address = Address.objects.create(
            cliente=self.user,
            street='Test Street',
            number='123',
            neighborhood='Test Neighborhood',
            city='Test City',
            state='TS',
            zip_code='12345678'
        )
        
        # Add item to cart
        self.carrinho = Carrinho.objects.create(cliente=self.user)
        self.cart_item = CartItem.objects.create(carrinho=self.carrinho, produto=self.produto, quantidade=2)

    def test_checkout_success(self):
        url = '/api/v1/orders/checkout/'
        data = {
            'address_id': self.address.id,
            'payment_method': 'PIX'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        
        # Verify Order Created
        venda = Venda.objects.get(id=response.data['venda_id'])
        self.assertEqual(venda.cliente, self.user)
        self.assertEqual(venda.total, 200.00) # 2 * 100
        self.assertEqual(venda.status, 'PAID')
        
        # Verify Stock Decremented
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.estoque, 8) # 10 - 2
        
        # Verify Cart Empty
        self.assertEqual(self.carrinho.items.count(), 0)
        
        # Verify Transaction
        transaction = PaymentTransaction.objects.get(venda=venda)
        self.assertEqual(transaction.amount, 200.00)
        self.assertEqual(transaction.method, 'PIX')
        self.assertEqual(transaction.status, 'APPROVED')

    def test_checkout_insufficient_stock(self):
        # Set stock to 1
        self.produto.estoque = 1
        self.produto.save()
        
        url = '/api/v1/orders/checkout/'
        data = {
            'address_id': self.address.id,
            'payment_method': 'PIX'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Estoque insuficiente', response.data['error'])
