from flask import(
    Blueprint,
    request,
    jsonify
)
import pandas as pd

from services.db_functions import (
    get_all_seasons,
    get_players_by_season,
    get_himdex_cluster_by_player,
    get_himdex_cluster_by_player_season
)

himdex_blueprint = Blueprint('himdex_blueprint', __name__)


@himdex_blueprint.route('/api/get_seasons', methods = ['GET'])
def get_seasons():
    seasons = get_all_seasons()
    response = {
        'seasons': seasons
    }

    return jsonify(response), 200

@himdex_blueprint.route('/api/get_players', methods = ['GET'])
def get_players():
    body = request.get_json()

    season_year = body['season_year']
    players = get_players_by_season(season_year = season_year)

    response = {
        'season_year': season_year,
        'players': players
    }

    return jsonify(response), 200

@himdex_blueprint.route('/api/get_himdex_cluster', methods = ['GET'])
def get_players():
    body = request.get_json()

    season_year = body['season_year']
    player_id = body['player_id']
    him_players = get_himdex_cluster_by_player_season(
        player_id = player_id,
        season_year = season_year
    )

    response = {
        'season_year': season_year,
        'player_id': player_id,
        'him_players': him_players
    }

    return jsonify(response), 200
