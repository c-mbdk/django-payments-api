from django.urls import reverse

from rest_framework import status

from transactions_api.models import Transaction
from transactions_api.serializers import TransactionSerializer
from payments.utils.utils_test import BaseAPITestCase, validate_response_headers
from accounts_api.models import Account


class TransactionBaseAPITestCase(BaseAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_transaction_one = Transaction.objects.create(
            transaction_type=Transaction.TransactionType.CREDIT, credit_from=Account.objects.get(id=1), debit_to=Account.objects.get(id=2), amount=230.00, currency='EUR', status=Transaction.Status.UNCLEARED
        )

        cls.test_transaction_two = Transaction.objects.create(
            transaction_type=Transaction.TransactionType.DEBIT, credit_from=Account.objects.get(id=2), debit_to=Account.objects.get(id=1), amount=8700.00, currency='GBP', status=Transaction.Status.UNCLEARED
        )       
        

class TestTransactionListView(TransactionBaseAPITestCase):

    def test_lists_all_transactions(self):
        """Tests GET request to view all transactions is successful"""

        response = self.client.get(reverse('transactions-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Check response against db
        transactions_in_db = Transaction.objects.all()
        expected_transactions = TransactionSerializer(transactions_in_db,many=True).data

        self.assertEqual(response.data, expected_transactions)


    def test_list_all_transactions_correct_headers(self):
        """Tests GET request to view all transactions has correct headers"""

        response = self.client.get(reverse('transactions-list'))
        
        validate_response_headers(response)
    
             
    def test_no_transactions_returned_with_unauthenticated_request(self):
        """Tests unauthenticated GET request does not return transactions"""
        self.client.credentials()

        response = self.client.get(reverse('transactions-list'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_transaction_create_successful_view(self):
        """Tests authenticated POST request is successful"""
        data = {
            "credit_from": 1,
            "debit_to": 2,
            "amount": 12500.00,
            "currency": "USD",
            "transaction_date": "2024-05-11",
            "status": "CLEARED"
        } 

        response = self.client.post(reverse('transactions-list'), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Transaction.objects.filter().count(), 3)

        transaction_db_data = Transaction.objects.filter(id=3)
        expected_data = TransactionSerializer(transaction_db_data, many=True).data

        self.assertTrue(response.data, expected_data)


    def test_create_transaction_correct_headers(self):
        """Tests authenticated POST request for transactions has the correct headers"""

        data = {
            "transaction_type": "CREDIT",
            "credit_from": 1,
            "debit_to": 2,
            "amount": 2800.00,
            "currency": "USD",
            "transaction_date": "2024-05-19",
            "status": "UNCLEARED"
        }

        response = self.client.post(reverse('transactions-list'), data=data)

        validate_response_headers(response)    


    def test_transaction_create_fails_with_no_authentication(self):
        """Tests POST request fails when no credentials are provided"""

        self.client.credentials()

        data = {
            "transaction_type": "CREDIT",
            "credit_from": 2,
            "debit_to": 1,
            "amount": 32500.00,
            "currency": "CAD",
            "transaction_date": "2024-05-03",
            "status": "CLEARED"
        } 

        response = self.client.post(reverse('transactions-list'), data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Transaction.objects.filter().count(), 2)


    def test_invalid_data_in_transaction_post_request(self):
        """Tests that an authenticated POST request fails when the data in the request is invalid"""

        data = {
            "transaction_type": "CREDITS",
            "credit_from": 2,
            "debit_to": 1,
            "amount": 39500.00,
            "currency": "CAD",
            "transaction_date": "2024-05-03",
            "status": "CLEARED"
        } 

        response = self.client.post(reverse('transactions-list'), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(Transaction.objects.filter().count(), 2)


    def test_post_request_no_data_transaction_create_view(self):
        """Tests requests with no data do not update the database"""         

        response = self.client.post(reverse('transactions-list'), data={})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Transaction.objects.filter().count(), 2)


    def test_post_request_fails_with_incorrect_currency(self):
        """Tests authenticated POST requests are not successful when the currency provided is not 3 characters"""

        data = {
                "transaction_type": "CREDIT",
                "credit_from": 2,
                "debit_to": 1,
                "amount": 43500.00,
                "currency": "US",
                "transaction_date": "2024-05-03",
                "status": "CLEARED"
            }     
        
        response = self.client.post(reverse('transactions-list'), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Transaction.objects.filter().count(), 2)


    def test_unsupported_method_delete_in_list_view(self):
        """Tests DELETE requests are not supported at the /transactions/api endpoint"""

        response = self.client.delete(reverse('transactions-list'))

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        self.assertEqual(Transaction.objects.filter().count(), 2)


    def test_get_transactions_fails_from_invalid_content_type(self):      
        """Tests GET requests retrieve no data when invalid values are set for the accepted content-type header"""
        
        self.client.credentials(HTTP_ACCEPT='appplication/json; version=1.0')
        response = self.client.get(reverse('transactions-list'))

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)


    def test_create_transaction_unsuccessful_with_invalid_content_type(self):
        """Tests POST request is unsuccessful when invalid values are set for the accepted content-type header"""

        self.client.credentials(HTTP_ACCEPT='application/jsonify; version=1.0')

        data = {
            "transaction_type": "CREDIT",
            "credit_from": 2,
            "debit_to": 1,
            "amount": 4900.00,
            "currency": "CAD",
            "transaction_date": "2024-05-07",
            "status": "UNCLEARED"
        }    

        response = self.client.post(reverse('transactions-list'), data=data)

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(Transaction.objects.filter().count(), 2)


    def test_create_transaction_unsuccessful_invalid_amount(self):
        """Tests POST request is unsuccessful when the amount in the field does not match the database field constraint"""

        data = {
            "transaction_type": "CREDIT",
            "credit_from": 1,
            "debit_to": 2,
            "amount": 6000.545,
            "currency": "CAD",
            "transaction_date": "2024-05-15",
            "status": "UNCLEARED"
        }    

        response = self.client.post(reverse('transactions-list'), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check database not updated

        self.assertNotEqual(Transaction.objects.filter().count(), 3)


class TestTransactionDetailView(TransactionBaseAPITestCase):
    def test_view_single_transaction(self):
        """Tests GET request is successful using the transaction id"""

        response = self.client.get(reverse('transactions-detail', args=[self.test_transaction_one.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        transaction_db_record = Transaction.objects.get(id=self.test_transaction_one.id)
        expected_data = TransactionSerializer(transaction_db_record).data

        self.assertEqual(response.data, expected_data)


    def test_view_single_transaction_correct_headers(self):
        """Tests GET request for a single transaction has the correct headers"""

        response = self.client.get(reverse('transactions-detail', args=[self.test_transaction_one.id]))     

        validate_response_headers(response)


    def test_view_single_invalid_transaction(self):
        """Tests GET request is unsuccessful using a transaction id that doesn't exist"""

        response = self.client.get(reverse('transactions-detail', args=[6]))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_single_transaction_successful(self):
        """Tests PUT request is successful for a given transaction id"""

        data_update = {
            "transaction_type": "DEBIT",
            "credit_from": 2,
            "debit_to": 1,
            "amount": '250.00',
            "currency": "GBP",
            "transaction_date": "2024-04-18",
            "status": "CLEARED"
        }

        response = self.client.put(reverse('transactions-detail', args=[self.test_transaction_one.id]), data=data_update)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        transaction_db_record = Transaction.objects.get(id=self.test_transaction_one.id)
        expected_data = TransactionSerializer(transaction_db_record).data

        self.assertEqual(response.data, expected_data)


    def test_update_single_transaction_correct_headers(self):
            """Tests that an authenticated PUT request for a single transaction has the correct headers"""
            
            data_update = {
                "transaction_type": "DEBIT",
                "credit_from": 2,
                "debit_to": 1,
                "amount": '250.00',
                "currency": "GBP",
                "transaction_date": "2024-04-18",
                "status": "CLEARED"
            }
            
            response = self.client.put(reverse('transactions-detail', args=[self.test_transaction_one.id]), data=data_update)
            
            validate_response_headers(response)       


    def test_update_single_transaction_unsuccessful_no_authentication(self):
        """Tests PUT request is unsuccessful for a given transaction id when there is no authentication"""

        self.client.credentials()

        data_update = {
            "transaction_type": "DEBIT",
            "credit_from": 2,
            "debit_to": 1,
            "amount": '250.00',
            "currency": "GBP",
            "transaction_date": "2024-04-18",
            "status": "CLEARED"
        }

        response = self.client.put(reverse('transactions-detail', args=[self.test_transaction_two.id]), data=data_update)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Check db is not updated

        transaction_db_record = Transaction.objects.get(id=self.test_transaction_two.id)
        expected_data = TransactionSerializer(transaction_db_record).data    

        self.assertNotEqual(response.data, expected_data)


    def test_delete_transaction_successful(self):
        """Tests DELETE request is successful for a given transaction id"""   

        response = self.client.delete(reverse('transactions-detail', args=[self.test_transaction_two.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK) 

        # Check against db
        with self.assertRaises(Transaction.DoesNotExist):
            Transaction.objects.get(id=self.test_transaction_two.id)


    def test_delete_transaction_correct_headers(self):
        """Tests DELETE request for a given transaction id has the correct headers"""

        response = self.client.delete(reverse('transactions-detail', args=[self.test_transaction_two.id]))

        validate_response_headers(response)


    def test_delete_transaction_unsuccessful_no_authentication(self):
        """Tests DELETE request is unsuccessful for a given transaction id when there is no authentication"""

        self.client.credentials()

        response = self.client.delete(reverse('transactions-detail', args=[self.test_transaction_one.id]))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Verify record still in database
        self.assertTrue
        (Transaction.objects.filter(id=self.test_transaction_one.id).exists())      
