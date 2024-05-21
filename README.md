# README

This is a hobby project aiming to create an SMS-based budgeting app with the following behavior:

1. When I make a transaction on my debit card,
2. Plaid notices that transaction and pings a Flask server running on Vercel,
3. Which in turn uses Twilio to text me, asking me to describe and categorize the transaction
4. Twilio forwards my response to the Flask server, which then parses the response and adds it to a Google Sheet

This is not yet functional.
