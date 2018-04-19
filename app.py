import os.path
from flask import Flask, render_template, request
import pandas as pd
import model
from bokeh.models import (HoverTool, FactorRange, Plot,
                          LinearAxis, Grid, Range1d)
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

app = Flask(__name__)

def handle_name(pname):
    names = pname.split(".")
    fullname = names[0]
    for i in range(1,len(names)):
        fullname = fullname + " " + names[i]
    return fullname

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

# @app.route('/team/<abbr>/stats')
# def team_chart(abbr):
#     abbr = abbr.upper()
#     team_name = model.teams_dict[abbr]
#     stat = request.args.get("feature_name")
#     if stat == None:
#         stat = "Age"
#
#     roster = model.get_roster(abbr)
#     plot = model.create_histogram(roster, stat)
#     script, div = components(plot)
#     return render_template('histogram.html', team_name = team_name,
#         stat = "Age", the_div = div, the_script = script)

@app.route('/player/<pname>')
def show_player(pname):
    fullname = handle_name(pname)
    if request.args.get("feature_name") == None:
        current_feature_name = "Points Per Game"
    else:
        current_feature_name = request.args.get("feature_name")

    retlist = model.get_player_stats(fullname, current_feature_name)
    player_stats = retlist[0]
    plot = retlist[1]

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(plot)
    html = render_template(
        'player.html',
        player_name=fullname,
        table=player_stats.to_html(),
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
        pname = pname,
        feature_names = model.feature_names.keys(),
        current_feature_name = current_feature_name
    )
    return encode_utf8(html)

@app.route('/player/<pname>/news')
def get_news(pname):
    fullname = handle_name(pname)
    retlist = model.get_top_news(fullname)
    news_list = retlist[0]
    plot = retlist[1]

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(plot)
    html = render_template(
        'news.html',
        player_name=fullname,
        news_list=news_list,
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
        pname = pname
    )
    return encode_utf8(html)


if __name__== "__main__":
    # dropq = 'yes'
    # if os.path.exists(DB_NAME):
    #     dropq = input("Database already exists. Drop tables? yes/no \n")
    #     while dropq != 'yes' and dropq != 'no':
    #         dropq = input("Please enter yes or no: ")
    #
    # if dropq == 'yes':
    #     model.init_db(DB_NAME)
    #     for key in model.teams_dict.keys():
    #         print("Adding data for " + key)
    #         model.insert_player_data(key, DB_NAME)

    app.run(debug=True)
