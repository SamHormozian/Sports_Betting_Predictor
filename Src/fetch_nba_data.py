import requests
import os
import json
import time

# Define NBA endpoints
NBA_TEAMS_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams"
NBA_SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"

# Create directory to store data
os.makedirs("Data/raw/nba", exist_ok=True)

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

def fetch_nba_teams():
    """
    Fetch NBA teams and save to a JSON file.
    """
    data = fetch_with_retry(NBA_TEAMS_URL)
    if data:
        with open("data/raw/nba/teams.json", "w") as f:
            json.dump(data, f, indent=4)
        print("NBA team data saved to Data/raw/nba/teams.json")
    else:
        print("Failed to fetch NBA teams after retries")

def fetch_nba_scoreboard():
    """
    Fetch NBA scoreboard data and save to a JSON file.
    """
    data = fetch_with_retry(NBA_SCOREBOARD_URL)
    if data:
        with open("Data/raw/nba/scoreboard.json", "w") as f:
            json.dump(data, f, indent=4)
        print("NBA scoreboard data saved to data/raw/nba/scoreboard.json")
    else:
        print("Failed to fetch NBA scoreboard after retries")

if __name__ == "__main__":
    fetch_nba_teams()
    fetch_nba_scoreboard()
