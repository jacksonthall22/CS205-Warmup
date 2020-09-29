import sql_queries

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
        'Athlete':
            ['Name', 'Age', 'Sex', 'Gold', 'Silver', 'Bronze', 'Team', 'Event'],
        'Sport': ['Name', 'Season', 'Type']
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
    print(
        'Help message goes here, enter commands like these ones in this format -- select <Athlete/Sport> <field1>="x" [, <field2>="y"]: -- with strings in "quotes" and ints without'
    )
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
    print('----Event -- execute Athlete subcommand find by athlete event competed')
    print('----Age -- execute Athlete subcommand find by age')
    print(
        '----Team -- execute Athlete subcommand find by Team, the country an athelte represents'
    )
    print('----Sex -- execute Athlete subcommand find by sex')
    print('----Gold -- execute Athlete subcommand find by gold medals')
    print('----Silver -- execute Athlete subcommand find by silver medals')
    print('----Bronze -- execute Athlete subcommand find by bronze medals')

    print('Example commands: ')
    print('Select Sport = "skiing"')
    print('Select Athlete Gold = 3')

    # new print statements


def displayFirstUnrecognizedToken(cmd, commandDict=FLAGS, depth=0):
    # Variables
    global VALIDATED
    VALIDATED = True
    index = 0
    first = True
    cmd2 = ""
    correct = True
    found = False
    sportsTime = False

    # Adds spacing to user input after and before "=" if not there so tokens list for validation is correct

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

    # if length of user input is longer than one word, split by spaces and assign to tokens list
    if (len(cmd2.split()) > 1):
        tokens = cmd2.split()
    else:
        # else assign tokens to word
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
                # if user input is still correct and token is second word in list
        elif count == 1 and correct:
            # checks if token is not Sport or Athlete key word
            if token != "Sport" and token != "Athlete":
                correct = False
            else:
                count += 1

                # if user input is still correct and tokens are getting into specific keywords
        elif correct and count == 2:
            correctCount = -1

            # if the first keyword was Sport or there is a foriegn key to Sport table
            if tokens[1] == "Sport" or sportsTime:
                correct = checkSport(token, tokens, correctCount, ct, correct)

            correctCount = -1

            # if the first keyword was Athlete and there is no foriegn key to Sport table
            # if the first keyword was Athlete and there is no foriegn key to Sport table
            if tokens[1] == "Athlete" and not sportsTime:
                # if the token checked is Sport and has no "=" after it, it is foriegn key to Sports table
                if token == "Sport":
                    if index != len(tokens) - 1:
                        index = tokens.index(token)
                        if tokens[index + 1] != "=":
                            newToken = tokens[index + 1]
                            # check Sports validation instead of Athlete b/c of foriegn key
                            correct = checkSport(newToken, tokens,
                                                 correctCount, ct, correct)
                            sportsTime = True

                            # Otherwise, check Athlete validation and keys
                        else:
                            correct = checkAthlete(token, tokens, correctCount, ct,
                                                   correct)
                else:
                    correct = checkAthlete(token, tokens, correctCount, ct,
                                           correct)

        # If the user search and input was invalid, print error message, and set VALIDATED to false so nothing invalid is passed to execute()
    if correct is False:
        VALIDATED = False
        print("Invalid command")

    # return the parsed list by spaces to main()
    return tokens


# User validation to check sport keywords against user input
def checkSport(token, tokens, correctCount, ct, correct):
    commandDict = FLAGS

    # is list of sport key words
    sportList = commandDict['Select']['Sport']

    # checks every sport key word against user keyword to see if valid
    for key in sportList:
        index = tokens.index(token)
        # checks to see if item is last in list
        if index != len(tokens) - 1:
            # if the next item in list is an "=", check for keyword
            if tokens[index + 1] == "=":
                if tokens[index - 1] != "Sport":
                    correct = False
                elif token == key:
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
    athleteList = commandDict['Select']['Athlete']

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
                    if token == "Age" or token == "Gold" or token == "Silver" or token == "Bronze":
                        userInput = tokens[index + 2]
                        # converts search string to integer
                        try:
                            value = int(userInput)
                            tokens[index + 2] = value
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
        Execute the given command cmd.

        cmd should be checked against COMMANDS before
        execute(cmd) is called to verify it is valid - that way any "errors" in this
        function are a result of terminatorRegex check, not a result of misused keywords:
        unknown filenames, athlete names that don't exist, etc.


    """

    # I just added this b/c in line 164 it couldn't recognize commandDict b/c it wasn't a parameter LP
    # Added as default parameter - JH
    # commandDict = FLAGS

    # Split on spaces only
    # ex: ['Select', 'Athlete', 'age=21', 'sport=skiing']

    # updated dict - tokensDict

    firstToken = cmd[0]
    remainingTokens = cmd

    # Making the validated list of commands into a dictionary for SQL ease
    tokensDict = {}
    for token in remainingTokens:
        for index, item in enumerate(remainingTokens):
            if item.lower() == "select":
                tokensDict["Table"] = remainingTokens[index + 1]
            elif item == '=':
                tokensDict[remainingTokens[index - 1]] = remainingTokens[index + 1]

    print(tokensDict)

    # Implement all the commands - query calls go here eventually
    # if firstToken == 'load data': # TODO: when you uncomment this change 'if' to 'elif' below
    if firstToken == 'Help':
        printCommandsDict()
    elif firstToken.lower() == 'load data':
        print("LOAD DATA")
    #     Class the load data logic here
    elif firstToken.lower() == 'select':
        sql_queries.executeSQL(tokensDict)



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
        # print(tokensList)

        # needs to return false if not recognized and prompt user for another input
        # cmd = input('Invalid command. Enter a command:\n——> ')

        # Main command
        # Run command

        # make test list thats already "validated"

        # if VALIDATED:
        # execute(tokensList)

        sql_queries.connect()




if __name__ == '__main__':
    main()
