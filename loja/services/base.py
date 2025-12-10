"""
Base service interfaces and response classes.
All external integrations should implement these interfaces.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Optional, List
from datetime import datetime


# ============== ENUMS ==============

class PaymentStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class PaymentMethod(Enum):
    PIX = "pix"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    BOLETO = "boleto"


class ShipmentStatus(Enum):
    PENDING = "pending"
    POSTED = "posted"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    RETURNED = "returned"


# ============== DATA CLASSES ==============

@dataclass
class PixResponse:
    """Response from PIX creation"""
    qr_code: str  # Base64 image
    qr_code_text: str  # Copy-paste code
    transaction_id: str
    expires_at: datetime


@dataclass
class CardChargeResponse:
    """Response from card charge"""
    transaction_id: str
    status: PaymentStatus
    authorization_code: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class BoletoResponse:
    """Response from boleto creation"""
    barcode: str
    digitable_line: str
    pdf_url: str
    transaction_id: str
    due_date: datetime


@dataclass
class PaymentStatusResponse:
    """Response from payment status check"""
    transaction_id: str
    status: PaymentStatus
    paid_at: Optional[datetime] = None
    amount_paid: Optional[Decimal] = None


@dataclass
class ShippingOption:
    """A shipping option with carrier and price"""
    carrier_code: str
    carrier_name: str
    service_name: str
    price: Decimal
    delivery_days: int
    delivery_range: tuple  # (min_days, max_days)


@dataclass 
class ShipmentResponse:
    """Response from shipment creation"""
    shipment_id: str
    tracking_code: Optional[str] = None
    label_url: Optional[str] = None


@dataclass
class TrackingEvent:
    """A tracking event"""
    status: str
    description: str
    location: Optional[str]
    timestamp: datetime


@dataclass
class TrackingInfo:
    """Tracking information for a shipment"""
    tracking_code: str
    status: ShipmentStatus
    events: List[TrackingEvent]


@dataclass
class NFeResponse:
    """Response from NF-e emission"""
    nfe_id: str
    nfe_number: str
    access_key: str  # Chave de acesso
    status: str
    xml_url: Optional[str] = None
    pdf_url: Optional[str] = None


# ============== INTERFACES ==============

class PaymentServiceInterface(ABC):
    """
    Interface for payment gateway integrations.
    Implementations: MercadoPago, PagSeguro, Stripe
    """
    
    @abstractmethod
    def create_pix(self, order_id: int, amount: Decimal, 
                   customer_email: str, description: str) -> PixResponse:
        """Generate PIX QR code for payment"""
        pass
    
    @abstractmethod
    def create_card_charge(self, order_id: int, amount: Decimal,
                          card_token: str, installments: int = 1) -> CardChargeResponse:
        """Process credit/debit card payment"""
        pass
    
    @abstractmethod
    def create_boleto(self, order_id: int, amount: Decimal,
                     customer_data: dict, due_days: int = 3) -> BoletoResponse:
        """Generate boleto bancário"""
        pass
    
    @abstractmethod
    def check_payment_status(self, transaction_id: str) -> PaymentStatusResponse:
        """Check payment status by transaction ID"""
        pass
    
    @abstractmethod
    def refund_payment(self, transaction_id: str, 
                       amount: Optional[Decimal] = None) -> bool:
        """Refund a payment (partial or full)"""
        pass
    
    @abstractmethod
    def process_webhook(self, payload: dict) -> PaymentStatusResponse:
        """Process webhook notification from payment gateway"""
        pass


class ShippingServiceInterface(ABC):
    """
    Interface for shipping carrier integrations.
    Implementations: MelhorEnvio, Correios, Kangu
    """
    
    @abstractmethod
    def calculate_shipping(self, zip_from: str, zip_to: str,
                          items: List[dict]) -> List[ShippingOption]:
        """
        Calculate shipping options.
        items: [{"weight": 0.5, "height": 10, "width": 15, "length": 20, "quantity": 1}]
        """
        pass
    
    @abstractmethod
    def create_shipment(self, order_id: int, carrier_code: str,
                       sender: dict, recipient: dict,
                       items: List[dict]) -> ShipmentResponse:
        """Create shipment and generate label"""
        pass
    
    @abstractmethod
    def get_tracking(self, tracking_code: str) -> TrackingInfo:
        """Get tracking information"""
        pass
    
    @abstractmethod
    def cancel_shipment(self, shipment_id: str) -> bool:
        """Cancel a shipment"""
        pass


class InvoiceServiceInterface(ABC):
    """
    Interface for NF-e (Nota Fiscal Eletrônica) integrations.
    Implementations: Bling, TinyERP, NuvemFiscal
    """
    
    @abstractmethod
    def emit_nfe(self, order_id: int, customer_data: dict,
                items: List[dict], shipping_value: Decimal) -> NFeResponse:
        """Emit NF-e for an order"""
        pass
    
    @abstractmethod
    def cancel_nfe(self, nfe_id: str, reason: str) -> bool:
        """Cancel an emitted NF-e"""
        pass
    
    @abstractmethod
    def get_nfe_xml(self, nfe_id: str) -> str:
        """Get NF-e XML content"""
        pass
    
    @abstractmethod
    def get_nfe_pdf(self, nfe_id: str) -> bytes:
        """Get NF-e PDF (DANFE)"""
        pass


class MarketplaceServiceInterface(ABC):
    """
    Interface for marketplace integrations.
    Implementations: MercadoLivre, Magalu, Shopee
    """
    
    @abstractmethod
    def sync_product(self, product_id: int) -> dict:
        """Sync product to marketplace, returns marketplace product ID"""
        pass
    
    @abstractmethod
    def update_stock(self, product_id: int, quantity: int) -> bool:
        """Update stock on marketplace"""
        pass
    
    @abstractmethod
    def update_price(self, product_id: int, price: Decimal) -> bool:
        """Update price on marketplace"""
        pass
    
    @abstractmethod
    def import_orders(self) -> List[dict]:
        """Import new orders from marketplace"""
        pass
    
    @abstractmethod
    def update_order_status(self, marketplace_order_id: str, 
                           status: str, tracking_code: Optional[str] = None) -> bool:
        """Update order status on marketplace"""
        pass
