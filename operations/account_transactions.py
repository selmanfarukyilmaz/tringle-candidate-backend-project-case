from random import randint
import decimal as dec
from local_database import accounts_data, transaction_history_data


class AccountTransactions:
    """
   A class that contains the functions of create_account and account_info_route.
    """
    @staticmethod
    def create_account(owner_name: str, currency_code: str, account_type: str):
        """
        Creates a personal or corporate bank account defined in a specific currency

        :param owner_name: Name of the owner of the account to be created
        :param currency_code: Currency code of the account to be created
        :param account_type: Account type of the account to be created
        :return: If the parameters are entered correctly, a dictionary containing the 'accountNumber', 'currencyCode',
            'ownerName' name, and 'accountType' is returned next to the response code. If the parameters are not correct,
            a string containing the reason for the error and a status code is returned.
        """
        dec.getcontext().prec = 12
        random_acc_number = randint(1000000, 9999999)
        if not owner_name:
            return "To create the account, you must enter the name of the account holder.", 400

        if not account_type:
            return "To create the account, you must enter the account type.", 400

        if not currency_code:
            return "To create the account, you must enter the currency code.", 400

        if account_type not in ["individual", "corporate"]:
            return "The currency you entered [individual, corporate] must be one of them.", 400

        if currency_code not in ["TRY", "USD", "EUR"]:
            return "The currency you entered [TRY, USD, EUR] must be one of them.", 400

        if type(owner_name) != str:
            return "The account owner name you entered to create the account should be string.", 400

        if not owner_name.replace(" ", "").isalpha():
            return "The account owner name you entered to create the account is invalid.", 400

        if random_acc_number in accounts_data:
            return AccountTransactions.create_account(owner_name, currency_code, account_type), 201

        else:
            accounts_data[random_acc_number] = {"accountNumber": random_acc_number,
                                                "currencyCode": currency_code,
                                                "ownerName": owner_name, "accountType": account_type,
                                                "balance": dec.Decimal(0)}
            transaction_history_data[random_acc_number] = []
            return accounts_data[random_acc_number], 201

    @staticmethod
    def account_info_route(account_number: int):
        """
        Provides access to up-to-date account information

        :param account_number: Account number of the account for which you want to access account information

        :return: If the parameters are entered correctly, a dictionary containing the 'accountNumber', 'currencyCode',
            'ownerName', 'accountType' and 'balance' is returned next to the response code. If the parameters are
            not correct, a string containing the reason for the error and a status code is returned.
        """
        if not account_number:
            return "You need to enter the account number of the account whose information you want to view.", 400

        if account_number not in accounts_data:
            return "The account number you entered does not belong to anyone.", 404

        else:
            return accounts_data[account_number], 200
