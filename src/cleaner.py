import pandas as pd
import os
from rapidfuzz import process

# Define directories relative to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def standardize_column(df, column_name):
    """
    Standardize a column by stripping whitespace, converting to lowercase, 
    and removing special characters.
    """
    df[column_name] = (
        df[column_name]
        .str.strip()
        .str.lower()
        .str.replace(r"[^\w\s]", "", regex=True)  # Remove special characters
    )
    return df

def standardize_team_names(df, column_name, team_mapping, valid_teams):
    """
    Standardize team names using a mapping dictionary and fuzzy matching.
    """
    unmatched_teams = set()

    def map_team_name(name):
        if name in valid_teams:
            if name in team_mapping:
                return team_mapping[name]
            # Fuzzy matching for unmatched names
            best_match = process.extractOne(name, valid_teams, score_cutoff=80)
            if best_match:
                return team_mapping.get(best_match[0], best_match[0])
        unmatched_teams.add(name)
        return name

    df[column_name] = df[column_name].apply(map_team_name)

    # Log unmatched teams
    if unmatched_teams:
        print(f"Unmatched teams for column {column_name}: {', '.join(sorted(unmatched_teams))}")

    return df

def preprocess_and_standardize_team_columns(df, home_cols, away_cols, team_mapping, valid_teams):
    """
    Preprocess and standardize home and away team columns for consistency.
    
    Args:
        df (DataFrame): The dataset to process.
        home_cols (list): List of home team column names.
        away_cols (list): List of away team column names.
        team_mapping (dict): Mapping dictionary for team names.
        valid_teams (set): Valid teams for fuzzy matching.

    Returns:
        DataFrame: Updated DataFrame with standardized columns.
    """
    # Combine and standardize home team columns
    df['home_team_combined'] = (
        df[home_cols]
        .fillna("")  # Fill NaNs with empty strings
        .astype(str)
        .agg(" ".join, axis=1)  # Combine all columns into a single string
        .str.strip()
        .str.lower()
        .str.replace(r"[^\w\s]", "", regex=True)  # Remove special characters
    )

    # Combine and standardize away team columns
    df['away_team_combined'] = (
        df[away_cols]
        .fillna("")
        .astype(str)
        .agg(" ".join, axis=1)
        .str.strip()
        .str.lower()
        .str.replace(r"[^\w\s]", "", regex=True)
    )

    # Apply team mapping to the combined columns
    df = standardize_team_names(df, 'home_team_combined', team_mapping, valid_teams)
    df = standardize_team_names(df, 'away_team_combined', team_mapping, valid_teams)

    return df

def create_team_mapping():
    """
    Create a dictionary mapping team names and abbreviations to standardized versions.
    """
    team_mapping = {
        # NFL Teams
        "arizona cardinals": "cardinals",
        "atlanta falcons": "falcons",
        "baltimore colts": "colts",
        "baltimore ravens": "ravens",
        "boston patriots": "patriots",
        "buffalo bills": "bills",
        "carolina panthers": "panthers",
        "chicago bears": "bears",
        "cincinnati bengals": "bengals",
        "cleveland browns": "browns",
        "dallas cowboys": "cowboys",
        "denver broncos": "broncos",
        "detroit lions": "lions",
        "green bay packers": "packers",
        "houston oilers": "oilers",
        "houston texans": "texans",
        "indianapolis colts": "colts",
        "jacksonville jaguars": "jaguars",
        "kansas city chiefs": "chiefs",
        "las vegas raiders": "raiders",
        "los angeles chargers": "chargers",
        "los angeles raiders": "raiders",
        "los angeles rams": "rams",
        "miami dolphins": "dolphins",
        "minnesota vikings": "vikings",
        "new england patriots": "patriots",
        "new orleans saints": "saints",
        "new york giants": "giants",
        "new york jets": "jets",
        "oakland raiders": "raiders",
        "philadelphia eagles": "eagles",
        "phoenix cardinals": "cardinals",
        "pittsburgh steelers": "steelers",
        "san diego chargers": "chargers",
        "san francisco 49ers": "49ers",
        "seattle seahawks": "seahawks",
        "st louis cardinals": "cardinals",
        "st louis rams": "rams",
        "tampa bay buccaneers": "buccaneers",
        "tennessee oilers": "oilers",
        "tennessee titans": "titans",
        "washington commanders": "commanders",
        "washington football team": "commanders",
        "washington redskins": "commanders",
        # NBA Teams
        "boston celtics": "celtics",
    "dallas mavericks": "mavericks",
    "golden state warriors": "warriors",
    "new orleans pelicans": "pelicans",
    "new york knicks": "knicks",
    "phoenix suns": "suns",
    "sacramento kings": "kings",
    "toronto raptors": "raptors",
    "denver nuggets": "nuggets",
    "houston rockets": "rockets",
    "indiana pacers": "pacers",
    "los angeles lakers": "lakers",
    "minnesota timberwolves": "timberwolves",
    "philadelphia 76ers": "76ers",
    "san antonio spurs": "spurs",

        "atl": "hawks",
        "bkn": "nets",
        "bos": "celtics",
        "cha": "hornets",
        "chi": "bulls",
        "cle": "cavaliers",
        "dal": "mavericks",
        "den": "nuggets",
        "det": "pistons",
        "gs": "warriors",
        "hou": "rockets",
        "ind": "pacers",
        "lac": "clippers",
        "lal": "lakers",
        "mem": "grizzlies",
        "mia": "heat",
        "mil": "bucks",
        "min": "timberwolves",
        "no": "pelicans",
        "ny": "knicks",
        "okc": "thunder",
        "orl": "magic",
        "phi": "76ers",
        "phx": "suns",
        "por": "trail blazers",
        "sa": "spurs",
        "sac": "kings",
        "tor": "raptors",
        "utah": "jazz",
        "wsh": "wizards",
    }
    return team_mapping

