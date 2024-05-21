from datetime import datetime
from os import path 
import sys

import plaid 
from plaid.api import plaid_api
from plaid.model.transactions_sync_request import TransactionsSyncRequest

from flask import Flask, request, redirect

sys.path.append( path.abspath( path.join(path.dirname(__file__), '..')) )
sys.path.append( path.abspath( path.join(path.dirname(__file__), '../..')) )
import externalconstants as ec

import mygoogle as mygoogle
from entryclass import Entry

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

# bobby = Entry( get_transactions()[0], False )
# bobby.enter_to_sheet()
# date_format = "%Y-%m-%d"
# print (datetime.strptime( mygoogle.date_of_last_transaction(), date_format ) )

for transaction in get_transactions():
    print(transaction.date)