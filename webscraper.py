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
    def __init__(self, number, name, pos, exp, height, college, age,
                 gp, mpg, fgm, fga, fgp, tpm, tpa, tpp, ftm, fta,
                 ftp, rpg, apg, spg, bpg, topg, pfpg, ppg, url = None):
        self.number = number
        self.name = name
        self.pos = pos
        self.exp = exp
        self.height = height
        self.college = college
        self.age = age
        self.gp = gp
        self.mpg = mpg
        self.fgm = fgm
        self.fga = fga
        self.fgp = fgp
        self.tpm = tpm
        self.tpa = tpa
        self.tpp = tpp
        self.ftm = ftm
        self.fta = fta
        self.ftp = ftp
        self.rpg = rpg
        self.apg = apg
        self.spg = spg
        self.bpg = bpg
        self.topg = topg
        self.pfpg = pfpg
        self.ppg = ppg
        self.url = url

    def __str__(self):
        s = self.name + ", " + self.pos
        return s

class Team():
    # def __init__(self, players, fgm, fga, fgp, tpm, tpa, tpp, ftm, fta, ftp,
    #              rpg, apg, spg, bpg, topg, pfpg, ppg):
    def __init__(self, players):
        self.players = players
        # self.fgm = fgm
        # self.fga = fga
        # self.fgp = fgp
        # self.tpm = tpm
        # self.tpa = tpa
        # self.tpp = tpp
        # self.ftm = ftm
        # self.fta = fta
        # self.ftp = ftp
        # self.rpg = rpg
        # self.apg = apg
        # self.spg = spg
        # self.bpg = bpg
        # self.topg = topg
        # self.pfpg = pfpg
        # self.ppg = ppg

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

def convert_string_to_float(string_to_convert):
    if string_to_convert == "":
        return 0
    else:
        return float(string_to_convert)

def get_player_info_from_row(rows):
    players = []
    base_url = "https://www.basketball-reference.com/"
    for row in rows:
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

        site_text = make_request_using_cache(base_url+url)
        site_soup = BeautifulSoup(site_text, 'html.parser')

        playerrow = None
        try:
            stats_table = site_soup.find('table', id='per_game_clone')
            playerrow = stats_table.find('tr', id="per_game.2018.clone")
        except:
            stats_table = site_soup.find('table', id='per_game')
            playerrow = stats_table.find('tr', id="per_game.2018")

        if playerrow is not None:
            s = playerrow.find_all('td')

            age = int(s[0].text)
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
            age = 0
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

        p = Player(number, name, pos, exp, height, college, age,
                   gp, mpg, fgm, fga, fgp, tpm, tpa, tpp, ftm, fta,
                   ftp, rpg, apg, spg, bpg, topg, pfpg, ppg, base_url + url)
        players.append(p)
    return players


def make_team_from_scraping(team_abbr):
    start_url = "https://www.basketball-reference.com/teams/"
    end_url = "/2018.html"
    url = start_url + team_abbr + end_url

    page_text = make_request_using_cache(url)
    page_soup = BeautifulSoup(page_text, 'html.parser')

    table_div = page_soup.find('div', id = "div_roster")
    table_rows = table_div.find('tbody').find_all('tr')
    players = get_player_info_from_row(table_rows)

    #team_div = page_soup.find('div', class_ = 'table_outer_container mobile_table')
    # per_game_row = team_div.find('tbody').find_all('tr')[1]
    # s = per_game_row.find_all('td')
    # fgm = float(s[2].text)
    # fga = float(s[3].text)
    # fgp = float(s[4].text)
    # tpm = float(s[5].text)
    # tpa = float(s[6].text)
    # tpp = float(s[7].text)
    # ftm = float(s[11].text)
    # fta = float(s[12].text)
    # ftp = float(s[13].text)
    # rpg = float(s[16].text)
    # apg = float(s[17].text)
    # spg = float(s[18].text)
    # bpg = float(s[19].text)
    # topg = float(s[20].text)
    # pfpg = float(s[21].text)
    # ppg = float(s[22].text)

    # team = Team(players, fgm, fga, fgp, tpm, tpa, tpp, ftm, fta, ftp,
    #             rpg, apg, spg, bpg, topg, pfpg, ppg)

    team = Team(players)
    return team


def pull_article_data(player_name):
    


if __name__ == "__main__":
    team1 = make_team_from_scraping("OKC")
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
