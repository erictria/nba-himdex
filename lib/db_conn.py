import csv
import os
import pandas as pd
import psycopg2
import re

from dotenv import load_dotenv
from io import StringIO
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

def clean_columns_names(s: str) -> str:
    '''
    PURPOSE: Clean up column names

    INPUT:
    s - str column name

    OUTPUT
    clean_str - str cleaned up column name
    '''

    clean_str = re.sub(r'[^0-9a-z]+', '_', s.lower()).strip('_')
    return clean_str

def psql_insert_copy(table, conn, keys, data_iter):
    '''
    PURPOSE: Gets a 

    INPUT:
    table - str table name
    conn - sqlalchemy DB connection
    keys - list of str column names
    data_iter - pandas dataframe of data
    '''

    db_conn = conn.connection
    with db_conn.cursor() as cur:
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)
        columns = ', '.join('"{}"'.format(k) for k in keys)
        if table.schema:
            table_name = '{}.{}'.format(table.schema, table.name)
        else:
            table_name = table.name
        sql = 'COPY {} ({}) FROM STDIN WITH CSV'.format(table_name, columns)
        cur.copy_expert(sql = sql, file = s_buf)

def copy_df_to_sql(df: pd.DataFrame, table: str, schema: str, if_exists: str = 'append', con = DB_CONN):
    '''
    PURPOSE: Ingests a table to PostgreSQL using COPY

    INPUT:
    df - pandas dataframe of data
    table - str table name
    schema - str schema name
    if_exists - str behavior to follow if table exists. Default: append
    con - db connection
    '''

    df.columns = df.columns.str.lower()
    df.columns = df.columns.to_series().apply(clean_columns_names)
    df.to_sql(
        table,
        schema = schema,
        con = con,
        index = False,
        if_exists = if_exists,
        method = psql_insert_copy
    )

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