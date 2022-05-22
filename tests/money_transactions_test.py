import unittest
from operations.account_transactions import AccountTransactions
from operations.money_transactions import MoneyTransactions
from local_database import accounts_data
from operations.helpers import reset_all_data, acc_numbers_list

class PaymentTest(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        AccountTransactions.create_account(owner_name="Jack Light", currency_code="USD", account_type="individual")
        AccountTransactions.create_account(owner_name="Steffi Graf", currency_code="USD", account_type="corporate")
        AccountTransactions.create_account(owner_name="Andre Agassi", currency_code="USD", account_type="individual")
        AccountTransactions.create_account(owner_name="Serena Williams", currency_code="USD", account_type="corporate")
        AccountTransactions.create_account(owner_name="Zeynep Uz", currency_code="TRY", account_type="individual")
        acc_numbers = acc_numbers_list(accounts_data)
        MoneyTransactions.deposit_route(account_number=acc_numbers[0], amount=100, currency_code="USD")
        MoneyTransactions.deposit_route(account_number=acc_numbers[1], amount=100, currency_code="USD")
        MoneyTransactions.deposit_route(account_number=acc_numbers[4], amount=100, currency_code="TRY")

    def tearDown(self) -> None:
        reset_all_data()
        super().tearDown()

    def test_if_not_sender_account(self):
        acc_numbers = acc_numbers_list(accounts_data)
        result = MoneyTransactions.payment_route(sender_account=None, receiver_account=acc_numbers[1], amount=50)
        should_be = "You must enter the account number of the sending account.", 400
        self.assertEqual(result, should_be)

    def test_if_not_receiver_account(self):
        acc_numbers = acc_numbers_list(accounts_data)
        result = MoneyTransactions.payment_route(sender_account=acc_numbers[0], receiver_account=None, amount=50)
        should_be = "You must enter the account number of the receiver account.", 400
        self.assertEqual(result, should_be)

    def test_if_amount_not_integer(self):
        acc_numbers = acc_numbers_list(accounts_data)
        result = MoneyTransactions.payment_route(sender_account=acc_numbers[0], receiver_account=acc_numbers[1],
                                                 amount="tests")
        should_be = "Amount must be entered in decimal type.", 400
        self.assertEqual(result, should_be)

    def test_if_not_amount(self):
        acc_numbers = acc_numbers_list(accounts_data)

        result = MoneyTransactions.payment_route(sender_account=acc_numbers[0], receiver_account=acc_numbers[1],
                                                 amount=None)
        should_be = "You must enter the amount you will pay.", 400
        self.assertEqual(result, should_be)

    def test_if_sender_account_not_in_accounts_data(self):
        acc_numbers = acc_numbers_list(accounts_data)

        result = MoneyTransactions.payment_route(sender_account=404, receiver_account=acc_numbers[1], amount=50)
        should_be = "The sender account number you entered does not belong to anyone", 404
        self.assertEqual(result, should_be)

    def test_if_receiver_account_not_in_accounts_data(self):
        acc_numbers = acc_numbers_list(accounts_data)

        result = MoneyTransactions.payment_route(sender_account=acc_numbers[0], receiver_account=404, amount=50)
        should_be = "The receiver account number you entered does not belong to anyone", 404
        self.assertEqual(result, should_be)

    def test_if_amount_lower_than_zero(self):
        acc_numbers = acc_numbers_list(accounts_data)

        result = MoneyTransactions.payment_route(sender_account=acc_numbers[0], receiver_account=acc_numbers[1],
                                                 amount=-5)
        should_be = "Enter the amount you want to pay as a number greater than 0.", 400
        self.assertEqual(result, should_be)

    def test_if_sender_account_is_not_individual(self):
        acc_numbers = acc_numbers_list(accounts_data)

        result = MoneyTransactions.payment_route(sender_account=acc_numbers[1], receiver_account=acc_numbers[3],
                                                 amount=50)
        should_be = "Your transaction could not be processed because the sending account is not an individual account.", 400
        self.assertEqual(result, should_be)

    def test_if_receiver_account_is_not_corporate(self):
        acc_numbers = acc_numbers_list(accounts_data)

        result = MoneyTransactions.payment_route(sender_account=acc_numbers[0], receiver_account=acc_numbers[2],
                                                 amount=50)
        should_be = "Your transaction could not be processed because the recipient account is not a corporate account.", 400
        self.assertEqual(result, should_be)

    def test_if_amount_lower_than_balance(self):
        acc_numbers = acc_numbers_list(accounts_data)

        result = MoneyTransactions.payment_route(sender_account=acc_numbers[0], receiver_account=acc_numbers[1],
                                                 amount=1500)
        should_be = "Your transaction could not be completed because there is no money in the balance of the sender account.", \
                    400
        self.assertEqual(result, should_be)

    def test_if_the_currencies_not_match(self):
        acc_numbers = acc_numbers_list(accounts_data)
        result = MoneyTransactions.payment_route(sender_account=acc_numbers[4], receiver_account=acc_numbers[1],
                                                 amount=50)
        should_be = "The transaction could not be performed because the sending account and the receiving account were " \
                   "defined in different currencies. ", 400
        self.assertEqual(result, should_be)

    def test_if_correct(self):
        acc_numbers = acc_numbers_list(accounts_data)
        result = MoneyTransactions.payment_route(sender_account=acc_numbers[0], receiver_account=acc_numbers[1],
                                                 amount=50)
        should_be = {"senderAccount": acc_numbers[0], "receiverAccount": acc_numbers[1], "amount": 50}, 200
        self.assertEqual(result, should_be)


class DepositTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        AccountTransactions.create_account(owner_name="Jack Light", currency_code="USD", account_type="individual")
        AccountTransactions.create_account(owner_name="Steffi Graf", currency_code="USD", account_type="corporate")
        AccountTransactions.create_account(owner_name="Andre Agassi", currency_code="USD", account_type="individual")
        AccountTransactions.create_account(owner_name="Serena Williams", currency_code="USD", account_type="corporate")
        AccountTransactions.create_account(owner_name="Zeynep Uz", currency_code="TRY", account_type="individual")
        acc_numbers = acc_numbers_list(accounts_data)
        MoneyTransactions.deposit_route(account_number=acc_numbers[0], amount=100, currency_code="USD")
        MoneyTransactions.deposit_route(account_number=acc_numbers[1], amount=100, currency_code="USD")
        MoneyTransactions.deposit_route(account_number=acc_numbers[4], amount=100, currency_code="USD")

    def tearDown(self) -> None:
        reset_all_data()
        super().tearDown()

    def test_if_not_account_number(self):
        result = MoneyTransactions.deposit_route(account_number=None, amount=100, currency_code="USD")
        should_be = "You have to enter the account number you want to deposit money into.", 400
        self.assertEqual(result, should_be)

    def test_if_not_amount(self):
        acc_numbers = acc_numbers_list(accounts_data)

        result = MoneyTransactions.deposit_route(account_number=acc_numbers[0], amount=None, currency_code="USD")
        should_be = "You must enter the amount you will deposit.", 400
        self.assertEqual(result, should_be)

    def test_if_account_number_not_in_accounts_data(self):
        result = MoneyTransactions.deposit_route(account_number=404, amount=50, currency_code="USD")
        should_be = 'The account number you entered does not belong to anyone.', 404
        self.assertEqual(result, should_be)

    def test_if_amount_lower_than_zero(self):
        acc_numbers = acc_numbers_list(accounts_data)

        result = MoneyTransactions.deposit_route(account_number=acc_numbers[0], amount=-50, currency_code="USD")
        should_be = "Enter the amount you want to deposit as a number greater than 0.", 400
        self.assertEqual(result, should_be)

    def test_if_correct(self):
        acc_numbers = acc_numbers_list(accounts_data)

        result = MoneyTransactions.deposit_route(account_number=acc_numbers[0], amount=50, currency_code="USD")
        should_be = {"accountNumber": acc_numbers[0], "amount": 50}, 200
        self.assertEqual(result, should_be)


class WithdrawTest(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()

        AccountTransactions.create_account(owner_name="Jack Light", currency_code="USD", account_type="individual")
        AccountTransactions.create_account(owner_name="Steffi Graf", currency_code="USD", account_type="corporate")
        AccountTransactions.create_account(owner_name="Andre Agassi", currency_code="USD", account_type="individual")
        AccountTransactions.create_account(owner_name="Serena Williams", currency_code="USD", account_type="corporate")
        AccountTransactions.create_account(owner_name="Zeynep Uz", currency_code="TRY", account_type="individual")
        acc_numbers = acc_numbers_list(accounts_data)
        MoneyTransactions.deposit_route(account_number=acc_numbers[0], amount=100, currency_code="USD")
        MoneyTransactions.deposit_route(account_number=acc_numbers[1], amount=100, currency_code="USD")
        MoneyTransactions.deposit_route(account_number=acc_numbers[4], amount=100, currency_code="TRY")

    def tearDown(self) -> None:
        reset_all_data()

        super().tearDown()

    def test_if_not_account_number(self):
        result = MoneyTransactions.withdraw_route(account_number=None, amount=100)
        should_be = "You have to enter the account number you want to withdraw money into.", 400
        self.assertEqual(result, should_be)

    def test_if_not_amount(self):
        acc_numbers = acc_numbers_list(accounts_data)

        result = MoneyTransactions.withdraw_route(account_number=acc_numbers[0], amount=None)
        should_be = "You must enter the amount you will withdraw.", 400
        self.assertEqual(result, should_be)

    def test_if_account_number_not_in_accounts_data(self):
        result = MoneyTransactions.withdraw_route(account_number=404, amount=50)
        should_be = "The account number you entered does not belong to anyone", 404
        self.assertEqual(result, should_be)

    def test_if_amount_lower_than_zero(self):
        acc_numbers = acc_numbers_list(accounts_data)

        result = MoneyTransactions.withdraw_route(account_number=acc_numbers[0], amount=-50)
        should_be = "Enter the amount you want to withdraw as a number greater than 0.", 400
        self.assertEqual(result, should_be)

    def test_if_amount_lower_balance(self):
        acc_numbers = acc_numbers_list(accounts_data)
        result = MoneyTransactions.withdraw_route(account_number=acc_numbers[0], amount=1500)
        should_be = "The amount of money you want to withdraw is not available in the account where you entered the " \
                    "account number. ", 400
        self.assertEqual(result, should_be)

    def test_if_correct(self):
        acc_numbers = acc_numbers_list(accounts_data)

        result = MoneyTransactions.withdraw_route(account_number=acc_numbers[0], amount=50)
        should_be = {"accountNumber": acc_numbers[0], "amount": 50}, 200
        self.assertEqual(result, should_be)


if __name__ == '__main__':
    unittest.main()
