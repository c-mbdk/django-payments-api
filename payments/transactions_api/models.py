import uuid
from django.utils import timezone
from django.db import models

class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        CREDIT = "CREDIT"
        DEBIT = "DEBIT"

    class Status(models.TextChoices):
        CLEARED = "CLEARED"
        UNCLEARED = "UNCLEARED"    

    transaction_guid = models.UUIDField( default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=6, choices=TransactionType,default=TransactionType.CREDIT)
    credit_from = models.ForeignKey("accounts_api.Account", on_delete=models.CASCADE, related_name='+')
    debit_to = models.ForeignKey("accounts_api.Account", on_delete=models.CASCADE, related_name='+')
    amount = models.DecimalField(max_digits=19,decimal_places=2)
    currency = models.CharField(max_length=3)
    transaction_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=9, choices=Status, default=Status.UNCLEARED)
    last_updated = models.DateTimeField(auto_now=True)