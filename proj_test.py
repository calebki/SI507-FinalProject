import unittest
from model import *

class TestDatabase(unittest.TestCase):
    def test_players_table(self):
        conn = sqlite.connect(DB_NAME)
        cur = conn.cursor()

        sql = '''
            SELECT PlayerName
            FROM Players
            WHERE Position="PF"
            Order By Experience DESC
            '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('LeBron James',), result_list)

        sql = '''
            SELECT PlayerName, College
            FROM Players
            WHERE PlayerName="Antonius Cleveland"
        '''
        results = cur.execute(sql)
        result_list = results.fetchone()
        #print(result_list)
        self.assertEqual(result_list[1], "Southeast Missouri State University")

        sql = '''
            SELECT DISTINCT CurrentTeam
            FROM Players
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 30)

        conn.close()

    def test_seasons_table(self):
        conn = sqlite.connect(DB_NAME)
        cur = conn.cursor()

        sql = '''
            SELECT Season
            FROM Seasons
            ORDER BY Season DESC
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual('2017-18', result_list[0][0])

        sql = '''
            SELECT MIN(PTS)
            FROM Seasons
        '''
        results = cur.execute(sql)
        result_list = results.fetchone()
        self.assertEqual(0.0, result_list[0])

        conn.close()

    def test_joins(self):
        conn = sqlite.connect(DB_NAME)
        cur = conn.cursor()

        sql = '''
            SELECT PlayerName
            FROM Seasons
                JOIN Players
                ON Players.Id=Seasons.PlayerId
            WHERE Players.Number=17
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Dennis Schroder',), result_list)
        conn.close()

class TestFunctions(unittest.TestCase):

    def test_player_class(self):
        player1 = Player("LeBron James")
        self.assertEqual("CLE", player1.team)
        self.assertEqual(19, player1.df['Age'][0])

        player2 = Player("Kevin Durant")
        try:
            plot1 = player2.get_word_plot()
            plot2 = player2.get_stats_plot("Rebounds Per Game")
        except:
            self.fail()

    def test_get_player_stats(self):
        try:
            retlist = get_player_stats("Klay Thompson", "Points Per Game")
            self.assertEqual(3, len(retlist))
            self.assertEqual("GSW", retlist[2])
        except:
            self.fail()

    def test_get_top_news(self):
        try:
            retlist = get_top_news("Draymond Green")
        except:
            self.fail()

unittest.main()
