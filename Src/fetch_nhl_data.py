import requests
import os
import json
import time

# Define NHL endpoints
NHL_TEAMS_URL = "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/teams"
NHL_SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard"

# Create directory to store data
os.makedirs("data/raw/nhl", exist_ok=True)

def fetch_with_retry(url, retries=3, delay=5):
    """
    Fetch data from the given URL with retries on failure.
    """
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Attempt {attempt + 1} failed with status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
        time.sleep(delay)
    print(f"All {retries} attempts failed for URL: {url}")
    return None

def fetch_nhl_teams():
    """
    Fetch NHL teams and save to a JSON file.
    """
    data = fetch_with_retry(NHL_TEAMS_URL)
    if data:
        with open("data/raw/nhl/teams.json", "w") as f:
            json.dump(data, f, indent=4)
        print("NHL team data saved to data/raw/nhl/teams.json")
    else:
        print("Failed to fetch NHL teams after retries")

def fetch_nhl_scoreboard():
    """
    Fetch NHL scoreboard data and save to a JSON file.
    """
    data = fetch_with_retry(NHL_SCOREBOARD_URL)
    if data:
        with open("data/raw/nhl/scoreboard.json", "w") as f:
            json.dump(data, f, indent=4)
        print("NHL scoreboard data saved to data/raw/nhl/scoreboard.json")
    else:
        print("Failed to fetch NHL scoreboard after retries")

if __name__ == "__main__":
    fetch_nhl_teams()
    fetch_nhl_scoreboard()
