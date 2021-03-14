import uuid

from django.db import models


class MetricConfig(models.Model):
    name = models.CharField(unique=True, max_length=64)
    token = models.UUIDField(default=uuid.uuid4)
    prefix = models.CharField(
        max_length=64,
        blank=True,
        default="",
        help_text="add this prefix to the metric path",
    )
    carbon_host = models.CharField(
        max_length=64,
        help_text="used for the socket connection",
    )
    carbon_port = models.PositiveIntegerField(
        help_text="used for the socket connection",
    )
