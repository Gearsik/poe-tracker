import time
import schedule
from poe_fetcher import fetch_and_store_currency
from poe_database import create_table

def fetch():
    print("Starting POE currency tracker...")
    create_table()
    fetch_and_store_currency()

if __name__ == "__main__":
    print("POE Currency Tracker started - Scheduler active")

    schedule.every(60).minutes.do(fetch)

    fetch()

    while True:
        schedule.run_pending()
        time.sleep(30)