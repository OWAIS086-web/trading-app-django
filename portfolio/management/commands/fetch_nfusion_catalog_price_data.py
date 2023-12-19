from django.core.management.base import BaseCommand
from ...utils import *
from django.utils import timezone


class Command(BaseCommand):
    help = 'Fetch Product Prices data from nfusion-catalog API and save in local database'

    def handle(self, *args, **kwargs):
        save_product_prices_to_database()
        # Get the current date and time
        timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        # Add the timestamp to the success message
        success_message = f"Product Prices fetched and saved successfully at {timestamp}!"
        self.stdout.write(self.style.SUCCESS(success_message))
