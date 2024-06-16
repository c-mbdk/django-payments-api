import uuid
from django.db import models
from django.utils import timezone

class Account(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE"
        INACTIVE = "INACTIVE"

    account_guid = models.UUIDField(default=uuid.uuid4, editable=False)
    account_name = models.CharField(max_length=100)
    status = models.CharField(max_length=8, choices=Status, default=Status.ACTIVE)
    created_on = models.DateTimeField(auto_now_add=True)
    status_valid_from = models.DateTimeField(default=timezone.now)
    status_valid_to = models.DateTimeField( null=True, blank=True)
    balance = models.DecimalField(max_digits=19, decimal_places=2)
    currency = models.CharField(max_length=3)
    last_updated = models.DateTimeField(auto_now=True)