import json
import sys

import sys
sys.path.insert(0, '..')

from services.gbq_functions import (
    get_all_seasons,
    get_players_by_season,
    get_players_by_season_and_team
)

def generate_season_players():
    seasons = get_all_seasons()
    season_players = {}
    for season in seasons:
        players = get_players_by_season_and_team(season_year = season, order_by = 'player_name')
        season_players[season] = players
    
    with open('season_players_team.json', 'w') as fp:
        json.dump(season_players, fp)

if __name__ == '__main__':
    generate_season_players()

