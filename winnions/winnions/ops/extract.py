from dagster import Out, Output, job, op
import logging

import requests
import pandas as pd
import os
from dotenv import load_dotenv
import numpy as np

load_dotenv(dotenv_path=".env")

API_KEY = os.getenv("RIOT_API_KEY")
logger = logging.getLogger('console_logger')

# if not API_KEY:
#     logger.error("❌ API key not loaded")
# else:
#     logger.log("✅ API key loaded")

region = "europe"

headers = {
        "X-Riot-Token": "RGAPI-712cf5e4-2ca4-441e-9403-18e4a3de1dc5"  # or hardcoded for testing
    }


@op(out=Out(str))
def get_puuid(gameName="Pergih", tagLine="AKL"):

    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    return data['puuid']


@op(out=Out(list))
def get_20_most_recent_matches(puuid):
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
    
    

@op(out=Out(str))
def get_first_match_id(matches: list[str]) -> str:
    return matches[0]
    
@op(out=Out(dict))
def get_match_info(matchId):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{matchId}"
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    # print(data)
    return data




@op(out=Out(dict))
def get_minions_lost(data: dict) -> dict:
    mydict = {100: 0, 200: 0}
    for player in data['info']['participants']:
        print(player['riotIdGameName'])
        print(player['totalMinionsKilled'])
        print(player['teamId'])
        mydict[player['teamId']] += player['totalMinionsKilled']
    
    total_minions = count_minions(player['timePlayed']) * 3  # 3 lanes
    
    for team in mydict:
        print(team)
        print(mydict[team] / (player['timePlayed'] // 60))
    
    for team in mydict:
        mydict[team] = total_minions - mydict[team]

    print(mydict)
    return mydict
    
@op(out=Out(int))
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

    return base_minions + siege_minions