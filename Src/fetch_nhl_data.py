import requests
import os
import json
import time
import pandas as pd  # Import pandas for CSV operations

# Define NHL endpoints
NHL_TEAMS_URL = "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/teams"
NHL_SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard"

# Create directories to store raw and CSV data
os.makedirs("data/raw/nhl", exist_ok=True)
os.makedirs("data/csv/nhl", exist_ok=True)

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

def save_as_csv(data, file_path, columns=None):
    """
    Save the data as a CSV file using pandas.
    """
    if isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, dict):
        df = pd.json_normalize(data)  # Flatten nested JSON
    else:
        print(f"Unsupported data format for CSV conversion: {type(data)}")
        return

    if columns:
        df = df[columns]  # Keep only specified columns

    df.to_csv(file_path, index=False)
    print(f"Data saved as CSV to {file_path}")

def fetch_nhl_teams():
    """
    Fetch NHL teams and save to both JSON and CSV files.
    """
    data = fetch_with_retry(NHL_TEAMS_URL)
    if data:
        # Save raw JSON
        raw_file_path = "data/raw/nhl/teams.json"
        with open(raw_file_path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"NHL team data saved to {raw_file_path}")

        # Convert teams data to CSV
        teams_data = data.get("sports", [])[0].get("leagues", [])[0].get("teams", [])
        teams_list = [team["team"] for team in teams_data if "team" in team]
        csv_file_path = "data/csv/nhl/teams.csv"
        save_as_csv(teams_list, csv_file_path)
    else:
        print("Failed to fetch NHL teams after retries")

def fetch_nhl_scoreboard():
    """
    Fetch NHL scoreboard data and save to both JSON and CSV files.
    """
    data = fetch_with_retry(NHL_SCOREBOARD_URL)
    if data:
        # Save raw JSON
        raw_file_path = "data/raw/nhl/scoreboard.json"
        with open(raw_file_path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"NHL scoreboard data saved to {raw_file_path}")

        # Convert scoreboard data to CSV
        events = data.get("events", [])
        csv_file_path = "data/csv/nhl/scoreboard.csv"
        save_as_csv(events, csv_file_path)
    else:
        print("Failed to fetch NHL scoreboard after retries")

if __name__ == "__main__":
    fetch_nhl_teams()
    fetch_nhl_scoreboard()
