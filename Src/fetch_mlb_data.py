import requests
import os
import json
import time

# Define MLB endpoints
MLB_TEAMS_URL = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/teams"
MLB_SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"

# Create directory to store data
os.makedirs("data/raw/mlb", exist_ok=True)

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

def fetch_mlb_teams():
    """
    Fetch MLB teams and save to a JSON file.
    """
    data = fetch_with_retry(MLB_TEAMS_URL)
    if data:
        with open("data/raw/mlb/teams.json", "w") as f:
            json.dump(data, f, indent=4)
        print("MLB team data saved to data/raw/mlb/teams.json")
    else:
        print("Failed to fetch MLB teams after retries")

def fetch_mlb_scoreboard():
    """
    Fetch MLB scoreboard data and save to a JSON file.
    """
    data = fetch_with_retry(MLB_SCOREBOARD_URL)
    if data:
        with open("data/raw/mlb/scoreboard.json", "w") as f:
            json.dump(data, f, indent=4)
        print("MLB scoreboard data saved to data/raw/mlb/scoreboard.json")
    else:
        print("Failed to fetch MLB scoreboard after retries")

if __name__ == "__main__":
    fetch_mlb_teams()
    fetch_mlb_scoreboard()
