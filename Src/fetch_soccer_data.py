import requests
import os
import json
import time

# Define Soccer endpoints
SOCCER_TEAMS_URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/teams"  # English Premier League
SOCCER_SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard"

# Create directory to store data
os.makedirs("data/raw/soccer", exist_ok=True)

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

def fetch_soccer_teams():
    """
    Fetch Soccer teams and save to a JSON file.
    """
    data = fetch_with_retry(SOCCER_TEAMS_URL)
    if data:
        with open("data/raw/soccer/teams.json", "w") as f:
            json.dump(data, f, indent=4)
        print("Soccer team data saved to data/raw/soccer/teams.json")
    else:
        print("Failed to fetch Soccer teams after retries")

def fetch_soccer_scoreboard():
    """
    Fetch Soccer scoreboard data and save to a JSON file.
    """
    data = fetch_with_retry(SOCCER_SCOREBOARD_URL)
    if data:
        with open("data/raw/soccer/scoreboard.json", "w") as f:
            json.dump(data, f, indent=4)
        print("Soccer scoreboard data saved to data/raw/soccer/scoreboard.json")
    else:
        print("Failed to fetch Soccer scoreboard after retries")

if __name__ == "__main__":
    fetch_soccer_teams()
    fetch_soccer_scoreboard()
