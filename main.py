################# CONSTANTS #################

# Set list of commands with their descriptions, functionality of each
# command is defined in execute()
# (Basically JSON format: )
COMMANDS = {
    'test': {
        'description': 'this is a test function',
        'subCommands': {},
    },
    'subCommandsTest': {
        'description': 'test use of multiple tokens / nested commands',
        'subCommands': {
            'testA': {
                'description': 'execute subcommand A',
                'subCommands': {},
            },
            'testB': {
                'description': 'execute subcommand B',
                'subCommands': {
                    'B1': {
                        'description': 'execute testB subcommand B1',
                        'subCommands': {},
                    },
                    'B2': {
                        'description': 'execute testB subcommand B2',
                        'subcommands': {},
                    },
                },
            },
        },
    },
    'help': {
        'description': 'list available commands',
        'subCommands': {},
    },
    'quit': {
        'description': 'quit this program',
        'subCommands': {},
    },
}

# Used when recursively printing descriptions of available commands & subCommands
SPACES_PER_DEPTH = 2

def printCommandsDict(commandDict, depth):
    """
        Take a dictionary of commands and print formatted description
        of their functions.

        If any command in commandDict has subcommands, make a recursive call
        to print those commands indented by one more level. Starts at depth = 1
    """

    # Show initial help message
    if depth == 1:
        print('Help message goes here, enter commands like these ones:')
        print()
        print('Commands')
        print('--------')

    # Print descriptions for all commands
    for command in commandDict:
        print(f'{" " * depth * SPACES_PER_DEPTH}{command} : {commandDict[command]["description"]}')

        # If there are subcommands, recursive call to print their descriptions
        if commandDict[command]['subCommands'] != {}:
            printCommandsDict(commandDict[command]['subCommands'], depth + 1)

def execute(cmd):
    """ Execute the given command cmd. """

    # Do a check to make sure first token in cmd is a valid command
    # (Assert raises AssertionError if expression is False)
    # Just for testing, error checking should be done before calling execute()
    assert cmd.split()[0] in COMMANDS

    # Split into 'first' and 'everything else' tokens
    # Ex. 'gcc -std=gnu99 filename.c' becomes:
    # firstToken = 'gcc'
    # remainingTokens = '-std=gnu99 filename.c'
    firstToken = cmd.split()[0].lower()
    remainingTokens = ' '.join(cmd.split()[1:])

    if firstToken == 'help':
        printCommandsDict(COMMANDS, 1)

    elif firstToken == 'test':
        print(f'Test command run with remainingTokens = "{remainingTokens}"')

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
        while cmd.split()[0] not in COMMANDS:
            cmd = input('Invalid command. Enter a command with arguments:\n——> ')

        # Main command 
        # Run command
        execute(cmd)

        print()

if __name__ == '__main__':
    main()