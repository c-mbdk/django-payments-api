from rest_framework import status
from django.urls import reverse

from accounts_api.models import Account
from accounts_api.serializers import AccountSerializer

from payments.utils.utils_test import BaseAPITestCase, validate_response_headers

class AccountBaseAPITestCase(BaseAPITestCase):
    @classmethod
    def setUpTestData(cls):
        return super().setUpTestData()

class TestAccountListView(AccountBaseAPITestCase):

    def test_lists_all_accounts(self):
        """Tests GET request to retrieve all accounts is successful"""

        response = self.client.get(reverse('accounts-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Check response against db

        accounts_in_db = Account.objects.all()
        expected_accounts = AccountSerializer(accounts_in_db, many=True).data
        
        self.assertEqual(response.data, expected_accounts)


    def test_list_all_accounts_correct_headers(self):
        """Tests GET request to view all accounts has correct headers"""

        response = self.client.get(reverse('accounts-list'))

        validate_response_headers(response)


    def test_no_accounts_returned_with_unauthenticated_request(self):
        """Tests unauthenticated GET request does not return all accounts"""

        self.client.credentials()

        response = self.client.get(reverse('accounts-list'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_create_account_successful(self):
        """Tests authenticated POST request successfully creates account"""
        data = {
            "created_on": "2024-06-08",
            "account_name": "Test Account 3", 
            "status": "ACTIVE",
            "balance": 180000.00,
            "currency": "GBP",
            "status_valid_to": "2024-06-12"
        }    

        response = self.client.post(reverse('accounts-list'), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Account.objects.filter().count(), 3)

        account_db_data = Account.objects.filter(id=3)
        expected_data = AccountSerializer(account_db_data, many=True).data

        self.assertTrue(response.data, expected_data)


    def test_create_account_correct_headers(self):
        """Tests authenticated POST request for accounts has the correct headers"""

        data = {
            "account_name": "Test Account 4", 
            "status": "ACTIVE", 
            "balance": 200000.00,
            "currency": "JMD"
        }    

        response = self.client.post(reverse('accounts-list'), data=data)

        validate_response_headers(response)


    def test_create_account_fails_with_no_authentication(self):
        """Tests POST request for accounts fails when no credentials are provided"""

        self.client.credentials()

        data = {
            "account_name": "Test Account 4", 
            "status": "ACTIVE", 
            "balance": 256000.00,
            "currency": "AUD"
        }    

        response = self.client.post(reverse('accounts-list'), data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Account.objects.filter().count(), 2)


    def test_invalid_data_in_account_post_request(self):
        """Tests that an authenticated POST request with invalid data fails to create an account """   

        data = {
            "account_name": "Test Account 5", 
            "status": "INACTIVITY", 
            "balance": 299000.00,
            "currency": "AED"
        } 

        response = self.client.post(reverse('accounts-list'), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(Account.objects.filter().count(), 2)


    def test_post_request_fails_incorrect_base_currency(self):
        """Tests that an authenticated POST request with incorrect base currency data fails"""

        data = {
            "account_name": "Test Account 5.5", 
            "status": "ACTIVE", 
            "balance": 23000.00,
            "currency": "JPAN"
        }

        response = self.client.post(reverse('accounts-list'), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(Account.objects.filter().count(), 2)
        

    def test_post_request_no_data_account(self):
        """Tests POST request with no data do not update the database"""

        response = self.client.post(reverse('accounts-list'), data={})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Account.objects.filter().count(), 2)


    def test_unsupported_method_in_list_view(self):
        """Tests DELETE requests are not supported at the /accounts/api endpoint""" 

        response = self.client.delete(reverse('accounts-list'))

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        self.assertEqual(Account.objects.filter().count(), 2)  


    def test_get_accounts_fails_from_invalid_content_type(self):
        """Tests GET request retrieves no account data when invalid values are set for the accepted content-type header""" 

        self.client.credentials(HTTP_ACCEPT='appplication/json; version=1.0')
        response = self.client.get(reverse('accounts-list')) 

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)  


    def test_create_account_unsuccessful_with_invalid_content_type(self):
        """Tests POST request for accounts is unsuccessful when invalid values are set for the accepted content-type header"""

        self.client.credentials(HTTP_ACCEPT='application/jsonify; version=1.0')

        data = {
            "account_name": "Test Account 6", 
            "status": "ACTIVE", 
            "balance": 600000.00,
            "currency": "NGN"
        }

        response = self.client.post(reverse('accounts-list'), data=data)

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(Account.objects.filter().count(), 2)


    def test_create_account_unsuccessful_invalid_balance(self):
        """Tests POST request is unsuccessful when the balance does not match the database constraint"""

        data = {
            "account_name": "Test Account 6", 
            "status": "ACTIVE", 
            "balance": 600000.0001,
            "currency": "CAD"
        } 

        response = self.client.post(reverse('accounts-list'), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check database was not updated

        self.assertNotEqual(Account.objects.filter().count(), 3)   


class TestAccountDetailView(BaseAPITestCase):

    def test_view_single_account(self):
        """Tests GET request is successful using the account id"""

        response = self.client.get(reverse('accounts-detail', args=[self.test_account_one.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        account_db_record = Account.objects.get(id=self.test_account_one.id)
        expected_data = AccountSerializer(account_db_record).data

        self.assertEqual(response.data, expected_data)


    def test_view_single_invalid_account(self):
        """Tests GET request is unsuccessful using an account id that doesn't exist"""

        response = self.client.get(reverse('accounts-detail', args=[19]))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_single_account_successful(self):
        """Tests PUT request is successful for a given account id"""

        data= {
            'account_name': 'Test Account 2',
            'status': "ACTIVE",
            'balance': 5000.00,
            'currency': 'GBP',
        }

        response = self.client.put(reverse('accounts-detail', args=[self.test_account_two.id]), data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        account_db_record = Account.objects.get(id=self.test_account_two.id)
        expected_data = AccountSerializer(account_db_record).data

        self.assertEqual(response.data, expected_data) 


    def test_update_single_account_correct_headers(self):
        """Tests PUT request for a given account id has the correct headers"""

        data_update = {
            "account_name": "Test Account 2",
            "status": "ACTIVE",
            "balance": 9000.00,
            "currency": "EUR"
        }  

        response = self.client.put(reverse('accounts-detail', args=[self.test_account_two.id]), data=data_update)

        validate_response_headers(response)


    def test_update_single_account_unsuccessful_no_authentication(self):
        """Tests PUT request is unsuccessful for a given account id when there are no credentials provided""" 

        self.client.credentials()

        data_update = {
            "account_name": "Test Account 2",
            "status": "ACTIVE",
            "balance": 11000.00,
            "currency": "GBP"
        }

        response = self.client.put(reverse('accounts-detail', args=[self.test_account_two.id]), data=data_update)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Check db not updated
        account_db_record = Account.objects.get(id=self.test_account_two.id)
        expected_data = AccountSerializer(account_db_record).data

        self.assertNotEqual(response.data, expected_data)


    def test_delete_account_successful(self):
        """Tests DELETE request is successful for a given account id"""

        response = self.client.delete(reverse('accounts-detail', args=[self.test_account_one.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK) 

        # Check against db
        with self.assertRaises(Account.DoesNotExist):
            Account.objects.get(id=self.test_account_one.id)    


    def test_delete_account_correct_headers(self):
        """Tests DELETE request for a given account id has the correct headers"""

        response = self.client.delete(reverse('accounts-detail', args=[self.test_account_two.id]))

        validate_response_headers(response)


    def test_delete_account_successful_no_authentication(self):
        """Tests DELETE request is unsuccessful for a given account id when there is no authentication"""

        self.client.credentials()

        response = self.client.delete(reverse('accounts-detail', args=[self.test_account_two.id]))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Verify account still in db
        self.assertTrue(Account.objects.filter(id=self.test_account_two.id).exists())