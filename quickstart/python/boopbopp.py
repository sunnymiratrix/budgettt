import plaid
from plaid.api import plaid_api
from plaid.model.sandbox_item_fire_webhook_request import SandboxItemFireWebhookRequest

configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox,
    api_key={
        'clientId': '5a8205d48d9239244b80577c',
        'secret': '9588566147266d62edb4986ec8ce2f',
    }
)

access_token = 'access-sandbox-320ae570-2725-428f-9182-1b2cce0a7493'
api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

# fire a DEFAULT_UPDATE webhook for an item
request = SandboxItemFireWebhookRequest(
  access_token='access-sandbox-320ae570-2725-428f-9182-1b2cce0a7493',
  webhook_code='SYNC_UPDATES_AVAILABLE'
)
response = client.sandbox_item_fire_webhook(request)