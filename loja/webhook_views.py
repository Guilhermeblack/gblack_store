"""
Webhook endpoints for external service notifications.
"""
import json
import logging

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import PaymentTransaction, Venda
from .services import get_payment_service

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def payment_webhook(request):
    """
    Webhook endpoint for payment gateway notifications.
    
    MercadoPago sends notifications when payment status changes.
    URL: /api/v1/webhooks/payment/
    """
    try:
        payload = json.loads(request.body)
        logger.info(f"Payment webhook received: {payload}")
        
        payment_service = get_payment_service()
        
        # Process the webhook
        status_response = payment_service.process_webhook(payload)
        
        # Find and update the transaction
        transaction = PaymentTransaction.objects.filter(
            transaction_id=status_response.transaction_id
        ).first()
        
        if transaction:
            # Map status
            status_map = {
                'pending': 'PENDING',
                'approved': 'APPROVED',
                'rejected': 'FAILED',
                'cancelled': 'CANCELLED',
                'refunded': 'REFUNDED',
            }
            new_status = status_map.get(status_response.status.value, 'PENDING')
            
            if transaction.status != new_status:
                transaction.status = new_status
                transaction.save()
                
                # Update order status if payment approved
                if new_status == 'APPROVED':
                    venda = transaction.venda
                    if venda.status == 'PENDING_PAYMENT':
                        venda.status = 'PAID'
                        venda.save()
                        logger.info(f"Order {venda.id} marked as PAID")
                
                elif new_status in ['CANCELLED', 'REFUNDED']:
                    venda = transaction.venda
                    venda.status = 'CANCELLED'
                    venda.save()
                    # TODO: Restore stock
                    logger.info(f"Order {venda.id} cancelled")
        
        return JsonResponse({'status': 'ok'})
        
    except Exception as e:
        logger.error(f"Payment webhook error: {e}")
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_POST
def shipping_webhook(request):
    """
    Webhook endpoint for shipping notifications.
    
    Melhor Envio sends tracking updates.
    URL: /api/v1/webhooks/shipping/
    """
    try:
        payload = json.loads(request.body)
        logger.info(f"Shipping webhook received: {payload}")
        
        # Extract tracking info
        tracking_code = payload.get('tracking')
        status = payload.get('status')
        
        # Find order by tracking code
        venda = Venda.objects.filter(tracking_code=tracking_code).first()
        
        if venda:
            # Update order status based on shipping status
            status_map = {
                'posted': 'SHIPPED',
                'in_transit': 'SHIPPED',
                'out_for_delivery': 'SHIPPED',
                'delivered': 'DELIVERED',
                'returned': 'RETURNED',
            }
            
            new_status = status_map.get(status)
            if new_status and venda.status != new_status:
                venda.status = new_status
                venda.save()
                logger.info(f"Order {venda.id} updated to {new_status}")
        
        return JsonResponse({'status': 'ok'})
        
    except Exception as e:
        logger.error(f"Shipping webhook error: {e}")
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_POST  
def marketplace_webhook(request, marketplace):
    """
    Webhook endpoint for marketplace notifications.
    
    URL: /api/v1/webhooks/marketplace/<marketplace>/
    """
    try:
        payload = json.loads(request.body)
        logger.info(f"Marketplace {marketplace} webhook received: {payload}")
        
        # Handle different marketplace events
        event_type = payload.get('type') or payload.get('action') or 'unknown'
        
        if event_type in ['order.created', 'orders']:
            # New order from marketplace
            # TODO: Import order to local database
            logger.info(f"New order from {marketplace}")
        
        elif event_type in ['order.cancelled', 'order_cancellation']:
            # Order cancelled on marketplace
            # TODO: Update local order status
            logger.info(f"Order cancelled on {marketplace}")
        
        return JsonResponse({'status': 'ok'})
        
    except Exception as e:
        logger.error(f"Marketplace webhook error: {e}")
        return JsonResponse({'error': str(e)}, status=400)
