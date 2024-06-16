from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken

from accounts_api.models import Account
from transactions_api.models import Transaction

class BaseAPITestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
                email='testuser@test.com',
                username='user123',
                password='password123$'
            )
        self.client = APIClient()

        token = AccessToken.for_user(user=user)
    
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

    @classmethod
    def setUpTestData(cls):
        
        cls.test_account_one = Account.objects.create(
            account_name='Test Account 1', status=Account.Status.ACTIVE, balance=120000.00, currency='CAD'
        )

        cls.test_account_two = Account.objects.create(
            account_name='Test Account 2', status=Account.Status.ACTIVE, balance=180000.00, currency='USD'
        )   



def validate_response_headers(response):
        """Validates the headers of the response are as expected"""
        
        assert response.headers.get("Content-Type") == 'application/json'

        assert response.headers.get("Vary") == 'Accept'

        assert response.headers.get("X-Content-Type-Options") == 'nosniff'

        assert "X-Powered-By" not in response.headers    