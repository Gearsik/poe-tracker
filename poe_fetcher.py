import requests
import sys
from datetime import datetime
from poe_database import get_connection
from poe_db_config import POE_GAMES, POE_REQUEST_HEADERS, get_currency_url, get_leagues_url

def get_current_league(game):
    response = requests.get(
        get_leagues_url(game),
        headers=POE_REQUEST_HEADERS,
        timeout=15
    )

    response.raise_for_status()

    leagues = response.json()

    if not leagues:
        raise ValueError(
            f'No active PoE economy leagues returned for {game}'
        )

    return leagues[0]

def parse_currency_data(poe_data, game, league_id, league_name):

    core = poe_data.get('core', {})

    currency_name_lookup = {
        item.get('id'): item.get('name')
        for item in core.get('items', [])
        if item.get('id') and item.get('name')
    }

    primary_currency = core.get('primary')

    if not primary_currency:
        raise ValueError(
            'No primary currency returned by PoE API'
        )

    currencies = []

    for currency in poe_data.get('lines', []):
        currency_id = currency.get('id')
        name = currency_name_lookup.get(currency_id)
        value = currency.get('primaryValue')

        if currency_id and name and value is not None:
            currencies.append(
                (game, league_id, league_name, currency_id, name, value, primary_currency)
            )
        
    return currencies

def fetch_and_store_currency(game):
    print("Starting currency fetch...", file=sys.stderr)

    current_league = get_current_league(game)

    league_id = current_league['id']
    league_name = current_league['name']

    print(f'Current {game} league: {league_name}', file=sys.stderr)

    api_response = requests.get(get_currency_url(game), params={'league': league_id, 'type': 'Currency'}, headers=POE_REQUEST_HEADERS, timeout=15)
    api_response.raise_for_status()

    print(f"Received {game} response from POE API", file=sys.stderr)

    poe_data = api_response.json()

    currencies = parse_currency_data(poe_data, game, league_id, league_name)

    with get_connection() as conn:
        with conn.cursor() as cur:
            inserted = 0

            for game, league_id, league_name, currency_id, name, value, primary_currency in currencies:
                cur.execute("""
                    INSERT INTO poe_currency_history
                    (game, league_id, league_name, currency_id, currency_name, primary_value, primary_currency)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (game, league_id, league_name, currency_id, name, value, primary_currency))
                inserted += 1

    print(f"Successfully inserted {inserted} {game} currencies at {datetime.now()}", file=sys.stderr)

def fetch_all_games():
    for game in POE_GAMES:
        fetch_and_store_currency(game)