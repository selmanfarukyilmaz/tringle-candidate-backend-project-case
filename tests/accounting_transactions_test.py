import unittest
from operations.account_transactions import AccountTransactions
from operations.money_transactions import MoneyTransactions
from operations.accounting_transactions import AccountingTransactions
from money_transactions_test import acc_numbers_list
from local_database import accounts_data, transaction_history_data
from operations.helpers import reset_all_data

class TransactionHistoryTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        AccountTransactions.create_account(owner_name="Zehra Ay", currency_code="TRY", account_type="individual")
        AccountTransactions.create_account(owner_name="Mustafa Kara", currency_code="TRY", account_type="individual")
        acc_numbers = acc_numbers_list(accounts_data)
        MoneyTransactions.deposit_route(account_number=acc_numbers[0], amount=100, currency_code="TRY")

    def tearDown(self) -> None:
        reset_all_data()
        super().tearDown()

    def test_if_not_account_number(self):
        result = AccountingTransactions.transaction_history(None)
        should_be = "You need to enter the account number of the account whose account history you want to view.", 400
        self.assertEqual(result, should_be)

    def test_if_account_number_not_in_accounts_data(self):
        result = AccountingTransactions.transaction_history(404)
        should_be = "The account number you entered does not belong to anyone", 404
        self.assertEqual(result, should_be)

    def test_if_correct(self):
        acc_numbers = acc_numbers_list(accounts_data)

        result = AccountingTransactions.transaction_history(acc_numbers[0])
        should_be = transaction_history_data[acc_numbers[0]], 200
        self.assertEqual(result, should_be)

if __name__ == '__main__':
    unittest.main()