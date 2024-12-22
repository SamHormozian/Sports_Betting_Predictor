import os
import pandas as pd

# Define the raw data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "training_data")

def preview_datasets(data_dir):
    """
    Display column names and the first 5 rows of each dataset in the specified directory.

    Args:
        data_dir (str): Path to the directory containing datasets.
    """
    if not os.path.exists(data_dir):
        print(f"Error: The directory {data_dir} does not exist!")
        return

    # List all files in the directory
    files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]

    if not files:
        print(f"No CSV files found in {data_dir}.")
        return

    # Loop through each file and display column names and first 5 rows
    for file in files:
        file_path = os.path.join(data_dir, file)
        print(f"\n{'=' * 40}")
        print(f"Previewing dataset: {file}")
        print(f"{'=' * 40}")

        try:
            # Load the dataset
            df = pd.read_csv(file_path)

            # Display columns
            print("Columns:")
            print(df.columns.tolist())

            # Display first 5 rows
            print("\nFirst 5 rows:")
            print(df.head())

        except Exception as e:
            print(f"Error reading {file}: {e}")

if __name__ == "__main__":
    preview_datasets(DATA_DIR)
