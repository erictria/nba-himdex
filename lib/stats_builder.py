import pandas as pd

from models import *

class StatsBuilder:
    '''
    A class for the functions needed to build engineered stats
    '''

    def __init__(self):
        return
    
    def compute_player_totals(player_game_log: PlayerGameLog) -> PlayerGameTotals:
        player_buckets = player_game_log['fgm'] + player_game_log['ftm'] + player_game_log['ast']
        player_stops = player_game_log['dreb'] + player_game_log['stl'] + player_game_log['blk']
        
        player_totals = PlayerGameTotals(
            player_id = player_game_log['player_id'],
            player_name = player_game_log['player_name'],
            team_id = player_game_log['team_id'],
            game_id = player_game_log['game_id'],
            buckets = player_buckets,
            stops = player_stops,
            plus_minus = player_game_log['plus_minus'],
            min = player_game_log['min']
        )

        return player_totals
    
    def compute_player_totals(team_game_log: TeamGameLog) -> TeamGameTotals:
        team_buckets = team_game_log['fgm'] + team_game_log['ftm'] + team_game_log['ast']
        team_stops = team_game_log['dreb'] + team_game_log['stl'] + team_game_log['blk']
        
        team_totals = TeamGameTotals(
            team_id = team_game_log['team_id'],
            game_id = team_game_log['game_id'],
            buckets = team_buckets,
            stops = team_stops,
            min = team_game_log['min']
        )

        return team_totals
    
    def compute_player_contribution(player_game_totals: PlayerGameTotals, team_game_totals: TeamGameTotals) -> PlayerGameMetrics:
        bucket_contribution = player_game_totals['buckets'] / team_game_totals['buckets']
        stop_contribution = player_game_totals['stops'] / team_game_totals['stops']
        minute_percentage = player_game_totals['min'] / team_game_totals['min']

        player_metrics = PlayerGameMetrics(
            player_id = player_game_totals['player_id'],
            player_name = player_game_totals['player_name'],
            team_id = player_game_totals['team_id'],
            game_id = player_game_totals['game_id'],
            plus_minus = player_game_totals['plus_minus'],
            minute_percentage = minute_percentage,
            bucket_contribution = bucket_contribution,
            stop_contribution = stop_contribution,
            bucket_contribution_rate = bucket_contribution * 100,
            stop_contribution_rate = stop_contribution * 100
        )

        return player_metrics