"""
Melhor Envio Shipping Service Implementation.
https://docs.melhorenvio.com.br/

Requires: pip install requests
"""
import logging
from decimal import Decimal
from typing import List, Optional
from datetime import datetime

import requests
from django.conf import settings

from .base import (
    ShippingServiceInterface,
    ShippingOption,
    ShipmentResponse, 
    TrackingInfo,
    TrackingEvent,
    ShipmentStatus
)

logger = logging.getLogger(__name__)


class MelhorEnvioService(ShippingServiceInterface):
    """
    Melhor Envio integration for shipping calculation and label generation.
    Supports: Correios, Jadlog, Azul Cargo, Latam Cargo, etc.
    
    Required settings:
    - MELHORENVIO_TOKEN
    - MELHORENVIO_SANDBOX (True for testing)
    """
    
    SANDBOX_URL = "https://sandbox.melhorenvio.com.br/api/v2"
    PRODUCTION_URL = "https://melhorenvio.com.br/api/v2"
    
    def __init__(self):
        self.token = getattr(settings, 'MELHORENVIO_TOKEN', '')
        self.sandbox = getattr(settings, 'MELHORENVIO_SANDBOX', True)
        self.base_url = self.SANDBOX_URL if self.sandbox else self.PRODUCTION_URL
    
    @property
    def headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def calculate_shipping(self, zip_from: str, zip_to: str,
                          items: List[dict]) -> List[ShippingOption]:
        """
        Calculate shipping options.
        items: [{"weight": 0.5, "height": 10, "width": 15, "length": 20, "quantity": 1, "insurance_value": 100}]
        """
        # Calculate total dimensions and weight
        total_weight = sum(item.get("weight", 0.3) * item.get("quantity", 1) for item in items)
        max_height = max(item.get("height", 5) for item in items)
        max_width = max(item.get("width", 15) for item in items)
        max_length = max(item.get("length", 20) for item in items)
        total_value = sum(item.get("insurance_value", 0) * item.get("quantity", 1) for item in items)
        
        payload = {
            "from": {"postal_code": zip_from.replace("-", "")},
            "to": {"postal_code": zip_to.replace("-", "")},
            "products": [
                {
                    "id": "1",
                    "width": max_width,
                    "height": max_height,
                    "length": max_length,
                    "weight": total_weight,
                    "insurance_value": total_value,
                    "quantity": 1
                }
            ]
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/me/shipment/calculate",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            logger.error(f"Melhor Envio calculate error: {e}")
            return []
        
        options = []
        for service in data:
            if service.get("error"):
                continue
                
            options.append(ShippingOption(
                carrier_code=f"{service.get('company', {}).get('id')}-{service.get('id')}",
                carrier_name=service.get("company", {}).get("name", ""),
                service_name=service.get("name", ""),
                price=Decimal(str(service.get("price", 0))),
                delivery_days=service.get("delivery_time", 0),
                delivery_range=(
                    service.get("delivery_range", {}).get("min", 0),
                    service.get("delivery_range", {}).get("max", 0)
                )
            ))
        
        return sorted(options, key=lambda x: x.price)
    
    def create_shipment(self, order_id: int, carrier_code: str,
                       sender: dict, recipient: dict,
                       items: List[dict]) -> ShipmentResponse:
        """
        Create shipment and generate label.
        
        sender/recipient: {name, phone, email, document, address, number, complement, neighborhood, city, state, postal_code}
        """
        # Parse carrier code
        company_id, service_id = carrier_code.split("-")
        
        # Step 1: Add to cart
        cart_payload = {
            "service": int(service_id),
            "from": {
                "name": sender.get("name"),
                "phone": sender.get("phone"),
                "email": sender.get("email"),
                "document": sender.get("document"),
                "address": sender.get("address"),
                "number": sender.get("number"),
                "complement": sender.get("complement", ""),
                "district": sender.get("neighborhood"),
                "city": sender.get("city"),
                "state_abbr": sender.get("state"),
                "postal_code": sender.get("postal_code").replace("-", "")
            },
            "to": {
                "name": recipient.get("name"),
                "phone": recipient.get("phone"),
                "email": recipient.get("email"),
                "document": recipient.get("document"),
                "address": recipient.get("address"),
                "number": recipient.get("number"),
                "complement": recipient.get("complement", ""),
                "district": recipient.get("neighborhood"),
                "city": recipient.get("city"),
                "state_abbr": recipient.get("state"),
                "postal_code": recipient.get("postal_code").replace("-", "")
            },
            "products": items,
            "options": {
                "insurance_value": sum(item.get("insurance_value", 0) for item in items),
                "receipt": False,
                "own_hand": False
            }
        }
        
        try:
            # Add to cart
            response = requests.post(
                f"{self.base_url}/me/cart",
                json=cart_payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            cart_data = response.json()
            shipment_id = cart_data.get("id")
            
            # Checkout (pay for label)
            checkout_response = requests.post(
                f"{self.base_url}/me/shipment/checkout",
                json={"orders": [shipment_id]},
                headers=self.headers,
                timeout=30
            )
            checkout_response.raise_for_status()
            
            # Generate label
            label_response = requests.post(
                f"{self.base_url}/me/shipment/generate",
                json={"orders": [shipment_id]},
                headers=self.headers,
                timeout=30
            )
            label_response.raise_for_status()
            
            # Get shipment details
            detail_response = requests.get(
                f"{self.base_url}/me/orders/{shipment_id}",
                headers=self.headers,
                timeout=30
            )
            detail_data = detail_response.json()
            
            return ShipmentResponse(
                shipment_id=shipment_id,
                tracking_code=detail_data.get("tracking"),
                label_url=f"{self.base_url}/me/shipment/print?orders={shipment_id}"
            )
            
        except requests.RequestException as e:
            logger.error(f"Melhor Envio create shipment error: {e}")
            raise Exception(f"Erro ao criar envio: {str(e)}")
    
    def get_tracking(self, tracking_code: str) -> TrackingInfo:
        """Get tracking information"""
        try:
            response = requests.post(
                f"{self.base_url}/me/shipment/tracking",
                json={"orders": [tracking_code]},
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            tracking_data = data.get(tracking_code, {})
            events = []
            
            for event in tracking_data.get("tracking", []):
                events.append(TrackingEvent(
                    status=event.get("status", ""),
                    description=event.get("message", ""),
                    location=event.get("locale", ""),
                    timestamp=datetime.fromisoformat(event.get("date", ""))
                ))
            
            # Map status
            status = ShipmentStatus.PENDING
            if tracking_data.get("status") == "delivered":
                status = ShipmentStatus.DELIVERED
            elif tracking_data.get("status") == "posted":
                status = ShipmentStatus.POSTED
            elif events:
                status = ShipmentStatus.IN_TRANSIT
                
            return TrackingInfo(
                tracking_code=tracking_code,
                status=status,
                events=events
            )
            
        except requests.RequestException as e:
            logger.error(f"Melhor Envio tracking error: {e}")
            raise Exception(f"Erro ao buscar rastreio: {str(e)}")
    
    def cancel_shipment(self, shipment_id: str) -> bool:
        """Cancel a shipment"""
        try:
            response = requests.post(
                f"{self.base_url}/me/shipment/cancel",
                json={"order": {"id": shipment_id, "reason_id": 2}},
                headers=self.headers,
                timeout=30
            )
            return response.status_code == 200
        except requests.RequestException as e:
            logger.error(f"Melhor Envio cancel error: {e}")
            return False


class MockShippingService(ShippingServiceInterface):
    """Mock shipping service for development/testing."""
    
    def calculate_shipping(self, zip_from: str, zip_to: str,
                          items: List[dict]) -> List[ShippingOption]:
        return [
            ShippingOption(
                carrier_code="correios-sedex",
                carrier_name="Correios",
                service_name="SEDEX",
                price=Decimal("25.90"),
                delivery_days=3,
                delivery_range=(2, 4)
            ),
            ShippingOption(
                carrier_code="correios-pac", 
                carrier_name="Correios",
                service_name="PAC",
                price=Decimal("18.50"),
                delivery_days=7,
                delivery_range=(5, 10)
            ),
            ShippingOption(
                carrier_code="jadlog-package",
                carrier_name="Jadlog",
                service_name=".Package",
                price=Decimal("22.00"),
                delivery_days=5,
                delivery_range=(3, 6)
            ),
        ]
    
    def create_shipment(self, order_id: int, carrier_code: str,
                       sender: dict, recipient: dict,
                       items: List[dict]) -> ShipmentResponse:
        return ShipmentResponse(
            shipment_id=f"MOCK-SHIP-{order_id}",
            tracking_code=f"BR{order_id}12345678BR",
            label_url=f"https://example.com/labels/{order_id}.pdf"
        )
    
    def get_tracking(self, tracking_code: str) -> TrackingInfo:
        return TrackingInfo(
            tracking_code=tracking_code,
            status=ShipmentStatus.IN_TRANSIT,
            events=[
                TrackingEvent(
                    status="posted",
                    description="Objeto postado",
                    location="São Paulo, SP",
                    timestamp=datetime.now()
                )
            ]
        )
    
    def cancel_shipment(self, shipment_id: str) -> bool:
        return True


def get_shipping_service() -> ShippingServiceInterface:
    """Factory function to get the configured shipping service."""
    provider = getattr(settings, 'SHIPPING_PROVIDER', 'mock')
    
    if provider == 'melhorenvio':
        return MelhorEnvioService()
    else:
        return MockShippingService()
