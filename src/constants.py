REQUIRED_COLUMNS = [
    "Month",
    "Crime type",
    "Longitude",
    "Latitude",
    "Location",
    "LSOA code",
    "LSOA name",
    "Last outcome category",
]

OPTIONAL_COLUMNS = [
    "Crime ID",
    "Reported by",
    "Falls within",
    "Context",
]

COLUMNS_TO_DROP_IF_PRESENT = [
    "Unnamed: 0",
    "Context",
]

TEXT_COLUMNS = [
    "Crime type",
    "Location",
    "LSOA code",
    "LSOA name",
    "Last outcome category",
    "Reported by",
    "Falls within",
]

DERIVED_COLUMNS = [
    "Month Parsed",
    "Month Label",
    "Year",
    "Month Number",
    "Record Count",
    "District",
    "Crime ID Missing",
]

MONTH_INPUT_FORMAT = "%Y-%m"

MAP_REQUIRED_COLUMNS = [
    "Latitude",
    "Longitude",
]

TOP_N_DEFAULT = 15
MAP_SAMPLE_SIZE = 5000
