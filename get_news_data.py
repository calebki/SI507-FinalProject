import secrets
import cache_data
import sqlite3 as sqlite

consumer_key = secrets.api_key
CACHE_FNAME = 'news_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}

def get_news(search_term):
    url = 'https://newsapi.org/v2/everything?'
    params = {'q' : search_term, 'language' : 'en',
              'sortBy' : 'popularity', 'apiKey' : consumer_key}
    searched_news = cache_data.make_request_using_cache(url, CACHE_DICTION,
                                                        CACHE_FNAME, params)
    return searched_news['articles']

def init_db(db_name):

    #code to create a new database goes here

    try:
        conn = sqlite.connect(db_name)
        cur = conn.cursor()

        statement = '''
            SELECT name FROM sqlite_master WHERE type='table' AND name='Articles'
        '''
        cur.execute(statement)

        table_statement = '''
            CREATE TABLE 'Articles' (
                'Title' TEXT NOT NULL,
                'Description' TEXT NOT NULL
            );
        '''

        #code to test whether table already exists goes here
        #if exists, prompt to user: "Table exists. Delete?yes/no"
        #if user input is yes, drop table. Else, use move on and use existing table
        if cur.fetchone():
            dropq = input("Articles Table already exists. Drop table? yes/no: ")
            if dropq == 'yes':
                # Drop tables
                statement = '''
                    DROP TABLE IF EXISTS 'Tweets';
                '''
                cur.execute(statement)
                cur.execute(table_statement)
        else:
            #code to create table(if not exists) goes here
            cur.execute(table_statement)

        #close database connection
        conn.commit()
        conn.close()

    #handle exception if connection fails by printing the error
    except:
        print("Failed to create SQLite database.")

def insert_article_data(articles, DB_NAME):

    conn = sqlite.connect(DB_NAME)
    cur = conn.cursor()

    statement = 'INSERT INTO "Articles" '
    statement += 'VALUES (?, ?)'
    for article in articles:
        insertion = (article['title'], article['description'])
        cur.execute(statement, insertion)

    #Close database connection
    conn.commit()
    conn.close()

db_name = 'test.sqlite'
init_db(db_name)

testquery = 'Damian Lillard'
testarticles = get_news(testquery)

insert_article_data(testarticles, db_name)
