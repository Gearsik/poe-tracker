import requests
from datetime import datetime
from poe_database import get_connection
from poe_db_config import poe_api

def fetch_and_store_currency():
    try:
        api_response = requests.get(poe_api, timeout=15)
        api_response.raise_for_status() 

        poe_data = api_response.json()

        with get_connection() as conn:
            with conn.cursor() as cur:
                inserted = 0

                currency_name_lookup = {item["id"]: item["name"] for item in poe_data.get("items" , [])}
                for currency in poe_data.get("lines" , [])[:5]:
                    currency_id = currency.get("id")
                    name = currency_name_lookup.get(currency_id)
                    value = currency.get("primaryValue")

                    if currency_id and value is None:
                        cur.execute("""
                            INSERT INTO poe_currency
                            (currency_id, currency_name, chaos_value)
                            VALUES (%s, %s, %s)
                        """, (currency_id, name, value))
                        inserted += 1

                print(f"Inserted {inserted} currencies at {datetime.now()}")

    except Exception as e:
        print(f"Error fetching/storing data: {e}")