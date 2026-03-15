from typing import Dict

import streamlit as st


def render_kpi_row(kpi_summary: Dict[str, int]) -> None:
    """
    Render the top-level KPI cards for the dashboard.
    """
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Incidents", f"{kpi_summary.get('total_incidents', 0):,}")

    with col2:
        st.metric("Crime Categories", f"{kpi_summary.get('unique_crime_types', 0):,}")

    with col3:
        st.metric("Locations", f"{kpi_summary.get('unique_locations', 0):,}")

    with col4:
        st.metric("Missing Crime IDs", f"{kpi_summary.get('missing_crime_ids', 0):,}")

    with col5:
        st.metric("Months Covered", f"{kpi_summary.get('months_covered', 0):,}")
