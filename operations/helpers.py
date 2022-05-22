import json
import decimal
from local_database import *


class DecimalEncoder(json.JSONEncoder):
    """
    It serves to serialize the Decimal object.
    """

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


def two_decimal_accounts_data(data, key_word):
    """
    Allows 2 digits after the comma
    """
    if type(data) != dict:
        return data

    if key_word in data:
        str_obj = str(data[key_word])
        result = ""
        counter = 0
        for i in str_obj:
            if counter == 0:
                if i != ".":
                    result += i
                if i == ".":
                    result += i
                    counter += 1
            elif counter < 3:
                result += i
                counter += 1
        data[key_word] = decimal.Decimal(result)
        return data


def two_decimal_transaction_history(data):
    """
    Allows 2 digits after the comma
    """
    if type(data) != list:
        return data

    for i in range(len(data)):
        str_obj = str(data[i]["amount"])
        result = ""
        counter = 0
        for ii in str_obj:
            if counter == 0:
                if ii != ".":
                    result += ii
                if ii == ".":
                    result += ii
                    counter += 1
            elif counter < 3:
                result += ii
                counter += 1
        data[i]["amount"] = decimal.Decimal(result)
    return data


def reset_all_data():
    """
    Used to reset all data
    """
    while accounts_data:
        accounts_data.popitem()

    while transaction_history_data:
        transaction_history_data.popitem()


def acc_numbers_list(data):
    """
    Collects current account numbers in a list
    :param data: Dictionary of accounts information
    :return: List of account numbers
    """
    acc_numbers = []
    for acc_number in data:
        acc_numbers.append(acc_number)
    return acc_numbers
