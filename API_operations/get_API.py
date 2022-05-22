import json
from operations.account_transactions import AccountTransactions
from operations.accounting_transactions import AccountingTransactions
from operations.helpers import DecimalEncoder, two_decimal_accounts_data, two_decimal_transaction_history
from flask import *

get_API = Blueprint('get_API', __name__)


class GetAPI:
    @staticmethod
    @get_API.route("/account/accountNumber/", methods=["GET"])
    def account_info_route():
        """
        API to access account information
        :return: json file and status code if request is true
            If the request is false, a string containing the reason for the error and a status code
        """
        account_number = (request.args.get("accountNumber"))  # /account/accountNumber/?accountNumber=925051
        data_set, status_code = AccountTransactions.account_info_route(account_number=int(account_number))
        data_set = two_decimal_accounts_data(data_set, key_word="balance")

        json_dump = json.dumps(data_set, cls=DecimalEncoder)
        return make_response(json_dump, status_code)

    @staticmethod
    @get_API.route("/accounting/", methods=["GET"])
    def transaction_history():
        """
        API for accessing account transactions
        :return:json file and status code if request is true
            If the request is false, a string containing the reason for the error and a status code
        """
        account_number = (request.args.get("account_number"))  # /accounting/?account_number=925051
        data_set, status_code = AccountingTransactions.transaction_history(account_number=int(account_number))
        data_set = two_decimal_transaction_history(data_set)

        json_dump = json.dumps(data_set, cls=DecimalEncoder)
        return make_response(json_dump, status_code)
