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


command = input('Enter your command:\n>>> ')

ALL_VALID_FILTERS = []

def parseCommand(command):
    command = command.strip()
    
    for token in command.split():
