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

def insert_article_data(search_term, db_name):
    url = 'https://newsapi.org/v2/everything?'
    params = {'q' : search_term, 'language' : 'en',
              'sortBy' : 'popularity', 'apiKey' : consumer_key}
    searched_news = cache_data.make_request_using_cache(url, CACHE_DICTION,
                                                        CACHE_FNAME, params)
    articles = searched_news['articles']
    conn = sqlite.connect(db_name)
    cur = conn.cursor()

    statement = 'INSERT INTO "Articles" '
    statement += 'VALUES (?, ?)'
    for article in articles:
        insertion = (article['title'], article['description'])
        cur.execute(statement, insertion)

    #Close database connection
    conn.commit()
    conn.close()
