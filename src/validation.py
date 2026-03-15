from typing import Dict, List

import pandas as pd

from src.constants import MAP_REQUIRED_COLUMNS, REQUIRED_COLUMNS


def get_missing_required_columns(df: pd.DataFrame) -> List[str]:
    """
    Return a list of required columns that are missing from the dataframe.
    """
    return [col for col in REQUIRED_COLUMNS if col not in df.columns]


def validate_required_columns(df: pd.DataFrame) -> None:
    """
    Raise an error if any required columns are missing.
    """
    missing_columns = get_missing_required_columns(df)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def get_null_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a null summary table for all columns.
    """
    summary = pd.DataFrame(
        {
            "column": df.columns,
            "null_count": df.isna().sum().values,
            "null_pct": (df.isna().mean().values * 100).round(2),
            "dtype": df.dtypes.astype(str).values,
        }
    )
    return summary.sort_values(by="null_pct", ascending=False).reset_index(drop=True)


def get_duplicate_row_count(df: pd.DataFrame) -> int:
    """
    Return the number of fully duplicated rows.
    """
    return int(df.duplicated().sum())


def get_duplicate_count_for_columns(df: pd.DataFrame, columns: List[str]) -> int:
    """
    Return duplicate count based on a subset of columns.
    """
    valid_columns = [col for col in columns if col in df.columns]
    if not valid_columns:
        return 0
    return int(df.duplicated(subset=valid_columns).sum())


def get_coordinate_validity_summary(df: pd.DataFrame) -> Dict[str, int]:
    """
    Check presence and basic validity of latitude/longitude columns.
    """
    if not all(col in df.columns for col in MAP_REQUIRED_COLUMNS):
        return {
            "missing_coordinate_columns": 1,
            "missing_latitude_values": 0,
            "missing_longitude_values": 0,
            "invalid_latitude_range": 0,
            "invalid_longitude_range": 0,
        }

    latitude = pd.to_numeric(df["Latitude"], errors="coerce")
    longitude = pd.to_numeric(df["Longitude"], errors="coerce")

    return {
        "missing_coordinate_columns": 0,
        "missing_latitude_values": int(latitude.isna().sum()),
        "missing_longitude_values": int(longitude.isna().sum()),
        "invalid_latitude_range": int(
            ((latitude < -90) | (latitude > 90)).fillna(False).sum()
        ),
        "invalid_longitude_range": int(
            ((longitude < -180) | (longitude > 180)).fillna(False).sum()
        ),
    }


def get_month_parse_failure_count(df: pd.DataFrame, month_column: str = "Month") -> int:
    """
    Count how many month values fail datetime parsing using the expected format YYYY-MM.
    """
    if month_column not in df.columns:
        return len(df)

    parsed = pd.to_datetime(df[month_column], format="%Y-%m", errors="coerce")
    return int(parsed.isna().sum())


def build_validation_report(df: pd.DataFrame) -> Dict[str, object]:
    """
    Build a compact validation report dictionary for logging or display.
    """
    missing_columns = get_missing_required_columns(df)

    report = {
        "row_count": int(len(df)),
        "column_count": int(df.shape[1]),
        "missing_required_columns": missing_columns,
        "duplicate_rows": get_duplicate_row_count(df),
        "duplicate_month_location_crime_rows": get_duplicate_count_for_columns(
            df, ["Month", "Location", "Crime type"]
        ),
        "month_parse_failures": get_month_parse_failure_count(df),
        "coordinate_summary": get_coordinate_validity_summary(df),
        "null_summary": get_null_summary(df),
    }
    return report
