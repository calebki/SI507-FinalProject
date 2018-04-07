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

    help_string = '''
       list <teamabbr>
            lists roster of an NBA team
            valid inputs: a three-letter team abbreviation
       stats <player_name>
            gives more options to see how to visualize player stats
       news <player_name>
            lists headlines of players
            gives more options to see some basic analysis of the headlines
       exit
            exits the program
       help
            lists available commands (these instructions)
    '''
    user_input = input("Enter command or ('help' for options): ")
    command_list = user_input.split()
    command = command_list[0]
    site_list = []
    nearby_list = []
    valid_commands = ['list', 'stats', 'news', 'help', 'exit']

    print("")

    while True:
        while command not in valid_commands:
            print("Not a valid command.")
            user_input = input("Enter valid command or ('help' for options): ")
            print("")
            command_list = user_input.split()
            command = command_list[0]

        if command == 'exit':
            break

        elif command == 'help':
            print(help_string)
            print("")

        elif command == 'list':
            if len(command_list) < 2:
                team_abbr = input("Forgot to enter team abbreviation. Enter now: ")
            else:
                team_abbr = command_list[1]
            while team_abbr.upper() not in get_player_data.teams_dict.keys():
                team_abbr = input("Please enter a valid state abbreviation: ")

            #flask app here

        elif command == 'nearby':
            if not site_list:
                print("There is no active results set of sites.")
            else:
                if len(command_list) < 2:
                    index = int(input("Forgot to enter result number. Enter now: "))
                else:
                    index = int(command_list[1])
                while index < 1 or index > len(site_list):
                    state_abbr = input("Please enter a valid state abbreviation: ")

                site = site_list[index-1]
                nearby_list = get_nearby_places_for_site(site)
                print("Places near " + site.name + " " + site.type)
                for i in range(len(nearby_list)):
                    print(str(i+1) + " " + nearby_list[i].__str__())
                print("")

        else:
            if not site_list and not nearby_list:
                print("No active results set. Please enter another command.")
            elif site_list and not nearby_list:
                plot_sites_for_state(state_abbr, active_list = site_list)
            else:
                map_type = input("Enter 1 for plot of National Sites or 2 for plot of places nearby national site: ")
                if map_type != 1 and map_type != 2:
                    while map_type != 1 or map_type != 2:
                        map_type = input("Invalid input. \nEnter 1 for plot of National Sites or 2 for plot of places nearby national site: ")
                elif map_type == 1:
                    plot_sites_for_state(site, active_list = site_list)
                else:
                    plot_nearby_for_site(site, active_list = nearby_list)
            print("")

        user_input = input("Enter command or ('help' for options): ")
        command_list = user_input.split()
        command = command_list[0]
        print("")
