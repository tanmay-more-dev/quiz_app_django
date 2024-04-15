from django.core.management.base import BaseCommand
from django_redis import get_redis_connection


class Command(BaseCommand):
    help = 'Clears all cache in Redis'

    def handle(self, *args, **kwargs):
        # Get the default Redis connection
        redis_connection = get_redis_connection()

        try:
            # Flush all keys from Redis
            redis_connection.flushall()
            self.stdout.write(self.style.SUCCESS(
                'Successfully cleared cache in Redis.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(
                f'Failed to clear cache in Redis: {e}'))
