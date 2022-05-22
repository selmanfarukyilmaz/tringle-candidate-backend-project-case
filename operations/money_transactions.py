from operations.account_transactions import accounts_data
from operations.accounting_transactions import AccountingTransactions
import decimal as dec


class MoneyTransactions:
    dec.getcontext().prec = 12

    @staticmethod
    def payment_route(sender_account: int, receiver_account: int, amount: int or dec.Decimal):
        """
        Allows payment from individual account to corporate account

        :param sender_account: Account number of the account sending the payment
        :param receiver_account: Account number of the account receiving the payment
        :param amount: Payment amount
        :return: If the parameters are entered correctly, a dictionary containing the 'senderAccount', 'receiverAccount',
            and 'amount' is returned next to the response code. If the parameters are not
            correct, a string containing the reason for the error and a status code is returned.
        """
        dec.getcontext().prec = 12
        if not sender_account:
            return "You must enter the account number of the sending account.", 400

        if not receiver_account:
            return "You must enter the account number of the receiver account.", 400

        if not amount:
            return "You must enter the amount you will pay.", 400

        if type(amount) not in [int, dec.Decimal, float]:
            return "Amount must be entered in decimal type.", 400

        if type(sender_account) != int:
            return "Sender Account number must be entered as integer type.", 400

        if type(receiver_account) != int:
            return "Receiver Account number must be entered as integer type.", 400

        if sender_account not in accounts_data:
            return "The sender account number you entered does not belong to anyone", 404

        if receiver_account not in accounts_data:
            return "The receiver account number you entered does not belong to anyone", 404

        if amount < 0:
            return "Enter the amount you want to pay as a number greater than 0.", 400

        if accounts_data[sender_account]["accountType"] != "individual":
            return "Your transaction could not be processed because the sending account is not an individual account.", 400

        if accounts_data[receiver_account]["accountType"] != "corporate":
            return "Your transaction could not be processed because the recipient account is not a corporate account.", 400

        if accounts_data[sender_account]["balance"] < amount:
            return "Your transaction could not be completed because there is no money in the balance of the sender " \
                   "account.", \
                   400

        if accounts_data[sender_account]["currencyCode"] != accounts_data[receiver_account]["currencyCode"]:
            return "The transaction could not be performed because the sending account and the receiving account were " \
                   "defined in different currencies. ", 400

        else:
            AccountingTransactions.log_transaction(account_number=sender_account, amount=amount,
                                                   transaction_type="payment",
                                                   receiver_number=receiver_account)

            accounts_data[sender_account]["balance"] -= dec.Decimal(amount)
            accounts_data[receiver_account]["balance"] += dec.Decimal(amount)

            return {"senderAccount": sender_account, "receiverAccount": receiver_account, "amount": amount}, 200

    @staticmethod
    def deposit_route(account_number: int, amount: int or dec.Decimal, currency_code: str):
        """
        Allows deposits to the account

        :param currency_code: Currency code to be deposited into the account
        :param account_number: Account number of the account to which money is to be deposited
        :param amount: Deposit amount
        :return: If the parameters are entered correctly, a dictionary containing the 'accountNumber', and 'amount' is
            returned next to the response code. If the parameters are not correct, a string containing the reason
            for the error and a status code is returned.
        """
        dec.getcontext().prec = 12
        if not account_number:
            return "You have to enter the account number you want to deposit money into.", 400

        if type(account_number) != int:
            return "Account number must be entered as integer type.", 400

        if not amount:
            return "You must enter the amount you will deposit.", 400

        if type(amount) not in [int, dec.Decimal, float]:
            return "Amount must be entered in decimal type.", 400

        if not currency_code:
            return "You need to enter the unit code of the currency you want to deposit.", 400

        if account_number not in accounts_data:
            return "The account number you entered does not belong to anyone.", 404

        if accounts_data[account_number]["accountType"] != "individual":
            return "Only individual accounts can do this.", 400

        if currency_code != accounts_data[account_number]["currencyCode"]:
            return "The currency you want to deposit does not match the currency in which the account is defined.", 400

        if amount < 0:
            return "Enter the amount you want to deposit as a number greater than 0.", 400

        else:
            AccountingTransactions.log_transaction(account_number=account_number, amount=amount,
                                                   transaction_type="deposit")
            accounts_data[account_number]["balance"] += dec.Decimal(amount)
            return {"accountNumber": account_number, "amount": amount}, 200

    @staticmethod
    def withdraw_route(account_number: int, amount: int or dec.Decimal):
        """
        Allows money to be withdrawn from the account

        :param account_number: Account number of the account to which money is to be withdrawn
        :param amount: Withdrawn amount
        :return: If the parameters are entered correctly, a dictionary containing the 'accountNumber', and 'amount' is
            returned next to the response code. If the parameters are not correct, a string containing the reason
            for the error and a status code is returned.
        """
        dec.getcontext().prec = 12
        if not account_number:
            return "You have to enter the account number you want to withdraw money into.", 400

        if type(account_number) != int:
            return "Account number must be entered as integer type.", 400

        if not amount:
            return "You must enter the amount you will withdraw.", 400

        if type(amount) not in [int, dec.Decimal, float]:
            return "Amount must be entered in decimal type.", 400

        if account_number not in accounts_data:
            return "The account number you entered does not belong to anyone", 404

        if accounts_data[account_number]["accountType"] != "individual":
            return "Only individual accounts can do this..", 400

        if amount < 0:
            return "Enter the amount you want to withdraw as a number greater than 0.", 400

        if amount > accounts_data[account_number]["balance"]:
            return "The amount of money you want to withdraw is not available in the account where you entered the " \
                   "account number. ", 400

        else:
            AccountingTransactions.log_transaction(account_number=account_number, amount=amount,
                                                   transaction_type="withdraw")
            accounts_data[account_number]["balance"] -= dec.Decimal(amount)
            return {"accountNumber": account_number, "amount": amount}, 200
