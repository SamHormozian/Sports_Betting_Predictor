from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import os
from webdriver_manager.chrome import ChromeDriverManager

# Create directory to store data
os.makedirs("data/raw/nfl", exist_ok=True)

def scrape_nfl_injuries():
    url = "https://www.espn.com/nfl/injuries"

    # Set up Chrome options for headless browsing
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # Launch the browser
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    # Wait for table to load
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "Table"))
        )
        print("NFL injury table loaded successfully!")
    except:
        print("Timeout: Table did not load.")
        driver.quit()
        return

    # Parse page source
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    # Extract injury table
    injuries = []
    rows = soup.select(".Table__TR")
    print(f"Number of rows found: {len(rows)}")

    for row in rows:
        team = row.select_one(".col-team.Table__TD").text.strip() if row.select_one(".col-team.Table__TD") else "N/A"
        player = row.select_one(".col-name.Table__TD").text.strip() if row.select_one(".col-name.Table__TD") else "N/A"
        position = row.select_one(".col-pos.Table__TD").text.strip() if row.select_one(".col-pos.Table__TD") else "N/A"
        injury = row.select_one(".col-desc.Table__TD").text.strip() if row.select_one(".col-desc.Table__TD") else "N/A"
        status = row.select_one(".col-stat.Table__TD").text.strip() if row.select_one(".col-stat.Table__TD") else "N/A"

        injuries.append({
            "team": team,
            "player": player,
            "position": position,
            "injury": injury,
            "status": status
        })

    # Save data to CSV
    if injuries:
        df = pd.DataFrame(injuries)
        df.to_csv("data/csv/nfl/nfl_injuries.csv", index=False)
        print("NFL injury data saved to data/raw/nfl/nfl_injuries.csv")
    else:
        print("No injury data found.")

if __name__ == "__main__":
    scrape_nfl_injuries()
