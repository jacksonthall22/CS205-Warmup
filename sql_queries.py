'''
Jackson and Jake will write function here that can be called in main (since
it was 'include'd in main.py)
'''
import os
import sqlite3
import pandas as pd
from pandas import DataFrame

dbConnection = None
dbCursor = None
dbExists = False
DB_FILENAME = 'database_filename.db' # TODO be mroe creative
CSV_FILENAME_ATHLETES = 'tblAthlete.csv' # TODO
CSV_FILENAME_SPORTS = 'tblSport.csv' # TODO

VALID_FIELDS = ['name', 'age', 'sex', 'gold', 'silver', 'bronze', 'team', 'event', 'season']

# Connect to the database and see if the DB is already open
def connect(dbFilename=DB_FILENAME):
    """ Create connection to database with given filename. """
    global dbExists

    if os.path.isfile(DB_FILENAME):
        print('Database already exists. Over writing database')
        dbExists = True

    global dbConnection
    dbConnection = sqlite3.connect(dbFilename)

    global dbCursor
    dbCursor = dbConnection.cursor()
    
def executeSQL(fieldsDict, cursor=dbCursor):
    """ Translate command specified by fieldsDict to SQL and execute it. """
    
    # Raises AssertionError if fieldsDict is not formatted correctly on input
    # assert 'table' in fieldsDict
    #     and fieldsDict['table'].lower() in ['sport', 'athlete']
    #     and all([i.lower() in VALID_FIELDS for i in fieldsDict])

    # Check if global db_connection is None
    if not dbConnection:
        connect()

    print('test: here\'s fieldsDict:')
    print(fieldsDict)
    if fieldsDict['table'].lower() == 'athlete':
        sql_string = 'SELECT pmkId,fldName,fldSex,fldAge,fldTeam,fldCountryCode,fldYear,fldVenue,fnkSport,fldEvent FROM tblAthlete ORDER BY fldName;'
    elif fieldsDict['table'].lower() == 'sport':
        sql_string = 'tblSport'
    else:
        print('test: fieldsDict didn\'t have "table" key')

    # Construct and execute the SQL from fieldsDict
    # return cursor.execute(f'SELECT FROM {['tblAthlete', 'tblSport'][fieldsDict['table'].lower() == 'sport']} WHERE {' AND '.join([f'{i} == {fieldsDict[i]}' for i in fieldsDict])} OUTER JOIN')

    """
        user enters:
        select athlete name="athlete name" sport=swimming gold=3 bronze=2

        SQL pseudocode:
                                                                                notice here \/
        SELECT WHERE COUNT(SELECT WHERE fldName="athlete name" AND sport="swimming" AND gold=1) == 3
                AND COUNT(SELECT WHERE name="athlete name" AND sport="swimming" AND bronze=1) == 2
    """
        
        
def loadData():
    if not dbConnection:
        connect()

    loadCSV(CSV_FILENAME_ATHLETES, 'tblAthlete')
    loadCSV(CSV_FILENAME_SPORTS, 'tblSports')

# This will load in the data with specified csv file name
def loadCSV(csvFileName, tableName):
    # These should read the data in the csvFile and put it into a table with the given name
    read_data = pd.read_csv(csvFileName)

    global dbConnection, dbExists

    # If the data base existed before then we should override it
    if dbExists:
        read_data.to_sql(tableName, dbConnection, if_exists='replace')
    else:
        read_data.to_sql(tableName, dbConnection)

    queryValues = []
    with open(csvFileName, newline='') as file:
        for i, line in enumerate(file):
            # testing
            if i > 200:
                break

            print(line)

# Just testing
if __name__ == '__main__':
    print('Just testing, to run main code go to .replit file and change sql_queries.py to main_2.py -JTH')
    load()