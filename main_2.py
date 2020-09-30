################# GROUP NOTES #################
'''
Write any stuff here that everyone should see!
--------
JH = Jackson
JW = Jake
LP = Lauren
SO = Sarah

Group Notes:
-talk to lauren about how shes sending over validated - SO
  - ctrl-f for TODO for stuff that still needs doing to be done - JH
  - Check if the commands are the ones we wanted/correct? or if 
    they should change - LP
  - LP & SO will we want some keywords/syntax/"output mode" to
    decide how much info from a particular record to display on screen?
    Maybe two modes: 1 displays all info and 2 displays less, like Name, Age, Sport,
    Country Code, Golds, Silvers, Bronzes? - JH
  - Clarification thing: probably no need to ever display a list of 
    sports that match criteria right? Ex "Select Sport Soccer" I assume
    still shows a list of athleteS? - JH

'''

################# CONSTANTS #################
#list of
FLAGS = {
    'select': {
        'athlete':
        ['fullname', 'age', 'sex', 'team', 'event'],
        'sport': ['name', 'season', 'type']
    },
    'quit': 'Quits program',
    'help': 'Displays Menu',
    'load': 'Loads data',
}

VALIDATED = True

################# FUNCTIONS #################


def printCommandsDict(commandDict=FLAGS, depth=1):
    """
        print formatted description of the command functions as well as examples
    """

    # Show initial help message
    print(
        'Help message goes here, enter commands like these ones in this format -- select <Athlete/Sport> <field1>="x" [, <field2>="y"]: -- with strings in "quotes" and integers without. This is not case sensitive'
    )
    print()
    print('┌──────────┐')
    print('│ COMMANDS │')
    print('├──────────┘')

    print('Select -- will get athlete/sport data based on nested commands')
    print('-Sport -- select Sport data table')
    print('----Name -- execute Sport subcommand find by name')
    print('----Season -- select sport season - (winter/summer)')
    print('----Type -- select sport type - (individual/team)')
    print('-Athlete -- select Athlete data table')
    print('----fullname -- execute Athlete subcommand find by name')
    print('----Event -- execute Athlete subcommand find by athlete sport competed')
    print('----Age -- execute Athlete subcommand find by age')
    print('----Team -- execute Athlete subcommand find by Team, the country an athlete represents eg. United States, Germany, Russia')
    print('----Sex -- execute Athlete subcommand find by sex (M/F)')

    print('Example commands: ')
    print('Select Sport = "skiing"')
    print('Select Athlete fullname = "Simone Biles"')
    print('Select Athlete Event = "Basketball" Sex = "F" Team = "United States"')
    print('Select Athlete Age = 20 Sport Season = "winter"')
    print('Select Sport Season = "winter" Athlete age = 24')

