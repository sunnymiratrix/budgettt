import plaid 
from plaid.api import plaid_api
from plaid.model.transactions_sync_request import TransactionsSyncRequest

#from datetime import datetime
def get_transactions(): 

    # Available environments are
    # 'Production'
    # 'Development'
    # 'Sandbox'
    configuration = plaid.Configuration(
        host=plaid.Environment.Production,
        api_key={
            # item_id = 'w4zqE9MdzzSv4NnJ981Rc0Bn7DKJXDULD7eBn'
            'clientId': '5a8205d48d9239244b80577c',
            'secret': '9588566147266d62edb4986ec8ce2f',
        }
    )

    access_token = 'access-production-4e56913d-c487-4c02-b23b-5df777afdcd6'
    api_client = plaid.ApiClient(configuration)
    client = plaid_api.PlaidApi(api_client)

    request = TransactionsSyncRequest(
        access_token=access_token,
    )
    response = client.transactions_sync(request)
    transactions = response['added']

    # the transactions in the response are paginated, so make multiple calls while incrementing the cursor to
    # retrieve all transactions
    while (response['has_more']):
        request = TransactionsSyncRequest(
            access_token=access_token,
            cursor=response['next_cursor']
        )
        response = client.transactions_sync(request)
        transactions += response['added']

    print (transactions)
    return(transactions)