import pandas as pd

from nba_api.stats.static import players
from nba_api.stats.static import teams
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import playergamelogs
from nba_api.stats.endpoints import teamgamelogs

class NbaHelper:
    '''
    A class that makes use of different functions from the NBA Stats API

    Source: https://github.com/swar/nba_api
    '''

    def __init__(self):
        return
    
    def get_players(self):
        '''
        PURPOSE: Retrieves a list of all NBA players

        OUTPUT:
        all_players - list of player data
        '''

        all_players = players.get_players()
        return all_players
    
    def get_active_players(self):
        '''
        PURPOSE: Retrieves a list of all active NBA players

        OUTPUT:
        all_active_players - list of active player data
        '''

        all_active_players = players.get_active_players()
        return all_active_players

    def get_player_stats(self, player_id: str):
        '''
        PURPOSE: Gets a player's career stats

        INPUT:
        player_id - str player id

        OUTPUT:
        final_stats - pandas dataframe of a player's stats
        '''

        player_stats = playercareerstats.PlayerCareerStats(player_id = player_id, per_mode36 = 'PerGame')
        player_stats_df = player_stats.get_data_frames()

        if len(player_stats_df) > 0:
            final_stats = player_stats_df[0]
        else:
            final_stats = pd.DataFrame()

        return final_stats
    
    def get_player_game_stats(self, player_id: str, season_id: str):
        '''
        PURPOSE: Gets a player's game log stats

        INPUT:
        player_id - str player id
        season_id - str season id formatted '2015-16'

        OUTPUT:
        final_player_games_stats - pandas dataframe of a player's game stats
        '''

        player_games = playergamelogs.PlayerGameLogs(
            player_id_nullable = player_id,
            season_nullable = season_id
        )
        player_games_df = player_games.get_data_frames()

        if len(player_games_df) > 0:
            final_player_games_stats = player_games_df[0]
        else:
            final_player_games_stats = pd.DataFrame()

        return final_player_games_stats
    
    def get_player_game_stats_by_team(self, team_id: str, season_id: str):
        '''
        PURPOSE: Gets a player's game log stats

        INPUT:
        team_id - str team id
        season_id - str season id formatted '2015-16'

        OUTPUT:
        final_player_games_stats - pandas dataframe of a player's game stats
        '''

        player_games = playergamelogs.PlayerGameLogs(
            team_id_nullable = team_id,
            season_nullable = season_id
        )
        player_games_df = player_games.get_data_frames()

        if len(player_games_df) > 0:
            final_player_games_stats = player_games_df[0]
        else:
            final_player_games_stats = pd.DataFrame()

        return final_player_games_stats

    def get_teams(self):
        '''
        PURPOSE: Retrieves a list of all NBA teams

        OUTPUT:
        all_teams - list of team data
        '''

        all_teams = teams.get_teams()
        return all_teams
    
    def get_team_game_stats(self, team_id: str, season_id: str):
        '''
        PURPOSE: Gets a team's game log stats

        INPUT:
        team_id - str team id
        season_id - str season id formatted '2015-16'

        OUTPUT:
        final_team_game_stats - pandas dataframe of a team's game stats
        '''

        team_games = teamgamelogs.TeamGameLogs(
            team_id_nullable = team_id,
            season_nullable = season_id
        )
        team_games_df = team_games.get_data_frames()
        
        if len(team_games_df) > 0:
            final_team_game_stats = team_games_df[0]
        else:
            final_team_game_stats = pd.DataFrame()

        return final_team_game_stats