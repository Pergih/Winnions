from dagster import job, op
from winnions.ops.extract import *

@job
def run_extract_job():
    puuid = get_puuid()
    matches = get_20_most_recent_matches(puuid)
    matchId = get_first_match_id(matches)
    data = get_match_info(matchId)
    get_minions_lost(data)
