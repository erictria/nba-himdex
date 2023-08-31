import os
import pandas as pd
import psycopg2

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PW = os.getenv('DB_PW')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

DB_CHUNK_SIZE = 1000

# SCHEMAS
# raw - raw data
# stats - feature engineered data

DB_CONN = create_engine('postgresql+psycopg2://{user}:{pw}@{host}/{db}'.format(
    user = DB_USER, 
    pw = DB_PW, 
    host = DB_HOST,
    db = DB_NAME
))

# TODO: Add clean up of column names
def write_df_to_sql(df: pd.DataFrame, table: str, schema: str, if_exists: str = 'append', con = DB_CONN):
    '''
    PURPOSE: writes to a psql table from a pandas dataframe

    INPUT:
    df - pandas dataframe data
    table - str table name
    schema - str schema name
    if_exists - str behavior to follow if table exists. Default: append
    con - db connection
    '''

    df.to_sql(
        table,
        con = con,
        schema = schema,
        if_exists = if_exists,
        index = False,
        chunksize = DB_CHUNK_SIZE
    )