from flask import render_template, request
from aram.models import Champion, db
from aram import app

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/<champion>")
def champion(champion):
    # Need to grab champion name from database rather than url
    return render_template('champ.html', champ_name = champion.capitalize())



import os
import json, requests

RIOT_API_KEY = os.environ.get("RIOT_API_KEY")

# Initialize champions into database
if db.session.query(Champion).first() == None:
    champ_url = "https://ddragon.leagueoflegends.com/cdn/8.15.1/data/en_US/champion.json"
    champions = (requests.get(champ_url)).json()
    # print(type(champions['data']))
    # print(champions.items())
    # print(champions['data'])

    for champion in champions['data'].items():
        # print(type(champion)) # tuple
        # print(champion[1]) # dictionary containing the champion info
        print(champion[1]['id'], champion[1]['key'], champion[1]['name'])
        champ = Champion(champion[1]['name'], champion[1]['key'])
        db.session.add(champ)

    db.session.commit()



games_url = "https://na1.api.riotgames.com/lol/spectator/v3/featured-games?api_key=" + RIOT_API_KEY # returns 5 games
data = (requests.get(games_url)).json()
# for each game returned
# check if the game is an ARAM
# if it is an aram, look up the match to see which team won (teamID 100 blue team, team id 200 red team)
# lookup the champion on the
# for game in data['gameList']:
#     if game['gameMode'] == 'ARAM':
#         print(1)
