from typing import Dict, List

import pandas as pd
import streamlit as st


def _get_sorted_unique_values(df: pd.DataFrame, column: str) -> List[str]:
    """
    Return sorted unique non-null values from a column.
    """
    if column not in df.columns:
        return []
    return sorted(df[column].dropna().astype(str).unique().tolist())


def render_sidebar_filters(df: pd.DataFrame) -> Dict[str, List[str]]:
    """
    Render sidebar filters and return selected values.
    """
    st.sidebar.header("Filters")

    month_options = _get_sorted_unique_values(df, "Month Label")
    crime_options = _get_sorted_unique_values(df, "Crime type")
    outcome_options = _get_sorted_unique_values(df, "Last outcome category")
    district_options = _get_sorted_unique_values(df, "District")

    selected_months = st.sidebar.multiselect(
        "Months",
        options=month_options,
        default=month_options,
    )

    selected_crimes = st.sidebar.multiselect(
        "Crime types",
        options=crime_options,
        default=crime_options,
    )

    selected_outcomes = st.sidebar.multiselect(
        "Outcome categories",
        options=outcome_options,
        default=outcome_options,
    )

    selected_districts = st.sidebar.multiselect(
        "Districts / areas",
        options=district_options,
        default=district_options,
    )

    return {
        "months": selected_months,
        "crime_types": selected_crimes,
        "outcome_categories": selected_outcomes,
        "districts": selected_districts,
    }


def apply_filters(df: pd.DataFrame, filters: Dict[str, List[str]]) -> pd.DataFrame:
    """
    Apply sidebar filter selections to the dataframe.
    """
    result = df.copy()

    if "Month Label" in result.columns and filters.get("months"):
        result = result[result["Month Label"].isin(filters["months"])]

    if "Crime type" in result.columns and filters.get("crime_types"):
        result = result[result["Crime type"].isin(filters["crime_types"])]

    if "Last outcome category" in result.columns and filters.get("outcome_categories"):
        result = result[
            result["Last outcome category"].isin(filters["outcome_categories"])
        ]

    if "District" in result.columns and filters.get("districts"):
        result = result[result["District"].isin(filters["districts"])]

    return result.reset_index(drop=True)
