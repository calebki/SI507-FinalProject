import secrets
from bs4 import BeautifulSoup
import cache_data
import sqlite3 as sqlite
import pandas as pd

DB_NAME = 'data.sqlite'

consumer_key = secrets.api_key
CACHE_FNAME1 = 'news_cache.json'
try:
    cache_file = open(CACHE_FNAME1, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION1 = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION1 = {}

CACHE_FNAME2 = 'nba_cache.json'
try:
    cache_file = open(CACHE_FNAME2, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION2 = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION2 = {}

teams_dict = {
    "ATL" : "Atlanta Hawks",
    "BRK" :	"Brooklyn Nets",
    "BOS" :	"Boston Celtics",
    "CHO" :	"Charlotte Hornets",
    "CHI" :	"Chicago Bulls",
    "CLE" :	"Cleveland Cavaliers",
    "DAL" :	"Dallas Mavericks",
    "DEN" :	"Denver Nuggets",
    "DET" :	"Detroit Pistons",
    "GSW" :	"Golden State Warriors",
    "HOU" :	"Houston Rockets",
    "IND" :	"Indiana Pacers",
    "LAC" :	"LA Clippers",
    "LAL" :	"Los Angeles Lakers",
    "MEM" :	"Memphis Grizzlies",
    "MIA" :	"Miami Heat",
    "MIL" :	"Milwaukee Bucks",
    "MIN" :	"Minnesota Timberwolves",
    "NOP" :	"New Orleans Pelicans",
    "NYK" :	"New York Knicks",
    "OKC" :	"Oklahoma City Thunder",
    "ORL" :	"Orlando Magic",
    "PHI" :	"Philadelphia 76ers",
    "PHO" :	"Phoenix Suns",
    "POR" :	"Portland Trail Blazers",
    "SAC" :	"Sacramento Kings",
    "SAS" :	"San Antonio Spurs",
    "TOR" :	"Toronto Raptors",
    "UTA" :	"Utah Jazz",
    "WAS" :	"Washington Wizards"
}

def convert_string_to_float(string_to_convert):
    if string_to_convert == "":
        return 0
    else:
        return float(string_to_convert)

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
            'Number' INTEGER,
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

def insert_article_data(search_term, db_name):
    url = 'https://newsapi.org/v2/everything?'
    params = {'q' : search_term, 'language' : 'en',
              'sortBy' : 'popularity', 'apiKey' : consumer_key}
    searched_news = cache_data.make_request_using_cache(url, CACHE_DICTION1,
                                                        CACHE_FNAME1, params)
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

def insert_into_tables(team_abbr, db_name):
    base_url = "https://www.basketball-reference.com/"
    end_url = "/2018.html"
    url = base_url + "teams/" + team_abbr + end_url

    page_text = cache_data.make_request_using_cache(url, CACHE_DICTION2,
                CACHE_FNAME2)
    page_soup = BeautifulSoup(page_text, 'html.parser')

    table_div = page_soup.find('div', id = "div_roster")
    table_rows = table_div.find('tbody').find_all('tr')

    conn = sqlite.connect(db_name)
    cur = conn.cursor()

    statement1 = 'INSERT INTO "Players" '
    statement1 += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?)'

    for row in table_rows:
        number = int(row.find('th').text)
        fields = row.find_all('td')
        name = fields[0].find('a').text
        url = fields[0].find('a')['href']
        pos = fields[1].text
        try:
            exp = int(fields[6].text)
        except:
            exp = 0
        height = fields[2].text
        college = fields[7].text

        insertion1 = (None, number, name, pos, team_abbr, height, exp, college)
        cur.execute(statement1, insertion1)

        site_text = cache_data.make_request_using_cache(base_url+url,
                    CACHE_DICTION2, CACHE_FNAME2)
        site_soup = BeautifulSoup(site_text, 'html.parser')

        content_div = site_soup.find('div', id = 'all_per_game')

        if content_div is not None:
            stats_table = content_div.find('table')
            stats_table_rows = stats_table.find('tbody').find_all('tr')

            statement2 = '''
                SELECT Id FROM 'Players'
                    WHERE PlayerName = ?
            '''
            insertion2 = (name, )
            cur.execute(statement2, insertion2)
            unique_id = cur.fetchone()[0]

            statement3 = 'INSERT INTO "Seasons" '
            statement3 += (
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ' +
                '?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')

            for season in stats_table_rows:
                table_header = season.find('th')
                if table_header is not None:
                    year = table_header.text
                    s = season.find_all('td')
                    age = int(s[0].text)
                    team = s[1].text
                    gp = int(s[4].text)
                    mpg = convert_string_to_float(s[6].text)
                    fgm = convert_string_to_float(s[7].text)
                    fga = convert_string_to_float(s[8].text)
                    fgp = convert_string_to_float(s[9].text)
                    tpm = convert_string_to_float(s[10].text)
                    tpa = convert_string_to_float(s[11].text)
                    tpp = convert_string_to_float(s[12].text)
                    ftm = convert_string_to_float(s[17].text)
                    fta = convert_string_to_float(s[18].text)
                    ftp = convert_string_to_float(s[19].text)
                    rpg = convert_string_to_float(s[22].text)
                    apg = convert_string_to_float(s[23].text)
                    spg = convert_string_to_float(s[24].text)
                    bpg = convert_string_to_float(s[25].text)
                    topg = convert_string_to_float(s[26].text)
                    pfpg = convert_string_to_float(s[27].text)
                    ppg = convert_string_to_float(s[28].text)

                else:
                    s = season.find_all('td')
                    year = s[0].text
                    age = s[1].text
                    team = "Did not play"
                    gp = 0
                    mpg = 0
                    fgm = 0
                    fga = 0
                    fgp = 0
                    tpm = 0
                    tpa = 0
                    tpp = 0
                    fta = 0
                    ftp = 0
                    rpg = 0
                    apg = 0
                    spg = 0
                    bpg = 0
                    topg = 0
                    pfpg = 0
                    ppg = 0

                insertion3 = (unique_id, year, age, team, gp, mpg, fgm, fga, fgp, tpm,
                              tpa, tpp, ftm, fta, ftp, rpg, apg, spg, bpg, topg,
                              pfpg, ppg)
                cur.execute(statement3, insertion3)

    conn.commit()
    conn.close()

def get_roster(team_abbr):
    global DB_NAME
    conn = sqlite.connect(DB_NAME)
    cur = conn.cursor()

    statement = '''
        SELECT * FROM 'Players'
        WHERE CurrentTeam =
    '''
    statement += '"' + team_abbr + '"'
    roster = pd.read_sql_query(statement, conn)
    conn.close()
    roster.drop('Id', axis=1, inplace=True)
    roster.set_index(['PlayerName'], inplace=True)
    roster.index.name=None
    return roster

def get_player_stats(player_name):
    global DB_NAME
    conn = sqlite.connect(DB_NAME)
    cur = conn.cursor()

    statement = '''
        SELECT Id FROM 'Players'
        WHERE PlayerName = ?
    '''
    cur.execute(statement, (player_name, ))
    id = cur.fetchone()[0]

    statement = '''
        SELECT * FROM 'Seasons'
        WHERE PlayerId =
    '''
    statement += str(id)
    df = pd.read_sql_query(statement, conn)
    conn.close()
    df.set_index(['Season'], inplace=True)
    df.drop('PlayerId', axis=1, inplace=True)
    df.index.name=None
    return df
