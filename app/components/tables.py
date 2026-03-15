from typing import Dict

import pandas as pd
import streamlit as st


def render_key_takeaways(takeaways: Dict[str, str]) -> None:
    """
    Render narrative dashboard takeaways.
    """
    st.subheader("Key Takeaways")

    notes = [
        f"**{takeaways.get('top_crime_type', 'N/A')}** is the most frequent crime category in the current selection.",
        f"The peak month is **{takeaways.get('peak_month', 'N/A')}** with **{takeaways.get('peak_month_incidents', '0')} incidents**.",
        f"The most common recorded outcome category is **{takeaways.get('top_outcome', 'N/A')}**.",
        f"The highest-volume location in the current selection is **{takeaways.get('top_location', 'N/A')}**.",
    ]

    for note in notes:
        st.markdown(f"- {note}")


def render_data_quality_summary(summary: Dict[str, int]) -> None:
    """
    Render compact data quality metrics.
    """
    st.subheader("Data Quality Summary")

    quality_df = pd.DataFrame(
        {
            "Metric": [
                "Row count",
                "Duplicate rows",
                "Missing crime type",
                "Missing location",
                "Missing outcome",
                "Missing latitude",
                "Missing longitude",
            ],
            "Value": [
                summary.get("row_count", 0),
                summary.get("duplicate_rows", 0),
                summary.get("missing_crime_type", 0),
                summary.get("missing_location", 0),
                summary.get("missing_outcome", 0),
                summary.get("missing_latitude", 0),
                summary.get("missing_longitude", 0),
            ],
        }
    )

    st.dataframe(quality_df, use_container_width=True, hide_index=True)


def render_filtered_data_preview(df: pd.DataFrame, max_rows: int = 250) -> None:
    """
    Render a preview of filtered records.
    """
    st.subheader("Filtered Data Preview")

    if df.empty:
        st.info("No records available for the current filter selection.")
        return

    preview_columns = [
        col
        for col in [
            "Month Label",
            "Crime type",
            "Location",
            "District",
            "Last outcome category",
            "Crime ID",
            "Latitude",
            "Longitude",
        ]
        if col in df.columns
    ]

    st.dataframe(
        df[preview_columns].head(max_rows),
        use_container_width=True,
        hide_index=True,
    )
