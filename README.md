# SI507-FinalProject

## Data Sources
Data was pulled from 2 different sources.

### Basketball Reference (https://www.basketball-reference.com/)
Data was scraped from each team's roster page (e.g. https://www.basketball-reference.com/teams/IND/2018.html). Then the program would crawl one level deeper into the players to grab stats about the players. The data is already populated in the database, but there is an option when the program is run to refresh the data. No extra instructions are needed to obtain the data from this source. One simply needs to just run the program. 

WARNING: If you try to scrape from Basketball Reference too many times, they will block you. Make sure you do not refresh the data too often.

### News API (https://newsapi.org/)
News data about the players was gathered via the news api. In order for the program to run, a secrets.py file must be created with the api key inside.

secrets.py format:
api_key = "your api key inside here"

## Code Structure
The project is split into 2 main files: app.py and model.py. 

### model.py
This file handles all the data accessing, storage, and processing. The main functions are insert_player_data(team_Abbr), get_top_news(player_name), and get_player_stats(player_name, current_feature_name). The function insert_player_data(team_abbr) is the main scraping function and organizes and inserts the data into the database for quick access. The function get_top_news(player_name) retrieves the top articles involving a player and returns a word frequency plot as well as the top headlines and articles in the form of a list of dictionaries. The function get_player_stats(player_name, current_feature_name) returns the stats of a given player in a pandas dataframe and a plot of a selected feature.

### app.py
This file handles the flask application. The app.py calls the get_top_news(player_name) and get_player_stats(player_name, current_feature_name) from the model file in order to deploy various tables and figures to the flask application.

## Instructions
After installing all necessary modules from requirements.txt, run the app.py file (e.g., python app.py). Open your browser and go to http://127.0.0.1:5000/ to see the flask app.