def merge_nfl_datasets(team_mapping):
    valid_nfl_teams = set(team_mapping.keys())

    # Load datasets
    player_stats = pd.read_csv(os.path.join(DATA_DIR, "nfl_stats_2000_2024.csv"))
    team_scores = pd.read_csv(os.path.join(DATA_DIR, "nfl_spreadspoke_scores.csv"))
    injuries = pd.read_csv(os.path.join(DATA_DIR, "nfl_injuries.csv"))
    odds = pd.read_csv(os.path.join(DATA_DIR, "americanfootball_nfl_odds.csv"))

    # Preprocess team columns for team_scores
    team_scores = preprocess_and_standardize_team_columns(
        team_scores, home_cols=["team_home"], away_cols=["team_away"], 
        team_mapping=team_mapping, valid_teams=valid_nfl_teams
    )

    # Preprocess team columns for odds
    odds = preprocess_and_standardize_team_columns(
        odds, home_cols=["home_team"], away_cols=["away_team"], 
        team_mapping=team_mapping, valid_teams=valid_nfl_teams
    )

    # Merge team-level data
    team_data = team_scores.merge(
        odds, left_on=["home_team_combined", "away_team_combined"], 
        right_on=["home_team_combined", "away_team_combined"], how="left"
    )
    team_data.to_csv(os.path.join(OUTPUT_DIR, "nfl_team_data.csv"), index=False)

    # Standardize and merge player-level data
    player_stats = standardize_column(player_stats, "Player")
    injuries = standardize_column(injuries, "NAME")
    player_data = player_stats.merge(injuries, left_on="Player", right_on="NAME", how="left")
    player_data.to_csv(os.path.join(OUTPUT_DIR, "nfl_player_data.csv"), index=False)

    print("NFL datasets merged and saved.")

def merge_nba_datasets(team_mapping):
    valid_nba_teams = set(team_mapping.keys())

    # Load datasets
    player_stats = pd.read_csv(os.path.join(DATA_DIR, "nba_stats_2000_2024.csv"))
    team_scores = pd.read_csv(os.path.join(DATA_DIR, "nba_2008-2024.csv"))
    injuries = pd.read_csv(os.path.join(DATA_DIR, "nba_injuries.csv"))
    odds = pd.read_csv(os.path.join(DATA_DIR, "basketball_nba_odds.csv"))

    # Preprocess team columns for team_scores
    team_scores = preprocess_and_standardize_team_columns(
        team_scores, home_cols=["home"], away_cols=["away"], 
        team_mapping=team_mapping, valid_teams=valid_nba_teams
    )

    # Preprocess team columns for odds
    odds = preprocess_and_standardize_team_columns(
        odds, home_cols=["home_team"], away_cols=["away_team"], 
        team_mapping=team_mapping, valid_teams=valid_nba_teams
    )

    # Merge team-level data
    team_data = team_scores.merge(
        odds, left_on=["home_team_combined", "away_team_combined"], 
        right_on=["home_team_combined", "away_team_combined"], how="left"
    )
    team_data.to_csv(os.path.join(OUTPUT_DIR, "nba_team_data.csv"), index=False)

    # Standardize and merge player-level data
    player_stats = standardize_column(player_stats, "Player")
    injuries = standardize_column(injuries, "NAME")
    player_data = player_stats.merge(injuries, left_on="Player", right_on="NAME", how="left")
    player_data.to_csv(os.path.join(OUTPUT_DIR, "nba_player_data.csv"), index=False)

    print("NBA datasets merged and saved.")

if __name__ == "__main__":
    print("Creating team name mapping...")
    team_mapping = create_team_mapping()

    print("Merging NFL datasets...")
    merge_nfl_datasets(team_mapping)

    print("Merging NBA datasets...")
    merge_nba_datasets(team_mapping)
