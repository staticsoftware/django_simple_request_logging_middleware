from datetime import timedelta
from django.utils import timezone
from django.db import models

class WebEvent(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("django.contrib.auth.models.User", blank=True, null=True, on_delete=models.SET_NULL)
    absolute_uri = models.CharField(max_length=1000, null=True, blank=True)
    session_id = models.CharField(max_length=500, blank=True, null=True)
    scout_id = models.CharField(max_length=1000, blank=True, null=True, help_text="The first-http-request tag we set on handshake")
    google_analytics_client_id = models.CharField(max_length=500, blank=True, null=True)
    full_event = models.JSONField(null=True, blank=True)


    def __str__(self) -> str:
        return f"{self.created_at}: {self.absolute_uri}"


    @classmethod
    def purge_events(cls) -> None:
        """utility to purge the db"""
        purge_mark = timezone.now() - timedelta(hours=2)
        cls.objects.filter(created_at__lt=purge_mark).delete()

