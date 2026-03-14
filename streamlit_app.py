import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Crime Analytics Dashboard",
    page_icon="📊",
    layout="wide",
)

# -----------------------------
# Helpers
# -----------------------------
@st.cache_data
def load_data(uploaded_file=None) -> pd.DataFrame:
    """
    Loads a CSV file if uploaded; otherwise returns demo data
    based on the West Yorkshire crime analysis structure.
    Expected columns include:
    - Month
    - Crime type
    - Reported by
    - Falls within
    - Longitude
    - Latitude
    - Location
    - LSOA code
    - LSOA name
    - Last outcome category
    """
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        demo_data = {
            "Month": pd.date_range("2020-04-01", periods=6, freq="MS").repeat(6),
            "Crime type": [
                "Violence and sexual offences",
                "Anti-social behaviour",
                "Public order",
                "Criminal damage and arson",
                "Burglary",
                "Vehicle crime",
            ] * 6,
            "Count": [
                8271, 3398, 2468, 1726, 1089, 1014,
                8793, 4388, 2853, 1932, 1037, 891,
                9780, 5384, 3039, 2160, 1180, 1084,
                10721, 5825, 3329, 2353, 1330, 1150,
                10514, 5828, 3303, 2504, 1500, 1151,
                9397, 4491, 2919, 2379, 1223, 1152,
            ],
            "Reported by": ["West Yorkshire Police"] * 36,
        }
        df = pd.DataFrame(demo_data)

    if "Month" in df.columns:
        df["Month"] = pd.to_datetime(df["Month"], errors="coerce")

    return df


def ensure_count_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    If the dataset is incident-level and has no Count column,
    create one so charts can aggregate records cleanly.
    """
    if "Count" not in df.columns:
        df = df.copy()
        df["Count"] = 1
    return df


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("Crime Analytics Dashboard")
st.sidebar.markdown(
    "Upload a crime dataset CSV or use the built-in demo data."
)

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
df = load_data(uploaded_file)
df = ensure_count_column(df)

st.sidebar.markdown("---")

crime_col = "Crime type" if "Crime type" in df.columns else None
month_col = "Month" if "Month" in df.columns else None
agency_col = "Reported by" if "Reported by" in df.columns else None

crime_types = sorted(df[crime_col].dropna().unique().tolist()) if crime_col else []
agencies = sorted(df[agency_col].dropna().unique().tolist()) if agency_col else []

selected_crimes = st.sidebar.multiselect(
    "Filter by crime type",
    options=crime_types,
    default=crime_types[:6] if crime_types else [],
)

selected_agencies = st.sidebar.multiselect(
    "Filter by reporting agency",
    options=agencies,
    default=agencies,
)

# -----------------------------
# Filtering
# -----------------------------
filtered_df = df.copy()

if crime_col and selected_crimes:
    filtered_df = filtered_df[filtered_df[crime_col].isin(selected_crimes)]

if agency_col and selected_agencies:
    filtered_df = filtered_df[filtered_df[agency_col].isin(selected_agencies)]

# -----------------------------
# Header
# -----------------------------
st.title("Crime Analytics Dashboard")
st.caption(
    "Template dashboard for crime trend analysis, offence distribution, and decision-support visuals."
)

with st.expander("About this dashboard"):
    st.markdown(
        """
        This template is designed for your crime analytics portfolio and can be adapted for:
        - police open data
        - neighbourhood-level crime monitoring
        - offence trend analysis
        - seasonal and time-series analysis
        - stakeholder-facing analytical reporting

        Replace the demo dataset with your cleaned project dataset and extend the filters as needed.
        """
    )

# -----------------------------
# KPI Row
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Records", f"{len(filtered_df):,}")

with col2:
    total_incidents = filtered_df["Count"].sum() if "Count" in filtered_df.columns else len(filtered_df)
    st.metric("Total Incidents", f"{int(total_incidents):,}")

with col3:
    unique_crimes = filtered_df[crime_col].nunique() if crime_col else 0
    st.metric("Crime Categories", f"{unique_crimes:,}")

with col4:
    if month_col and filtered_df[month_col].notna().any():
        month_span = filtered_df[month_col].dt.to_period("M").nunique()
    else:
        month_span = 0
    st.metric("Months Covered", f"{month_span:,}")

st.markdown("---")

# -----------------------------
# Charts Row 1
# -----------------------------
left, right = st.columns((1, 1))

with left:
    st.subheader("Offence Distribution")
    if crime_col:
        crime_summary = (
            filtered_df.groupby(crime_col, dropna=False)["Count"]
            .sum()
            .reset_index()
            .sort_values("Count", ascending=False)
        )
        fig_bar = px.bar(
            crime_summary,
            x="Count",
            y=crime_col,
            orientation="h",
            title="Crime Counts by Category",
        )
        fig_bar.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No 'Crime type' column found.")

with right:
    st.subheader("Monthly Trend")
    if month_col and crime_col:
        monthly_summary = (
            filtered_df.groupby([month_col, crime_col], dropna=False)["Count"]
            .sum()
            .reset_index()
        )
        fig_line = px.line(
            monthly_summary,
            x=month_col,
            y="Count",
            color=crime_col,
            markers=True,
            title="Crime Trends Over Time",
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("Need 'Month' and 'Crime type' columns for the time-series plot.")

# -----------------------------
# Charts Row 2
# -----------------------------
left2, right2 = st.columns((1, 1))

with left2:
    st.subheader("Monthly Heatmap")
    if month_col and crime_col:
        heatmap_df = (
            filtered_df.assign(MonthLabel=filtered_df[month_col].dt.strftime("%b %Y"))
            .groupby([crime_col, "MonthLabel"], dropna=False)["Count"]
            .sum()
            .reset_index()
        )
        heatmap_pivot = heatmap_df.pivot(index=crime_col, columns="MonthLabel", values="Count").fillna(0)
        fig_heat = px.imshow(
            heatmap_pivot,
            aspect="auto",
            title="Crime Category Counts by Month",
            labels={"x": "Month", "y": "Crime type", "color": "Count"},
        )
        st.plotly_chart(fig_heat, use_container_width=True)
    else:
        st.info("Need 'Month' and 'Crime type' columns for the heatmap.")

with right2:
    st.subheader("Data Preview")
    st.dataframe(filtered_df.head(25), use_container_width=True)

# -----------------------------
# Insight Box
# -----------------------------
st.markdown("---")
st.subheader("Analytical Notes")

if month_col and crime_col and not filtered_df.empty:
    summary = (
        filtered_df.groupby(crime_col)["Count"].sum().sort_values(ascending=False)
    )
    top_crime = summary.index[0] if len(summary) else "N/A"
    st.success(
        f"Top observed category in the current selection: **{top_crime}**. "
        "Use this section to summarize trends, notable spikes, seasonality, disparities, or operational implications."
    )
else:
    st.info("Upload a cleaned dataset to generate automated summary highlights.")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown(
    "**Portfolio note:** This dashboard template was built in Streamlit for crime analytics, trend monitoring, and public-sector decision support."
)
