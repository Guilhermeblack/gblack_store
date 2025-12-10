"""
Marketplace Integration Services.
Supports: MercadoLivre, Magalu (Magazine Luiza), Shopee

Each marketplace requires separate OAuth/API credentials.
"""
import logging
from decimal import Decimal
from typing import List, Optional
from abc import ABC

from django.conf import settings

from .base import MarketplaceServiceInterface

logger = logging.getLogger(__name__)


class BaseMarketplaceService(MarketplaceServiceInterface, ABC):
    """Base class with common marketplace functionality."""
    
    marketplace_name: str = "Unknown"
    
    def log_sync(self, action: str, product_id: int, success: bool):
        status = "SUCCESS" if success else "FAILED"
        logger.info(f"[{self.marketplace_name}] {action} product {product_id}: {status}")


class MercadoLivreService(BaseMarketplaceService):
    """
    MercadoLivre integration.
    https://developers.mercadolivre.com.br/
    
    Required settings:
    - MERCADOLIVRE_ACCESS_TOKEN
    - MERCADOLIVRE_USER_ID
    """
    
    marketplace_name = "MercadoLivre"
    BASE_URL = "https://api.mercadolibre.com"
    
    def __init__(self):
        self.access_token = getattr(settings, 'MERCADOLIVRE_ACCESS_TOKEN', '')
        self.user_id = getattr(settings, 'MERCADOLIVRE_USER_ID', '')
    
    @property
    def headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def sync_product(self, product_id: int) -> dict:
        """
        Sync product to MercadoLivre.
        
        TODO: Implement API call to POST /items
        """
        logger.info(f"[MercadoLivre] Syncing product {product_id}")
        # Placeholder - needs actual ML category/attribute mapping
        return {"marketplace_id": f"MLB{product_id}000000", "status": "pending"}
    
    def update_stock(self, product_id: int, quantity: int) -> bool:
        logger.info(f"[MercadoLivre] Updating stock for {product_id}: {quantity}")
        return True
    
    def update_price(self, product_id: int, price: Decimal) -> bool:
        logger.info(f"[MercadoLivre] Updating price for {product_id}: R${price}")
        return True
    
    def import_orders(self) -> List[dict]:
        """
        Import orders from MercadoLivre.
        GET /orders/search?seller={user_id}&order.status=paid
        """
        logger.info("[MercadoLivre] Importing orders")
        return []  # Would return list of order dicts
    
    def update_order_status(self, marketplace_order_id: str,
                           status: str, tracking_code: Optional[str] = None) -> bool:
        logger.info(f"[MercadoLivre] Updating order {marketplace_order_id}: {status}")
        return True


class MagaluService(BaseMarketplaceService):
    """
    Magazine Luiza Marketplace integration.
    https://dev.magalu.com/
    
    Required settings:
    - MAGALU_CLIENT_ID
    - MAGALU_CLIENT_SECRET
    - MAGALU_ACCESS_TOKEN
    """
    
    marketplace_name = "Magalu"
    BASE_URL = "https://api.magalu.com"
    
    def __init__(self):
        self.client_id = getattr(settings, 'MAGALU_CLIENT_ID', '')
        self.client_secret = getattr(settings, 'MAGALU_CLIENT_SECRET', '')
        self.access_token = getattr(settings, 'MAGALU_ACCESS_TOKEN', '')
    
    def sync_product(self, product_id: int) -> dict:
        logger.info(f"[Magalu] Syncing product {product_id}")
        return {"marketplace_id": f"MAGALU-{product_id}", "status": "pending"}
    
    def update_stock(self, product_id: int, quantity: int) -> bool:
        logger.info(f"[Magalu] Updating stock for {product_id}: {quantity}")
        return True
    
    def update_price(self, product_id: int, price: Decimal) -> bool:
        logger.info(f"[Magalu] Updating price for {product_id}: R${price}")
        return True
    
    def import_orders(self) -> List[dict]:
        logger.info("[Magalu] Importing orders")
        return []
    
    def update_order_status(self, marketplace_order_id: str,
                           status: str, tracking_code: Optional[str] = None) -> bool:
        logger.info(f"[Magalu] Updating order {marketplace_order_id}: {status}")
        return True


class ShopeeService(BaseMarketplaceService):
    """
    Shopee integration.
    https://open.shopee.com/
    
    Required settings:
    - SHOPEE_PARTNER_ID
    - SHOPEE_PARTNER_KEY
    - SHOPEE_SHOP_ID
    - SHOPEE_ACCESS_TOKEN
    """
    
    marketplace_name = "Shopee"
    BASE_URL = "https://partner.shopeemobile.com/api/v2"
    
    def __init__(self):
        self.partner_id = getattr(settings, 'SHOPEE_PARTNER_ID', '')
        self.partner_key = getattr(settings, 'SHOPEE_PARTNER_KEY', '')
        self.shop_id = getattr(settings, 'SHOPEE_SHOP_ID', '')
        self.access_token = getattr(settings, 'SHOPEE_ACCESS_TOKEN', '')
    
    def sync_product(self, product_id: int) -> dict:
        logger.info(f"[Shopee] Syncing product {product_id}")
        return {"marketplace_id": f"SHOPEE-{product_id}", "status": "pending"}
    
    def update_stock(self, product_id: int, quantity: int) -> bool:
        logger.info(f"[Shopee] Updating stock for {product_id}: {quantity}")
        return True
    
    def update_price(self, product_id: int, price: Decimal) -> bool:
        logger.info(f"[Shopee] Updating price for {product_id}: R${price}")
        return True
    
    def import_orders(self) -> List[dict]:
        logger.info("[Shopee] Importing orders")
        return []
    
    def update_order_status(self, marketplace_order_id: str,
                           status: str, tracking_code: Optional[str] = None) -> bool:
        logger.info(f"[Shopee] Updating order {marketplace_order_id}: {status}")
        return True


class MockMarketplaceService(MarketplaceServiceInterface):
    """Mock marketplace service for development."""
    
    def sync_product(self, product_id: int) -> dict:
        return {"marketplace_id": f"MOCK-{product_id}", "status": "active"}
    
    def update_stock(self, product_id: int, quantity: int) -> bool:
        return True
    
    def update_price(self, product_id: int, price: Decimal) -> bool:
        return True
    
    def import_orders(self) -> List[dict]:
        return []
    
    def update_order_status(self, marketplace_order_id: str,
                           status: str, tracking_code: Optional[str] = None) -> bool:
        return True


def get_marketplace_service(marketplace: str) -> MarketplaceServiceInterface:
    """
    Factory function to get marketplace service by name.
    
    Args:
        marketplace: 'mercadolivre', 'magalu', 'shopee', or 'mock'
    """
    services = {
        'mercadolivre': MercadoLivreService,
        'magalu': MagaluService,
        'shopee': ShopeeService,
        'mock': MockMarketplaceService,
    }
    
    service_class = services.get(marketplace.lower(), MockMarketplaceService)
    return service_class()


def get_all_marketplace_services() -> List[MarketplaceServiceInterface]:
    """Get all configured marketplace services."""
    enabled = getattr(settings, 'ENABLED_MARKETPLACES', [])
    return [get_marketplace_service(mp) for mp in enabled]
