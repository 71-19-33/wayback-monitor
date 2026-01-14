import requests
import json
import os
import time

URL = "adamleyshop.co.uk/collections/scarves"
STATE_FILE = "last_snapshot.json"

CDX_URL = (
    "https://web.archive.org/cdx/search/cdx"
    f"?url={URL}&limit=1&sort=reverse&output=json"
)

def get_latest_snapshot(retries=3, timeout=60):
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(CDX_URL, timeout=timeout)
            r.raise_for_status()
            data = r.json()
            if len(data) < 2:
                return None
            return data[1][1]
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt < retries:
                time.sleep(10)
            else:
                print("Giving up for this run.")
                return None

def load_last_snapshot():
    if not os.path.exists(STATE_FILE):
        return None
    with open(STATE_FILE, "r") as f:
        return json.load(f).get("timestamp")

def save_last_snapshot(ts):
    with open(STATE_FILE, "w") as f:
        json.dump({"timestamp": ts}, f)

def main():
    latest = get_latest_snapshot()
    if not latest:
        print("No snapshot retrieved (timeout or none exists).")
        return

    last = load_last_snapshot()

    if latest != last:
        print(f"New snapshot found: {latest}")
        save_last_snapshot(latest)
    else:
        print("No new snapshot.")

if __name__ == "__main__":
    main()