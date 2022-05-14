from django.core.management.base import BaseCommand
from django_simple_request_logging_middleware.models import WebEvent
import logging
logger = logging.getLogger(__name__)

ANALYTICS_CLEANUP = "analytics_cleanup"

class Command(BaseCommand):
    """ Purges the web events table."""

    help = "Purges all previous web events from the database."

    def _success_msg(self, message:str):
        logger.info(message)
        self.stdout.write(self.style.SUCCESS(message))

    def handle(self, *args, **kwargs):
        self._success_msg("Purging WebEvents from Analytics...")
        WebEvent.purge_events()
        self._success_msg("WebEvents purged.")
