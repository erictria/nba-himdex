import pandas as pd

from lib.models import *
from lib.db_conn import read_sql_to_df

class StatsBuilder:
    '''
    A class for the functions needed to build engineered stats
    '''

    def __init__(self):
        pass
    
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
    
    def compute_engineered_features(self, season_year: str):
        sql_query = f"""
            WITH team_totals AS (
                SELECT DISTINCT
                    t.season_year
                    , t.team_id
                    , t.team_abbreviation
                    , t.team_name
                    , t.game_id
                    , t.wl
                    , t.fgm + t.ftm + t.ast AS game_buckets
                    , t.dreb + t.stl + t.blk AS game_stops
                    , t.min AS game_min
                FROM raw."team_stats" AS t
            )
            , player_totals AS (
                SELECT DISTINCT
                    p.season_year
                    , p.player_id
                    , p.player_name
                    , p.team_id
                    , p.game_id
                    , p.fgm + p.ftm + p.ast AS player_buckets
                    , p.dreb + p.stl + p.blk AS player_stops
                    , p.plus_minus
                    , p.min AS player_min
                FROM raw."player_stats" AS p
            )
            , engineered_stats AS (
                SELECT
                    p.season_year
                    , p.player_id
                    , p.player_name
                    , p.team_id
                    , t.team_abbreviation
                    , p.game_id
                    , p.plus_minus
                    , p.player_buckets
                    , p.player_stops
                    , p.player_buckets / t.game_buckets :: float AS bucket_contribution
                    , p.player_stops / t.game_stops :: float AS stop_contribution
                    , p.player_min / t.game_min :: float AS min_percentage
                FROM player_totals p
                JOIN team_totals t ON p.game_id = t.game_id AND p.team_id = t.team_id
            )
            , career_stats AS (
                SELECT
                    p.season_year
                    , p.player_id
                    , p.team_id
                    , AVG(player_min) AS average_min
                    , AVG(player_buckets) AS average_buckets
                    , AVG(player_stops) AS average_stops
                FROM player_totals p
                GROUP BY 1, 2, 3
            )
            , player_uplifts AS (
                SELECT
                    e.*
                    , e.bucket_contribution * 100.0 :: float as bucket_contribution_rate
                    , e.stop_contribution * 100.0 :: float as stop_contribution_rate
                    , c.average_min
                    , CASE
                        WHEN c.average_buckets = 0 THEN 0
                        ELSE ((e.player_buckets - c.average_buckets) / c.average_buckets)
                    END :: float AS bucket_uplift
                    , CASE
                        WHEN c.average_stops = 0 THEN 0
                        ELSE ((e.player_stops - c.average_stops) / c.average_stops)
                    END :: float AS stop_uplift
                FROM engineered_stats e
                JOIN career_stats c ON e.player_id = c.player_id AND e.team_id = c.team_id AND e.season_year = c.season_year
            )
            , uplift_aggs AS (
                SELECT
                    u.season_year
                    , u.team_id
                    , u.game_id
                    , SUM(u.bucket_uplift) AS total_bucket_uplift
                    , SUM(u.stop_uplift) AS total_stop_uplift
                    , COUNT(DISTINCT u.player_id) AS total_players
                FROM player_uplifts u
                GROUP BY 1, 2, 3
            )
            , engineered_raw AS (
                SELECT
                    p.*
                    , ((u.total_bucket_uplift - p.bucket_uplift) / (u.total_players - 1)) * p.min_percentage :: float AS tmt_bucket_uplift_cont_rate
                    , ((u.total_stop_uplift - p.stop_uplift) / (u.total_players - 1)) * p.min_percentage :: float AS tmt_stop_uplift_cont_rate
                FROM player_uplifts p
                JOIN uplift_aggs u ON p.team_id = u.team_id AND p.game_id = u.game_id AND p.season_year = u.season_year
            )

            SELECT
                season_year
                , team_id
                , team_abbreviation
                , player_id
                , player_name
                , AVG(average_min) AS average_min
                , SUM(plus_minus) AS total_plus_minus
                , AVG(bucket_contribution_rate) AS avg_bucket_contribution_rate
                , AVG(stop_contribution_rate) AS avg_stop_contribution_rate
                , AVG(tmt_bucket_uplift_cont_rate) AS avg_tmt_bucket_uplift_contribution_rate
                , AVG(tmt_stop_uplift_cont_rate) AS avg_tmt_stop_uplift_contribution_rate
            FROM engineered_raw
            WHERE season_year = '{season_year}'
            GROUP BY 1, 2, 3, 4, 5
            ORDER BY 1, 2, 3, 4, 5
        """

        results_df = read_sql_to_df(sql_query)
        return results_df
    
    def compute_himdex_scores(self, season_year: str):
        sql_query = f"""
            with percentiles as (
                select
                    nh.season_year
                    , nh.team_id
                    , nh.team_abbreviation
                    , nh.player_id
                    , nh.player_name
                    , ntile(100) over (partition by nh.season_year order by nh.total_plus_minus asc) as plus_minus_percentile
                    , ntile(100) over (partition by nh.season_year order by nh.avg_bucket_contribution_rate asc) as avg_bucket_contribution_rate_percentile
                    , ntile(100) over (partition by nh.season_year order by nh.avg_stop_contribution_rate asc) as avg_stop_contribution_rate_percentile
                    , ntile(100) over (partition by nh.season_year order by nh.avg_tmt_bucket_uplift_contribution_rate asc) as avg_tmt_bucket_uplift_contribution_rate_percentile
                    , ntile(100) over (partition by nh.season_year order by nh.avg_tmt_stop_uplift_contribution_rate asc) as avg_tmt_stop_uplift_contribution_rate_percentile
                from stats.nba_himdex nh
            )
            , himdex_scores as (
                select 
                    p.*
                    , 0.3 * p.plus_minus_percentile +
                        0.3 * p.avg_bucket_contribution_rate_percentile +
                        0.3 * p.avg_stop_contribution_rate_percentile +
                        0.05 * p.avg_tmt_bucket_uplift_contribution_rate_percentile +
                        0.05 * p.avg_tmt_stop_uplift_contribution_rate_percentile as himdex_score
                from percentiles p
            )

            select *
            from himdex_scores
            where season_year = '{season_year}'
        """

        results_df = read_sql_to_df(sql_query)
        return results_df