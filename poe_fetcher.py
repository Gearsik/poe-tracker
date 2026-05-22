import requests
import sys
from datetime import datetime
from poe_database import get_connection
from poe_db_config import poe_api

def fetch_and_store_currency():
    print("Starting fetch_and_currency...", file=sys.stderr)

    try:
        print(f"Making requests to: {poe_api}", file=sys.stderr)

        api_response = requests.get(poe_api, timeout=15)
        api_response.raise_for_status() 

        print("Recieved response from POE API", file=sys.stderr)
        poe_data = api_response.json()

        with get_connection() as conn:
            with conn.cursor() as cur:
                inserted = 0

                currency_name_lookup = {item["id"]: item["name"] for item in poe_data.get("items" , [])}

                for currency in poe_data.get("lines" , []):
                    currency_id = currency.get("id")
                    name = currency_name_lookup.get(currency_id)
                    value = currency.get("primaryValue")

                    if currency_id and name and value is not None:
                        cur.execute("""
                            INSERT INTO poe_currency
                            (currency_id, currency_name, chaos_value)
                            VALUES (%s, %s, %s)
                            ON CONFLICT (currency_id) DO UPDATE
                            SET chaos_value = EXCLUDED.chaos_value,
                                    updated_at = NOW()
                        """, (currency_id, name, value))
                        inserted += 1
                conn.commit()
                print(f"Successfully inserted/updated {inserted} currencies at {datetime.now()}", file=sys.stderr)

    except requests.exceptions.RequestException as e:
        print(f"Network error fetching POE data {e}", file=sys.stdeer)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stdeer)
        import traceback
        traceback.print_exc(file=sys.stdeer)