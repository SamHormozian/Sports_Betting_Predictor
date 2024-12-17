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
os.makedirs("data/raw/nba", exist_ok=True)

def scrape_nba_injuries():
    url = "https://www.espn.com/nba/injuries"

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
        print("Injury table loaded successfully!")
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
        player = row.select_one(".col-name.Table__TD").text.strip() if row.select_one(".col-name.Table__TD") else "N/A"
        position = row.select_one(".col-pos.Table__TD").text.strip() if row.select_one(".col-pos.Table__TD") else "N/A"
        date = row.select_one(".col-date.Table__TD").text.strip() if row.select_one(".col-date.Table__TD") else "N/A"
        status = row.select_one(".col-stat.Table__TD").text.strip() if row.select_one(".col-stat.Table__TD") else "N/A"
        details = row.select_one(".col-desc.Table__TD").text.strip() if row.select_one(".col-desc.Table__TD") else "N/A"

        injuries.append({
            "player": player,
            "position": position,
            "date": date,
            "status": status,
            "details": details
        })

    # Save data to CSV
    if injuries:
        df = pd.DataFrame(injuries)
        df.to_csv("data/csv/nba/injuries.csv", index=False)
        print("NBA injury data saved to data/raw/nba/injuries.csv")
    else:
        print("No injury data found.")

if __name__ == "__main__":
    scrape_nba_injuries()