# ValidatesUserInput validates the user input based on specific
# criteria of query language
def validateUserInput(cmd, commandDict=FLAGS, depth=0):
  # VARIABLES
  global VALIDATED
  VALIDATED = True
  index = 0
  first = True
  cmd2 = ""
  correct = True
  found = False
  sportsTime = False
  athleteTime = False

  # Adds spacing to user input after and before "=" if not there to split by spaces later
  try:
      while not found:
          
          # If there is no "=" and it is the first time cmd string is checked, set cmd2 to cmd
          if (cmd.find("=") == -1 and first):
              found = True
              cmd2 = cmd
          
          # else if there is no "=" left in cmd string, set cmd2 = cmd
          elif (cmd.find("=") == -1):
              cmd2 = cmd2 + cmd
              found = True
          
          # else there are "=" left in cmd string to be split
          else:
              first = False
              # find the index of "=" in string
              index = cmd.find("=")
              
              # if there is no space before "=", add one
              if cmd[index - 1] != " ":
                  cmd = cmd[:index] + ' ' + cmd[index:]
                  index += 1
              # if there is no space after "=", add one
              if cmd[index + 1] != " ":
                  cmd = cmd[:index + 1] + ' ' + cmd[index + 1:]
              # put string back together
              cmd2 = cmd2 + cmd[:index + 2]
              # if there are no more "=" left in cmd, go to very end of cmd and get rest of string
              if (cmd.find("=") == -1):
                  cmd = cmd[index + 2:len(cmd)]
              # Else re assign cmd to rest of string
              else:
                  cmd = cmd[index + 2:]
  except IndexError:
      correct = False
  print(cmd2)

  # Calculate number of the parentheses in the user input, if there is not opening & closing 
  # parentheses, set correct to false
  anotherOne = 0
  stringKeyWord = False
  for i in cmd2:
      if i == '"':
          anotherOne += 1
      if i == "name" or i == "fullname" or i == "event" or i == "team" or i == "sex" or i == "type" or i == "season":
          stringKeyWord = True
  if anotherOne % 2 != 0 or anotherOne == 0 and stringKeyWord:
      correct = False

  # Takes user input and appends all key words (not user search) to new string, and then 
  # splits by spaces 
  if correct:
      count = 0
      newCmd = ""
      for letter in cmd2:
          if letter == '"':
              count += 1
          if count == 0 or count % 2 == 0:
              if letter != '"':
                newCmd+=letter
      if (len(newCmd.split()) > 1):
          tokens = newCmd.split()
      else:
          tokens = cmd2

      # VARIABLES
      index = 0
      counter = 0
      searchList = []
      indexOfFirstParentheses = 0
      indexOfSecondParentheses = 0
      
      # Locates index of parantheses and seperates user search from rest of string, appends
      # to list searchList
      for letter in cmd2:
          if letter == '"':
              counter += 1
              if counter == 1:
                  indexOfFirstParentheses = index
              else:
                  indexOfSecondParentheses = index
          if indexOfFirstParentheses != 0 and indexOfSecondParentheses != 0:
              search = cmd2[indexOfFirstParentheses:indexOfSecondParentheses+1]
              indexOfSecondParentheses = 0
              indexOfFirstParentheses = 0
              counter = 0
              searchList.append(search)
          index += 1

      # Inserts user search back into tokens list after '=' and in proper place and removes 
      # from searchList, unless the search was for an integer value
      counter = 0
      for item in tokens:
          if item == '=':
            token = tokens[counter - 1]
            if token == "name" or token == "fullname" or token == "event" or token == "team" or token == "sex" or token == "type" or token == "season":
              try:
                search = searchList[0]
                searchList.remove(search)
                tokens.insert(counter+1,search)
              except:
                correct = False
          counter += 1
      count = 0

      print (tokens)
     
      # Makes sure user cannot enter same keyword search more than once - LP
      for item in tokens:
          if tokens.count(item) > 1 and item != "=":
              correct = False

      # Looks through key word dictionary and verifies user input is valid
      for token in tokens:
        ct = 0
        # If user input is still valid (correct) and token is the first word in list
        if len(tokens) > 2:
          if tokens[2] == "=":
            correct = False
        if cmd2.find("=") == -1:
          correct = False
        if count == 0 and correct:
          
          # if user input is not a key word
          if token not in commandDict:
            correct = False
          else:
            count += 1

        # if user input is still correct and token is second word in list
        elif count == 1 and correct:
          # checks if token is not Sport or Athlete key word
          if token != "sport" and token != "athlete":
              correct = False
          else:
            count += 1

        # if user input is still correct and tokens are getting into specific keywords
        elif correct and count == 2:
          correctCount = -1

          # if the first keyword was Sport or there is a foriegn key to Sport table
          if (tokens[1] == "sport" or sportsTime) and not athleteTime:
            if token == "athlete":
              if index != len(tokens) - 1:
                    index = tokens.index(token)
                    if tokens[index + 1] != "=":
                        newToken = tokens[index + 1]
                        # check Athlete validation instead of Sport b/c of foriegn key
                        correct = checkAthlete(newToken, tokens,correctCount, ct, correct)
                        athleteTime = True
                    
                    # Otherwise, check Sport validation and keys
                    else:
                           correct = checkSport(token, tokens, correctCount, ct, correct)
              else:
                 correct = checkSport(token, tokens, correctCount, ct, correct)

          correctCount = -1

          # if the first keyword was Athlete and there is no foriegn key to Sport table
          if (tokens[1] == "athlete" or athleteTime) and not sportsTime:
              if token == "sport":
                if index != len(tokens) - 1:
                    index = tokens.index(token)
                    if tokens[index + 1] != "=":
                        newToken = tokens[index + 1]
                        # check Sports validation instead of Athlete b/c of foriegn key
                        correct = checkSport(newToken, tokens,correctCount, ct, correct)
                        sportsTime = True

                    # Otherwise, check Athlete validation and keys
                    else:
                          correct = checkAthlete(token, tokens, correctCount, ct, correct)
              else:
                correct = checkAthlete(token, tokens, correctCount, ct, correct)

  # If the user search and input was invalid, print error message, and set VALIDATED to false so nothing invalid is passed to execute()
  if correct is False:
      VALIDATED = False
      print("Invalid command")

  # return the parsed list by spaces to main()
  if correct:
    return tokens

