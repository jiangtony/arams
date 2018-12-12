from flask import render_template, request
from aram.models import Champion, Ids, db
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
import urllib
import time

RIOT_API_KEY = os.environ.get("RIOT_API_KEY")


### testing ####
# try: 
#     db.session.query(Champion).delete()
#     db.session.commit()
#     print("successfully cleared champ db")
# except:
#     print("couldn't clear champion db")
###########

# Initialize champions into database
if db.session.query(Champion).first() == None:
    champ_url = "https://ddragon.leagueoflegends.com/cdn/8.24.1/data/en_US/champion.json"
    champions = (requests.get(champ_url)).json()
    # print(type(champions['data']))
    # print(champions.items())
    # print(champions['data'])

    for champion in champions['data'].items():
        # print(type(champion)) # tuple
        # print(champion[1]) # dictionary containing the champion info
        # print(champion[1]['id'], champion[1]['key'], champion[1]['name'])
        champ = Champion(champion[1]['name'], champion[1]['key'])
        db.session.add(champ)

    db.session.commit()

# print(db.session.query(Champion).all())

featured_games_url = "https://na1.api.riotgames.com/lol/spectator/v3/featured-games?api_key=" + RIOT_API_KEY
featured_games = (requests.get(featured_games_url)).json()

# get a list of games from featured games
for game in featured_games['gameList']:
    # timestamp
    ts = int(time.time() * 1000)
    one_day_ago = int(ts - 8.64e+7)
    # print(one_day_ago)

    ###########################################
    ## for testing purposes. delete all match IDs in database
    try:
        db.session.query(Ids).delete()
        db.session.commit()
        print('successfully cleared match id db')
    except:
        print('error clearing match id db')
        pass
    ###########################################


    if game['gameMode'] == 'ARAM' and game['gameType'] == 'MATCHED_GAME':
        # print(game)
        # Look up each player in the game
        for player in game['participants']:
            # summoner names may have special characters
            summoner_name = urllib.parse.quote(player['summonerName'])
            print("Summoner Name: ", summoner_name)

            # Get the player's account ID
            summoner_lookup_url = "https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/" + summoner_name + "?api_key=" + RIOT_API_KEY
            summoner_info = (requests.get(summoner_lookup_url)).json()
            print(summoner_info['accountId'])

            # Use the account ID to look up their match history
            # get a list of their aram games from the last 24 hours 
            match_history_url = "https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/" + str(summoner_info['accountId']) + "?beginTime=" + str(one_day_ago) + "&queue=450&api_key=" + RIOT_API_KEY
            print(match_history_url)
            match_history = (requests.get(match_history_url)).json()

            print("Match History: ", match_history)

            # print(db.session.query(Ids).all())
            

            try:
                match_history['totalGames']
            except KeyError:
                print("error retrieving match history")
                continue

            # need to fix double counting matches due to resetting match id db
            for match in match_history['matches']:
                # Query the database for the game id and add it if it does not exist
                game_id_str = str(match['gameId'])
                game_id = Ids(game_id_str)
                if db.session.query(Ids).filter(Ids.match_id == game_id_str).first() is None:
                    db.session.add(game_id)
                    db.session.commit()
                    # Use the gameId to see who won/lost the game - record win/loss for all 10 participants
                    match_url = "https://na1.api.riotgames.com/lol/match/v3/matches/" + game_id_str + "?api_key=" + RIOT_API_KEY
                    
                    print("Match url: ", match_url)
                    match_data = requests.get(match_url)
                    if match_data.status_code == 200:
                        match_data = match_data.json()

                        for participants in match_data['participants']:
                            # print(participants['stats']['win'])
                            if participants['stats']['win'] == True:
                                print(participants['championId'], " wins")
                                # Increments the # of wins the the champ db
                                winning_champ = db.session.query(Champion).filter_by(champion_id=participants['championId']).first()
                                winning_champ.wins+=1
                            else:
                                print(participants['championId'], " loses")
                                # Increments the # of losses the the champ db
                                losing_champ = db.session.query(Champion).filter_by(champion_id=participants['championId']).first()
                                losing_champ.losses+=1

                            db.session.commit()

                break

            print(db.session.query(Ids).all())
            print(db.session.query(Champion).all())
            break

    else:
        continue

    break
