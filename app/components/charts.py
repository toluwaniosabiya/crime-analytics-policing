import pandas as pd
import plotly.express as px
import streamlit as st


def render_crime_type_distribution(crime_df: pd.DataFrame) -> None:
    """
    Render horizontal bar chart for crime category distribution.
    """
    st.subheader("Crime Category Distribution")

    if crime_df.empty:
        st.info("No crime category data available for the current filter selection.")
        return

    fig = px.bar(
        crime_df,
        x="Incidents",
        y="Crime type",
        orientation="h",
        text_auto=True,
        title="Incidents by Crime Type",
    )
    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        height=500,
    )
    st.plotly_chart(fig, use_container_width=True)


def render_monthly_totals(monthly_totals_df: pd.DataFrame) -> None:
    """
    Render line chart for total incidents by month.
    """
    st.subheader("Overall Monthly Trend")

    if monthly_totals_df.empty:
        st.info("No monthly totals available for the current filter selection.")
        return

    fig = px.line(
        monthly_totals_df,
        x="Month Label",
        y="Incidents",
        markers=True,
        title="Total Incidents by Month",
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)


def render_monthly_trend_by_crime_type(trend_df: pd.DataFrame) -> None:
    """
    Render line chart for monthly crime trends by crime type.
    """
    st.subheader("Trend by Crime Type")

    if trend_df.empty:
        st.info("No trend data available for the current filter selection.")
        return

    fig = px.line(
        trend_df,
        x="Month Label",
        y="Incidents",
        color="Crime type",
        markers=True,
        title="Monthly Movement by Crime Type",
    )
    fig.update_layout(height=500, legend_title_text="Crime Type")
    st.plotly_chart(fig, use_container_width=True)


def render_crime_heatmap(heatmap_df: pd.DataFrame) -> None:
    """
    Render heatmap for crime counts by month and crime type.
    """
    st.subheader("Crime Heatmap")

    if heatmap_df.empty:
        st.info("No heatmap data available for the current filter selection.")
        return

    fig = px.imshow(
        heatmap_df,
        aspect="auto",
        labels={"x": "Month", "y": "Crime Type", "color": "Incidents"},
        title="Crime Type Counts by Month",
        color_continuous_scale="RdPu",
    )
    fig.update_layout(height=500)
    fig.update_traces(hovertemplate="Crime: %{y}<br>Month: %{x}<br>Incidents: %{z}")
    st.plotly_chart(fig, use_container_width=True)


def render_outcome_distribution(outcome_df: pd.DataFrame) -> None:
    """
    Render horizontal bar chart for top outcome categories.
    """
    st.subheader("Outcome Categories")

    if outcome_df.empty:
        st.info("No outcome data available for the current filter selection.")
        return

    fig = px.bar(
        outcome_df,
        x="Incidents",
        y="Last outcome category",
        orientation="h",
        text_auto=True,
        title="Top Outcome Categories",
    )
    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        height=500,
    )
    st.plotly_chart(fig, use_container_width=True)


def render_top_locations(location_df: pd.DataFrame) -> None:
    """
    Render horizontal bar chart for top incident locations.
    """
    st.subheader("Top Locations")

    if location_df.empty:
        st.info("No location data available for the current filter selection.")
        return

    fig = px.bar(
        location_df.sort_values("Incidents", ascending=True),
        x="Incidents",
        y="Location",
        orientation="h",
        text_auto=True,
        title="Locations with Highest Incident Counts",
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)


def render_top_districts(district_df: pd.DataFrame) -> None:
    """
    Render horizontal bar chart for top districts / areas.
    """
    st.subheader("Top Districts / Areas")

    if district_df.empty:
        st.info("No district data available for the current filter selection.")
        return

    fig = px.bar(
        district_df.sort_values("Incidents", ascending=True),
        x="Incidents",
        y="District",
        orientation="h",
        text_auto=True,
        title="Districts with Highest Incident Counts",
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)


def render_map(map_df: pd.DataFrame) -> None:
    """
    Render geographic incident map with Plotly.
    """
    st.subheader("Geographic View")

    if map_df.empty:
        st.info("No valid coordinate data available for the current filter selection.")
        return

    plot_df = map_df.copy()

    plot_df["Latitude"] = pd.to_numeric(plot_df["Latitude"], errors="coerce")
    plot_df["Longitude"] = pd.to_numeric(plot_df["Longitude"], errors="coerce")

    plot_df = plot_df.dropna(subset=["Latitude", "Longitude"]).copy()

    if plot_df.empty:
        st.info("No valid coordinate data available after coordinate cleaning.")
        return

    center_lat = float(plot_df["Latitude"].median())
    center_lon = float(plot_df["Longitude"].median())

    hover_fields = [
        col
        for col in ["Crime type", "Month Label", "Last outcome category"]
        if col in plot_df.columns
    ]

    fig = px.scatter_mapbox(
        plot_df,
        lat="Latitude",
        lon="Longitude",
        hover_name="Location" if "Location" in plot_df.columns else None,
        hover_data=hover_fields,
        color="Crime type" if "Crime type" in plot_df.columns else None,
        zoom=9,
        height=650,
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_center={"lat": center_lat, "lon": center_lon},
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
    )

    st.plotly_chart(fig, use_container_width=True)
