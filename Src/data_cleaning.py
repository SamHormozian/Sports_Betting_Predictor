import pandas as pd
import os


#-----------------------------------------LOAD DATA------------------------------------------------------------------------
# Path to CSV files
csv_root = "Data/csv"

# Dictionary to store combined DataFrames for each sport
sports_data = {}

# Loop through every sport folder
for sport in os.listdir(csv_root):
    sports_folder = os.path.join(csv_root, sport)

    if os.path.isdir(sports_folder):
        sport_dfs = []  # List to store DataFrames for each sport

        # Loop through all CSV files in the sport folder
        for file in os.listdir(sports_folder):
            if file.endswith(".csv"):
                file_path = os.path.join(sports_folder, file)
                print(f"Loading Data from: {file_path}")

                # Read CSV
                df = pd.read_csv(file_path)
                sport_dfs.append(df)

        # Combine all files for the sport into a single DataFrame
        if sport_dfs:
            combined_df = pd.concat(sport_dfs, ignore_index=True)
            sports_data[sport] = combined_df

# Print summary AFTER all sports are loaded
print("\nSummary of Loaded Sport Data:")
for sport, df in sports_data.items():
    print(f"{sport.capitalize()}: {df.shape[0]} rows, {df.shape[1]} columns")

#--------------------------------CLEANING DATA-------------------------------------------------
#check for missing values in each sport
for sport, df in sports_data.items():
    # Fill missing numerical values with median
    for col in df.select_dtypes(include=["int64", "float64"]).columns:
        df[col] = df[col].fillna(df[col].median())

    # Fill missing categorical values with "N/A"
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].fillna("N/A")

    sports_data[sport] = df  # Update cleaned DataFrame
    print(f"Cleaned missing data for {sport.capitalize()}.")

#--------------------Feature Engineering--------------------------------------------------------
