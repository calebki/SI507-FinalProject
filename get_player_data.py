from bs4 import BeautifulSoup
import cache_data
import sqlite3 as sqlite

CACHE_FNAME = 'nba_cache.json'
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

def convert_string_to_float(string_to_convert):
    if string_to_convert == "":
        return 0
    else:
        return float(string_to_convert)


def insert_into_tables(team_abbr, db_name):
    base_url = "https://www.basketball-reference.com/"
    end_url = "/2018.html"
    url = base_url + "teams/" + team_abbr + end_url

    page_text = cache_data.make_request_using_cache(url, CACHE_DICTION,
                CACHE_FNAME)
    page_soup = BeautifulSoup(page_text, 'html.parser')

    table_div = page_soup.find('div', id = "div_roster")
    table_rows = table_div.find('tbody').find_all('tr')

    conn = sqlite.connect(db_name)
    cur = conn.cursor()

    statement1 = 'INSERT INTO "Players" '
    statement1 += 'VALUES (?, ?, ?, ?, ?, ?, ?)'

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

        insertion1 = (None, name, pos, team_abbr, height, exp, college)
        cur.execute(statement1, insertion1)

        site_text = cache_data.make_request_using_cache(base_url+url,
                    CACHE_DICTION, CACHE_FNAME)
        site_soup = BeautifulSoup(site_text, 'html.parser')

        content_div = site_soup.find('div', id = 'all_per_game')
        stats_table = content_div.find('table')
        # try:
        #     stats_table = content_div.find('table', id='per_game_clone')
        #     print("LOL")
        # except:
        #     stats_table = content_div.find('table', id='per_game')
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
