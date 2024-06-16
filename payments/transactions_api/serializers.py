from rest_framework import serializers

from .models import Transaction
from payments.utils.utils_serializers import validate_currency

class TransactionSerializer(serializers.ModelSerializer):

    currency=serializers.CharField(validators=[validate_currency])

    class Meta:
        model = Transaction
        fields = ["transaction_guid", "transaction_type", "credit_from", "debit_to", "amount", "currency", "transaction_date", "status", "last_updated"]
        read_only = ["transaction_guid", "last_updated"]