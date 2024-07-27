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
    result_df = pandas_gbq.read_gbq(query, project_id = GCP_PROJECT, credentials = GSERVICE_ACCOUNT_CREDENTIALS)
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

def get_players_by_season_and_team(season_year: str, order_by: str = 'player_id') -> list:
    '''
    PURPOSE: gets the list of all players from a given season. 
             players on different teams in one season have multiple records.

    INPUT:
    season_year - str season year

    OUTPUT:
    players - list of dict with player info
    '''

    query = f'''
        WITH team_count AS (
            SELECT
                season_year
                , player_id
                , COUNT(DISTINCT team_id) AS teams
            FROM {GCP_PROJECT}.{GCP_SCHEMA}.nba_himdex
            GROUP BY 1, 2
        )
        SELECT DISTINCT
            CONCAT(nh.player_id, '-', nh.team_id) AS player_id
            , CASE
                WHEN tc.teams > 1 THEN Concat(nh.player_name, ', ', nh.team_abbreviation)
                ELSE nh.player_name
            END AS player_name
        FROM {GCP_PROJECT}.{GCP_SCHEMA}.nba_himdex nh
        JOIN team_count tc ON nh.season_year = tc.season_year and nh.player_id = tc.player_id
        WHERE nh.season_year = '{season_year}'
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

def get_himdex_cluster_by_player_season(player_id: int, season_year: str, team_id: int) -> list:
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
            AND team_id = {team_id}
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
            , nhs.himdex_score
            , CASE 
                WHEN nh.player_id = {player_id} THEN 0
                ELSE 1
            END AS sort_order
        FROM {GCP_PROJECT}.{GCP_SCHEMA}.nba_himdex nh
        JOIN him_group hg ON nh.season_year = hg.season_year AND nh.himdex_cluster = hg.himdex_cluster
        JOIN {GCP_PROJECT}.{GCP_SCHEMA}.nba_himdex_scores nhs 
            ON nh.player_id = nhs.player_id 
            AND nh.team_id = nhs.team_id 
            AND nh.season_year = nhs.season_year
        ORDER BY 13, 5
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

def get_himdex_rankings_by_season(season_year: str, limit: int = 50) -> list:
    query = f'''
        SELECT
            nhs.season_year
            , nhs.team_id
            , nh.team_abbreviation
            , nhs.player_id
            , nh.player_name
            , nhs.plus_minus_percentile
            , nhs.avg_bucket_contribution_rate_percentile
            , nhs.avg_stop_contribution_rate_percentile
            , nhs.avg_tmt_bucket_uplift_contribution_rate_percentile
            , nhs.avg_tmt_stop_uplift_contribution_rate_percentile
            , nhs.himdex_score
            , ROW_NUMBER () OVER (PARTITION BY nhs.season_year ORDER BY nhs.himdex_score DESC) AS himdex_ranking
        FROM {GCP_PROJECT}.{GCP_SCHEMA}.nba_himdex_scores nhs
        JOIN {GCP_PROJECT}.{GCP_SCHEMA}.nba_himdex nh
            ON nh.player_id = nhs.player_id 
            AND nh.team_id = nhs.team_id 
            AND nh.season_year = nhs.season_year
        WHERE nhs.season_year = '{season_year}'
        ORDER BY nhs.himdex_score DESC
        LIMIT {limit}
    '''

    him_rankings = read_gbq_records(query = query)

    return him_rankings