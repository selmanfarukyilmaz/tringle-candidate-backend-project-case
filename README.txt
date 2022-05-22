**PROJECT'S TITLE**

Tringle Candidate Backend Project

**Project Description**

The project created with REST API architecture which performs 6 banking transactions.
Requests to the API returns a JSON file and status code if it provided with necessary validations.
If it fails validations, it returns the reason and the status code.
API developed with FLASK framework.
The project includes unit tests of banking transactions.
The project is dockerized.


**DEVELOPED SYSTEM**

Environment: Linux Ubuntu 20.04
Software Language: Python 3.8
API Framework: FLASK


**GENERAL USAGE**

1- Run python3 main.py

2- For creating new account you should send a POST request to "http://127.0.0.1:5000/account" with payload which is json format.

3- For deposit money to your you should POST request to "http://127.0.0.1:5000/deposit" with json with payload which is json format.

4- For withdraw money from account you should POST request to "http://127.0.0.1:5000/withdraw" with json with payload which is json format.

5- For payment from account you should POST request to "http://127.0.0.1:5000/withdraw" with json with payload which is json format.

6- For access an account's information you should GET request to "http://127.0.0.1:5000/account/accountNumber/?accountNumber={ACCOUNT_NUMBER_HERE}"

7- For access an account's transaction history you should GET request to "http://127.0.0.1:5000/accounting/?account_number={ACCOUNT_NUMBER_HERE}"


**RULES**

1- POST request are using "JSON" type only.

2- Only "USD", "EUR" and "TRY" currency codes are valid.

3- Account type should be "individual" or "corporate".

4- Deposit and withdraw operations only supported for individual accounts.

5- The payment operation can be made from the personal account to the corporate account.


**JSON SCHEMAS for POST Request**
-----------------------------------------------------------------------
    CreateAccountPayload  =  {
                        "owner_name": "Jack",
                        "currency_code": "USD",
                        "account_type": "individual"
                    }
-----------------------------------------------------------------------
    DepositPayload = {
                        "account_number": 4518689,
                        "amount": 1000
                        "currency_code": "USD"
                    }
-----------------------------------------------------------------------
    WithdrawPayload = {
                    "account_number": 4518689,
                    "amount": 500
                    }
-----------------------------------------------------------------------
    PaymentPayload = {
                    "sender_account": 4518689,
                    "receiver_account": 6458356 ,
                    "amount": 300
                    }
-----------------------------------------------------------------------

**DOCKER USAGE**

If you don't have docker you should first install docker with "sudo snap install docker"

1- Open terminal

2- code = "sudo docker build -t {IMAGE_NAME_HERE}:{TAG_NAME_HERE} ."

3- code = "sudo docker run -p 127.0.0.1:5000:5000 {IMAGE_NAME_HERE}:{TAG_NAME_HERE}"

4- API will be run automatically. You can use all operations.


**UNIT TEST USAGE**

1- Open terminal

2- code = "python3 -m pytest"

3- All test cases will be run.




Created By: Selman Faruk YILMAZ
e-mail: selmanfarukyilmaz@gmail.com
