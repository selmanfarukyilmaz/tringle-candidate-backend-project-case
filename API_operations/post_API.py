from flask import *
import json
from operations.account_transactions import AccountTransactions
from operations.money_transactions import MoneyTransactions
from operations.helpers import DecimalEncoder, two_decimal_accounts_data
from API_operations.api_validations import validate_type_json, validate_json

post_API = Blueprint('post_API', __name__)


class PostAPI:
    @staticmethod
    @post_API.route("/account/", methods=["POST"])
    def create_route():
        """
        API for account creation operation
        :return: Json file and status code if request is true
            If the request is false, a string containing the reason for the error and a status code
        """
        if validate_type_json(request.data) != True:
            response, status_code = validate_type_json(request.data)
            return make_response(jsonify(response), status_code)

        account_info = json.loads(request.data)

        if validate_json(account_info, "CreateRoute") != True:
            response, status_code = validate_json(account_info, "CreateRoute")
            return make_response(jsonify(response), status_code)

        data_set, status_code = AccountTransactions.create_account(owner_name=account_info["owner_name"],
                                                                   currency_code=account_info["currency_code"],
                                                                   account_type=account_info["account_type"])
        json_dump = json.dumps(data_set, cls=DecimalEncoder)

        return make_response(json_dump, status_code)

    @staticmethod
    @post_API.route("/payment/", methods=["POST"])
    def payment_route():
        """
        API for payment operation
        :return: Json file and status code if request is true
            If the request is false, a string containing the reason for the error and a status code
        """
        if validate_type_json(request.data) != True:
            response, status_code = validate_type_json(request.data)
            return make_response(jsonify(response), status_code)

        account_info = json.loads(request.data)

        if validate_json(account_info, "PaymentRoute") != True:
            response, status_code = validate_json(account_info, "PaymentRoute")
            return make_response(jsonify(response), status_code)

        data_set, status_code = MoneyTransactions.payment_route(sender_account=account_info["sender_account"],
                                                                receiver_account=account_info["receiver_account"],
                                                                amount=account_info["amount"])
        data_set = two_decimal_accounts_data(data_set, key_word="amount")

        json_dump = json.dumps(data_set, cls=DecimalEncoder)
        return make_response(json_dump, status_code)

    @staticmethod
    @post_API.route("/deposit/", methods=["POST"])
    def deposit_route():
        """
        API for depositing operation
        :return: Json file and status code if request is true
            If the request is false, a string containing the reason for the error and a status code
        """
        if validate_type_json(request.data) != True:
            response, status_code = validate_type_json(request.data)
            return make_response(jsonify(response), status_code)

        account_info = json.loads(request.data)

        if validate_json(account_info, "DepositRoute") != True:
            response, status_code = validate_json(account_info, "DepositRoute")
            return make_response(jsonify(response), status_code)

        data_set, status_code = MoneyTransactions.deposit_route(account_number=account_info["account_number"],
                                                                amount=account_info["amount"],
                                                                currency_code=account_info["currency_code"])
        data_set = two_decimal_accounts_data(data_set, key_word="amount")

        json_dump = json.dumps(data_set, cls=DecimalEncoder)
        return make_response(json_dump, status_code)

    @staticmethod
    @post_API.route("/withdraw/", methods=["POST"])
    def withdraw_route():
        """
        API for withdrawal operation
        :return: Json file and status code if request is true
            If the request is false, a string containing the reason for the error and a status code
        """
        if validate_type_json(request.data) != True:
            response, status_code = validate_type_json(request.data)
            return make_response(jsonify(response), status_code)

        account_info = json.loads(request.data)

        if validate_json(account_info, "WithdrawRoute") != True:
            response, status_code = validate_json(account_info, "WithdrawRoute")
            return make_response(jsonify(response), status_code)

        data_set, status_code = MoneyTransactions.withdraw_route(account_number=account_info["account_number"],
                                                                 amount=account_info["amount"])
        data_set = two_decimal_accounts_data(data_set, key_word="amount")

        json_dump = json.dumps(data_set, cls=DecimalEncoder)
        return make_response(json_dump, status_code)
