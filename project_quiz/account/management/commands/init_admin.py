from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Initialize superuser if no exists'

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.WARNING('Superuser already exists.'))
        else:
            user = User.objects.create_superuser(
                username="quizyard_admin", password="randompass-QgF3uX2YV")
            if user:
                self.stdout.write(self.style.SUCCESS(
                    'Superuser created successfully.'))
