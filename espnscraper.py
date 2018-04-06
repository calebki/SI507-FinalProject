# Final Project
# Caleb Ki
import requests
import json
from bs4 import BeautifulSoup
import plotly.plotly as py

CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}

teams_dict = {
    "ATL" : "Atlanta Hawks",
    "BKN" :	"Brooklyn Nets",
    "BOS" :	"Boston Celtics",
    "CHA" :	"Charlotte Hornets",
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
    "PHX" :	"Phoenix Suns",
    "POR" :	"Portland Trail Blazers",
    "SAC" :	"Sacramento Kings",
    "SAS" :	"San Antonio Spurs",
    "TOR" :	"Toronto Raptors",
    "UTA" :	"Utah Jazz",
    "WAS" :	"Washington Wizards"
}

class Player():
    def __init__(self, number, name, pos, age, height,
                college, salary, url = None):
        self.number = number
        self.name = name
        self.pos = pos
        self.age = age
        self.height = height
        self.college = college
        self.url = url

        if self.url is not None:
            try:
                site_text = make_request_using_cache(url)
                site_soup = BeautifulSoup(site_text, 'html.parser')
                stats_table = site_soup.find_all('table', class_ = 'tablehead')
                row = stats_table[1].find('tr', class_ = 'oddrow')
                s = row.find_all('td')

                self.gp = int(s[1].text)
                self.mpg = float(s[2].text)
                self.fgm_fga = s[3].text
                self.fgp = float(s[4].text)
                self.tpm_tpa = s[5].text
                self.tpp = float(s[6].text)
                self.ftm_fta = s[7].text
                self.ftp = float(s[8].text)
                self.rpg = float(s[9].text)
                self.apg = float(s[10].text)
                self.bpg = float(s[11].text)
                self.spg = float(s[12].text)
                self.pfpg = float(s[13].text)
                self.topg = float(s[14].text)
                self.ppg = float(s[15].text)

            except:
                self.gp = 0
                self.mpg = 0
                self.fgm_fga = ""
                self.fgp = 0
                self.tpm_tpa = ""
                self.tpp = 0
                self.ftm_fta = ""
                self.ftp = 0
                self.rpg = 0
                self.apg = 0
                self.bpg = 0
                self.spg = 0
                self.pfpg = 0
                self.topg = 0
                self.ppg = 0


    def __str__(self):
        s = self.name + ", " + self.position
        return s

class Team():
    def __init__(self, players, ppg, rpg, apg, spg, bpg, tpg):
        self.players = players
        self.ppg = ppg
        self.rpg = rpg
        self.apg = apg
        self.spg = spg
        self.bpg = bpg
        self.tpg = tpg

    def add_player(self, player):
        self.players.append(player)

def params_unique_combination(url, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        if k != 'key':
            res.append("{}-{}".format(k, params[k]))
    return url + "_".join(res)

def make_request_using_cache(url, params=None):
    global header

    if params is not None:
        unique_ident = params_unique_combination(url,params)
    else:
        unique_ident = url

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        #print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        #print("Making a request for new data...")
        # Make the request and cache the new data
        if params is not None:
            resp = requests.get(url, params)
            CACHE_DICTION[unique_ident] = json.loads(resp.text)
        else:
            resp = requests.get(url)
            CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

def get_info_from_row(rows):
    players = []
    for row in rows:
        fields = row.find_all('td')
        number = int(fields[0].text)
        name = fields[1].text
        url = fields[1].find('a')['href']
        pos = fields[2]
        age = int(fields[3].text)
        height = fields[4].text
        college = fields[6].text
        try:
            salary = int(fields[7].text.strip('$').replace(',', ''))
        except:
            salary = None

        p = Player(number, name, pos, age, height, college, salary, url)
        players.append(p)
    return players


def get_players_for_team(team_abbr):
    start_url = "http://www.espn.com/nba/team/roster/_/name/"
    format_teamname = teams_dict[team_abbr].replace(" ", "-")
    url = start_url + team_abbr + "/" + format_teamname

    page_text = make_request_using_cache(url)
    page_soup = BeautifulSoup(page_text, 'html.parser')

    table = page_soup.find('div', class_ = "col-main", id = "my-players-table")
    table_oddrows = table.find_all('tr', class_ = "oddrow")
    table_evenrows = table.find_all('tr', class_ = "evenrow")
    odd_players = get_info_from_row(table_oddrows)
    even_players = get_info_from_row(table_evenrows)

    t = Team(odd_players + even_players)
    return t


if __name__ == "__main__":
    team1 = get_players_for_team("CLE")
    for player in team1.players:
        print(player)
    # help_string = '''
    #    list <teamabbr>
    #        available anytime
    #        lists all players on a team
    #        valid inputs: a three-letter team abbreviation (e.g., GSW, CLE)
    #    map
    #        available only if there is an active result set
    #        displays the current results on a map
    #    exit
    #        exits the program
    #    help
    #        lists available commands (these instructions)
    # '''
    # user_input = input("Enter command or ('help' for options): ")
