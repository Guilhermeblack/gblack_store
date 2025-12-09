from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal
import django
from django.conf import settings

if not settings.configured:
    django.setup()

print("INSTALLED_APPS:", settings.INSTALLED_APPS)
print("DATABASES:", settings.DATABASES)

# Models will be imported inside methods to avoid AppRegistryNotReady or similar issues during discovery if setup is flaky


class SalesFlowTests(TestCase):
    def setUp(self):
        from loja.models import Produto, Carrinho, CartItem, Venda, Address
        User = get_user_model()
        # Create User
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            first_name='Test',
            last_name='User',
            cpf='12345678901'
        )
        # Create cart for user
        self.carrinho = Carrinho.objects.create(cliente=self.user)
        
        self.client = Client()
        # Login using username, not email
        self.client.login(username='testuser', password='password123')

        # Create Product
        self.product = Produto.objects.create(
            nome='Test Product',
            preco=Decimal('100.00'),
            estoque=10,
            tipo='R'
        )

    def test_add_to_cart(self):
        from loja.models import Carrinho
        # Simulate adding to cart via prod view (or directly via model for unit test, but view is better for flow)
        # My prod view expects POST with 'add_carrinho'
        response = self.client.post(reverse('prod'), {'add_carrinho': self.product.id})
        
        # Check if item is in cart
        carrinho = Carrinho.objects.get(cliente=self.user)
        self.assertEqual(carrinho.items.count(), 1)
        item = carrinho.items.first()
        self.assertEqual(item.produto, self.product)
        self.assertEqual(item.quantidade, 1)

    def test_checkout_cart_view(self):
        from loja.models import Carrinho, CartItem
        # Add item to existing cart
        CartItem.objects.create(carrinho=self.carrinho, produto=self.product, quantidade=2)
        
        response = self.client.get(reverse('checkout_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
        self.assertContains(response, 'Test Product')
        # Check context for total to avoid L10N issues
        self.assertEqual(response.context['carrinho'].get_total(), Decimal('200.00'))

    def test_checkout_address_creation(self):
        from loja.models import Address
        response = self.client.post(reverse('checkout_address'), {
            'street': 'Rua Teste',
            'number': '123',
            'neighborhood': 'Bairro Teste',
            'city': 'Cidade Teste',
            'state': 'SP',
            'zip_code': '12345-678'
        })
        self.assertEqual(response.status_code, 302) # Redirect to payment
        self.assertTrue(Address.objects.filter(cliente=self.user, street='Rua Teste').exists())

    def test_process_payment_and_order_creation(self):
        from loja.models import Carrinho, CartItem, Address, Venda
        import json
        # Setup Cart and Address
        CartItem.objects.create(carrinho=self.carrinho, produto=self.product, quantidade=1)
        address = Address.objects.create(
            cliente=self.user, street='Rua Teste', number='123',
            neighborhood='Bairro', city='Cidade', state='SP', zip_code='12345'
        )
        
        # Set session
        session = self.client.session
        session['checkout_address_id'] = address.id
        session.save()
        
        # Store address in session (as my view logic might rely on it or I need to ensure it picks the last one)
        # Actually my view `process_payment` gets the last address: `address = request.user.addresses.last()`
        
        response = self.client.post(reverse('process_payment'), 
                                    content_type='application/json',
                                    data=json.dumps({'method': 'PIX'}))
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
        
        # Verify Order
        venda = Venda.objects.first()
        self.assertIsNotNone(venda)
        self.assertEqual(venda.cliente, self.user)
        self.assertEqual(venda.total, Decimal('100.00'))
        self.assertEqual(venda.status, 'PAID')
        
        # Verify Stock
        self.product.refresh_from_db()
        self.assertEqual(self.product.estoque, 9)
        
        # Verify Cart Empty
        self.assertEqual(self.carrinho.items.count(), 0)

