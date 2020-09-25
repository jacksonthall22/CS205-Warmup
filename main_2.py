

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

# Set list of commands with their descriptions and subcommands. terminatorRegex can be
# used to check that the last non-keywords of a command (athlete/sport name, etc) are valid
# (Basically JSON format: https://en.wikipedia.org/wiki/JSON#Example)

# import sql_queries.py

FLAGS = {
    'Select': {
        'Athlete': ['Name', 'Age', 'Sex', 'Gold', 'Silver', 'Bronze', 'Team', 'Sport'],
        'Sport': ['Name', 'Season']
    },
    'Quit': 'Quits program',
    'Help': 'Displays Menu',
    'Load': 'Loads data',
}

VALIDATED = True


################# FUNCTIONS #################

def printCommandsDict(commandDict=FLAGS, depth=1):
    """
        Take a dictionary of commands and print formatted description
        of their functions.

    """

    # Show initial help message
    print('Help message goes here, enter commands like these ones in this format -- select <Athlete/Sport> <field1>="x" [, <field2>="y"]: -- with strings in "quotes" and ints without')
    print()
    print('┌──────────┐')
    print('│ COMMANDS │')
    print('├──────────┘')

    print('Select -- will get athlete/sport data based on nested commands')
    print('-Sport -- select Sport data table')
    print('----Name -- execute Sport subcommand find by name')
    print('----Season -- select sport season - winter/summer')
    print('----Type -- select sport type - (individual/team)')
    print('-Athlete -- select Athlete data table')
    print('----Name -- execute Athlete subcommand find by name)')
    print('----Age -- execute Athlete subcommand find by age')
    print('----Team -- execute Athlete subcommand find by Team, the country an athelte represents')
    print('----Sex -- execute Athlete subcommand find by sex')
    print('----Gold -- execute Athlete subcommand find by gold medals')
    print('----Silver -- execute Athlete subcommand find by silver medals')
    print('----Bronze -- execute Athlete subcommand find by bronze medals')

    print('Example commands: ')
    print('Select Sport = "skiing"')
    print('Select Athlete Gold = 3')

    #new print statements    


def displayFirstUnrecognizedToken(cmd, commandDict=FLAGS, depth=0):
    """
        TODO: Print error help message showing carot under position of first unrecognized token.

        Maybe something like this:
            ——> subCommandsTest testSdkflefj B1 aldkjflskfj
            Command not recognized:
                subCommandsTest testSdkflefj B1 aldkjflskfj
                                ^ invalid token

        However, shouldn't be used for names/fields/etc that aren't recognized: the following still does a query check for
            ——> get athlete by name "name that doesn't exist"
            No results for athlete "name that doesn't exist"

        Note: The "commandDict=COMMANDS" and "depth=0" are default arguments - see here:
            https://www.geeksforgeeks.org/default-arguments-in-python/
        for example:
            displayFirstUnrecognizedToken('test')
          = displayFirstUnrecognizedToken('test', COMMANDS, 0)
    """
    # still buggy, but almost works - LP
    # Adds spacing to user input after and before "=" if not there so tokens list for validation is correct
    VALIDATED = True
    found = False
    index = 0
    first = True
    cmd2 = ""
    correct = True
    found = False

    try:
        while not found:
            if (cmd.find("=") == -1 and first):
                found = True
                cmd2 = cmd
            elif (cmd.find("=") == -1):
                cmd2 = cmd2 + cmd
                found = True
            else:
                first = False
                index = cmd.find("=")
                if cmd[index-1] != " ":
                    cmd = cmd[:index] + ' ' + cmd[index:]
                    index+=1
                if cmd[index + 1] != " ":
                    cmd = cmd[:index + 1] + ' ' + cmd[index + 1:]
                cmd2 = cmd2 + cmd[:index + 2]
                if (cmd.find("=") == -1):
                    cmd = cmd[index + 2:len(cmd)]
                else:
                    cmd = cmd[index + 2:]
    except IndexError:
        correct = False
    print(cmd2)

    # TODO
    if (len(cmd2.split()) > 1):
      tokens = cmd2.split()
    else:
      tokens = cmd2
    count = 0
    correct = True

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
        # while user input is still correct and token is second word in list
      elif count == 1 and correct:
            # checks if token is not Sport or Athlete key word
          if token != "Sport" and token != "Athlete":
              correct = False
          else:
              count += 1
        # while user input is still correct, verfies rest of user string

        # Just added this part, but it's a little buggy still - LP

      elif correct and count == 2:
          correctCount = -1
          if tokens[1] == "Sport":
              sportList = commandDict['Select']['Sport']
              for key in sportList:
                  index = tokens.index(token)
                  if index != len(tokens) - 1:
                      if tokens[index + 1] == "=":
                          if token == key:
                              correctCount += 1
                              correct = True
                              searchWord = tokens[index + 2]
                              for letter in searchWord:
                                  if letter == '"':
                                      ct += 1
                              if ct != 2:
                                  correct = False
                          elif correctCount != 0:
                              correct = False

          correctCount = -1
          if tokens[1] == "Athlete":
              athleteList = commandDict['Select']['Athlete']
              for key in athleteList:
                  index = tokens.index(token)
                  if index != len(tokens) - 1:
                      if tokens[index + 1] == "=":
                          if token == key:
                                  correctCount += 1
                                  correct = True
                                  if token == "Age" or token == "Gold" or token == "Silver" or token == "Bronze":
                                      userInput = tokens[index+2]
                                      try:
                                          value = int(userInput)
                                      except ValueError:
                                          correct = False
                                  else:
                                      searchWord = tokens[index+2]
                                      for letter in searchWord:
                                          if letter == '"':
                                              ct+=1
                                      if ct != 2:
                                          correct = False
                          elif correctCount != 0:
                              correct = False


    if correct is False:
        VALIDATED = False
        print("Invalid command")
    return tokens

