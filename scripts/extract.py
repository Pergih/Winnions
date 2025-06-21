import requests
import pandas as pd
import os
from dotenv import load_dotenv
import numpy as np

load_dotenv(dotenv_path=".env")

API_KEY = os.getenv("RIOT_API_KEY")

if not API_KEY:
    print("❌ API key not loaded")
else:
    print("✅ API key loaded")

# puuid = "g6Tg0NiwvlSTzK5ohu-RkqjwkSNuQ6HLGmuSiKRg_6CKnUNop0ROygQIW9w8IAG0qyS9DhCs2aWQDA"
region = "europe"

headers = {
        "X-Riot-Token": API_KEY
    }

def get_puuid(gameName, tagLine):
    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    return data['puuid']

def get_20_most_recent_matches(ouuid):
    # print(dict(os.environ))  # Temporarily — to debug

    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    
    params = {
        "start": 0,
        "count": 20
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raises HTTPError for bad responses
    
    data = response.json()
    print(data)
    return data
    
    
    
def get_match_info(matchId):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{matchId}"
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    # print(data)
    return data
    
def get_minions_lost(data):
    # blueteam == 100 redteam == 200
    mydict = {}
    mydict[100] = 0
    mydict[200] = 0
    for player in data['info']['participants']:
        print(player['riotIdGameName'])
        print(player['totalMinionsKilled'])
        print(player['teamId'])
        mydict[player['teamId']] = mydict[player['teamId']] + player['totalMinionsKilled']
        
    total_minions = count_minions(player['timePlayed']) * 3 # 3 lanes
    
    # print(total_minions)
    # print(mydict)

    for team in mydict:
        print(team)
        print(mydict[team]/(player['timePlayed'] // 60))
    
    for team in mydict:
        mydict[team] = total_minions - mydict[team]
        
    
    print(mydict)
    # print(type(data['info']['participants']))

def count_minions(time_played):
    # Subtract the initial delay
    if time_played < 65:
        return 0

    wave_count = (time_played - 65) // 30

    # Base minions: 3 melee + 3 caster per wave
    base_minions_per_wave = 6
    base_minions = wave_count * base_minions_per_wave

    # Count siege minions
    siege_minions = 0
    for wave in range(1, wave_count + 1):
        if wave >= 4:
            if wave < 15 * 2:  # First 15 minutes → every 3 waves
                if (wave - 4) % 3 == 0:
                    siege_minions += 1
            elif wave < 25 * 2:  # 15–25 minutes → every 2 waves
                if (wave - 4) % 2 == 0:
                    siege_minions += 1
            else:  # After 25 minutes → every wave
                siege_minions += 1

    total_minions = base_minions + siege_minions
    return total_minions

    
    
if __name__ == "__main__":
    puuid = get_puuid('BooGuga', 'LIFT')
    matches = get_20_most_recent_matches(puuid)
    data = get_match_info(matchId=matches[2])
    get_minions_lost(data)