import requests
import json
import os

URL = "adamleyshop.co.uk/collections/scarves"
STATE_FILE = "last_snapshot.json"

CDX_URL = (
    "https://web.archive.org/cdx/search/cdx"
    f"?url={URL}&limit=1&sort=reverse&output=json"
)

def get_latest_snapshot():
    r = requests.get(CDX_URL, timeout=30)
    r.raise_for_status()
    data = r.json()
    if len(data) < 2:
        return None
    return data[1][1]  # timestamp

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
        print("No snapshots found.")
        return

    last = load_last_snapshot()

    if latest != last:
        print(f"New snapshot found: {latest}")
        save_last_snapshot(latest)
    else:
        print("No new snapshot.")

if __name__ == "__main__":
    main()