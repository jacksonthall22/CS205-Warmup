'''
Jackson and Jake will write function here that can be called in main (since
it was 'include'd in main.py)
'''

import sqlite3
import pandas as pd
from pandas import DataFrame

dbConnection = None
dbCursor = None
DB_FILENAME = 'database_filename.db' # TODO be mroe creative
CSV_FILENAME_ATHLETES = 'athlete_csv.csv' # TODO
CSV_FILENAME_SPORTS = 'sport_csv.csv' # TODO

VALID_FIELDS = ['name', 'age', 'sex', 'gold', 'silver', 'bronze', 'team', 'sport', 'season']

# TODO check to see if the database already esists if not make open
# https://stackoverflow.com/questions/12932607/how-to-check-if-a-sqlite3-database-exists-in-python
# That might be able to help
def connect(dbFilename=DB_FILENAME):
    """ Create connection to database with given filename. """

    # Make sure hard-coded filename is valid
    success = True
    try:
        with open(dbFilename):
            pass
    except FileError:
        success = False
    
    assert success

    dbConnection = sqlite3.connect(dbFilename)
    dbCursor = dbConnection.cursor()

    # Load CSV data into DB
    load()
    
def executeSQL(fieldsDict, cursor=dbCursor):
    """ Execute command specified by fieldsDict. """
    
    # Raises AssertionError if fieldsDict is not formatted correctly on input
    assert 'table' in fieldsDict
            and fieldsDict['table'].lower() in ['sport', 'athlete']
            and all([i.lower() in VALID_FIELDS for i in fieldsDict])

    # Check if global db_connection is None
    if not dbConnection:
        connect()

    field = ''
    # Construct and execute the SQL from fieldsDict
    return cursor.execute(f'SELECT FROM {['tblAthlete', 'tblSport'][fieldsDict['table'].lower() == 'sport']} WHERE {' AND '.join([f'{i} == {fieldsDict[i]}' for i in fieldsDict])}')

def load():
    loadData(CSV_FILENAME_ATHLETES, 'tblAthlete')
    loadData(CSV_FILENAME_SPORTS, 'tblSports')

# This will load in the data with specified csv file name
def loadData(csvFileName, tableName):
    # These should read the data in the csvFile and put it into a table with the given name
    read_data = pd.read_csv(csvFile)
    read_data.to_sql(tableName, curs, if_exists='append',
                           index=False) # Insert the values from the csv file into the table tableName