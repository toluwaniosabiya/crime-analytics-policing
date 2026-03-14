from pathlib import Path


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Other project directories
APP_DIR = PROJECT_ROOT / "app"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
REPORTS_DIR = PROJECT_ROOT / "reports"
TESTS_DIR = PROJECT_ROOT / "tests"

# File patterns
RAW_CSV_GLOB = "*/**/*.csv"

# Default app settings
APP_TITLE = "West Yorkshire Crime Analytics Dashboard"
APP_ICON = "🚓"
APP_LAYOUT = "wide"

# Cached / derived files
MERGED_RAW_FILE = INTERIM_DATA_DIR / "merged_crime_data.csv"
PROCESSED_CRIME_FILE = PROCESSED_DATA_DIR / "processed_crime_data.csv"
