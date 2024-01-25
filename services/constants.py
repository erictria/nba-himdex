import os
from dotenv import load_dotenv

IS_DEV = os.environ.get('FLASK_ENV') == 'development'
if IS_DEV:
    load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PW = os.getenv('DB_PW')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

DB_CHUNK_SIZE = 1000

# SCHEMAS
# raw - raw data
# stats - feature engineered data

DB_SCHEMA = 'stats'