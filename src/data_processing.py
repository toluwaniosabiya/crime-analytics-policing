import pandas as pd

from src.constants import COLUMNS_TO_DROP_IF_PRESENT, MONTH_INPUT_FORMAT, TEXT_COLUMNS


def drop_unwanted_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop columns that are not needed for downstream analytics if present.
    """
    columns_to_drop = [col for col in COLUMNS_TO_DROP_IF_PRESENT if col in df.columns]
    return df.drop(columns=columns_to_drop).copy()


def parse_month_column(df: pd.DataFrame, month_column: str = "Month") -> pd.DataFrame:
    """
    Parse the raw month column and derive calendar helper fields.
    """
    result = df.copy()

    if month_column in result.columns:
        result["Month Parsed"] = pd.to_datetime(
            result[month_column],
            format=MONTH_INPUT_FORMAT,
            errors="coerce",
        )
        result["Month Label"] = result["Month Parsed"].dt.strftime("%b %Y")
        result["Year"] = result["Month Parsed"].dt.year
        result["Month Number"] = result["Month Parsed"].dt.month

    return result


def normalize_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Strip surrounding whitespace from configured text columns.
    """
    result = df.copy()

    for col in TEXT_COLUMNS:
        if col in result.columns:
            result[col] = result[col].astype("string").str.strip()

    return result


def clean_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply project-specific missing value handling.
    """
    result = df.copy()

    if "Crime type" in result.columns:
        result = result.dropna(subset=["Crime type"])

    if "Last outcome category" in result.columns:
        result["Last outcome category"] = result["Last outcome category"].fillna(
            "Outcome unknown / not recorded"
        )

    return result


def remove_blank_rows(
    df: pd.DataFrame,
    subset_columns: list[str] | None = None,
) -> pd.DataFrame:
    """
    Remove rows that are effectively blank across key analytical columns.
    """
    result = df.copy()

    if subset_columns is None:
        subset_columns = [
            col
            for col in ["Month", "Crime type", "Longitude", "Latitude", "Location"]
            if col in result.columns
        ]

    if subset_columns:
        result = result.dropna(how="all", subset=subset_columns)

    return result


def coerce_coordinate_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert coordinate fields to numeric types.
    """
    result = df.copy()

    for col in ["Latitude", "Longitude"]:
        if col in result.columns:
            result[col] = pd.to_numeric(result[col], errors="coerce")

    return result


def add_record_count(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a helper column for easy aggregations.
    """
    result = df.copy()
    result["Record Count"] = 1
    return result


def add_crime_id_missing_flag(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a boolean flag for missing Crime IDs.
    """
    result = df.copy()

    if "Crime ID" in result.columns:
        result["Crime ID Missing"] = result["Crime ID"].isna()
    else:
        result["Crime ID Missing"] = True

    return result


def add_district_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Derive a coarse district / area label from LSOA name.
    """
    result = df.copy()

    if "LSOA name" in result.columns:
        district = (
            result["LSOA name"]
            .astype("string")
            .str.extract(r"^([A-Za-z -]+)", expand=False)
            .str.strip()
        )
        result["District"] = district.fillna("Unknown")
    else:
        result["District"] = "Unknown"

    return result


def sort_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sort rows chronologically where parsed month exists.
    """
    result = df.copy()

    if "Month Parsed" in result.columns:
        result = result.sort_values(["Month Parsed"]).reset_index(drop=True)

    return result


def process_crime_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    End-to-end processing pipeline for raw crime data.
    """
    result = df.copy()

    result = drop_unwanted_columns(result)
    result = remove_blank_rows(result)
    result = normalize_text_columns(result)
    result = clean_missing_values(result)
    result = parse_month_column(result)
    result = coerce_coordinate_columns(result)
    result = add_record_count(result)
    result = add_crime_id_missing_flag(result)
    result = add_district_column(result)
    result = sort_by_month(result)

    return result
