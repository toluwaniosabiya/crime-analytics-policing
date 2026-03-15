import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import streamlit as st

from src.data_loading import load_raw_crime_data
from src.data_processing import process_crime_data
from src.analytics import (
    build_kpi_summary,
    get_crime_type_distribution,
    get_monthly_totals,
    get_monthly_trend_by_crime_type,
    get_crime_heatmap_data,
    get_outcome_distribution,
    get_top_locations,
    get_top_districts,
    get_map_data,
)
from app.components.filters import render_sidebar_filters, apply_filters
from app.components.kpis import render_kpi_row
from app.components.charts import (
    render_crime_type_distribution,
    render_monthly_totals,
    render_monthly_trend_by_crime_type,
    render_crime_heatmap,
    render_outcome_distribution,
    render_top_locations,
    render_top_districts,
    render_map,
)

st.set_page_config(page_title="West Yorkshire Crime Analytics", layout="wide")

raw_df = load_raw_crime_data()
processed_df = process_crime_data(raw_df)

filters = render_sidebar_filters(processed_df)
filtered_df = apply_filters(processed_df, filters)

st.title("West Yorkshire Crime Analytics Dashboard")

kpi_summary = build_kpi_summary(filtered_df)
render_kpi_row(kpi_summary)

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    render_crime_type_distribution(get_crime_type_distribution(filtered_df))
with col2:
    render_monthly_totals(get_monthly_totals(filtered_df))

col3, col4 = st.columns(2)
with col3:
    render_monthly_trend_by_crime_type(get_monthly_trend_by_crime_type(filtered_df))
with col4:
    render_crime_heatmap(get_crime_heatmap_data(filtered_df))

col5, col6 = st.columns(2)
with col5:
    render_outcome_distribution(get_outcome_distribution(filtered_df))
with col6:
    render_top_locations(get_top_locations(filtered_df))

render_top_districts(get_top_districts(filtered_df))
render_map(get_map_data(filtered_df))
