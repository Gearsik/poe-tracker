import os
from dotenv import load_dotenv

#loads environment variables from the .env file
load_dotenv()

#poe api configuration
POE_API_BASE = 'https://poe.ninja'

POE_REQUEST_HEADERS = {'User-Agent': 'PoE-Currency-Tracker/1.0'}

POE_GAMES = [
    game.strip().lower()
    for game in os.getenv(
        'POE_GAMES',
        'poe1,poe2'
    ).split(',')
    ]

VALID_GAMES = {'poe1', 'poe2'}
for game in POE_GAMES:
    if game not in VALID_GAMES:
        raise ValueError(
            f'Invalid game "{game}". Expected "poe1" or "poe2".'
        )

FETCH_INTERVAL_MINUTES = int(os.getenv('FETCH_INTERVAL_MINUTES', '60'))

def get_currency_url(game):
    return (
        f'{POE_API_BASE}/{game}'
        '/api/economy/exchange/current/overview'
    )

def get_leagues_url(game):
    return (
        f'{POE_API_BASE}/{game}'
        '/api/economy/leagues'
    )

#PostgreSQL configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST" , "db"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD") 
}