import os.path
import secrets
from bs4 import BeautifulSoup
import cache_data
import sqlite3 as sqlite
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from bokeh.plotting import figure

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

feature_names = {
    "Games Played": "GP",
    "Assists Per Game": "AST",
    "Rebounds Per Game": "TRB",
    "Steals Per Game": "STL",
    "Blocks Per Game": "BLK",
    "Turnovers Per Game": "TOV",
    "Points Per Game" : "PTS"
}

players = {}
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
news_url = 'https://newsapi.org/v2/everything?'

class Player():
    def __init__(self, name):
        global news_url
        global DB_NAME
        self.name = name

        #Pulling news data from Web API
        params = {'q' : self.name, 'language' : 'en',
                  'sortBy' : 'popularity', 'apiKey' : consumer_key}
        searched_news = cache_data.make_request_using_cache(news_url, CACHE_DICTION1,
                                                            CACHE_FNAME1, params)
        self.articles = searched_news['articles']

        #Pulling stats and team from database

        conn = sqlite.connect(DB_NAME)
        cur = conn.cursor()
        statement = '''
            SELECT Id, CurrentTeam FROM 'Players'
            WHERE PlayerName = ?
        '''
        cur.execute(statement, (self.name, ))
        fetched = cur.fetchone()
        id = fetched[0]
        # Assigning current team from database
        self.team = fetched[1]

        # Settings up stats in pandas dataframe
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
        self.df = df

    def get_word_plot(self):
        global stop_words
        words = []
        for a in self.articles:
            words = words + nltk.word_tokenize(a['title']) + \
                    nltk.word_tokenize(a['description'])
        words = [word for word in words if len(word) > 2]
        words = [word for word in words if not word.isnumeric()]
        words = [word.lower() for word in words]
        words = [word for word in words if word not in stop_words]
        counts = nltk.FreqDist(words)
        counts_series = pd.Series(counts)
        small_series = counts_series.sort_values(ascending = False).head()
        indices = list(small_series.index)
        p = figure(x_range=indices, plot_width = 600, plot_height=600,
                   title = "Most Frequent Words in News")
        p.vbar(x=indices, top=list(small_series.values), width=0.9)
        return p

    def get_stats_plot(self, current_feature_name):
        feature_abbr = feature_names[current_feature_name]
        indices = list(self.df.index)
        values = list(self.df[feature_abbr])
        i = 0
        while i  < len(indices) - 1:
            if indices[i] == indices[i+1]:
                values.pop(i)
                indices.pop(i)
                continue
            i = i + 1

        p = figure(plot_width=800, plot_height=300, x_range=indices,
                   title =  current_feature_name + " Over time")
        p.line(x=indices, y=values)
        return p

def get_player_stats(name, current_feature_name):
    global players
    if name not in players.keys():
        players[name] = Player(name)
    return [players[name].df, players[name].get_stats_plot(current_feature_name), players[name].team]

def get_top_news(name):
    global players
    if name not in players.keys():
        players[name] = Player(name)
    return [players[name].articles, players[name].get_word_plot()]

def convert_string_to_float(string_to_convert):
    if string_to_convert == "":
        return 0
    else:
        return float(string_to_convert)

def init_db():
    conn = sqlite.connect(DB_NAME)
    cur = conn.cursor()

    statement = '''
        DROP TABLE IF EXISTS 'Players'
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Seasons'
    '''
    cur.execute(statement)

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

    conn.commit()
    conn.close()

def insert_player_data(team_abbr):
    global DB_NAME
    base_url = "https://www.basketball-reference.com/"
    end_url = "/2018.html"
    url = base_url + "teams/" + team_abbr + end_url

    page_text = cache_data.make_request_using_cache(url, CACHE_DICTION2,
                CACHE_FNAME2)
    page_soup = BeautifulSoup(page_text, 'html.parser')

    table_div = page_soup.find('div', id = "div_roster")
    table_rows = table_div.find('tbody').find_all('tr')

    conn = sqlite.connect(DB_NAME)
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
    roster['PlayerName'] = roster['PlayerName'].apply(lambda x: "<a href='/player/" \
                       + ".".join(x.split()) + "' class = 'link'>" + x + "</a>")
    roster.set_index(['PlayerName'], inplace=True)
    roster.index.name=None
    return roster

def init(app):
    dropq = 'yes'
    if os.path.exists(DB_NAME):
        dropq = input("Database already exists. Drop tables? yes/no \n")
        while dropq != 'yes' and dropq != 'no':
            dropq = input("Please enter yes or no: ")

    if dropq == 'yes':
        init_db()
        for key in teams_dict.keys():
            print("Adding data for " + key)
            insert_player_data(key)
