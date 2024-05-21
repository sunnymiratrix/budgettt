import google.auth
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from googleapiclient.discovery import build

from os import path 

import externalconstants as ec
import q

# frankharperxi@finance-updater-middle-man.iam.gserviceaccount.com
credPath = path.abspath( path.join(path.dirname(__file__), "finance-updater-middle-man-bf7ab69c5f17.json"))
credentials = service_account.Credentials.from_service_account_file(credPath, scopes=["https://www.googleapis.com/auth/spreadsheets"])
service = build("sheets", "v4", credentials=credentials) # used globally

# works #
### Returns a ValueRange dictionary object, use '["values"]' to an actual list of values, individual cell values default to lists for god knows what reason
def get_value_range_dict(range, sheet=False): # omits tailing rows and columns, 
  range_id = ""
  if sheet: range_id += sheet + "!"
  range_id+= range 
  try:
    result = (
         service.spreadsheets() # global object, 'service' 
        .values()
        .get(spreadsheetId=ec.SPREADSHEET_ID, range=range_id)
        .execute()
    )
    # rows = result.get("values", [])
    # print(f"{len(rows)} rows retrieved")
    return result
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error
    output = ""
    now = date.today()
    output = ""

    #month
    if now.month < 10:
        output += "0"
    output += str( now.month )
    output += "/"

    #day
    if now.day < 10:
        output += "0"
    output += str( now.day )
    output += "/"

    #year
    if now.year < 1000:
        output += "0"
    if now.year < 100:
        output += "0"
    if now.year < 10:
        output += "0"
    output += str( now.year )

    return output

# works #
### Returns a list of strings with all the valid catagories ###
def get_valid_categories(): # hardcoded to get the list from the 'Wallet' sheet's first column, starting in the second row
    list = get_value_range_dict("A2:A20", "Wallet")["values"]
    output = []
    for thing in list:
        output.append(thing[0])
    return output

valid_catagories = get_valid_categories() #string list


def write_in_cell(thing, cell, sheet=False):
    cell_id = ""
    if sheet: cell_id += sheet + "!"
    cell_id += cell + ":" + cell

    print("I'm gonna add '" + thing + "' to '" + cell_id + "'")

    try:
        service.spreadsheets().values().update(spreadsheetId=ec.SPREADSHEET_ID, range=cell_id, valueInputOption="USER_ENTERED", body={"values": [[thing]]}).execute()
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

def date_of_last_transaction():
    dates = get_value_range_dict("A1:A1000", "Spending transactions")
    print (dates)
    return dates["values"][-1][0]