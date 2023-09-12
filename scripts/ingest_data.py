import pandas as pd
import sys

sys.path.append('..')

from lib.db_conn import copy_df_to_sql
from lib.nba_helper import NbaHelper

NBA = NbaHelper()
TEAM_STATS_TBL = 'team_stats'
PLAYER_STATS_TBL = 'player_stats'
PLAYER_CAREER_STATS_TBL = 'player_career_stats'
SCHEMA = 'raw'

def ingest_team_games(season_id: str):
    '''
    PURPOSE: ingest all team game stats for a given season
    '''
    
    teams = NBA.get_teams()
    team_dfs = []
    for team in teams:
        team_stats_df = NBA.get_team_game_stats(
            team_id = team,
            season_id = season_id
        )
        team_dfs.append(team_stats_df)
    
    len_teams = len(team_dfs)
    full_df = pd.concat(team_dfs)
    len_records = len(full_df)
    copy_df_to_sql(
        df = full_df,
        table = TEAM_STATS_TBL,
        schema = SCHEMA
    )
    print(f'DONE ingesting for season: {season_id}, teams: {len_teams}, rows: {len_records}')

def ingest_player_games(season_id: str):
    '''
    PURPOSE: ingest all player game stats for a given season
    '''

    teams = NBA.get_teams()
    team_dfs = []
    for team in teams:
        team_stats_df = NBA.get_player_game_stats_by_team(
            team_id = team,
            season_id = season_id
        )
        team_dfs.append(team_stats_df)
    
    len_teams = len(team_dfs)
    full_df = pd.concat(team_dfs)
    len_records = len(full_df)
    copy_df_to_sql(
        df = full_df,
        table = PLAYER_STATS_TBL,
        schema = SCHEMA
    )
    print(f'DONE ingesting for season: {season_id}, teams: {len_teams}, rows: {len_records}')

def ingest_player_stats():
    '''
    PURPOSE: ingest all player career stats
    '''

    # players = NBA.get_players()
    players = NBA.get_active_players()
    player_dfs = []
    for player in players:
        player_stats_df = NBA.get_player_stats(
            player_id = player['id']
        )
        player_dfs.append(player_stats_df)
    
    len_players = len(player_dfs)
    full_df = pd.concat(player_dfs)
    len_records = len(full_df)
    copy_df_to_sql(
        df = full_df,
        table = PLAYER_CAREER_STATS_TBL,
        schema = SCHEMA
    )
    print(f'DONE ingesting for players: {len_players}, rows: {len_records}')

if __name__ == '__main__':
    season_id = '2015-16'
    # ingest_team_games(season_id)
    # ingest_player_games(season_id)
    ingest_player_stats()

