import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

gdf = gpd.read_file("shapes/gadm41_IDN_2.shp")
bali = gdf[gdf["NAME_1"] == "Bali"].reset_index(drop=True)

data_kabupaten = {
    "Badung": 98, "Gianyar": 100, "Denpasar": 98,
    "Tabanan": 100, "Buleleng": 99, "Karangasem": 100,
    "Jembrana": 99, "Bangli": 95, "Klungkung": 100
}

def get_color(value):
    if value >= 85:
        return "#e31a1c"
    elif value >= 70:
        return "#ffd500"
    elif value >= 50:
        return "#3cfd6f"
    else:
        return "#4da6ff"

m = folium.Map(location=[-8.4, 115.1], zoom_start=9, tiles="cartodbpositron")

for _, row in bali.iterrows():
    nama = row["NAME_2"]
    nilai = data_kabupaten.get(nama, 0)

    geo = folium.GeoJson(
        data={
            "type": "Feature",
            "geometry": row.geometry.__geo_interface__,
            "properties": {"NAME_2": nama}
        },
        style_function=lambda x, val=nilai: {
            "fillColor": get_color(val),
            "color": "white",
            "weight": 2,
            "fillOpacity": 0.8
        },
        tooltip=folium.Tooltip(nama),  
        name=nama
    )
    geo.add_to(m)

st.title("DEBUG - Cek return value st_folium")

map_data = st_folium(m, width=700, height=500, key="map")

st.subheader("Raw map_data yang dikembalikan st_folium:")
st.json(map_data)
