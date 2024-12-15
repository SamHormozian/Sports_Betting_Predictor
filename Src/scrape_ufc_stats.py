from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import os
import string
from webdriver_manager.chrome import ChromeDriverManager

# Create directory to store UFC data
os.makedirs("data/raw/ufc", exist_ok=True)

def scrape_ufc_stats():
    base_url = "http://ufcstats.com/statistics/fighters?char={}"
    all_fighters = []  # List to store all fighter data

    # Set up Chrome options for headless browsing
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # Launch the browser
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Loop through all letters of the alphabet
    for letter in string.ascii_lowercase:
        url = base_url.format(letter)
        print(f"Scraping data for letter '{letter.upper()}' at {url}")
        driver.get(url)

        try:
            # Allow time for the page to load
            driver.implicitly_wait(5)
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Locate the table
            table = soup.find("table", {"class": "b-statistics__table"})
            if table:
                rows = table.find("tbody").find_all("tr")
                print(f"Found {len(rows)} rows for letter '{letter.upper()}'")

                for row in rows:
                    cells = row.find_all("td")
                    if len(cells) >= 7:  # Ensure the row contains enough columns
                        all_fighters.append({
                            "Name": cells[1].text.strip(),
                            "Height": cells[2].text.strip(),
                            "Weight": cells[3].text.strip(),
                            "Reach": cells[4].text.strip(),
                            "Stance": cells[5].text.strip(),
                            "Wins": cells[6].text.strip(),
                            "Losses": cells[7].text.strip(),
                            "Draws": cells[8].text.strip()
                        })
            else:
                print(f"No data found for letter '{letter.upper()}'")
        except Exception as e:
            print(f"Error while processing letter '{letter.upper()}': {e}")

    # Close the browser
    driver.quit()

    # Save all data to a CSV file
    if all_fighters:
        df = pd.DataFrame(all_fighters)
        df.to_csv("data/raw/ufc/ufc_fighter_stats.csv", index=False)
        print("UFC fighter stats saved to data/raw/ufc/ufc_fighter_stats.csv")
    else:
        print("No fighter data was found to save.")

if __name__ == "__main__":
    scrape_ufc_stats()
