from typing import Dict

import streamlit as st


import streamlit as st


def render_kpi_row(kpi_summary: dict) -> None:
    """
    Render KPI cards styled like flashcards.
    """

    st.markdown(
        """
        <style>
        .kpi-card {
            background-color: #F7F9FC;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #E5EAF0;
            text-align: center;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
        }

        .kpi-title {
            font-size: 14px;
            color: #6B7280;
            margin-bottom: 6px;
        }

        .kpi-value {
            font-size: 28px;
            font-weight: 700;
            color: #1F2937;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Incidents</div>
                <div class="kpi-value">{kpi_summary.get('total_incidents',0):,}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Crime Categories</div>
                <div class="kpi-value">{kpi_summary.get('unique_crime_types',0)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Locations</div>
                <div class="kpi-value">{kpi_summary.get('unique_locations',0):,}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Missing Crime IDs</div>
                <div class="kpi-value">{kpi_summary.get('missing_crime_ids',0)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col5:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Months Covered</div>
                <div class="kpi-value">{kpi_summary.get('months_covered',0)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
