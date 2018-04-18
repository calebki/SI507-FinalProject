import os.path
from flask import Flask, render_template
import pandas as pd
import model

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('home.html')

@app.route('/team/<abbr>')
def show_team(abbr):
    abbr = abbr.upper()
    team_name = model.teams_dict[abbr]
    roster = model.get_roster(abbr)
    return render_template('roster.html', team_name = team_name,
        table=roster.to_html(classes=abbr))

@app.route('/player/<pname>')
def show_player(pname):
    names = pname.split(".")
    fullname = names[0]
    for i in range(1,len(names)):
        fullname = fullname + " " + names[i]
    player_stats = model.get_player_stats(fullname)
    return render_template("player.html", player_name = fullname,
        table=player_stats.to_html())

if __name__== "__main__":
    # dropq = 'yes'
    # if os.path.exists(DB_NAME):
    #     dropq = input("Database already exists. Drop tables? yes/no \n")
    #     while dropq != 'yes' and dropq != 'no':
    #         dropq = input("Please enter yes or no: ")
    #
    # if dropq == 'yes':
    #     model.init_db(DB_NAME)
    #     for key in gp.teams_dict.keys():
    #         print("Adding data for " + key)
    #         gp.insert_into_tables(key, DB_NAME)

    app.run(debug=True)
