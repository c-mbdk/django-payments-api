from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer

from .models import Account
from payments.utils.utils_serializers import validate_currency


class AccountSerializer(serializers.ModelSerializer):
    currency = serializers.CharField(validators=[validate_currency])

    class Meta:
        model = Account
        fields = ["account_guid", "created_on", "account_name", "status", "last_updated", "balance", "currency", "status_valid_to"]

        read_only_fields = ["account_guid", "last_updated", "created_on"]


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'email', 'username', 'password']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'email', 'username', 'password']
