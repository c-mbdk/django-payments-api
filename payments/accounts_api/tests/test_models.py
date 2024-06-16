from django.test import TestCase

from accounts_api.models import Account

class AccountModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        account_one = Account.objects.create(account_name='Test Account 1', status=Account.Status.ACTIVE, balance=120000.00)
        account_two = Account.objects.create(account_name='Test Account 2', status=Account.Status.ACTIVE, balance=250000.00)

    def test_account_has_all_attributes(self):
        "Test account instances created with all attributes, even when not specified"
        account = Account.objects.get(id=1)
        
        self.assertTrue(hasattr(account, 'id'))
        self.assertTrue(hasattr(account, 'account_guid'))
        self.assertTrue(hasattr(account, 'account_name')) 
        self.assertTrue(hasattr(account, 'status'))
        self.assertTrue(hasattr(account, 'created_on'))
        self.assertTrue(hasattr(account, 'status_valid_from'))
        self.assertTrue(hasattr(account, 'status_valid_to'))
        self.assertTrue(hasattr(account, 'balance'))
        self.assertTrue(hasattr(account, 'last_updated'))

    def test_last_updated_label(self):
        "Testing the value of the field label"
        account = Account.objects.get(id=1)
        field_label = account._meta.get_field('last_updated').verbose_name

        self.assertEqual(field_label, 'last updated')

    def test_account_name_max_length(self):
        "Testing the account_name field is the expected size"
        account = Account.objects.get(id=1)
        max_length = account._meta.get_field('account_name').max_length

        self.assertEqual(max_length, 100)          

    def test_accounts_are_unique(self):
        "Testing two accounts with the same name, balance and status are still unique"
        account_three = Account.objects.create(account_name='Test Account 1', status=Account.Status.ACTIVE, balance=120000.00)
        account_two = Account.objects.create(account_name='Test Account 2', status=Account.Status.ACTIVE, balance=250000.00)

        self.assertNotEqual(account_two.id, account_three.id)

    def test_status_valid_from_populated(self):
        "Testing status_valid_from field is populated on creation"
        account = Account.objects.get(id=1)

        self.assertNotEqual(account.status_valid_from, 'null')  