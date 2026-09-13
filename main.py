import schedule
import time
import sys
import traceback

# Change this import if your fetch function is named differently
from poe_database import create_table_if_not_exists
from poe_fetcher import fetch_all_games
from poe_db_config import FETCH_INTERVAL_MINUTES

print("=== FETCHER CONTAINER STARTED ===", file=sys.stderr)
print(f"Python version: {sys.version}", file=sys.stderr)

schedule.every(FETCH_INTERVAL_MINUTES).minutes.do(fetch_all_games)

print("Running INITIAL fetch...", file=sys.stderr)

try:
    create_table_if_not_exists()

    if fetch_all_games():
        print('Initial fetch completed successfully!', file=sys.stderr)
    else:
        print('Initial fetch completed with errors.', file=sys.stderr)

except Exception as e:

    print(f"ERROR during initial fetch: {e}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)

print("Entering scheduler loop...", file=sys.stderr)

while True:
    try:
        schedule.run_pending()
        time.sleep(10)

    except Exception as e:
        
        print(f"Error in scheduler: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        time.sleep(10)