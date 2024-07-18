import pandas as pd
import sys
import time

sys.path.append('..')

from lib.db_conn import copy_df_to_sql
from lib.stats_builder import StatsBuilder

STATS = StatsBuilder()
SCORES_TABLE = 'nba_himdex_scores'
SCHEMA = 'stats'

def ingest_season_him_scores(season_id: str):
    '''
    PURPOSE: generate HIMdex scores per season
    '''

    himdex_scores = STATS.compute_himdex_scores(season_year = season_id)

    himdex_scores['version'] = 1
    himdex_scores['ingestion_timestamp'] = int(time.time())

    len_records = len(himdex_scores)

    copy_df_to_sql(
        df = himdex_scores,
        table = SCORES_TABLE,
        schema = SCHEMA
    )
    print(f'DONE ingesting HIM scores for season: {season_id}, rows: {len_records}')

if __name__ == '__main__':
    seasons = [
        '2008-09',
        '2009-10',
        '2010-11',
        '2011-12',
        '2012-13',
        '2013-14',
        '2014-15',
        '2015-16',
        '2016-17',
        '2017-18',
        '2018-19',
        '2019-20',
        '2020-21',
        '2021-22',
        '2022-23',
        '2023-24',
    ]
    for season_id in seasons:
        print(f'STARTING with {season_id}...')
        ingest_season_him_scores(season_id)
        print(f'DONE with {season_id}!')


