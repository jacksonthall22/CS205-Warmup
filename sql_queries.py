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
DB_FILENAME = 'database.db'  # TODO be mroe creative
CSV_FILENAME_ATHLETES = 'tblAthlete.csv'
CSV_FILENAME_SPORTS = 'tblSport.csv'
dbExists = False
loadedData = False

VALID_FIELDS = ['name', 'age', 'sex', 'gold', 'silver', 'bronze', 'team', 'sport', 'season']

VALID_ATHLETE_FILTERS = {
    'sport': 'fnkSport',
    'fullname': 'fldFullName',
    'age': 'fldAge',
    'sex': 'fldSex',
    'team': 'fldTeam',
    'countrycode': 'fldCountryCode',
    'year': 'fldYear',
    'venue': 'fldVenue',
    'event': 'fldEvent'
}
VALID_SPORT_FILTERS = {
    'name': 'pmkName',
    'season': 'fldSeason',
    'type': 'fldType'
}

# Can't add dictionary types, have to do it this way
ALL_VALID_FILTERS = VALID_ATHLETE_FILTERS
ALL_VALID_FILTERS.update(VALID_SPORT_FILTERS)
ALL_VALID_FILTERS.update({'table': None})
# TODO check to see if the database already esists if not make open
# TODO if the database already exists then overwrite the data
# https://stackoverflow.com/questions/12932607/how-to-check-if-a-sqlite3-database-exists-in-python
# That might be able to help
def connect(dbFilename=DB_FILENAME):
    """ Create connection to database with given filename. """
    global dbExists

    if os.path.isfile(DB_FILENAME):
        dbExists = True

    global dbConnection

    dbConnection = sqlite3.connect(dbFilename)

    global dbCursor
    dbCursor = dbConnection.cursor()


def executeSQL(commandDict, cursor=dbCursor):
    """ Translate command specified by fieldsDict to SQL and execute it. """
    global dbConnection
    # Raises AssertionError if fieldsDict is not formatted correctly on input
    assert all(['table' in commandDict,
                commandDict['table'].lower() in ['sport', 'athlete'],
                all([i.lower() in ALL_VALID_FILTERS for i in commandDict])
                ])

    # Check if global db_connection is None
    if os.path.isfile(DB_FILENAME):
        connect()
    else:
        print("Please enter load data to load the tables for the database!")

    if dbConnection is not None:
        # Start of the query process

        sqlQuery = ''
        # Should never throw error because 'table' must be in given dict
        if commandDict['table'].lower() == 'athlete':
            # Execute SELECT for athlete records
            del (commandDict['table'])
            fields = []
            conditions = []
            for _filter in commandDict:
                # Assume all filters are valid since assertion was done before
                fields.append(ALL_VALID_FILTERS[_filter])
                conditions.append(f'{ALL_VALID_FILTERS[_filter]} = {commandDict[_filter]}')

            for _filter in VALID_ATHLETE_FILTERS:
                if _filter not in fields and _filter != 'table':
                    fields.append(VALID_ATHLETE_FILTERS[_filter])

            # TODO - not sure if this should be INNER JOIN or OUTER JOIN
            sqlQuery = 'SELECT {} FROM tblAthlete INNER JOIN tblAthlete ON tblAthlete.pmkId = tblSport.pmkName{};'.format(
                ', '.join(fields), [' WHERE ' + ', '.join(conditions), ''][conditions != []])

        elif commandDict['table'].lower() == 'sport':
            # Execute SELECT for sport records
            del (commandDict['table'])
            fields = []
            conditions = []
            for _filter in commandDict:
                # Assume all filters are valid since assertion was done before
                fields.append(ALL_VALID_FILTERS[_filter])
                conditions.append(f'{ALL_VALID_FILTERS[_filter]} = {commandDict[_filter]}')

            for _filter in VALID_SPORT_FILTERS:
                if _filter not in fields and _filter != 'table':
                    fields.append(VALID_SPORT_FILTERS[_filter])

            # TODO - not sure if this should be INNER JOIN or OUTER JOIN
            sqlQuery = 'SELECT {} FROM tblSport INNER JOIN tblSport ON tblSport.pmkName = tblAthlete.pmkId{};'.format(
                ', '.join(fields), [' WHERE ' + ', '.join(conditions), ''][conditions != []])
        else:
            print('test: commandDict[\'table\'] wasn\'t "athlete" or "sport"')

        print(f'test: sqlQuery: {sqlQuery}')
        return dbCursor.execute(sqlQuery)


def loadData():
    if dbConnection is None:
        connect()

    loadCSV(CSV_FILENAME_ATHLETES, 'tblAthlete')
    loadCSV(CSV_FILENAME_SPORTS, 'tblSports')


# This will load in the data with specified csv file name
def loadCSV(csvFileName, tableName):
    # These should read the data in the csvFile and put it into a table with the given name
    read_data = pd.read_csv(csvFileName)

    # If the data base existed before then we should override it
    if dbExists:
        print('Overwriting data!')
        read_data.to_sql(tableName, dbConnection, if_exists='replace')
    else:
        read_data.to_sql(tableName, dbConnection)
