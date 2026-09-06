import requests
import sys
import traceback
from datetime import datetime
from poe_database import get_connection
from poe_db_config import POE_API_URL, POE_API_PARAMS, POE_LEAGUE

def parse_currency_data(poe_data, league):
    currency_name_lookup = {
        item.get('id'): item.get('name')
        for item in poe_data.get('items', [])
        if item.get('id') and item.get('name')
    }

    currencies = []

    for currency in poe_data.get('lines', []):
        currency_id = currency.get('id')
        name = currency_name_lookup.get(currency_id)
        value = currency.get('primaryValue')

        if currency_id and name and value is not None:
            currencies.append(
                (league, currency_id, name, value)
            )
    return currencies

def fetch_and_store_currency():
    print("Starting currency fetch...", file=sys.stderr)

    print(f"Making requests to: {POE_API_URL}", file=sys.stderr)

    api_response = requests.get(POE_API_URL, params=POE_API_PARAMS, timeout=15)
    api_response.raise_for_status() 

    print("Received response from POE API", file=sys.stderr)
    poe_data = api_response.json()

    currencies = parse_currency_data(poe_data, POE_LEAGUE)

    with get_connection() as conn:
        with conn.cursor() as cur:
            inserted = 0

            for league, currency_id, name, value in currencies:
                cur.execute("""
                    INSERT INTO poe_currency_history
                    (league, currency_id, currency_name, chaos_value)
                    VALUES (%s, %s, %s, %s)
                """, (league, currency_id, name, value))
                inserted += 1

    print(f"Successfully inserted {inserted} currencies at {datetime.now()}", file=sys.stderr)