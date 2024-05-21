import externalconstants 
import q

import mygoogle as mygoogle

class Entry:
    ### Constructer does these three ###
    date = "None"  #Column A 
    payee = "None" #Column B
    cost = "None"  #Column D

    ### These are gotten through text ###
    commodity = "None" #Column C
    category = "None"  #Column E

    def __init__ ( self, transaction, use_twilio=True ):
        #print(transaction)
        self.date = transaction.date
        print("date: ", end = "")
        print(self.date)
        self.payee = transaction.merchant_name
        print("merchant: ", end = "")
        print(self.merchant_name)
        self.cost = transaction.amount
        print("cost: ", end = "")
        print(self.cost)

        if use_twilio:
            # self.commodity = self.ask_commodity()

            # inputted_catagory = self.ask_category( False )
            # while not self.fixcheck_catagory( inputted_catagory ):
            #     inputted_catagory = self.ask_category( True )
            # self.category = self.fixcheck_catagory( inputted_catagory )
            pass
        else:
            self.commodity = ""
            self.category  = ""

    def fixcheck_catagory ( self, subject ): #fix to not be case sensitive and have room for up to 2 typos # returns False if not a valid catagory, returns the catagory if it is valid
        for catagory in mygoogle.valid_catagories:
            if subject.lower() == catagory.lower():
                return catagory
        return False
       
    # def ask_commodity( self ):
    #     #response = input("what did you just buy?:  ")
    #     response = server.get_response_to("what did you just buy?")
    #     output = q.camelcase_with_spaces(response, nopronouns=True)
    #     return output
    
    # def ask_category( self, annoyed:bool ):
    #     #if annoyed: print("that's not a valid catagory,")
    #     if annoyed: server.send_message("that's not a valid catagory")
    #     #response = input("what bit of your budget does this come from?:  ")
    #     response = server.get_response_to("what bit of your budget does this come from?")
    #     return response
               
    def enter_to_sheet( self ):
        print("I'm adding myself to the sheet!")
        my_row = str( len(mygoogle.get_value_range_dict("A1:A1000","Spending transactions")["values"])+1 )
        print("My row is " + str(my_row))

        mygoogle.write_in_cell( str(self.date), "A"+my_row, "Spending transactions") # try omiting 'Spending transactions' sometime for science
        mygoogle.write_in_cell( self.payee,     "B"+my_row, "Spending transactions") 
        mygoogle.write_in_cell( self.commodity, "C"+my_row, "Spending transactions") 
        if self.cost != -1:
            mygoogle.write_in_cell( str(self.cost), "D"+my_row, "Spending transactions")

    def __str__( self ) -> str:
        cleaned_cost = str(self.cost)
        if self.cost % 0.1:  cleaned_cost += ".0"
        if self.cost % 0.01: cleaned_cost += "0"

        output = "Transaction on " + self.date + " [" + self.category + "]"
        output += "\n    " + cleaned_cost + " to " + self.payee + " for " + self.commodity
        
        return output
    
# friend = Entry()
# print(friend)
# friend.enter_to_sheet()