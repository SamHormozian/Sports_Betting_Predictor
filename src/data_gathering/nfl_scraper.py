import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "../../data/raw")

def scrape_nfl_stats(year):
    """Scrape NFL player statistics from Pro Football Reference for a given year."""
    url = f"https://www.pro-football-reference.com/years/{year}/passing.htm"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve data for {year}")
        return None

    soup = BeautifulSoup(response.content, "lxml")
    table = soup.find("table", {"id": "passing"})

    # Convert the table to a pandas DataFrame
    if table:
        df = pd.read_html(str(table))[0]
        df = df.dropna(subset=["Player"])
        df = df[df["Player"] != "Player"]  # Filter out repeated headers
        df["Year"] = year  # Add a year column to distinguish data
        return df
    else:
        print(f"No data table found for {year}")
        return None

if __name__ == "__main__":
    combined_data = []

    for year in range(2000, 2025):  # Scrape data from 2000 to 2024
        print(f"Scraping data for {year}...")
        yearly_data = scrape_nfl_stats(year)

        if yearly_data is not None:
            combined_data.append(yearly_data)

    if combined_data:
        # Concatenate all yearly DataFrames into one
        final_df = pd.concat(combined_data, ignore_index=True)

        # Save the combined data to a single CSV file
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(OUTPUT_DIR, "nfl_stats_2000_2024.csv")
        final_df.to_csv(output_path, index=False)
        print(f"Combined NFL stats saved to {output_path}")
    else:
        print("No data was scraped.")