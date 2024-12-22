import os
import subprocess

# Directories
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
DATA_GATHERING_DIR = os.path.join(SRC_DIR, "data_gathering")
REQUIREMENTS_FILE = os.path.join(PROJECT_ROOT, "requirements.txt")

# Paths to individual scripts
NFL_SCRIPT = os.path.join(DATA_GATHERING_DIR, "nfl_scraper.py")
NBA_SCRIPT = os.path.join(DATA_GATHERING_DIR, "nba_scraper.py")
CLEANER_SCRIPT = os.path.join(SRC_DIR, "cleaner.py")
DATA_COMBINING_SCRIPT = os.path.join(SRC_DIR, "data_combining.py")
FEATURE_ENGINEER_SCRIPT = os.path.join(SRC_DIR, "feature_engineering.py")
DATA_SPLITTING_SCRIPT = os.path.join(SRC_DIR, "data_splitting.py")

def install_dependencies():
    """
    Install all dependencies from requirements.txt.
    """
    print(f"\n{'=' * 40}")
    print("Installing dependencies from requirements.txt...")
    print(f"{'=' * 40}")

    if not os.path.exists(REQUIREMENTS_FILE):
        print(f"Error: {REQUIREMENTS_FILE} does not exist! Please ensure it is in the project root.")
        exit(1)

    result = subprocess.run(["pip", "install", "-r", REQUIREMENTS_FILE], capture_output=True, text=True)
    if result.returncode == 0:
        print("Dependencies installed successfully.\n")
    else:
        print(f"Error installing dependencies:\n{result.stderr}")
        exit(1)

def run_script(script_path, description):
    """
    Run a Python script and display the status.
    """
    print(f"\n{'=' * 40}")
    print(f"Running: {description}")
    print(f"{'=' * 40}")
    if not os.path.exists(script_path):
        print(f"Error: {script_path} does not exist!")
        exit(1)

    result = subprocess.run(["python", script_path], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"{description} completed successfully.\n")
    else:
        print(f"Error while running {description}:\n{result.stderr}")
        exit(1)

if __name__ == "__main__":
    print(" Starting the Master Pipeline...")

    # Step 0: Install dependencies
    install_dependencies()

    # Step 1: Run NFL Stats Script
    run_script(NFL_SCRIPT, "Combine NFL Stats Script")

    # Step 2: Run NBA Stats Script
    run_script(NBA_SCRIPT, "Combine NBA Stats Script")

    # Step 3: Data Gathering
    for script in os.listdir(DATA_GATHERING_DIR):
        if script.endswith(".py") and script not in {"nfl_scraper.py", "nba_scraper.py"}:
            script_path = os.path.join(DATA_GATHERING_DIR, script)
            run_script(script_path, f"Running {script}")

    # Step 4: Data Cleaning
    run_script(CLEANER_SCRIPT, "Data Cleaning Pipeline")

    # Step 5: Data Combining
    run_script(DATA_COMBINING_SCRIPT, "Data Combining Pipeline")

    # Step 6: Feature Engineering
    # run_script(FEATURE_ENGINEER_SCRIPT, "Feature Engineering Pipeline")

    # Step 7: Data Splitting
    # run_script(DATA_SPLITTING_SCRIPT, "Data Splitting Pipeline")

    print("\n All tasks completed successfully!")
