from django.test import TestCase

from transactions_api.models import Transaction
from accounts_api.models import Account

class TransactionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        account_one = Account.objects.create(account_name='Test Account 1', status=Account.Status.ACTIVE, balance=120000.00)
        account_two = Account.objects.create(account_name='Test Account 2', status=Account.Status.ACTIVE, balance=250000.00)
        cls.transaction = Transaction.objects.create(transaction_type=Transaction.TransactionType.CREDIT, credit_from=account_one, debit_to=account_two, amount=230.00, currency='EUR', status=Transaction.Status.UNCLEARED)

    def test_transaction_has_all_attributes(self):
        "Test transaction instances created with all attributes"
        transaction = Transaction.objects.get(id=1)
        
        self.assertTrue(hasattr(transaction, 'id'))
        self.assertTrue(hasattr(transaction, 'created_on'))
        self.assertTrue(hasattr(transaction, 'transaction_guid'))
        self.assertTrue(hasattr(transaction, 'transaction_type'))
        self.assertTrue(hasattr(transaction, 'credit_from'))
        self.assertTrue(hasattr(transaction, 'debit_to'))
        self.assertTrue(hasattr(transaction, 'amount'))
        self.assertTrue(hasattr(transaction, 'currency'))
        self.assertTrue(hasattr(transaction, 'transaction_date'))
        self.assertTrue(hasattr(transaction, 'status'))
        self.assertTrue(hasattr(transaction, 'last_updated'))
    
    def test_transaction_type_label(self):
        "Test transaction_Type field label"
        transaction = Transaction.objects.get(id=1)
        field_label = transaction._meta.get_field('transaction_type').verbose_name
        
        self.assertEqual(field_label, 'transaction type')

    def test_currency_max_length(self):
        "Test currency field has correct maximum length"
        transaction = Transaction.objects.get(id=1)
        max_length = transaction._meta.get_field('currency').max_length
        
        self.assertEqual(max_length, 3)

    def test_date_not_null(self):
        "Testing date is populated when not specified in initial creation of the transaction instance"
        transaction = Transaction.objects.get(id=1)
       
        self.assertNotEqual(transaction.transaction_date, 'null')  

    def test_created_on_not_null(self):
        "Testing creation timestamp is still populated when not specified in intiial creation of the transaction instance"
        transaction = Transaction.objects.get(id=1)
        
        self.assertNotEqual(transaction.created_on, 'null')

    def test_last_updated_not_null(self):
        "Testing modification timestamp is populated upon creation"
        transaction = Transaction.objects.get(id=1)
        
        self.assertNotEqual(transaction.last_updated, 'null') 

    def test_transaction_creation_fails_with_invalid_account_data(self):
        "Testing a transaction instance cannot be created when accounts do not exist"

        with self.assertRaises(ValueError):
            invalid_transaction = Transaction.objects.create(transaction_type=Transaction.TransactionType.CREDIT, credit_from=3, debit_to=4, amount=230.00, currency='EUR', status=Transaction.Status.UNCLEARED)

        self.assertEqual(0, Transaction.objects.filter(id=2).count())    
 

        

              

               