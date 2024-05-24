from glob import glob
from os import access
import pandas as pd
from datetime import datetime, timedelta
from google.oauth2 import service_account
import pandas_gbq

from services.constants import (
    GCP_PROJECT, 
    GCP_SCHEMA
)

# Change to ../ if running generate_static_files.py
SERVICE_ACCOUNT_KEY_PATH = './credentials/nba_himdex_gbq.json'
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

GSERVICE_ACCOUNT_CREDENTIALS = (
    service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_KEY_PATH,
        scopes=SCOPES
    )
)

def upload_data(in_df, table_name):
    table_path = '{0}.{1}'.format(GCP_SCHEMA, table_name)
    try:
        in_df.to_gbq(table_path, GCP_PROJECT, if_exists = 'append', credentials = GSERVICE_ACCOUNT_CREDENTIALS)
        status = 'success'
    except Exception as e:
        status = "error: {}".format(str(e))
        print(status)
    
    return status

def read_gbq_records(query: str) -> list:
    '''
    PURPOSE: queries data from the database

    INPUT:
    query - str SQL query

    OUTPUT:
    records - list of dict records
    '''
    
    result_df = pandas_gbq.read_gbq(query, project_id = GCP_PROJECT)
    records = result_df.to_dict('records')

    return records

def get_all_seasons() -> list:
    '''
    PURPOSE: gets the list of all seasons

    OUTPUT:
    seasons - list of str season_year formatted like 2015-16
    '''

    query = f'''
        SELECT DISTINCT
            season_year
        FROM {GCP_PROJECT}.{GCP_SCHEMA}.nba_himdex
        ORDER BY season_year
    '''

    records = read_gbq_records(query = query)
    seasons = list(map(lambda x: x['season_year'], records))

    return seasons

def get_players_by_season(season_year: str, order_by: str = 'player_id') -> list:
    '''
    PURPOSE: gets the list of all players from a given season

    INPUT:
    season_year - str season year

    OUTPUT:
    players - list of dict with player info
    '''

    query = f'''
        SELECT DISTINCT
            player_id
            , player_name
        FROM {GCP_PROJECT}.{GCP_SCHEMA}.nba_himdex
        WHERE season_year = '{season_year}'
        ORDER BY {order_by}
    '''

    players = read_gbq_records(query = query)

    return players

def get_himdex_cluster_by_player(player_id: int) -> list:
    '''
    PURPOSE: gets the players in the him cluster of a specified player

    INPUTS:
    player_id - int player id

    OUTPUTS:
    him_players - list of dict with player and himdex info
    '''

    query = f'''
        WITH him_group AS (
            SELECT DISTINCT
                season_year
                , himdex_cluster
            FROM {GCP_PROJECT}.{GCP_SCHEMA}.nba_himdex
            WHERE player_id = {player_id}
        )

        SELECT
            nh.season_year
            , nh.team_id
            , nh.team_abbreviation
            , nh.player_id
            , nh.player_name
            , nh.average_min
            , nh.total_plus_minus
            , nh.avg_bucket_contribution_rate
            , nh.avg_stop_contribution_rate
            , nh.avg_tmt_bucket_uplift_contribution_rate
            , nh.avg_tmt_stop_uplift_contribution_rate
        FROM {GCP_PROJECT}.{GCP_SCHEMA}.nba_himdex nh
        JOIN him_group hg ON nh.season_year = hg.season_year AND nh.himdex_cluster = hg.himdex_cluster
        ORDER BY 1, 2, 4
    '''

    him_players = read_gbq_records(query = query)

    return him_players

def get_himdex_cluster_by_player_season(player_id: int, season_year: str, team_id: int = None) -> list:
    '''
    PURPOSE: gets the players in the him cluster of a specified player

    INPUTS:
    player_id - int player id
    season_year - str season year
    team_id - int team id

    OUTPUTS:
    him_players - list of dict with player and himdex info
    '''
    
    query = f'''
        WITH him_group AS (
            SELECT DISTINCT
                season_year
                , himdex_cluster
            FROM {GCP_PROJECT}.{GCP_SCHEMA}.nba_himdex
            WHERE player_id = {player_id}
            AND season_year = '{season_year}'
        )

        SELECT
            nh.season_year
            , nh.team_id
            , nh.team_abbreviation
            , nh.player_id
            , nh.player_name
            , nh.average_min
            , nh.total_plus_minus
            , nh.avg_bucket_contribution_rate
            , nh.avg_stop_contribution_rate
            , nh.avg_tmt_bucket_uplift_contribution_rate
            , nh.avg_tmt_stop_uplift_contribution_rate
            , CASE 
                WHEN nh.player_id = {player_id} THEN 0
                ELSE 1
            END AS sort_order
        FROM {GCP_PROJECT}.{GCP_SCHEMA}.nba_himdex nh
        JOIN him_group hg ON nh.season_year = hg.season_year AND nh.himdex_cluster = hg.himdex_cluster
        ORDER BY 12, 5
    '''

    him_players = read_gbq_records(query = query)

    return him_players

def get_himdex_player(player_id: int, season_year: str, team_id: int) -> list:
    '''
    PURPOSE: gets the cluster stats of a specified player

    INPUTS:
    player_id - int player id
    season_year - str season year
    team_id - int team id

    OUTPUTS:
    him_player - dict with player and himdex info
    '''
    
    query = f'''
        SELECT
            nh.season_year
            , nh.team_id
            , nh.team_abbreviation
            , nh.player_id
            , nh.player_name
            , nh.average_min
            , nh.total_plus_minus
            , nh.avg_bucket_contribution_rate
            , nh.avg_stop_contribution_rate
            , nh.avg_tmt_bucket_uplift_contribution_rate
            , nh.avg_tmt_stop_uplift_contribution_rate
        FROM {GCP_PROJECT}.{GCP_SCHEMA}.nba_himdex nh
        WHERE nh.player_id = {player_id}
        AND nh.season_year = '{season_year}'
        AND nh.team_id = {team_id}
    '''

    him_players = read_gbq_records(query = query)
    him_player = him_players[0]

    return him_player