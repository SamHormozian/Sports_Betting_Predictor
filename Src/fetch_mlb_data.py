import requests
import os
import json
import time
import pandas as pd  # Import pandas for CSV operations

# Define MLB endpoints
MLB_TEAMS_URL = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/teams"
MLB_SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"

# Create directories to store data
os.makedirs("data/raw/mlb", exist_ok=True)
os.makedirs("data/csv/mlb", exist_ok=True)  # Directory for CSV files

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
    if isinstance(data, list):  # Handle list of items
        df = pd.DataFrame(data)
    elif isinstance(data, dict):  # Handle dictionary
        df = pd.json_normalize(data)  # Flatten nested JSON
    else:
        print(f"Unsupported data format for CSV conversion: {type(data)}")
        return

    # Filter columns if specified
    if columns:
        df = df[columns]

    df.to_csv(file_path, index=False)
    print(f"Data saved as CSV to {file_path}")

def fetch_mlb_teams():
    """
    Fetch MLB teams and save to a JSON and CSV file.
    """
    data = fetch_with_retry(MLB_TEAMS_URL)
    if data:
        # Save raw JSON
        with open("data/raw/mlb/teams.json", "w") as f:
            json.dump(data, f, indent=4)
        print("MLB team data saved to data/raw/mlb/teams.json")

        # Convert teams to CSV
        teams_data = data.get("sports", [])[0].get("leagues", [])[0].get("teams", [])
        teams_list = [team["team"] for team in teams_data if "team" in team]
        save_as_csv(teams_list, "data/csv/mlb/teams.csv")
    else:
        print("Failed to fetch MLB teams after retries")

def fetch_mlb_scoreboard():
    """
    Fetch MLB scoreboard data and save to a JSON and CSV file.
    """
    data = fetch_with_retry(MLB_SCOREBOARD_URL)
    if data:
        # Save raw JSON
        with open("data/raw/mlb/scoreboard.json", "w") as f:
            json.dump(data, f, indent=4)
        print("MLB scoreboard data saved to data/raw/mlb/scoreboard.json")

        # Convert scoreboard to CSV
        events = data.get("events", [])
        save_as_csv(events, "data/csv/mlb/scoreboard.csv")
    else:
        print("Failed to fetch MLB scoreboard after retries")

if __name__ == "__main__":
    fetch_mlb_teams()
    fetch_mlb_scoreboard()
