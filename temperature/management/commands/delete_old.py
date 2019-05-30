from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from temperature.models import Reading
class Command(BaseCommand):
    help = 'Delete objects older than 10 days'

    def handle(self, *args, **options):
        Reading.objects.filter(created_date__lte=datetime.now()-timedelta(days=7)).delete()
