import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    POKEAPI_URL = os.getenv('POKEAPI_URL')
    LOG_FILE_PATH = 'queries.csv'
    DEBUG = os.getenv('DEBUG_METRICS', '0') == '1'