def execute(cmd, commandDict=FLAGS):
    """
        Execute the given command cmd.

        cmd should be checked against COMMANDS before
        execute(cmd) is called to verify it is valid - that way any "errors" in this
        function are a result of terminatorRegex check, not a result of misused keywords:
        unknown filenames, athlete names that don't exist, etc.

    
    """

    # Do a check to make sure first token in cmd is a valid command
    # (Assert raises AssertionError if expression is False)
    #assert cmd.split()[0] in FLAGS

    # I just added this b/c in line 164 it couldn't recognize commandDict b/c it wasn't a parameter LP
    # Added as default parameter - JH
    # commandDict = FLAGS

    # Split on spaces only
    # ex: ['Select', 'Athlete', 'age=21', 'sport=skiing']
    
    
    #cmdTokens = cmd.split()

   # for token in cmdTokens:
    #  if token not in 


    # changed but I think it will work - JW
    firstToken = cmd[0]
    cmdCopy = cmd
    cmdCopy.remove(firstToken)
    remainingTokens = cmdCopy

    #converting into a dictionary
    testList = ['Select','Sport', 'Swimming', 'Gold', '=', '3']
    testList.remove('Select')

    testDict = {'table': testList[0]}
    #range (0, len(testList)-1):

#break by = 
    for index, item in enumerate(testList) :
        if list(testList)[-1]:
            break
        testDict[item] = testList[index + 1]
        
        #talk to lauren about how shes sending over validated - SO
        


    
    
   
   #dict = {'table': testList[0]}
    #it = iter(testList)
    #testDict = dict(zip(it, it))
    print(testDict)
    

    if remainingTokens == '':
        # Implement all the commands - query calls go here eventually
        # if firstToken == 'load data': # TODO: when you uncomment this change 'if' to 'elif' below
        if firstToken == 'help':
            printCommandsDict()
        # elif firstToken == 'Athlete':
        # print(f'[run test command with remainingTokens = "{remainingTokens}"')
        elif firstToken == 'Select':
            # Update first & remaining tokens
            firstToken = remainingTokens.split()[0]
            remainingTokens = ' '.join(remainingTokens.split()[1:])
            if firstToken == 'Athlete':
                firstToken = cmd.split()[0]
                remainingTokens = ' '.join(cmd.split()[1:])
                if firstToken == 'Name':
                    print("Age")
                elif firstToken == 'Age':
                    print(f'[run "subCommandsTest testB B2" command with remainingTokens = "{remainingTokens}"]')
                elif firstToken == 'Team':
                    print(f'[run "subCommandsTest testB B2" command with remainingTokens = "{remainingTokens}"]')
                elif firstToken == 'Sex':
                    print(f'[run "subCommandsTest testB B2" command with remainingTokens = "{remainingTokens}"]')
                elif firstToken == 'Age':
                    print(f'[run "subCommandsTest testB B2" command with remainingTokens = "{remainingTokens}"]')
                elif firstToken == 'Gold':
                    print(f'[run "subCommandsTest testB B2" command with remainingTokens = "{remainingTokens}"]')
                elif firstToken == 'Silver':
                    print(f'[run "subCommandsTest testB B2" command with remainingTokens = "{remainingTokens}"]')
                elif firstToken == 'Bronze':
                    print(f'[run "subCommandsTest testB B2" command with remainingTokens = "{remainingTokens}"]')
                elif firstToken == 'Sport':
                    print(f'[run "subCommandsTest testB B2" command with remainingTokens = "{remainingTokens}"]')
                else:
                    print('That command hasn\'t been implemented yet.')
            if firstToken == 'Sport':
                firstToken = cmd.split()[0]
                remainingTokens = ' '.join(cmd.split()[1:])
                if firstToken == 'Name':
                    print(f'[run "subCommandsTest testB B1" command with remainingTokens = "{remainingTokens}"]')
                elif firstToken == 'Season':
                    print(f'[run "subCommandsTest testB B1" command with remainingTokens = "{remainingTokens}"]')
                elif firstToken == 'Type':
                    print(f'[run "subCommandsTest testB B1" command with remainingTokens = "{remainingTokens}"]')
                else:
                    print('That command hasn\'t been implemented yet.')
        else:
            #
            print('That command hasn\'t been implemented yet.')

    # elif firstToken == ... etc. continue for all commands


def main():

    while True:
        # Get command

        cmd = input('Enter a command:\n——> ')

        if cmd == 'quit':
            break

        # Validate input & make sure first token is a valid command
        # (.split() splits string on spaces)
        # ie: 'gcc -std=gnu99 filename.c'.split()[0]
        #   = ['gcc', '-std=gnu99', 'filename.c'][0]
        #   = 'gcc'
        # while cmd.split()[0] not in COMMANDS:
        # TODO - call displayFirstUnrecognizedToken() here and get rid of
        # "Invalid command. " in input()
        tokensList = displayFirstUnrecognizedToken(cmd)
        print(tokensList)
        # needs to return false if not recognized and prompt user for another input
        # cmd = input('Invalid command. Enter a command:\n——> ')

        # Main command
        # Run command
       
        #make test list thats already "validated"

        # if VALIDATED:
        execute(tokensList)

        print()


if __name__ == '__main__':
    main()