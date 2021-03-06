################# IMPORTS #################
from sql_queries import executeSQL
from sql_queries import loadData

################# CONSTANTS #################
# list of valid keywords from query language
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
        'Enter commands like these ones in this format -- select <Athlete/Sport> <field1>="x" [, <field2>="y"]: -- with strings in "quotes" and integers without. This is not case sensitive'
    )
    print()
    print('┌──────────┐')
    print('│ COMMANDS │')
    print('├──────────┘')
    print('├╴Select : will get athlete/sport data based on nested commands')
    print('│ ├╴Sport : select Sport data table')
    print('│ │ ├╴name : execute Sport subcommand find by name')
    print('│ │ ├╴season : select sport season - (winter/summer)')
    print('│ │ └╴type : select sport type - (individual/team)')
    print('│ └╴athlete : select Athlete data table')
    print('│   ├╴fullname : execute Athlete subcommand find by name')
    print('│   ├╴event : execute Athlete subcommand find by athlete sport competed')
    print('│   ├╴age : execute Athlete subcommand find by age')
    print('│   └╴team : execute Athlete subcommand find by Team, the country an athlete represents eg. United States')
    print('├╴help : show this help message')
    print('└╴load data : load data into database (only required once)')
    print('')
    print('Example commands:')
    print('    Select Sport = "skiing"')
    print('    Select Athlete age = 24 sport type = "individual"')
    print('    Select Athlete Event = "Basketball" Sex = "F" Team = "United States"')
    print('    Select Sport Season = "winter" athlete sex = "f"')
    print('    Select Athlete Age = 20 sport Season = "winter"')
    print('    Select Sport Season = "winter" ')


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
                    newCmd += letter
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
                search = cmd2[indexOfFirstParentheses:indexOfSecondParentheses + 1]
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
                        tokens.insert(counter + 1, search)
                    except:
                        correct = False
            counter += 1
        count = 0

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
                                correct = checkAthlete(newToken, tokens, correctCount, ct, correct)
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
                                correct = checkSport(newToken, tokens, correctCount, ct, correct)
                                sportsTime = True

                            # Otherwise, check Athlete validation and keys
                            else:
                                correct = checkAthlete(token, tokens, correctCount, ct, correct)
                    else:
                        correct = checkAthlete(token, tokens, correctCount, ct, correct)

    # If the user search and input was invalid, print error message, and set VALIDATED to false so nothing invalid is passed to execute()
    if not correct:
        VALIDATED = False
        print("Invalid command")

    # return the parsed list by spaces to main()
    countSport = 0
    if correct:

        # take out sport token in tokens list for query search (was only used
        # to validate user input)
        for sportItem in tokens:
            if sportItem == "sport":
                if countSport != 1:
                    tokens.remove(sportItem)
            countSport += 1

        # return validated list of keywords to exec()
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

                        # converts search string to integer
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
    correct = True
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

    if correct:
        outputList = executeSQL(tokensDict)
        if outputList is not None:
            displayRecords(outputList)


def displayRecords(records):
    """ Display records to user in a readable way """

    # TODO
    assert type(records) == list or not records

    if not records:
        print('There were no records for that query.')
        return

    print('Your query returned these results:')
    print('----------------------------------')

    # Stores length of longest string in each field (to be printed vertically)
    colWidths = []
    for col in range(len(records[0])):  # loop through columns
        colWidths.append(max([len(str(record[col])) for record in records]))

    # Define width in spaces between columns
    COL_GAP = 3
    NUM_RECORDS_AT_A_TIME = 25

    for i_record, record in enumerate(records):
        for i_field, field in enumerate(record):
            print(f'{field:{(colWidths[i_field])}}', end=' ' * COL_GAP)

        print()

        if (i_record + 1) % 25 == 0:
            showMore = input(
                f'Showing records {(i_record + 1) - 24} – {i_record + 1} of {len(records)}. Show more? (y/n)\n––> ')

            while showMore not in ['y', 'yes', 'n', 'no']:
                showMore = input('Please enter "y" or "n":\n––>')

            if showMore in ['n', 'no']:
                break


def welcome():
    """ Print a welcome banner (called when program first runs) """
    # Credit to: https://ascii.co.uk/art/olympics
    print('''╓───────────────────────────────────┐
║                                   │
║    .-===-.   .-===-.   .-===-.    │
║   /       \ /       \ /       \\   │
║  | Olympic | Athlete | Database|  │
║   \      ./=\.     ./=\.      /   │
║    '-==-/'    '\=/'    '\-==-'    │
║        |        |        |        │
║         \      / \      /         │
║          '-==-'   '-==-\'          │
║                                   │
╟───────────────────────────────────┘
║  Created by:
║    Jackson Hall
║    Jake Walburger
║    Lauren Paicopolis
║    Sarah O'Brien
║''')
    print()


def main():
    welcome()

    while True:
        global VALIDATED
        otherKeyWord = False
        # Get command
        cmd = input('Enter a command:\n——> ').lower()

        if cmd.lower() == 'quit':
            break
        # help prints out help text about commands
        if cmd.lower() == 'help':
            VALIDATED = False
            otherKeyWord = True
            printCommandsDict()

        if cmd.lower() == 'load data':
            VALIDATED = False
            otherKeyWord = True
            print('Loading...', end='')
            loadData()
            print(' data loaded!')

        # validate the user command against query language
        if otherKeyWord != True:
            cmd = cmd.lower()
            tokensList = validateUserInput(cmd)

        # if user command is valid, execute query search
        if VALIDATED:
            execute(tokensList)

        print()


if __name__ == '__main__':
    main()
