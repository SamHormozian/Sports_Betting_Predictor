import pandas as pd
import os
from sklearn.model_selection import train_test_split

# Define directories
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FEATURE_ENGINEERED_DIR = os.path.join(PROJECT_ROOT, "data", "feature_engineered_data")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "splits")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def bin_score_diff(score_diff):
    """
    Bin the score difference into categories for stratified splitting.
    """
    if score_diff < -10:
        return 'Large Loss'
    elif -10 <= score_diff < 0:
        return 'Small Loss'
    elif score_diff == 0:
        return 'Draw'
    elif 0 < score_diff <= 10:
        return 'Small Win'
    else:
        return 'Large Win'

def ensure_minimum_class_size(df, column, min_size=2):
    """
    Ensure that each class in the column has at least `min_size` members.
    Combine smaller classes into an 'Other' category or merge into neighboring classes.
    """
    class_counts = df[column].value_counts()
    rare_classes = class_counts[class_counts < min_size].index

    if len(rare_classes) > 0:
        print(f"Rare classes detected in '{column}': {rare_classes.tolist()}.")
        df[column] = df[column].apply(lambda x: 'Other' if x in rare_classes else x)

    # Check if "Other" is still too small and merge it into a meaningful class
    class_counts = df[column].value_counts()
    if "Other" in class_counts and class_counts["Other"] < min_size:
        # Merge "Other" into the most populated class
        most_populated_class = class_counts[class_counts.index != "Other"].idxmax()
        df[column] = df[column].replace("Other", most_populated_class)
        print(f"'Other' merged into '{most_populated_class}' due to insufficient members.")

    return df

def impute_and_remove_missing_columns(df):
    """
    Impute partially missing columns and remove entirely missing columns.
    """
    # Drop columns with all missing values
    df.dropna(axis=1, how='all', inplace=True)

    # Impute missing numerical values with the mean
    numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
    for col in numerical_columns:
        if df[col].isnull().any():
            df[col].fillna(df[col].mean(), inplace=True)

    # Impute missing categorical values with the mode
    categorical_columns = df.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        if df[col].isnull().any():
            df[col].fillna(df[col].mode()[0], inplace=True)

    return df

def split_data(df, target_col, test_size=0.2, val_size=0.1, random_state=42):
    """
    Split the dataset into training, validation, and testing sets.
    """
    train_val, test = train_test_split(df, test_size=test_size, random_state=random_state, stratify=df[target_col])
    train, val = train_test_split(
        train_val, test_size=val_size / (1 - test_size), random_state=random_state, stratify=train_val[target_col]
    )
    return train, val, test

def save_splits(train, val, test, prefix):
    """
    Save the split datasets to CSV files.
    """
    train.to_csv(os.path.join(OUTPUT_DIR, f"{prefix}_train.csv"), index=False)
    val.to_csv(os.path.join(OUTPUT_DIR, f"{prefix}_val.csv"), index=False)
    test.to_csv(os.path.join(OUTPUT_DIR, f"{prefix}_test.csv"), index=False)
    print(f"Data splits saved for {prefix}: train, validation, and test.")

def process_nba_splits():
    print("Processing NBA data splits...")
    nba_file = os.path.join(FEATURE_ENGINEERED_DIR, "nba_feature_engineered.csv")

    if not os.path.exists(nba_file):
        print(f"Error: {nba_file} does not exist. Please ensure the file is in the correct directory.")
        return

    nba_data = pd.read_csv(nba_file)

    # Impute and remove missing columns
    nba_data = impute_and_remove_missing_columns(nba_data)

    # Bin the score_diff column for stratification
    nba_data["score_diff_bin"] = nba_data["score_diff"].apply(bin_score_diff)

    # Ensure minimum class size for stratification
    nba_data = ensure_minimum_class_size(nba_data, "score_diff_bin")

    # Use the binned column as the target for stratification
    target_col = "score_diff_bin"
    train, val, test = split_data(nba_data, target_col)
    save_splits(train, val, test, "nba")

def process_nfl_splits():
    print("Processing NFL data splits...")
    nfl_file = os.path.join(FEATURE_ENGINEERED_DIR, "nfl_feature_engineered.csv")

    if not os.path.exists(nfl_file):
        print(f"Error: {nfl_file} does not exist. Please ensure the file is in the correct directory.")
        return

    nfl_data = pd.read_csv(nfl_file)

    # Impute and remove missing columns
    nfl_data = impute_and_remove_missing_columns(nfl_data)

    # Bin the score_diff column for stratification
    nfl_data["score_diff_bin"] = nfl_data["score_diff"].apply(bin_score_diff)

    # Ensure minimum class size for stratification
    nfl_data = ensure_minimum_class_size(nfl_data, "score_diff_bin")

    # Use the binned column as the target for stratification
    target_col = "score_diff_bin"
    train, val, test = split_data(nfl_data, target_col)
    save_splits(train, val, test, "nfl")

if __name__ == "__main__":
    process_nba_splits()
    process_nfl_splits()
