import pandas as pd
import os

# Define directories
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "training_data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_mixed_type_columns(df, column_name):
    """
    Convert mixed type columns to numeric, handling non-numeric values.
    """
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
    return df

def handle_missing_values(df, sport, is_team_data=False):
    """
    Handle missing values in the dataset.
    """
    if sport == "NBA":
        if is_team_data:
            # Handle missing values in team data
            df.fillna({
                "score_home": df["score_home"].mean(),
                "score_away": df["score_away"].mean(),
                "spread": df["spread"].mean(),
                "total": df["total"].mean(),
            }, inplace=True)
        else:
            # Handle missing values in player data
            df.fillna({
                "FG%": df["FG%"].mean(),
                "3P%": df["3P%"].mean(),
                "FT%": df["FT%"].mean(),
                "PTS": 0,
                "TRB": 0,
                "AST": 0,
            }, inplace=True)
    elif sport == "NFL":
        if is_team_data:
            # Clean mixed type columns
            df = clean_mixed_type_columns(df, "over_under_line")

            # Handle missing values in team data
            df.fillna({
                "score_home": df["score_home"].mean(),
                "score_away": df["score_away"].mean(),
                "spread_favorite": df["spread_favorite"].mean(),
                "over_under_line": df["over_under_line"].mean(),
            }, inplace=True)
        else:
            # Handle missing values in player data
            df.fillna({
                "Cmp%": df["Cmp%"].mean(),
                "Rate": df["Rate"].mean(),
                "Yds": 0,
                "TD": 0,
                "Int": 0,
                "4QC": 0,
                "GWD": 0,
            }, inplace=True)
    return df

def normalize_columns(df, columns):
    """
    Normalize numerical columns to a range [0, 1].
    """
    for col in columns:
        if col in df.columns:
            df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
    return df

def add_derived_features(df, sport):
    """
    Add derived features like score differences and aggregated player stats differences.
    """
    if sport == "NBA":
        df["score_diff"] = df["score_home"] - df["score_away"]
        df["PTS_diff"] = df["PTS"] - df["PTS_away"]
        df["AST_diff"] = df["AST"] - df["AST_away"]
        df["TRB_diff"] = df["TRB"] - df["TRB_away"]
    elif sport == "NFL":
        df["score_diff"] = df["score_home"] - df["score_away"]
        df["Yds_diff"] = df["Yds"] - df["Yds_away"]
        df["TD_diff"] = df["TD"] - df["TD_away"]
        df["Int_diff"] = df["Int"] - df["Int_away"]
    return df

def aggregate_player_stats(player_data, sport):
    """
    Aggregate player stats to the team level.
    """
    if sport == "NBA":
        agg_stats = player_data.groupby("Team").agg({
            "PTS": "sum",
            "TRB": "sum",
            "AST": "sum",
            "FG%": "mean",
            "3P%": "mean",
            "FT%": "mean"
        }).reset_index()
    elif sport == "NFL":
        agg_stats = player_data.groupby("Team").agg({
            "Yds": "sum",
            "TD": "sum",
            "Int": "sum",
            "Cmp%": "mean",
            "Rate": "mean",
            "4QC": "sum",
            "GWD": "sum"
        }).reset_index()
    else:
        raise ValueError("Sport must be 'NBA' or 'NFL'")
    return agg_stats

def combine_team_and_player_data(team_data, player_data, sport):
    """
    Combine team-level and player-level data into one dataset.
    """
    player_stats = aggregate_player_stats(player_data, sport)

    home_team_col = "home_team_combined"
    away_team_col = "away_team_combined"

    combined_data = team_data.merge(
        player_stats, left_on=home_team_col, right_on="Team", how="left", suffixes=("", "_home")
    ).merge(
        player_stats, left_on=away_team_col, right_on="Team", how="left", suffixes=("", "_away")
    )

    combined_data = add_derived_features(combined_data, sport)
    combined_data = normalize_columns(combined_data, ["score_home", "score_away", "score_diff"])
    return combined_data

def process_nba_data():
    print("Processing NBA data...")
    nba_team_data = pd.read_csv(os.path.join(DATA_DIR, "nba_team_data.csv"))
    nba_player_data = pd.read_csv(os.path.join(DATA_DIR, "nba_player_data.csv"))

    nba_team_data = handle_missing_values(nba_team_data, "NBA", is_team_data=True)
    nba_player_data = handle_missing_values(nba_player_data, "NBA", is_team_data=False)

    training_data = combine_team_and_player_data(nba_team_data, nba_player_data, "NBA")
    training_data.to_csv(os.path.join(OUTPUT_DIR, "nba_training_data.csv"), index=False)
    print(f"Training data saved to {os.path.join(OUTPUT_DIR, 'nba_training_data.csv')}")

def process_nfl_data():
    print("Processing NFL data...")
    nfl_team_data = pd.read_csv(os.path.join(DATA_DIR, "nfl_team_data.csv"))
    nfl_player_data = pd.read_csv(os.path.join(DATA_DIR, "nfl_player_data.csv"))

    nfl_team_data = handle_missing_values(nfl_team_data, "NFL", is_team_data=True)
    nfl_player_data = handle_missing_values(nfl_player_data, "NFL", is_team_data=False)

    training_data = combine_team_and_player_data(nfl_team_data, nfl_player_data, "NFL")
    training_data.to_csv(os.path.join(OUTPUT_DIR, "nfl_training_data.csv"), index=False)
    print(f"Training data saved to {os.path.join(OUTPUT_DIR, 'nfl_training_data.csv')}")

if __name__ == "__main__":
    process_nba_data()
    process_nfl_data()
