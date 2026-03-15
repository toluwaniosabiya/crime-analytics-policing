# from src.data_loading import load_raw_crime_data
# from src.validation import build_validation_report, validate_required_columns

# df = load_raw_crime_data()
# validate_required_columns(df)

# report = build_validation_report(df)
# print(report["row_count"])
# print(report["missing_required_columns"])
# print(report["coordinate_summary"])
# print(report["null_summary"])

# from src.data_loading import load_raw_crime_data
# from src.data_processing import process_crime_data

# raw_df = load_raw_crime_data()
# processed_df = process_crime_data(raw_df)

# print(processed_df.shape)
# print(processed_df.columns.tolist())
# print(processed_df[["Month", "Month Parsed", "Month Label"]].head())
# print(processed_df[["Crime type", "District", "Record Count"]].head())
# print(processed_df[["LSOA name", "District"]].head(50))

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
    get_map_data,
    build_key_takeaways,
)

raw_df = load_raw_crime_data()
processed_df = process_crime_data(raw_df)

print(build_kpi_summary(processed_df))
print(get_crime_type_distribution(processed_df).head())
print(get_monthly_totals(processed_df))
print(get_monthly_trend_by_crime_type(processed_df).head())
print(get_outcome_distribution(processed_df).head())
print(get_top_locations(processed_df).head())
print(get_map_data(processed_df).shape)
print(build_key_takeaways(processed_df))
