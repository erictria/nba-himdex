import pandas as pd
import sys

sys.path.append('..')

from lib.clustering import HimdexKMeans
from lib.db_conn import copy_df_to_sql
from lib.stats_builder import StatsBuilder

STATS = StatsBuilder()
CLUST_TABLE = 'nba_him_clust'
schema = 'himdex'

def ingest_season_him(season_id: str):
    '''
    PURPOSE: ingest HIM clustering values
    '''

    season_data = STATS.compute_engineered_features(season_year = season_id)

    model_features = [
        # 'average_min',
        'total_plus_minus',
        'avg_bucket_contribution_rate',
        'avg_stop_contribution_rate',
        'avg_tmt_bucket_uplift_contribution_rate',
        'avg_tmt_stop_uplift_contribution_rate'
    ]

    # Need max 10 players per cluster
    clusters = len(season_data) // 10

    data = season_data[model_features]
    himdex_kmeans = HimdexKMeans(data)
    labels = himdex_kmeans.generate_labels(
        clusters = clusters,
        max_iter = 500,
        random_state = 2016
    )

    # breakpoint()

if __name__ == '__main__':
    season_id = '2015-16'
    ingest_season_him(season_id)


