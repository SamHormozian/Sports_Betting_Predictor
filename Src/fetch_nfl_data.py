import requests
import os
import json
import time

# Define NFL endpoints
NFL_TEAMS_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"
NFL_SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"

# Create directory to store data
os.makedirs("Data/raw/nfl", exist_ok=True)

def fetch_with_retry(url, retries=3, delay=5):
    """
    Fetch data from the given URL with retries on failure.
    :param url: API endpoint URL
    :param retries: Number of retries before giving up
    :param delay: Delay between retries (in seconds)
    :return: JSON data if successful, None otherwise
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

def fetch_nfl_teams():
    """
    Fetch NFL teams and save to a JSON file.
    """
    data = fetch_with_retry(NFL_TEAMS_URL)
    if data:
        with open("Data/raw/nfl/teams.json", "w") as f:
            json.dump(data, f, indent=4)
        print("NFL team data saved to data/raw/nfl/teams.json")
    else:
        print("Failed to fetch NFL teams after retries")

def fetch_nfl_scoreboard():
    """
    Fetch NFL scoreboard data and save to a JSON file.
    """
    data = fetch_with_retry(NFL_SCOREBOARD_URL)
    if data:
        with open("Data/raw/nfl/scoreboard.json", "w") as f:
            json.dump(data, f, indent=4)
        print("NFL scoreboard data saved to data/raw/nfl/scoreboard.json")
    else:
        print("Failed to fetch NFL scoreboard after retries")

if __name__ == "__main__":
    fetch_nfl_teams()
    fetch_nfl_scoreboard()
