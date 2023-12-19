from django.core.management.base import BaseCommand
from portfolio.models import *

class Command(BaseCommand):
    help = 'Deletes model data'

    def handle(self, *args, **options):
        # Delete data from YourModel
        # Metals.objects.all().delete()
        # Grades.objects.all().delete()
        # AssetClasses.objects.all().delete()
        # ProductFamilies.objects.all().delete()
        Products.objects.all().delete()
        # ProductPrices.objects.all().delete()
        # Portfolios.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Model data deleted successfully'))