import unittest
from operations.account_transactions import AccountTransactions
from local_database import accounts_data


class CreateAccountTest(unittest.TestCase):

    def test_if_not_owner_name(self):
        result = AccountTransactions.create_account(owner_name="", currency_code="USD", account_type="individual")
        should_be = "To create the account, you must enter the name of the account holder.", 400
        self.assertEqual(result, should_be)

    def test_if_not_account_type(self):
        result = AccountTransactions.create_account(owner_name="Jack Light", currency_code="USD", account_type="")
        should_be = "To create the account, you must enter the account type.", 400
        self.assertEqual(result, should_be)

    def test_if_not_currency_code(self):
        result = AccountTransactions.create_account(owner_name="Jack Light", currency_code="",
                                                    account_type="individual")
        should_be = "To create the account, you must enter the currency code.", 400
        self.assertEqual(result, should_be)

    def test_if_account_type_different(self):
        result = AccountTransactions.create_account(owner_name="Jack Light", currency_code="USD",
                                                    account_type="personal")
        should_be = "The currency you entered [individual, corporate] must be one of them.", 400
        self.assertEqual(result, should_be)

    def test_if_currency_code_different(self):
        result = AccountTransactions.create_account(owner_name="Jack Light", currency_code="GBP",
                                                    account_type="individual")
        should_be = "The currency you entered [TRY, USD, EUR] must be one of them.", 400
        self.assertEqual(result, should_be)

    def test_if_owner_name_invalid(self):
        result = AccountTransactions.create_account(owner_name="123456789", currency_code="USD",
                                                    account_type="individual")
        should_be = "The account owner name you entered to create the account is invalid.", 400
        self.assertEqual(result, should_be)

        result = AccountTransactions.create_account(owner_name="Jack_Light", currency_code="USD",
                                                    account_type="individual")
        should_be = "The account owner name you entered to create the account is invalid.", 400
        self.assertEqual(result, should_be)

    def test_if_correct(self):
        result = AccountTransactions.create_account(owner_name="Jack Light", currency_code="USD",
                                                    account_type="individual")

        acc_numbers = []
        for acc_number in accounts_data:
            acc_numbers.append(acc_number)

        should_be = accounts_data[acc_numbers[0]], 201
        self.assertEqual(result, should_be)


class AccountInfoRouteTest(unittest.TestCase):

    def test_if_not_account_number(self):
        result = AccountTransactions.account_info_route(account_number=None)
        should_be = "You need to enter the account number of the account whose information you want to view.", 400
        self.assertEqual(result, should_be)

    def test_if_account_number_not_in_accounts_data(self):
        result = AccountTransactions.account_info_route(account_number=1)
        should_be = "The account number you entered does not belong to anyone.", 404
        self.assertEqual(result, should_be)

    def test_if_correct(self):
        AccountTransactions.create_account(owner_name="Jack Light", currency_code="USD", account_type="individual")

        acc_numbers = []
        for acc_number in accounts_data:
            acc_numbers.append(acc_number)

        result = AccountTransactions.account_info_route(account_number=acc_numbers[0])
        should_be = accounts_data[acc_numbers[0]], 200
        self.assertEqual(result, should_be)


if __name__ == '__main__':
    unittest.main()
