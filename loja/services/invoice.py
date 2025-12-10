"""
Invoice (NF-e) Service Implementation.
Currently a placeholder/stub for future integration.

Popular providers in Brazil:
- Bling (https://developer.bling.com.br/)
- Tiny ERP (https://tiny.com.br/)
- Nuvem Fiscal (https://nuvemfiscal.com.br/)
"""
import logging
from decimal import Decimal
from typing import List

from django.conf import settings

from .base import (
    InvoiceServiceInterface,
    NFeResponse
)

logger = logging.getLogger(__name__)


class MockInvoiceService(InvoiceServiceInterface):
    """
    Mock invoice service for development.
    Replace with Bling, Tiny, or NuvemFiscal when ready.
    """
    
    def emit_nfe(self, order_id: int, customer_data: dict,
                items: List[dict], shipping_value: Decimal) -> NFeResponse:
        """
        Emit NF-e for an order.
        
        customer_data: {name, cpf_cnpj, email, address}
        items: [{name, ncm, quantity, unit_price}]
        """
        logger.info(f"[MOCK] Emitting NF-e for order {order_id}")
        
        return NFeResponse(
            nfe_id=f"MOCK-NFE-{order_id}",
            nfe_number=str(order_id + 1000),
            access_key=f"35241201234567890001550010000{order_id:06d}0000000000",
            status="authorized",
            xml_url=f"https://example.com/nfe/{order_id}.xml",
            pdf_url=f"https://example.com/danfe/{order_id}.pdf"
        )
    
    def cancel_nfe(self, nfe_id: str, reason: str) -> bool:
        logger.info(f"[MOCK] Cancelling NF-e {nfe_id}: {reason}")
        return True
    
    def get_nfe_xml(self, nfe_id: str) -> str:
        return f"<?xml version=\"1.0\"?><NFe><id>{nfe_id}</id><mock>true</mock></NFe>"
    
    def get_nfe_pdf(self, nfe_id: str) -> bytes:
        return b"MOCK PDF CONTENT"


class BlingInvoiceService(InvoiceServiceInterface):
    """
    Bling ERP integration for NF-e.
    
    Required settings:
    - BLING_API_KEY
    """
    
    BASE_URL = "https://bling.com.br/api/v3"
    
    def __init__(self):
        self.api_key = getattr(settings, 'BLING_API_KEY', '')
    
    @property
    def headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def emit_nfe(self, order_id: int, customer_data: dict,
                items: List[dict], shipping_value: Decimal) -> NFeResponse:
        """
        Emit NF-e via Bling API.
        
        TODO: Implement when Bling account is configured.
        Reference: https://developer.bling.com.br/api/1.0/nota-fiscal
        """
        raise NotImplementedError("Bling integration not configured. Set BLING_API_KEY.")
    
    def cancel_nfe(self, nfe_id: str, reason: str) -> bool:
        raise NotImplementedError("Bling integration not configured.")
    
    def get_nfe_xml(self, nfe_id: str) -> str:
        raise NotImplementedError("Bling integration not configured.")
    
    def get_nfe_pdf(self, nfe_id: str) -> bytes:
        raise NotImplementedError("Bling integration not configured.")


def get_invoice_service() -> InvoiceServiceInterface:
    """Factory function to get the configured invoice service."""
    provider = getattr(settings, 'INVOICE_PROVIDER', 'mock')
    
    if provider == 'bling':
        return BlingInvoiceService()
    else:
        return MockInvoiceService()
