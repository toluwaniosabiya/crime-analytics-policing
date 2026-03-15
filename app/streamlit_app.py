import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import streamlit as st

from src.data_loading import load_raw_crime_data
from src.data_processing import process_crime_data
from app.components.filters import render_sidebar_filters, apply_filters

st.set_page_config(page_title="Test Filters", layout="wide")

raw_df = load_raw_crime_data()
processed_df = process_crime_data(raw_df)

filters = render_sidebar_filters(processed_df)
filtered_df = apply_filters(processed_df, filters)

st.write("Original shape:", processed_df.shape)
st.write("Filtered shape:", filtered_df.shape)
st.dataframe(filtered_df.head(20))
