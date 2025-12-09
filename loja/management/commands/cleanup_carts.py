from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from loja.models import Carrinho, StoreConfig, Produto

class Command(BaseCommand):
    help = 'Cleans up expired carts and restores stock'

    def handle(self, *args, **options):
        config = StoreConfig.objects.first()
        if not config:
            self.stdout.write(self.style.WARNING('StoreConfig not found. Using default 3 days.'))
            days = 3
        else:
            days = config.cart_expiration_days
            
        expiration_date = timezone.now() - timezone.timedelta(days=days)
        
        expired_carts = Carrinho.objects.filter(updated_at__lt=expiration_date)
        count = expired_carts.count()
        
        if count == 0:
            self.stdout.write(self.style.SUCCESS('No expired carts found.'))
            return

        self.stdout.write(f'Found {count} expired carts. Processing...')
        
        for cart in expired_carts:
            try:
                with transaction.atomic():
                    # Restore stock for each item
                    for item in cart.items.all():
                        produto = Produto.objects.select_for_update().get(pk=item.produto.id)
                        produto.estoque += item.quantidade
                        produto.save()
                        self.stdout.write(f'Restored {item.quantidade} of {produto.nome}')
                    
                    cart.delete()
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing cart {cart.id}: {e}'))
                
        self.stdout.write(self.style.SUCCESS(f'Successfully cleaned up {count} carts.'))
