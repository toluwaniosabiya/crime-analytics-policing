# import streamlit as st
# import pandas as pd
# import pydeck as pdk

# st.title("Map Debug")

# df = pd.DataFrame(
#     {
#         "lat": [53.8008, 53.7920],
#         "lon": [-1.5491, -1.5400],
#     }
# )

# st.write(df)

# layer = pdk.Layer(
#     "ScatterplotLayer",
#     data=df,
#     get_position="[lon, lat]",
#     get_radius=500,
#     get_fill_color=[255, 0, 0, 180],
#     pickable=True,
# )

# view_state = pdk.ViewState(
#     latitude=53.8008,
#     longitude=-1.5491,
#     zoom=10,
#     pitch=0,
# )

# deck = pdk.Deck(
#     layers=[layer],
#     initial_view_state=view_state,
#     map_style="light",
# )

# st.pydeck_chart(deck)

import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Plotly Map Debug")

df = pd.DataFrame(
    {
        "lat": [53.8008, 53.7920],
        "lon": [-1.5491, -1.5400],
        "label": ["Point A", "Point B"],
    }
)

fig = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    hover_name="label",
    zoom=10,
    height=600,
)

fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
)

st.plotly_chart(fig, use_container_width=True)