# User validation to check sport keywords against user input
def checkSport(token, tokens, correctCount, ct, correct):
    commandDict = FLAGS

    # is list of sport key words
    sportList = commandDict['select']['sport']

    # checks every sport key word against user keyword to see if valid
    for key in sportList:
        index = tokens.index(token)
        
        # checks to see if item is last in list
        if index != len(tokens) - 1:
            
            # if the next item in list is an "=", check for keyword
            if tokens[index + 1] == "=":
                if token == key:
                    correctCount += 1
                    correct = True
                    searchWord = tokens[index + 2]
                    
                    # user search must be a string with ""
                    for letter in searchWord:
                        if letter == '"':
                            ct += 1
                    if ct != 2:
                        correct = False
                # if the token is not a keyword, it is invalid
                elif correctCount != 0:
                    correct = False
    
    # return if keyword and user search was valid
    return correct

# User validation to check athlete keywords against user input
def checkAthlete(token, tokens, correctCount, ct, correct):
    commandDict = FLAGS

    # is list of athlete key words
    athleteList = commandDict['select']['athlete']

    # checks every athlete key word against user keyword to see if valid
    for key in athleteList:
        index = tokens.index(token)
        
        # checks to see if item is last in list
        if index != len(tokens) - 1:
            
            # if the next item in list is an "=", check for keyword
            if tokens[index + 1] == "=":
                if token == key:
                    correctCount += 1
                    correct = True
                    
                    # validates user search to make sure it is an integer for specific keywords
                    if token == "age":
                        userInput = tokens[index + 2]
                        
                         #converts search string to integer
                        try:
                            value = int(userInput)
                        except ValueError:
                            correct = False
                    
                    # otherwise, user search must be a string with ""
                    else:
                        searchWord = tokens[index + 2]
                        for letter in searchWord:
                            if letter == '"':
                                ct += 1
                        if ct != 2:
                            correct = False
                
                # if the token is not a keyword, it is invalid
                elif correctCount != 0:
                    correct = False
    
    # return if keyword and user search was valid
    return correct


def execute(cmd, commandDict=FLAGS):
    """
        Makes a dictionary of the already validated comands
        Prints data output 
    """

    # Making the validated list of commands into a dictionary for SQL ease
    correct  = True
    tokensDict = {}
    try:
      for token in cmd:
        for index, item in enumerate(cmd):
          if item == "select":
            tokensDict["table"] = cmd[index + 1]
          elif item == '=':
            tokensDict[cmd[index - 1]] = (cmd[index + 1]).strip('"')
    except:
      print("Invalid command")
      correct = False
    
    if correct == True:  
        print(tokensDict)
        outputList = executeSQL(tokensDict)
        
        displayRecords(outputList)

def displayRecords(records):
    """ Display records to user in a readable way """

    # TODO
    assert type(record) == list

    if not records:
        print('There were no records for that query.')
        return

    print('Your query returned these results:')
    print('----------------------------------')
    
    # Get what widths of columns should be based on longest element of any record in that field
    colWidths = []
    for col in range(len(records[0])):
        colWidths.append(max((len(record[col]) for record in records))

    # Define width in spaces between columns
    COL_GAP = 3

    for record in records:
        for i, field in enumerate(record):
            print(f'{field: colWidths[i] + COL_GAP}')

def main():
    while True:
        global VALIDATED
        # Get command
        cmd = input('Enter a command:\n——> ').lower()

        if cmd.lower() == 'quit':
            break
        # help prints out help text about commands
        if cmd.lower() == 'help':
          VALIDATED = False
          printCommandsDict()

        # validate the user command against query language
        else:
          cmd = cmd.lower()
          tokensList = validateUserInput(cmd)
        
        # if user command is valid, execute query search
        if VALIDATED:
            execute(tokensList)

        print()

if __name__ == '__main__':
    main()
