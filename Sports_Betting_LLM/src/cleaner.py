import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

# Directories
RAW_DATA_DIR = "data/raw/"
PROCESSED_DATA_DIR = "data/processed/"
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

def clean_odds_data(file_name, output_file):
    """Clean and normalize odds data."""
    file_path = os.path.join(RAW_DATA_DIR, file_name)
    try:
        # Load dataset
        df = pd.read_csv(file_path)

        # Standardize column names
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

        # Convert commence_time to datetime
        if 'commence_time' in df.columns:
            df['commence_time'] = pd.to_datetime(df['commence_time'], errors='coerce')

        # Fill missing values
        df.fillna({'price': 0, 'point': 0, 'market_type': 'unknown', 'bookmaker': 'unknown'}, inplace=True)

        # Normalize numeric columns
        scaler = MinMaxScaler()
        for col in ['price', 'point']:
            if col in df.columns:
                df[f'{col}_normalized'] = scaler.fit_transform(df[[col]])

        # Encode categorical columns
        encoder = LabelEncoder()
        for col in ['home_team', 'away_team', 'market_type', 'bookmaker']:
            if col in df.columns:
                df[f'{col}_encoded'] = encoder.fit_transform(df[col])

        # Save cleaned dataset
        output_path = os.path.join(PROCESSED_DATA_DIR, output_file)
        df.to_csv(output_path, index=False)
        print(f"Processed and saved: {output_path}")

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

def clean_injury_data(file_name, output_file):
    """Clean and normalize an injury dataset."""
    file_path = os.path.join(RAW_DATA_DIR, file_name)
    try:
        # Load dataset
        df = pd.read_csv(file_path)

        # Standardize column names
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

        # Convert estimated return date to datetime
        if 'est._return_date' in df.columns:
            df['est._return_date'] = pd.to_datetime(df['est._return_date'], errors='coerce')

        # Fill missing values
        df['pos'].fillna('Unknown', inplace=True)
        df['status'].fillna('Unknown', inplace=True)
        df['comment'].fillna('', inplace=True)  # Keep empty comments as blank strings

        # Encode categorical data
        encoder = LabelEncoder()
        for col in ['name', 'pos', 'status']:
            df[f'{col}_encoded'] = encoder.fit_transform(df[col])

        # Save cleaned dataset
        output_path = os.path.join(PROCESSED_DATA_DIR, output_file)
        df.to_csv(output_path, index=False)
        print(f"Processed and saved: {output_path}")

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

def process_nfl_data(file_name, output_file):
    """Clean and process NFL spread spoke scores data."""
    file_path = os.path.join(RAW_DATA_DIR, file_name)
    try:
        # Load dataset
        df = pd.read_csv(file_path)

        # Standardize column names
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

        # Convert schedule_date to datetime
        df['schedule_date'] = pd.to_datetime(df['schedule_date'], errors='coerce')

        # Fill missing values
        df['spread_favorite'].fillna(0, inplace=True)
        df['over_under_line'].fillna(0, inplace=True)
        df['weather_temperature'].fillna(df['weather_temperature'].mean(), inplace=True)
        df['weather_wind_mph'].fillna(df['weather_wind_mph'].mean(), inplace=True)
        df['weather_humidity'].fillna(df['weather_humidity'].mean(), inplace=True)
        df['weather_detail'].fillna('Unknown', inplace=True)

        # Compute derived features
        df['total_points'] = df['score_home'] + df['score_away']
        df['winner'] = df.apply(lambda x: 'home' if x['score_home'] > x['score_away'] else 'away', axis=1)
        df['spread_covered'] = df.apply(lambda x: 1 if (x['spread_favorite'] > 0 and x['score_home'] + x['spread_favorite'] > x['score_away']) else 0, axis=1)

        # Save cleaned dataset
        output_path = os.path.join(PROCESSED_DATA_DIR, output_file)
        df.to_csv(output_path, index=False)
        print(f"Processed and saved: {output_path}")

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

def process_nba_data(file_name, output_file):
    """Clean and process NBA game data."""
    file_path = os.path.join(RAW_DATA_DIR, file_name)
    try:
        # Load dataset
        df = pd.read_csv(file_path)

        # Standardize column names
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # Fill missing values
        df['spread'].fillna(0, inplace=True)
        df['total'].fillna(0, inplace=True)

        # Compute derived features
        df['total_points'] = df['score_home'] + df['score_away']
        df['winner'] = df.apply(lambda x: 'home' if x['score_home'] > x['score_away'] else 'away', axis=1)
        df['spread_covered'] = df.apply(lambda x: 1 if (x['spread'] > 0 and x['score_home'] + x['spread'] > x['score_away']) else 0, axis=1)

        # Save cleaned dataset
        output_path = os.path.join(PROCESSED_DATA_DIR, output_file)
        df.to_csv(output_path, index=False)
        print(f"Processed and saved: {output_path}")

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

