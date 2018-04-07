import get_player_data
import get_news_data
import os.path
import sqlite3 as sqlite

def init_db(db_name):
    conn = sqlite.connect(db_name)
    cur = conn.cursor()

    statement = '''
        DROP TABLE IF EXISTS 'Players'
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Seasons'
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Articles'
    '''
    cur.execute(statement)
    conn.commit()

    table_statement = '''
        CREATE TABLE 'Players' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'PlayerName' TEXT NOT NULL,
            'Position' TEXT NOT NULL,
            'CurrentTeam' TEXT NOT NULL,
            'Height' TEXT NOT NULL,
            'Experience' INTEGER,
            'College' TEXT
        );
    '''
    cur.execute(table_statement)

    table_statement = '''
        CREATE TABLE 'Seasons' (
            'PlayerId' INTEGER NOT NULL,
            'Season' TEXT NOT NULL,
            'Age' INTEGER NOT NULL,
            'Team' TEXT NOT NULL,
            'GP' INTEGER NOT NULL,
            'MPG' REAL NOT NULL,
            'FG' REAL NOT NULL,
            'FGA' REAL NOT NULL,
            'FG%' REAL NOT NULL,
            '3PM' REAL NOT NULL,
            '3PA' REAL NOT NULL,
            '3P%' REAL NOT NULL,
            'FT' REAL NOT NULL,
            'FTA' REAL NOT NULL,
            'FT%' REAL NOT NULL,
            'TRB' REAL NOT NULL,
            'AST' REAL NOT NULL,
            'STL' REAL NOT NULL,
            'BLK' REAL NOT NULL,
            'TOV' REAL NOT NULL,
            'PF' REAL NOT NULL,
            'PTS' REAL NOT NULL,
            FOREIGN KEY ('PlayerId') REFERENCES 'Players'('Id')
        );
    '''
    cur.execute(table_statement)

    table_statement = '''
        CREATE TABLE 'Articles' (
            'PlayerId' INTEGER NOT NULL,
            'Title' TEXT NOT NULL,
            'Description' TEXT NOT NULL,
            FOREIGN KEY ('PlayerId') REFERENCES 'Players'('Id')
        );
    '''
    cur.execute(table_statement)

    conn.commit()
    conn.close()

if __name__== "__main__":
    DB_NAME = 'test.sqlite'
    if os.path.exists(DB_NAME):
        dropq = input("Database already exists. Drop tables? yes/no \n")
        while dropq != 'yes' and dropq != 'no':
            dropq = input("Please enter yes or no: ")

        if dropq == 'yes':
            init_db(DB_NAME)

    team = input("Enter team abbreviation: ")
    get_player_data.insert_into_tables(team, DB_NAME)
