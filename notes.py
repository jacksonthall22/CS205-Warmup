import sqlite3

'''
CREATE TABLE IF NOT EXISTS tblAthlete...

CREATE TABLE IF NOT EXISTS tblSport...

================

Examples:

    -- projects table
    CREATE TABLE IF NOT EXISTS projects (
        id integer PRIMARY KEY,
        name text NOT NULL,
        begin_date text,
        end_date text
    );

    -- tasks table
    CREATE TABLE IF NOT EXISTS tasks (
        id integer PRIMARY KEY,
        name text NOT NULL,
        priority integer,
        project_id integer NOT NULL,
        status_id integer NOT NULL,
        begin_date text NOT NULL,
        end_date text NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects (id)
    );


temp:
pmkId	fldName	fldSex	fldAge	fldTeam	fldCountryCode	fldYear	fldVenue	fldSport	fldEvent	fldGolds	fldSilvers	fldBronzes

CREATE TABLE IF NOT EXISTS tblAthlete (
    pmkId integer PRIMARY KEY,
    fldName text NOT NULL,
    fldSex text NOT NULL,
    fldAge integer NOT NULL,
    fldTeam text NOT NULL,
    fldCountryCode text NOT NULL, # ---------- text or something else?
    fldYear date NOT NULL,
    fldVenue text NOT NULL,
    fldSport text NOT NULL,
    fldGolds integer NOT NULL,
    
)




'''

ALL_VALID_FILTERS = ['fullname', 'name', 'age', 'sex', 'team', 'sport', 'season']

def main():
    command = None
    while command != '':
        command = input('Enter your command:\n>>> ')

        if isValidCommand(command):
            print('\tCommand is valid!')
        else:
            print('\tCommand invalid.')

def tokenize(command):
    command = command.strip()
    quoteStack = []
    splitBoundaryIndex = 0

    # select athlete fullname="test name"
    for currentIndex, letter in enumerate(command):
        if letter == '"':
            if quoteStack and quoteStack[-1] == '"':
                del quoteStack[-1]
            else:
                quoteStack.append('"')

        if letter == ' ' or currentIndex == len(command)-1:
            if not quoteStack:
                tokens.append(command[splitBoundaryIndex: currentIndex+1].strip())
                splitBoundaryIndex = currentIndex
        
    print(f'test: tokens: {tokens}')

def parseCommand(command):
    if not isValidCommand(command):
        print('Invalid command.')
        return None

    tokens = tokenize(command)
    commandDict = {}

    for token in tokens:
        commandDict[token.split('=')[0]] = token.split('=')[1]
    
def isValidCommand(command):
    tokens = tokenize(command)
    
    if tokens[0].lower() in ['help', 'load'] and len(tokens) == 1:
        return True
    elif tokens[0].lower() == 'select':
        if tokens[1].lower() in ['athlete', 'sport']:
            filters = tokens[2:]

            for _filter in filters:
                if '=' not in _filter:
                    return False
                
                filterKey = _filter.split('=')[0]
                filterVal = _filter.split('=')[1].strip('"')

                if filterKey not in ALL_VALID_FILTERS:
                    return False
                
            return True

    return False
        
    
if __name__ == '__main__':
    main()