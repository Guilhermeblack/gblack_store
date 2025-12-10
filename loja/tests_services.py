"""
Tests for the services layer.
Tests mock implementations to ensure interfaces work correctly.
"""
from decimal import Decimal
from datetime import datetime
from django.test import TestCase, override_settings

from loja.services import (
    get_payment_service,
    get_shipping_service,
    get_invoice_service,
    get_marketplace_service
)
from loja.services.base import PaymentStatus, ShipmentStatus


class PaymentServiceTest(TestCase):
    """Test payment service interface."""
    
    def setUp(self):
        self.service = get_payment_service()
    
    def test_create_pix(self):
        """Test PIX creation returns valid response."""
        response = self.service.create_pix(
            order_id=1,
            amount=Decimal('100.00'),
            customer_email='test@test.com',
            description='Test order'
        )
        
        self.assertIsNotNone(response.qr_code)
        self.assertIsNotNone(response.qr_code_text)
        self.assertIsNotNone(response.transaction_id)
        self.assertIsInstance(response.expires_at, datetime)
    
    def test_create_card_charge(self):
        """Test card charge returns valid response."""
        response = self.service.create_card_charge(
            order_id=1,
            amount=Decimal('100.00'),
            card_token='MOCK_TOKEN'
        )
        
        self.assertIsNotNone(response.transaction_id)
        self.assertEqual(response.status, PaymentStatus.APPROVED)
    
    def test_create_boleto(self):
        """Test boleto creation returns valid response."""
        response = self.service.create_boleto(
            order_id=1,
            amount=Decimal('100.00'),
            customer_data={'email': 'test@test.com'}
        )
        
        self.assertIsNotNone(response.barcode)
        self.assertIsNotNone(response.transaction_id)
        self.assertIsInstance(response.due_date, datetime)
    
    def test_check_payment_status(self):
        """Test payment status check."""
        response = self.service.check_payment_status('MOCK-123')
        
        self.assertEqual(response.transaction_id, 'MOCK-123')
        self.assertIn(response.status, list(PaymentStatus))
    
    def test_refund_payment(self):
        """Test payment refund."""
        result = self.service.refund_payment('MOCK-123')
        self.assertTrue(result)


class ShippingServiceTest(TestCase):
    """Test shipping service interface."""
    
    def setUp(self):
        self.service = get_shipping_service()
    
    def test_calculate_shipping(self):
        """Test shipping calculation returns options."""
        options = self.service.calculate_shipping(
            zip_from='01310100',
            zip_to='04538132',
            items=[{'weight': 0.5, 'height': 10, 'width': 15, 'length': 20}]
        )
        
        self.assertIsInstance(options, list)
        self.assertGreater(len(options), 0)
        
        for option in options:
            self.assertIsNotNone(option.carrier_code)
            self.assertIsNotNone(option.carrier_name)
            self.assertIsInstance(option.price, Decimal)
            self.assertIsInstance(option.delivery_days, int)
    
    def test_create_shipment(self):
        """Test shipment creation."""
        response = self.service.create_shipment(
            order_id=1,
            carrier_code='correios-sedex',
            sender={'name': 'Store', 'postal_code': '01310100'},
            recipient={'name': 'Customer', 'postal_code': '04538132'},
            items=[{'weight': 0.5}]
        )
        
        self.assertIsNotNone(response.shipment_id)
        self.assertIsNotNone(response.tracking_code)
    
    def test_get_tracking(self):
        """Test tracking retrieval."""
        info = self.service.get_tracking('BR123456789BR')
        
        self.assertEqual(info.tracking_code, 'BR123456789BR')
        self.assertIn(info.status, list(ShipmentStatus))
    
    def test_cancel_shipment(self):
        """Test shipment cancellation."""
        result = self.service.cancel_shipment('MOCK-SHIP-1')
        self.assertTrue(result)


class InvoiceServiceTest(TestCase):
    """Test invoice service interface."""
    
    def setUp(self):
        self.service = get_invoice_service()
    
    def test_emit_nfe(self):
        """Test NF-e emission."""
        response = self.service.emit_nfe(
            order_id=1,
            customer_data={'name': 'Test', 'cpf_cnpj': '12345678900'},
            items=[{'name': 'Product', 'quantity': 1, 'unit_price': 100}],
            shipping_value=Decimal('20.00')
        )
        
        self.assertIsNotNone(response.nfe_id)
        self.assertIsNotNone(response.nfe_number)
        self.assertIsNotNone(response.access_key)
    
    def test_cancel_nfe(self):
        """Test NF-e cancellation."""
        result = self.service.cancel_nfe('MOCK-NFE-1', 'Test cancellation')
        self.assertTrue(result)
    
    def test_get_nfe_xml(self):
        """Test NF-e XML retrieval."""
        xml = self.service.get_nfe_xml('MOCK-NFE-1')
        self.assertIn('xml', xml.lower())
    
    def test_get_nfe_pdf(self):
        """Test NF-e PDF retrieval."""
        pdf = self.service.get_nfe_pdf('MOCK-NFE-1')
        self.assertIsInstance(pdf, bytes)


class MarketplaceServiceTest(TestCase):
    """Test marketplace service interface."""
    
    def test_get_mock_marketplace(self):
        """Test mock marketplace service."""
        service = get_marketplace_service('mock')
        
        # Test sync product
        result = service.sync_product(1)
        self.assertIn('marketplace_id', result)
        
        # Test update stock
        self.assertTrue(service.update_stock(1, 10))
        
        # Test update price
        self.assertTrue(service.update_price(1, Decimal('99.99')))
        
        # Test import orders
        orders = service.import_orders()
        self.assertIsInstance(orders, list)
        
        # Test update order status
        self.assertTrue(service.update_order_status('ORDER-1', 'shipped'))
    
    def test_get_mercadolivre_service(self):
        """Test MercadoLivre service instantiation."""
        service = get_marketplace_service('mercadolivre')
        self.assertEqual(service.marketplace_name, 'MercadoLivre')
    
    def test_get_magalu_service(self):
        """Test Magalu service instantiation."""
        service = get_marketplace_service('magalu')
        self.assertEqual(service.marketplace_name, 'Magalu')
    
    def test_get_shopee_service(self):
        """Test Shopee service instantiation."""
        service = get_marketplace_service('shopee')
        self.assertEqual(service.marketplace_name, 'Shopee')
