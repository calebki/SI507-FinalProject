import webscraper
import get_news_data
import os.path
import sqlite3 as sqlite

DB_NAME = 'test.sqlite'

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
            'CurrentTeam' TEXT NOT NULL
        );
    '''
    cur.execute(table_statement)

    table_statement = '''
        CREATE TABLE 'Seasons' (
            'PlayerId' INTEGER NOT NULL,
            'age' INTEGER NOT NULL,
            'gp' INTEGER NOT NULL,
            'mpg' REAL NOT NULL,
            'fgm' REAL NOT NULL,
            'fga' REAL NOT NULL,
            'fgp' REAL NOT NULL,
            'tpm' REAL NOT NULL,
            'tpa' REAL NOT NULL,
            'tpp' REAL NOT NULL,
            'ftm' REAL NOT NULL,
            'fta' REAL NOT NULL,
            'ftp' REAL NOT NULL,
            'rpg' REAL NOT NULL,
            'apg' REAL NOT NULL,
            'spg' REAL NOT NULL,
            'bpg' REAL NOT NULL,
            'topg' REAL NOT NULL,
            'pfpg' REAL NOT NULL,
            'ppg' REAL NOT NULL,
            'url' REAL NOT NULL
        );
    '''
    cur.execute(table_statement)

    table_statement = '''
        CREATE TABLE 'Articles' (
            'PlayerId' INTEGER NOT NULL,
            'Title' TEXT NOT NULL,
            'Description' TEXT NOT NULL
        );
    '''
    cur.execute(table_statement)

    conn.commit()
    conn.close()

if __name__== "__main__":
    if os.path.exists(DB_NAME):
        dropq = input("Database already exists. Drop tables? yes/no \n")
        while dropq != 'yes' and 'no':
            dropq = input("Please enter yes or no: ")

        if dropq == 'yes':
            init_db(DB_NAME)
