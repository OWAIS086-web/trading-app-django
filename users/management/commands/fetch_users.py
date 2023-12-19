# myapp/management/commands/fetch_users.py
from django.core.management.base import BaseCommand
from users.utils import save_users_to_database

class Command(BaseCommand):
    help = 'Fetch users from Random User Generator API and save them in the database'

    def handle(self, *args, **kwargs):
        save_users_to_database()
        self.stdout.write(self.style.SUCCESS('Users fetched and saved successfully!'))
