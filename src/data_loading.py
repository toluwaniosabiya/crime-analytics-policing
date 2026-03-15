from pathlib import Path
from typing import List, Optional

import pandas as pd

from src.config import RAW_DATA_DIR, MERGED_RAW_FILE


def discover_csv_files(raw_data_dir: Path = RAW_DATA_DIR) -> List[Path]:
    """
    Recursively discover all CSV files inside the raw data directory.
    Returns a sorted list for deterministic loading.
    """
    return sorted(raw_data_dir.rglob("*.csv"))


def read_csv_file(file_path: Path) -> pd.DataFrame:
    """
    Read a single CSV file and append source metadata.
    """
    df = pd.read_csv(file_path)
    df["source_file"] = file_path.name
    df["source_folder"] = file_path.parent.name
    return df


def load_raw_crime_data(raw_data_dir: Path = RAW_DATA_DIR) -> pd.DataFrame:
    """
    Load and concatenate all raw crime CSV files into one dataframe.
    """
    csv_files = discover_csv_files(raw_data_dir)

    if not csv_files:
        raise FileNotFoundError(
            f"No CSV files found under raw data directory: {raw_data_dir}"
        )

    frames = [read_csv_file(file_path) for file_path in csv_files]
    combined_df = pd.concat(frames, ignore_index=True)

    return combined_df


def save_merged_raw_data(
    df: pd.DataFrame,
    output_path: Path = MERGED_RAW_FILE,
    index: bool = False,
) -> Path:
    """
    Save the merged raw dataframe to the interim directory.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=index)
    return output_path


def load_and_optionally_save_raw_data(
    raw_data_dir: Path = RAW_DATA_DIR,
    save_output: bool = False,
    output_path: Optional[Path] = None,
) -> pd.DataFrame:
    """
    Convenience wrapper to load all raw data and optionally persist it.
    """
    df = load_raw_crime_data(raw_data_dir)

    if save_output:
        save_merged_raw_data(df, output_path=output_path or MERGED_RAW_FILE)

    return df
