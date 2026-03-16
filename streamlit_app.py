import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import streamlit as st

from src.config import APP_ICON, APP_LAYOUT, APP_TITLE
from src.dashboard_service import load_dashboard_base_data, build_dashboard_data
from app.components.filters import render_sidebar_filters
from app.components.kpis import render_kpi_row
from app.components.charts import (
    render_crime_heatmap,
    render_crime_type_distribution,
    render_map,
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


@st.cache_data(show_spinner=True)
def load_app_data():
    return load_dashboard_base_data()


def render_header() -> None:
    st.title(APP_TITLE)
    st.caption(
        "Interactive crime analytics dashboard built from West Yorkshire street-level crime data."
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
    render_kpi_row(dashboard_data["kpi_summary"])

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        render_crime_type_distribution(dashboard_data["crime_distribution"])
    with col2:
        render_monthly_totals(dashboard_data["monthly_totals"])

    col3, col4 = st.columns(2)
    with col3:
        render_monthly_trend_by_crime_type(dashboard_data["trend_by_crime_type"])
    with col4:
        render_crime_heatmap(dashboard_data["heatmap_data"])

    col5, col6 = st.columns(2)
    with col5:
        render_outcome_distribution(dashboard_data["outcome_distribution"])
    with col6:
        render_top_locations(dashboard_data["top_locations"])

    render_top_districts(dashboard_data["top_districts"])

    # Re-enable after map debugging
    #### Debugging Map #####
    st.markdown("### Map Debug")

    map_df = dashboard_data["map_data"]

    st.write("map_df shape:", map_df.shape)
    st.write("map_df columns:", map_df.columns.tolist())

    if not map_df.empty:
        st.write("Latitude dtype:", map_df["Latitude"].dtype)
        st.write("Longitude dtype:", map_df["Longitude"].dtype)
        st.write("Latitude nulls:", int(map_df["Latitude"].isna().sum()))
        st.write("Longitude nulls:", int(map_df["Longitude"].isna().sum()))
        st.write(
            "Latitude min/max:",
            float(map_df["Latitude"].min()),
            float(map_df["Latitude"].max()),
        )
        st.write(
            "Longitude min/max:",
            float(map_df["Longitude"].min()),
            float(map_df["Longitude"].max()),
        )
        st.dataframe(map_df[["Latitude", "Longitude"]].head(20))

        st.write("map_df shape:", map_df.shape)

        if not map_df.empty:
            st.write(
                "Latitude min/max:",
                float(map_df["Latitude"].min()),
                float(map_df["Latitude"].max()),
            )
            st.write(
                "Longitude min/max:",
                float(map_df["Longitude"].min()),
                float(map_df["Longitude"].max()),
            )

            st.write("Rows going into st.map():", len(map_df))
            st.dataframe(
                map_df[["Latitude", "Longitude"]].head(10),
                use_container_width=True,
                hide_index=True,
            )

            test_map_df = (
                map_df[["Latitude", "Longitude"]]
                .rename(columns={"Latitude": "lat", "Longitude": "lon"})
                .dropna()
                .head(10)
                .copy()
            )

            st.write("Test map rows:", len(test_map_df))
            st.dataframe(test_map_df, use_container_width=True, hide_index=True)

            st.map(test_map_df)

            import pandas as pd

            known_good_df = pd.DataFrame(
                {
                    "lat": [53.8008, 53.7920],
                    "lon": [-1.5491, -1.5400],
                }
            )

            st.write("Known-good Leeds test points")
            st.dataframe(known_good_df, use_container_width=True, hide_index=True)
            st.map(known_good_df)

            st.map(
                map_df.rename(columns={"Latitude": "lat", "Longitude": "lon"})[
                    ["lat", "lon"]
                ]
            )

        #### Debugging Map #####

    render_map(dashboard_data["map_data"])

    st.markdown("---")

    col7, col8 = st.columns(2)
    with col7:
        render_key_takeaways(dashboard_data["takeaways"])
    with col8:
        render_data_quality_summary(dashboard_data["data_quality_summary"])

    st.markdown("---")
    render_filtered_data_preview(dashboard_data["filtered_df"])


def main() -> None:
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout=APP_LAYOUT,
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
