from datetime import datetime

import plaid 
from plaid.api import plaid_api
from plaid.model.transactions_sync_request import TransactionsSyncRequest

from flask import Flask, request, redirect

from twilio.rest import Client
import externalconstants as ec

import mygoogle
from entryclass import Entry

import q

app = Flask(__name__)

responses = []

@app.route('/')
def home():
    return f'Last transaction at who knows, built at {str(datetime.now())}'

@app.route('/gimme', methods = ['POST'])
def gimme():
    date_format = "%Y-%m-%d"
    last_transaction_time = datetime.strptime( mygoogle.date_of_last_transaction(), date_format )
    #last_transaction_time = datetime(1970, 12, 25)
    print("new transactions availible")
    
    transactions = get_transactions()
    new_transactions = []

    for transaction in transactions:
        if transaction.date > last_transaction_time:
            new_transactions.append(transaction)

    for new_transaction in new_transactions:
        row = str( len(mygoogle.get_value_range_dict("A1:A1000","Spending transactions")["values"])+1 )
        mygoogle.write_in_cell( str(new_transaction.date),    "A"+row, "Spending transactions") # try omiting 'Spending transactions' sometime for science
        mygoogle.write_in_cell( new_transaction.merchant,     "B"+my_row, "Spending transactions") 
        mygoogle.write_in_cell( new_transaction.amount,       "D"+my_row, "Spending transactions")

        send_message("what did you just buy and what catagory was it?")

        # output = q.camelcase_with_spaces(, nopronouns=True)
    
    return "godd'em"

def send_message(contents):
    client = Client(ec.TWILI_ACCOUNT_SID, ec.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
      from_=ec.BOT_PHONE,
      body=contents,
      to=ec.MY_PHONE
    ) 

def get_transactions():
    # Available environments are
    # 'Production'
    # 'Development'
    # 'Sandbox'
    configuration = plaid.Configuration(
        host=plaid.Environment.Production,
        api_key={
            'clientId': ec.PLAID_CLIENT_ID,
            'secret': ec.PLAID_SECRET,
        }
    )

    api_client = plaid.ApiClient(configuration)
    client = plaid_api.PlaidApi(api_client)

    request = TransactionsSyncRequest(
        access_token=ec.PLAID_ACCESS_TOKEN,
    )
    response = client.transactions_sync(request)
    transactions = response['added']

    # the transactions in the response are paginated, so make multiple calls while incrementing the cursor to
    # retrieve all transactions
    while (response['has_more']):
        request = TransactionsSyncRequest(
            access_token=ec.PLAID_ACCESS_TOKEN,
            cursor=response['next_cursor']
        )
        response = client.transactions_sync(request)
        transactions += response['added']

    # for transaction in transactions:
    #     transaction.account_id != '8MqJn7ZkqqImpY4PLeJgi6KKPJBbbgCJ815Lv'
    #     transactions.pop(transactions.index(transaction))
    # print (transactions)
    transactions = list(filter(lambda transaction: transaction.account_id == '8MqJn7ZkqqImpY4PLeJgi6KKPJBbbgCJ815Lv', transactions))
    return list(filter(lambda transaction: transaction.amount > 0.0, transactions))

@app.route("/sms", methods=['GET', 'POST'])
def reseive_message():
    response = request.form['Body']
    row = str( len(mygoogle.get_value_range_dict("A1:A1000","Spending transactions")["values"])+1 )

    if ":" in response:
        mygoogle.write_in_cell(q.camelcase_with_spaces(response[0: response.index(":")], nopronouns=True), "C"+row, "Spending transactions") 
        
        a = False
        for catagory in mygoogle.valid_catagories:
            if response[response.index(":") + 1:].lower() == catagory.lower():
                mygoogle.write_in_cell(response[response.index(":") + 1:], "E"+row, "Spending transactions")
                a = True
        if not a:
            send_message("not a valid catagory")
        
    else: 
        a = False
        for catagory in mygoogle.valid_catagories:
            if response.lower() == catagory.lower():
                mygoogle.write_in_cell(response, "E"+row, "Spending transactions")
                a = True
        if not a:
            send_message("not a valid catagory")
        



    # print("got a thing!/n the thing is '" + response + "'")
    # send_message("uhh…")

if __name__ == "__main__":
    app.run(debug=True)

