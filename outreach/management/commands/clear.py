# filepath: /Users/admin/Desktop/output/django/outreach/management/commands/clear_database.py
from django.core.management.base import BaseCommand
from django.apps import apps
from outreach.models import OutreachPost

class Command(BaseCommand):
    help = 'Clear OutreachPost data from the database'

    def handle(self, *args, **kwargs):
        OutreachPost.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("OutreachPost data cleared successfully!"))