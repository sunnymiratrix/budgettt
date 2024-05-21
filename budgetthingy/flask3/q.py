from datetime import date

# handy-dandy functions to be used where needed #
# (named after Q from the James Bond franchise, and it's easy to type)

#returns a list in backwards order
def turnyturny (list):
  output = []
  for thing in list:
     output.insert(0, thing)
  return output

#returns a copy of a list
def clone_list(list):
  copy = []
  copy.extend(list)
  return copy

#hard to explain lol
def camelcase_with_spaces(string, nopronouns=False): # for example "tHis StriNG" would turn into "This String"
  words = string.split()
  output = ""
  for word in words:
      word = word.lower()
      if not nopronouns and (word == "a" or word == "an" or word == "some"):
        pass
      else:
        output += word.lower().capitalize()
        output += " "  

  return output

#this should be removed and date taken from the transaction data but rn it's fine
def today(): #returns in format 'mm/dd/yyyy'
  today = date.today()
  output = ""

  if today.month < 10: output += "0"
  output += str(today.month) + "/"

  if today.day < 10: output += "0"
  output += str(today.day) + "/"

  output += str(today.year)

  return output