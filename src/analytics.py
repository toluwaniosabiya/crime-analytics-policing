from typing import Dict

import pandas as pd

from src.constants import MAP_SAMPLE_SIZE, TOP_N_DEFAULT


def get_total_incidents(df: pd.DataFrame) -> int:
    """
    Return the total incident count.
    """
    if "Record Count" not in df.columns:
        return int(len(df))
    return int(df["Record Count"].sum())


def get_unique_crime_types(df: pd.DataFrame) -> int:
    """
    Return the number of unique crime categories.
    """
    if "Crime type" not in df.columns:
        return 0
    return int(df["Crime type"].nunique())


def get_unique_locations(df: pd.DataFrame) -> int:
    """
    Return the number of unique locations.
    """
    if "Location" not in df.columns:
        return 0
    return int(df["Location"].nunique())


def get_missing_crime_id_count(df: pd.DataFrame) -> int:
    """
    Return the number of rows with missing Crime IDs.
    """
    if "Crime ID Missing" in df.columns:
        return int(df["Crime ID Missing"].sum())
    if "Crime ID" in df.columns:
        return int(df["Crime ID"].isna().sum())
    return int(len(df))


def get_months_covered(df: pd.DataFrame) -> int:
    """
    Return the number of unique month labels in the dataframe.
    """
    if "Month Label" not in df.columns:
        return 0
    return int(df["Month Label"].nunique())


def build_kpi_summary(df: pd.DataFrame) -> Dict[str, int]:
    """
    Build a dictionary of top-level KPI values for the dashboard.
    """
    return {
        "total_incidents": get_total_incidents(df),
        "unique_crime_types": get_unique_crime_types(df),
        "unique_locations": get_unique_locations(df),
        "missing_crime_ids": get_missing_crime_id_count(df),
        "months_covered": get_months_covered(df),
    }


def get_crime_type_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return chart-ready crime category counts.
    """
    if "Crime type" not in df.columns:
        return pd.DataFrame(columns=["Crime type", "Incidents"])

    return (
        df.groupby("Crime type", as_index=False)["Record Count"]
        .sum()
        .rename(columns={"Record Count": "Incidents"})
        .sort_values("Incidents", ascending=False)
        .reset_index(drop=True)
    )


def get_monthly_totals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return total incidents per month.
    """
    required_cols = {"Month Parsed", "Month Label", "Record Count"}
    if not required_cols.issubset(df.columns):
        return pd.DataFrame(columns=["Month Parsed", "Month Label", "Incidents"])

    return (
        df.groupby(["Month Parsed", "Month Label"], as_index=False)["Record Count"]
        .sum()
        .rename(columns={"Record Count": "Incidents"})
        .sort_values("Month Parsed")
        .reset_index(drop=True)
    )


def get_monthly_trend_by_crime_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return monthly incidents split by crime type.
    """
    required_cols = {"Month Parsed", "Month Label", "Crime type", "Record Count"}
    if not required_cols.issubset(df.columns):
        return pd.DataFrame(
            columns=["Month Parsed", "Month Label", "Crime type", "Incidents"]
        )

    return (
        df.groupby(["Month Parsed", "Month Label", "Crime type"], as_index=False)[
            "Record Count"
        ]
        .sum()
        .rename(columns={"Record Count": "Incidents"})
        .sort_values(["Month Parsed", "Crime type"])
        .reset_index(drop=True)
    )


def get_crime_heatmap_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return matrix-style data for crime counts by month.
    """
    trend_df = get_monthly_trend_by_crime_type(df)
    if trend_df.empty:
        return pd.DataFrame()

    return (
        trend_df.pivot(index="Crime type", columns="Month Label", values="Incidents")
        .fillna(0)
        .sort_index()
    )


def get_outcome_distribution(
    df: pd.DataFrame, top_n: int = TOP_N_DEFAULT
) -> pd.DataFrame:
    """
    Return top outcome categories by incident count.
    """
    if "Last outcome category" not in df.columns:
        return pd.DataFrame(columns=["Last outcome category", "Incidents"])

    return (
        df.groupby("Last outcome category", as_index=False)["Record Count"]
        .sum()
        .rename(columns={"Record Count": "Incidents"})
        .sort_values("Incidents", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


def get_top_locations(df: pd.DataFrame, top_n: int = TOP_N_DEFAULT) -> pd.DataFrame:
    """
    Return top locations by incident count.
    """
    if "Location" not in df.columns:
        return pd.DataFrame(columns=["Location", "Incidents"])

    return (
        df.groupby("Location", as_index=False)["Record Count"]
        .sum()
        .rename(columns={"Record Count": "Incidents"})
        .sort_values("Incidents", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


def get_top_districts(df: pd.DataFrame, top_n: int = TOP_N_DEFAULT) -> pd.DataFrame:
    """
    Return top districts / areas by incident count.
    """
    if "District" not in df.columns:
        return pd.DataFrame(columns=["District", "Incidents"])

    return (
        df.groupby("District", as_index=False)["Record Count"]
        .sum()
        .rename(columns={"Record Count": "Incidents"})
        .sort_values("Incidents", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


def get_data_quality_summary(df: pd.DataFrame) -> Dict[str, int]:
    """
    Return a compact data quality summary for the dashboard.
    """
    summary = {
        "row_count": int(len(df)),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_crime_type": (
            int(df["Crime type"].isna().sum()) if "Crime type" in df.columns else 0
        ),
        "missing_location": (
            int(df["Location"].isna().sum()) if "Location" in df.columns else 0
        ),
        "missing_outcome": (
            int(df["Last outcome category"].isna().sum())
            if "Last outcome category" in df.columns
            else 0
        ),
        "missing_latitude": (
            int(df["Latitude"].isna().sum()) if "Latitude" in df.columns else 0
        ),
        "missing_longitude": (
            int(df["Longitude"].isna().sum()) if "Longitude" in df.columns else 0
        ),
    }
    return summary


def build_key_takeaways(df: pd.DataFrame) -> Dict[str, str]:
    """
    Return simple dashboard narrative takeaways based on the current filtered data.
    """
    takeaways = {
        "top_crime_type": "N/A",
        "peak_month": "N/A",
        "peak_month_incidents": "0",
        "top_outcome": "N/A",
        "top_location": "N/A",
    }

    crime_dist = get_crime_type_distribution(df)
    monthly_totals = get_monthly_totals(df)
    outcome_dist = get_outcome_distribution(df, top_n=1)
    top_locations = get_top_locations(df, top_n=1)

    if not crime_dist.empty:
        takeaways["top_crime_type"] = str(crime_dist.iloc[0]["Crime type"])

    if not monthly_totals.empty:
        peak_row = monthly_totals.sort_values("Incidents", ascending=False).iloc[0]
        takeaways["peak_month"] = str(peak_row["Month Label"])
        takeaways["peak_month_incidents"] = f"{int(peak_row['Incidents']):,}"

    if not outcome_dist.empty:
        takeaways["top_outcome"] = str(outcome_dist.iloc[0]["Last outcome category"])

    if not top_locations.empty:
        takeaways["top_location"] = str(top_locations.iloc[0]["Location"])

    return takeaways
