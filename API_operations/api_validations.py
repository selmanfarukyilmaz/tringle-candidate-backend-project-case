from cerberus import Validator
import json


def schematics(func_name: str):
    """
    Contains the schemas of the rules of the json file where the functions are used

    :param func_name: Name of the function used
    :return: A dictionary containing the schema
    """
    schemas = {"CreateRoute": {'owner_name': {'required': True, 'empty': False},
                               'currency_code': {'required': True, 'empty': False},
                               'account_type': {'required': True, 'empty': False},
                               'field3': {'required': False,
                                          'dependencies': ['owner_name', 'currency_code', "account_type"]}},

               "PaymentRoute": {'sender_account': {'required': True, 'empty': False},
                                'receiver_account': {'required': True, 'empty': False},
                                'amount': {'required': True, 'empty': False},
                                'field3': {'required': False,
                                           'dependencies': ['sender_account', 'receiver_account', "account_type"]}},

               "DepositRoute": {'account_number': {'required': True, 'empty': False},
                                'amount': {'required': True, 'empty': False},
                                'currency_code': {'required': True, 'empty': False},
                                'field3': {'required': False, 'dependencies': ['account_number', 'amount', "currency_code"]}},

               "WithdrawRoute": {'account_number': {'required': True, 'empty': False},
                                 'amount': {'required': True, 'empty': False},
                                 'field3': {'required': False, 'dependencies': ['account_number', 'amount']}},
               }

    return schemas[func_name]


def validate_json(json_data: json, func_name: str):
    """
    Checks if the json file conforms to the rules

    :param json_data: Json file
    :param func_name: Name of the function used
    :return: True or error with status code
    """
    schema = schematics(func_name=func_name)
    document = json_data
    v = Validator(schema)
    if v.validate(document, schema) == True:
        return True
    else:
        return v.errors, 404


def validate_type_json(data: json):
    """
    Checks if the incoming data is json

    :param data: Json file
    :return: True or string containing the reason for the error with status code
    """
    try:
        json.loads(data)
        return True
    except:
        return "Only json data type is supported", 400
