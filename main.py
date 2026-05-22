import schedule
import time
import sys
import traceback

# Change this import if your fetch function is named differently
from poe_fetcher import fetch_and_store_currency

print("=== FETCHER CONTAINER STARTED ===", file=sys.stderr)
print(f"Python version: {sys.version}", file=sys.stderr)

schedule.every(5).minutes.do(fetch_and_store_currency)

print("Running INITIAL fetch...", file=sys.stderr)
try:
    fetch_and_store_currency()
    print("✅ Initial fetch completed successfully!", file=sys.stderr)
except Exception as e:
    print(f"❌ ERROR during initial fetch: {e}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)

print("Entering scheduler loop...", file=sys.stderr)

while True:
    try:
        schedule.run_pending()
        time.sleep(10)
    except Exception as e:
        print(f"❌ Error in scheduler: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        time.sleep(10)