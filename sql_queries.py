'''
Jackson and Jake will write function here that can be called in main (since
it was 'include'd in main.py)



'''

import sqlite3
import pandas as pd
from pandas import DataFrame

def connect(dName):
    conn = sqlite3.connect(dName + '.db') # ??????? should we attack the .db file extension or specify that they need to pass in a .db file
    c = conn.cursor()
    # Return the cursor so that 
    return c
    pass

def executeSQL(fieldsDict):
    pass

# This will load in the data with specified csv file name
def loadData(csvFile, tableName, conn):
  read_data = pd.read_csv(csvFile)
  read_data.to_sql(tableName, conn, if_exists='append',
                           index=False)  # Insert the values from the csv file into the table 'SPORTS'

def load():
    pass
