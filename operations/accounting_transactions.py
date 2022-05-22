from operations.account_transactions import accounts_data
import decimal as dec
import datetime
from local_database import transaction_history_data


class AccountingTransactions:
    """
     A class that contains the functions of transaction_history and log_transaction.
    """
    @staticmethod
    def transaction_history(account_number: int):
        """
        Provides access to past transactions of the account

        :param account_number: Account number of the account for which you want to access transaction history
        :return: If the parameters are entered correctly, a dictionary containing the 'accountNumber', 'amount',
            transactionType', and 'createdAt' is returned next to the response code. If the parameters are not
            correct, a string containing the reason for the error and a status code is returned.
        """
        if not account_number:
            return "You need to enter the account number of the account whose account history you want to view.", 400

        if account_number not in accounts_data:
            return "The account number you entered does not belong to anyone", 404

        if account_number not in transaction_history_data:
            return "There is no transaction history for the account number you entered to see the transaction history.", 404

        else:
            return transaction_history_data[account_number], 200

    @staticmethod
    def log_transaction(account_number: int, amount: int or dec.Decimal, transaction_type: str, receiver_number=None):
        """
        Allows account transactions to be recorded

        :param account_number: Account number of the account whose account transaction is to be recorded
        :param amount: The amount in the account transaction to be recorded
        :param transaction_type: Type of account transaction to be recorded
        :param receiver_number: The account number of the receiving account (only for payments)

        """
        curr_time = str(datetime.datetime.now())
        log = {"accountNumber": account_number, "amount": amount,
               "transactionType": transaction_type, "createdAt": curr_time}

        if transaction_type == "payment":
            log_payment_receiver = {"accountNumber": account_number, "amount": amount,
                                    "transactionType": transaction_type, "createdAt": curr_time}

            if receiver_number not in transaction_history_data:
                transaction_history_data[receiver_number] = [log_payment_receiver]

            else:
                new_log = transaction_history_data[receiver_number]
                new_log.append(log_payment_receiver)
                transaction_history_data[receiver_number] = new_log

        if account_number not in transaction_history_data:
            transaction_history_data[account_number] = [log]

        else:
            new_log = transaction_history_data[account_number]
            new_log.append(log)
            transaction_history_data[account_number] = new_log
