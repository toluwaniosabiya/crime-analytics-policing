from typing import Dict, List, Tuple

import pandas as pd

from src.data_loading import load_raw_crime_data
from src.data_processing import process_crime_data
from src.validation import build_validation_report, validate_required_columns
from src.analytics import (
    build_kpi_summary,
    build_key_takeaways,
    get_crime_heatmap_data,
    get_crime_type_distribution,
    get_data_quality_summary,
    get_monthly_totals,
    get_monthly_trend_by_crime_type,
    get_outcome_distribution,
    get_top_districts,
    get_top_locations,
    get_district_crime_mix,
)


def load_dashboard_base_data() -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, object]]:
    """
    Load raw data, validate schema, process records, and return
    raw data, processed data, and a validation report.
    """
    raw_df = load_raw_crime_data()
    validate_required_columns(raw_df)
    processed_df = process_crime_data(raw_df)
    validation_report = build_validation_report(raw_df)

    return raw_df, processed_df, validation_report


def apply_dashboard_filters(
    df: pd.DataFrame,
    months: List[str] | None = None,
    crime_types: List[str] | None = None,
    outcome_categories: List[str] | None = None,
    districts: List[str] | None = None,
) -> pd.DataFrame:
    """
    Apply dashboard filters to a processed dataframe.
    """
    result = df.copy()

    if months and "Month Label" in result.columns:
        result = result[result["Month Label"].isin(months)]

    if crime_types and "Crime type" in result.columns:
        result = result[result["Crime type"].isin(crime_types)]

    if outcome_categories and "Last outcome category" in result.columns:
        result = result[result["Last outcome category"].isin(outcome_categories)]

    if districts and "District" in result.columns:
        result = result[result["District"].isin(districts)]

    return result.reset_index(drop=True)


def build_dashboard_outputs(filtered_df: pd.DataFrame) -> Dict[str, object]:
    """
    Build all chart-ready, KPI-ready, and table-ready outputs
    for the Streamlit dashboard.
    """
    return {
        "filtered_df": filtered_df,
        "kpi_summary": build_kpi_summary(filtered_df),
        "crime_distribution": get_crime_type_distribution(filtered_df),
        "monthly_totals": get_monthly_totals(filtered_df),
        "trend_by_crime_type": get_monthly_trend_by_crime_type(filtered_df),
        "heatmap_data": get_crime_heatmap_data(filtered_df),
        "outcome_distribution": get_outcome_distribution(filtered_df),
        "top_locations": get_top_locations(filtered_df),
        "top_districts": get_top_districts(filtered_df),
        "district_crime_mix": get_district_crime_mix(filtered_df),
        "data_quality_summary": get_data_quality_summary(filtered_df),
        "takeaways": build_key_takeaways(filtered_df),
    }


def build_dashboard_data(
    processed_df: pd.DataFrame,
    filters: Dict[str, List[str]],
) -> Dict[str, object]:
    """
    Apply filters and return the full dashboard payload.
    """
    filtered_df = apply_dashboard_filters(
        processed_df,
        months=filters.get("months"),
        crime_types=filters.get("crime_types"),
        outcome_categories=filters.get("outcome_categories"),
        districts=filters.get("districts"),
    )

    return build_dashboard_outputs(filtered_df)
