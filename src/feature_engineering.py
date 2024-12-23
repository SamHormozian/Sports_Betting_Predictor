import pandas as pd
import os

# Define directories
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "feature_engineered_data")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "cleaned")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_dataset(df, drop_threshold=0.9):
    """
    Impute numerical values and drop features with excessive missing values.
    """
    # Calculate the missing value ratio
    missing_ratio = df.isnull().sum() / len(df)

    # Drop features with missing ratio greater than the threshold
    drop_cols = missing_ratio[missing_ratio > drop_threshold].index.tolist()
    df = df.drop(columns=drop_cols)
    print(f"Dropped columns: {drop_cols}")

    # Impute numerical features
    for col in df.select_dtypes(include=["float64", "int64"]).columns:
        if df[col].isnull().sum() > 0:
            # Use median for imputation
            df[col].fillna(df[col].median(), inplace=True)

    return df

def process_nba_data():
    print("Processing NBA feature-engineered data...")
    nba_file_path = os.path.join(DATA_DIR, "nba_feature_engineered.csv")
    nba_data = pd.read_csv(nba_file_path)

    nba_cleaned = clean_dataset(nba_data)
    output_path = os.path.join(OUTPUT_DIR, "nba_cleaned.csv")
    nba_cleaned.to_csv(output_path, index=False)
    print(f"Cleaned NBA data saved to {output_path}")

def process_nfl_data():
    print("Processing NFL feature-engineered data...")
    nfl_file_path = os.path.join(DATA_DIR, "nfl_feature_engineered.csv")
    nfl_data = pd.read_csv(nfl_file_path)

    nfl_cleaned = clean_dataset(nfl_data)
    output_path = os.path.join(OUTPUT_DIR, "nfl_cleaned.csv")
    nfl_cleaned.to_csv(output_path, index=False)
    print(f"Cleaned NFL data saved to {output_path}")

if __name__ == "__main__":
    process_nba_data()
    process_nfl_data()
