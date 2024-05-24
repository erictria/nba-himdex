from flask import(
    Blueprint,
    request,
    jsonify
)

from services.gbq_functions import (
    get_all_seasons,
    get_players_by_season,
    get_himdex_cluster_by_player_season,
    get_himdex_player
)
from services.nba_functions import get_pictures

himdex_blueprint = Blueprint('himdex_blueprint', __name__)

@himdex_blueprint.route('/api/get_seasons', methods = ['POST'])
def get_seasons():
    seasons = get_all_seasons()
    response = {
        'seasons': seasons
    }

    return jsonify(response), 200

@himdex_blueprint.route('/api/get_players', methods = ['POST'])
def get_players():
    body = request.get_json()

    season_year = body['season_year']
    players = get_players_by_season(season_year = season_year, order_by = 'player_name')

    response = {
        'season_year': season_year,
        'players': players
    }

    return jsonify(response), 200

@himdex_blueprint.route('/api/get_himdex_cluster', methods = ['POST'])
def get_himdex_cluster():
    body = request.get_json()

    season_year = body['season_year']
    player_id = body['player_id']
    # team_id = body['team_id']
    him_players = get_himdex_cluster_by_player_season(
        player_id = player_id,
        season_year = season_year
    )
    him_players = list(map(lambda x: get_pictures(x), him_players))

    # Add sort order for UI table
    for idx, player in enumerate(him_players):
        player['sort_order'] = idx

    response = {
        'season_year': season_year,
        'player_id': player_id,
        # 'team_id': team_id,
        'him_players': him_players
    }

    return jsonify(response), 200

@himdex_blueprint.route('/api/get_player', methods = ['GET'])
def get_player():
    body = request.get_json()

    season_year = body['season_year']
    player_id = body['player_id']
    team_id = body['team_id']
    him_player = get_himdex_player(
        player_id = player_id,
        season_year = season_year,
        team_id = team_id
    )
    him_player = get_pictures(him_player)

    response = {
        'season_year': season_year,
        'player_id': player_id,
        'team_id': team_id,
        'him_player': him_player
    }

    return jsonify(response), 200
