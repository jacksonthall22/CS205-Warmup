import os
import sqlite3
import pandas as pd

DB_FILENAME = 'database.db'
CSV_FILENAME_ATHLETES = 'tblAthlete.csv'
CSV_FILENAME_SPORTS = 'tblSport.csv'
dbConnection = None
dbCursor = None
dbExists = False
loadedData = False

VALID_FIELDS = ['name', 'age', 'sex', 'gold', 'silver', 'bronze', 'team', 'sport', 'season']

VALID_ATHLETE_FILTERS = {
    'fullname': 'tblAthlete.fldFullName',
    'age': 'tblAthlete.fldAge',
    'sex': 'tblAthlete.fldSex',
    'team': 'tblAthlete.fldTeam',
    'countrycode': 'tblAthlete.fldCountryCode',
    'year': 'tblAthlete.fldYear',
    'venue': 'tblAthlete.fldVenue',
    'event': 'tblAthlete.fldEvent'
}
VALID_SPORT_FILTERS = {
    'name': 'tblSport.pmkName',
    'season': 'tblSport.fldSeason',
    'type': 'tblSport.fldType'
}

ALL_VALID_FILTERS = VALID_ATHLETE_FILTERS.copy()
ALL_VALID_FILTERS.update(VALID_SPORT_FILTERS)
ALL_VALID_FILTERS.update({'table': None})


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
        if dbConnection is not None:
            # Start of the query process

            sqlQuery = ''
            # Should never throw error because 'table' must be in given dict
            if commandDict['table'].lower() == 'athlete':
                # Execute SELECT for athlete records
                del (commandDict['table'])

                fields = set()
                conditions = set()

                for _filter in commandDict:
                    # Add _filters only from the other table - ones from this table are SELECTed by default
                    if _filter not in VALID_ATHLETE_FILTERS:
                        fields.add(ALL_VALID_FILTERS[_filter])

                    # Put quotes around vaule in SQL query for string fields
                    if _filter.lower() in ['fullname', 'sex', 'team', 'countrycode', 'venue', 'event', 'name', 'season', 'type']:
                        conditions.add(f'lower({ALL_VALID_FILTERS[_filter]})="{commandDict[_filter]}"')
                    else:
                        conditions.add(f'{ALL_VALID_FILTERS[_filter]}="{commandDict[_filter]}"')

                # for _filter in VALID_ATHLETE_FILTERS:
                #     if VALID_ATHLETE_FILTERS[_filter] not in fields:
                #         fields.add(VALID_ATHLETE_FILTERS[_filter])

                # TODO - not sure if this should be INNER JOIN or OUTER JOIN
                sqlQuery = 'SELECT tblAthlete.fldFullName, tblAthlete.fldTeam, tblAthlete.fldAge,  tblAthlete.fldSex, tblAthlete.fldVenue, tblAthlete.fldYear{} FROM tblAthlete JOIN tblSport ON tblAthlete.fldEvent = tblSport.pmkName {};'.format(''.join([', ' + field for field in fields]),
                    ['', ' WHERE ' + ' AND '.join(conditions)][conditions != []])

            elif commandDict['table'].lower() == 'sport':
                # Execute SELECT for sport records
                del (commandDict['table'])

                fields = set()
                conditions = set()

                for _filter in commandDict:
                    # Add _filters only from the other table - ones from this table are SELECTed by default
                    if _filter not in VALID_SPORT_FILTERS:
                        fields.add(ALL_VALID_FILTERS[_filter])
                    
                    # Put quotes around vaule in SQL query for string fields
                    if _filter.lower() in ['fullname', 'sex', 'team', 'countrycode', 'venue', 'event', 'name', 'season', 'type']:
                        conditions.add(f'lower({ALL_VALID_FILTERS[_filter]})="{commandDict[_filter]}"')
                    else:
                        conditions.add(f'{ALL_VALID_FILTERS[_filter]}="{commandDict[_filter]}"')

                # for _filter in VALID_SPORT_FILTERS:
                #     print(f'_filter: {VALID_SPORT_FILTERS[_filter]}')
                #     if VALID_SPORT_FILTERS[_filter] not in fields:
                #         fields.add(VALID_SPORT_FILTERS[_filter])

                # TODO - not sure if this should be INNER JOIN or OUTER JOIN
                sqlQuery = 'SELECT tblSport.pmkName, tblSport.fldType, tblSport.fldSeason{} FROM tblSport LEFT JOIN tblAthlete ON tblSport.pmkName = tblAthlete.fldEvent{};'.format(''.join([', ' + field for field in fields]),
                    ['', ' WHERE ' + ' AND '.join(conditions)][conditions != []])

            
            return list(dbCursor.execute(sqlQuery))
    else:
        print('Please enter "load data" to load the tables for the database!')

        return None # Happens implicitly anyway


def loadData():
    if dbConnection is None:
        connect()
    if dbExists:
        print('Overwriting data!')

    loadCSV(CSV_FILENAME_ATHLETES, 'tblAthlete')
    loadCSV(CSV_FILENAME_SPORTS, 'tblSport')


# This will load in the data with specified csv file name
def loadCSV(csvFileName, tableName):
    # Read the data in the csvFile and put it into a table with the given col names
    read_data = pd.read_csv(csvFileName)

    # If the data base existed before then we should override it
    if dbExists:
        read_data.to_sql(tableName, dbConnection, if_exists='replace')
    else:
        read_data.to_sql(tableName, dbConnection)