def process_nfl_stadiums(file_name, output_file):
    """Clean and process NFL stadium data."""
    file_path = os.path.join(RAW_DATA_DIR, file_name)
    try:
        # Attempt to read with a compatible encoding
        df = pd.read_csv(file_path, encoding='latin1')  # Change encoding if needed
        
        # Standardize column names
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

        # Convert numeric and date columns
        df['stadium_open'] = pd.to_datetime(df['stadium_open'], errors='coerce')
        df['stadium_close'] = pd.to_datetime(df['stadium_close'], errors='coerce')
        df['stadium_capacity'] = pd.to_numeric(df['stadium_capacity'].str.replace(',', ''), errors='coerce')

        # Fill missing values
        df['stadium_weather_station_zipcode'].fillna('Unknown', inplace=True)
        df['stadium_weather_type'].fillna('Unknown', inplace=True)
        df['stadium_surface'].fillna('Unknown', inplace=True)
        df['stadium_latitude'].fillna(df['stadium_latitude'].mean(), inplace=True)
        df['stadium_longitude'].fillna(df['stadium_longitude'].mean(), inplace=True)

        # Encode categorical columns
        encoder = LabelEncoder()
        for col in ['stadium_type', 'stadium_surface', 'stadium_weather_type']:
            if col in df.columns:
                df[f'{col}_encoded'] = encoder.fit_transform(df[col])

        # Save cleaned dataset
        output_path = os.path.join(PROCESSED_DATA_DIR, output_file)
        df.to_csv(output_path, index=False)
        print(f"Processed and saved: {output_path}")

    except UnicodeDecodeError as e:
        print(f"Encoding issue encountered with {file_name}: {e}")
        print("Trying with a different encoding...")
        try:
            # Retry with 'latin1' encoding
            df = pd.read_csv(file_path, encoding='latin1')

            # Standardize column names
            df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

            # Convert numeric and date columns
            df['stadium_open'] = pd.to_datetime(df['stadium_open'], errors='coerce')
            df['stadium_close'] = pd.to_datetime(df['stadium_close'], errors='coerce')
            df['stadium_capacity'] = pd.to_numeric(df['stadium_capacity'].str.replace(',', ''), errors='coerce')

            # Fill missing values
            df['stadium_weather_station_zipcode'].fillna('Unknown', inplace=True)
            df['stadium_weather_type'].fillna('Unknown', inplace=True)
            df['stadium_surface'].fillna('Unknown', inplace=True)
            df['stadium_latitude'].fillna(df['stadium_latitude'].mean(), inplace=True)
            df['stadium_longitude'].fillna(df['stadium_longitude'].mean(), inplace=True)

            # Encode categorical columns
            encoder = LabelEncoder()
            for col in ['stadium_type', 'stadium_surface', 'stadium_weather_type']:
                if col in df.columns:
                    df[f'{col}_encoded'] = encoder.fit_transform(df[col])

            # Save cleaned dataset
            output_path = os.path.join(PROCESSED_DATA_DIR, output_file)
            df.to_csv(output_path, index=False)
            print(f"Processed and saved: {output_path}")
        except Exception as inner_e:
            print(f"Failed to process {file_name} with alternate encoding: {inner_e}")

    except Exception as e:
        print(f"Error processing {file_name}: {e}")



if __name__ == "__main__":
    # Process NBA odds
    clean_odds_data("basketball_nba_odds.csv", "nba_odds_cleaned.csv")

    # Process NFL odds
    clean_odds_data("americanfootball_nfl_odds.csv", "nfl_odds_cleaned.csv")

    # Process NBA injuries
    clean_injury_data("nba_injuries.csv", "nba_injuries_cleaned.csv")

    # Process NFL injuries
    clean_injury_data("nfl_injuries.csv", "nfl_injuries_cleaned.csv")

    # Process NFL games
    process_nfl_data("nfl_spreadspoke_scores.csv", "nfl_games_cleaned.csv")

    # Process NBA games
    process_nba_data("nba_2008-2024.csv", "nba_games_cleaned.csv")

    # Process NFL stadiums
    process_nfl_stadiums("nfl_stadiums.csv", "nfl_stadiums_cleaned.csv")
