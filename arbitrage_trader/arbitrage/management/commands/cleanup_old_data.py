from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from arbitrage.models import ArbitrageOpportunity

class Command(BaseCommand):
    help = 'Deletes arbitrage opportunities older than 30 days'

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(days=30)
        deleted = ArbitrageOpportunity.objects.filter(timestamp__lt=cutoff).delete()
        self.stdout.write(f"Deleted {deleted[0]} old records")