from django.core.management.base import BaseCommand
from ...utils import *


class Command(BaseCommand):
    help = 'Fetch Directories data from nfusion-catalog API and save in local database'

    def handle(self, *args, **kwargs):
        save_metals_to_database()
        save_asset_classes_to_database()
        save_product_families_to_database()
        save_products_to_database()
        self.stdout.write(self.style.SUCCESS('Directories fetched and saved successfully!'))
