
from django.core.management.base import BaseCommand
from django.utils import timezone
from shop.models import Order
from datetime import timedelta

class Command(BaseCommand):
    help = 'Automatically confirm pending orders older than 2 days'

    def handle(self, *args, **options):
        # Calculate the threshold time (2 days ago)
        threshold_time = timezone.now() - timedelta(days=2)
        
        # Find pending orders older than threshold
        orders_to_update = Order.objects.filter(
            status='pending',
            created_at__lte=threshold_time
        )
        
        count = orders_to_update.count()
        
        if count > 0:
            # Update statuses
            orders_to_update.update(status='confirmed')
            self.stdout.write(self.style.SUCCESS(f'Successfully confirmed {count} orders'))
        else:
            self.stdout.write(self.style.SUCCESS('No pending orders older than 2 days found'))
