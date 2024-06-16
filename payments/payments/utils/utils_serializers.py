from rest_framework import serializers

# Common error messages

CURRENCY_ERROR_MESSAGE = 'Currency must be a 3 character ISO code'


# Additional functions for the serializers

def validate_currency(value):
        """Check that the currency code is 3 characters (valid ISO code)"""
        if len(value) != 3:
            raise serializers.ValidationError(CURRENCY_ERROR_MESSAGE)

        return value