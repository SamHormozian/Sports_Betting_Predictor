import os

def run_script(script_name):
    print(f"\nRunning {script_name}...")
    result = os.system(f"python {script_name}")
    if result == 0:
        print(f"{script_name} completed successfully!")
    else:
        print(f"Error: {script_name} failed to run. Check for issues.")

def main():
    print("Starting all scraping and API fetch scripts...\n")

    # List of all scripts to execute
    scripts = [
        "fetch_mlb_data.py",
        "fetch_nba_data.py",
        "fetch_nfl_data.py",
        "fetch_nhl_data.py",
        "fetch_soccer_data.py",
        "scrape_nba_injuries.py",
        "scrape_nfl_injuries.py",
        "scrape_ufc_stats.py"
    ]

    # Run each script
    for script in scripts:
        run_script(script)

    print("\nAll scraping and API scripts have been executed!")

if __name__ == "__main__":
    main()
