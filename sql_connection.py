import sqlite3
import pandas as pd
from pandas import DataFrame

def main():
    conn = sqlite3.connect('TestDB.db')
    c = conn.cursor()

    read_sport_data = pd.read_csv(r'OlympicSportData.csv')
    read_sport_data.to_sql('SPORTS', conn, if_exists='append',
                           index=False)  # Insert the values from the csv file into the table 'SPORTS'

    read_olympic_data = pd.read_csv(r'OlympicDataSet.csv')
    read_olympic_data.to_sql('ATHELETES', conn, if_exists='append', index=False)

    # These print out our two tables as proof
    df = DataFrame(c.execute('''SELECT * from ATHELETES'''))
    print(df)

    df2 = DataFrame(c.execute('''SELECT * FROM SPORTS'''))
    print(df2)

# This will open the database called TESTDB.db for now
# Uses pandas to read in the csv data and place it into a sqlite3 table
# you can test this by changing ATHELETES to SPORTS on like 16 to see if the data that is read in is correct.
# Might need to test around with it a little more the SQL snytax started to confuse me just a little.

# This is what I reference: https://datatofish.com/create-database-python-using-sqlite3/#:~:text=Import%20the%20CSV%20files%20using,file%20using%20the%20to_csv%20command


if __name__ == '__main__':
    main()
