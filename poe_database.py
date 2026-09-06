import psycopg2
from poe_db_config import DB_CONFIG

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def create_table_if_not_exists():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                    CREATE TABLE IF NOT EXISTS poe_currency_history (
                        id SERIAL PRIMARY KEY,
                        game TEXT NOT NULL,
                        league_id TEXT NOT NULL,
                        league_name TEXT NOT NULL,
                        currency_id TEXT NOT NULL,
                        currency_name TEXT NOT NULL,
                        primary_value NUMERIC NOT NULL,
                        primary_currency TEXT NOT NULL,
                        fetched_at TIMESTAMPTZ DEFAULT NOW()
                    );
            """)