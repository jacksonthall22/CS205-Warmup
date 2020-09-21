

################# GROUP NOTES #################
'''
Write any stuff here that everyone should see!
--------
JH = Jackson
JW = Jake
LP = Lauren
SO = Sarah

Group Notes:
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
FLAGS = {
    'Select': {
        'Athlete': ['Name', 'Age', 'Sex', 'Gold', 'Silver', 'Bronze', 'Team', 'Sport'],
        'Sport': ['Name', 'Season']
    },
    'Quit': 'Quits program',
    'Help': 'Displays Menu',
    'Load': 'Loads data',
}


################# FUNCTIONS #################

def printCommandsDict(commandDict=FLAGS, depth=1):
    """
        Take a dictionary of commands and print formatted description
        of their functions.

        If any command in commandDict has subcommands, make a recursive call
        to print those commands indented by one more level. Uses COMMANDS dict
        and starts at depth 1 by default
    """

    # Show initial help message
    if depth == 1:
        print('Help message goes here, enter commands like these ones:')
        print()
        print('┌──────────┐')
        print('│ COMMANDS │')
        print('├──────────┘')

    # Basically "for command in commandDict", but this allows for "hasnext()"ish functionality
    commandDictItr = iter(commandDict)
    while commandDictItr.__length_hint__() > 0:
        # Get next key from iterable - next() decreases output of __length_hint__() by 1
        command = next(commandDictItr)

        # Checks if dictionary has next element - if not print └ instead of ├
        # Also checks that there isn't another nested layer of │s the bottom of the
        # connector should connect to
        connector = '├╴'
        if commandDictItr.__length_hint__() == 0 and commandDict[command]['subcommands'] is None:
            connector = '└╴'

        print('│ ' * (depth - 1) + connector + f'{command} : {commandDict[command]["description"]}')

        # If there are subcommands, recursive call to print their descriptions
        if commandDict[command]['subcommands'] is not None:
            printCommandsDict(commandDict[command]['subcommands'], depth + 1)
        # else:
        #     print('│ ' * (depth-1) + '├╴' + f'{command} : {commandDict[command]["description"]}')
        #     # print(f'{" " * depth * SPACES_PER_DEPTH}{command} : {commandDict[command]["description"]}')

        #     # If there are subcommands, recursive call to print their descriptions
        #     if commandDict[command]['subcommands'] is not None:
        #         printCommandsDict(commandDict[command]['subcommands'], depth + 1)


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

    # TODO
    tokens = cmd.split()
    count = 0
    correct = True
    # Looks through key word dictionary and verifies user input is valid
    for token in tokens:
        ct = 0
        # If user input is still valid (correct) and token is the first word in list
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
            if tokens[1] == "Sport":
                sportList = commandDict['Select']['Sport']
                for key in sportList:
                    if token == key:
                        index = tokens.index(token)
                        if tokens[index + 1] == "=":
                            searchWord = tokens[index + 2]
                            for letter in searchWord:
                                if letter == '"':
                                    ct += 1
                            if ct != 2:
                                correct = False



            if tokens[1] == "Athlete":
                athleteList = commandDict['Select']['Athlete']
                for key in athleteList:
                    if token == key:
                        index = tokens.index(token)
                        if tokens[index+1] == "=":
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
    if correct is False:
        print("Invalid command")


def execute(cmd):
    """
        Execute the given command cmd.

        cmd should be checked against COMMANDS before
        execute(cmd) is called to verify it is valid - that way any "errors" in this
        function are a result of terminatorRegex check, not a result of misused keywords:
        unknown filenames, athlete names that don't exist, etc.

    """

    # Do a check to make sure first token in cmd is a valid command
    # (Assert raises AssertionError if expression is False)
    assert cmd.split()[0] in FLAGS

    # I just added this b/c in line 164 it couldn't recognize commandDict b/c it wasn't a parameter LP
    commandDict = FLAGS

    # Split into 'first' and 'everything else' tokens as strings
    # Ex. 'gcc -std=gnu99 filename.c' becomes:
    # firstToken = 'gcc'
    # remainingTokens = '-std=gnu99 filename.c'
    firstToken = cmd.split()[0]
    remainingTokens = ' '.join(cmd.split()[1:])

    if remainingTokens == '' and commandDict[cmd]['subcommands'] is None:
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
        displayFirstUnrecognizedToken(cmd)
        # needs to return false if not recognized and prompt user for another input
        # cmd = input('Invalid command. Enter a command:\n——> ')

        # Main command
        # Run command
        execute(cmd)

        print()


if __name__ == '__main__':
    main()