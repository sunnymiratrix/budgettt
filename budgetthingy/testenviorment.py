import os
from twilio.rest import Client

import flask3.externalconstants as ec

client = Client(ec.TWILIO_ACCOUNT_SID, ec.TWILIO_AUTH_TOKEN)

message = client.messages.create(
  from_=ec.BOT_PHONE,
  body='Hello twilio',
  to=ec.MY_PHONE
)

print(message.sid)