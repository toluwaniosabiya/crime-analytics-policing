import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import streamlit as st

# import plotly.io as pio

from src.config import APP_ICON, APP_LAYOUT, APP_TITLE
from src.dashboard_service import load_dashboard_base_data, build_dashboard_data
from app.components.filters import render_sidebar_filters
from app.components.kpis import render_kpi_row
from app.components.charts import (
    render_crime_heatmap,
    render_crime_type_distribution,
    render_district_crime_mix,
    render_monthly_totals,
    render_monthly_trend_by_crime_type,
    render_outcome_distribution,
    render_top_districts,
    render_top_locations,
)
from app.components.tables import (
    render_data_quality_summary,
    render_filtered_data_preview,
    render_key_takeaways,
)
from app.components.layout import two_column_divider
from app.components.section_headers import render_section_header, render_title_header

# Custom Plotly theme aligned with dashboard color #006e68
# pio.templates["crime_dashboard"] = pio.templates["plotly"]

# pio.templates["crime_dashboard"].layout.update(
#     # Primary color palette used for bars, lines, etc.
#     colorway=[
#         "#006e68",  # primary teal
#         "#2aa198",  # lighter teal
#         "#4DB6AC",  # soft teal
#         "#00897B",  # darker teal
#         "#26A69A",  # secondary teal
#         "#80CBC4",  # pastel teal
#     ],
#     # Chart background styling
#     plot_bgcolor="white",
#     paper_bgcolor="white",
#     # Font styling
#     font=dict(
#         family="sans-serif",
#         color="#1F2937",
#     ),
#     # Grid styling
#     xaxis=dict(
#         gridcolor="#E5E7EB",
#         zeroline=False,
#     ),
#     yaxis=dict(
#         gridcolor="#E5E7EB",
#         zeroline=False,
#     ),
# )

# # Activate the template globally
# pio.templates.default = "crime_dashboard"


@st.cache_data(show_spinner=True)
def load_app_data():
    return load_dashboard_base_data()


def render_header() -> None:
    render_title_header(APP_TITLE)
    st.caption(
        "Interactive crime analytics dashboard built from West Yorkshire street-level crime data."
    )
    st.markdown(
        "Note: Use the filters on the left to explore how crime patterns change across months, locations, and offence categories."
    )

    with st.expander("About this application", expanded=False):
        st.markdown(
            """
            This dashboard explores offence patterns, monthly trends, outcomes,
            and location-level concentration in the West Yorkshire street crime dataset.

            **Architecture**
            - modular data loading
            - schema validation
            - reusable processing pipeline
            - separate analytics layer
            - service-layer orchestration
            - Streamlit presentation components

            **Purpose**
            To demonstrate a production-style analytics application for crime and public-safety data.
            """
        )


def render_sidebar_snapshot(raw_df, processed_df, validation_report) -> None:
    with st.sidebar:
        st.markdown("### Data Snapshot")
        st.write(f"Raw rows: {len(raw_df):,}")
        st.write(f"Processed rows: {len(processed_df):,}")
        st.write(
            f"Missing required columns: {len(validation_report['missing_required_columns'])}"
        )


def render_dashboard_sections(dashboard_data: dict) -> None:

    # KPI SECTION
    render_section_header("Overview")
    render_kpi_row(dashboard_data["kpi_summary"])

    st.markdown("---")

    # DISTRIBUTION SECTION
    render_section_header("Crime Distribution")

    col1, col2 = two_column_divider()

    with col1:
        render_crime_type_distribution(dashboard_data["crime_distribution"])

    with col2:
        render_monthly_totals(dashboard_data["monthly_totals"])

    st.markdown("---")

    # TREND ANALYSIS
    render_section_header("Trend Analysis")

    render_monthly_trend_by_crime_type(dashboard_data["trend_by_crime_type"])

    render_crime_heatmap(dashboard_data["heatmap_data"])

    st.markdown("---")

    # LOCATION ANALYSIS
    render_section_header("Location Insights")

    col5, col6 = two_column_divider()

    with col5:
        render_top_locations(dashboard_data["top_locations"])

    with col6:
        render_outcome_distribution(dashboard_data["outcome_distribution"])

    render_top_districts(dashboard_data["top_districts"])

    render_district_crime_mix(dashboard_data["district_crime_mix"])

    st.markdown("---")

    # INTERPRETATION SECTION
    st.markdown("## Analytical Insights")

    col7, col8 = st.columns(2)

    with col7:
        render_key_takeaways(dashboard_data["takeaways"])

    with col8:
        render_data_quality_summary(dashboard_data["data_quality_summary"])

    st.markdown("---")

    # DATA EXPLORATION
    render_section_header("Filtered Dataset")

    render_filtered_data_preview(dashboard_data["filtered_df"])


def main() -> None:
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout=APP_LAYOUT,
    )

    st.markdown(
        """
    <style>

    h1 {
        color: #4dbeff;
    }

    h2 {
        color: #4dbeff;
    }

    h3 {
        color: #4dbeff;
    }

    </style>
    """,
        unsafe_allow_html=True,
    )

    render_header()

    try:
        raw_df, processed_df, validation_report = load_app_data()
    except FileNotFoundError as exc:
        st.error(f"Data loading error: {exc}")
        st.stop()
    except ValueError as exc:
        st.error(f"Schema validation error: {exc}")
        st.stop()
    except Exception as exc:
        st.error(f"Unexpected application error: {exc}")
        st.stop()

    render_sidebar_snapshot(raw_df, processed_df, validation_report)

    filters = render_sidebar_filters(processed_df)
    dashboard_data = build_dashboard_data(processed_df, filters)

    if dashboard_data["filtered_df"].empty:
        st.warning(
            "No records match the current filter selection. Adjust the filters and try again."
        )
        st.stop()

    render_dashboard_sections(dashboard_data)


if __name__ == "__main__":
    main()
