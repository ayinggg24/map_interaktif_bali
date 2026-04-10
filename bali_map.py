import streamlit as st
import geopandas as gpd
import folium
from streamlit.components.v1 import html



st.set_page_config(layout="wide")

# peta bali

gdf = gpd.read_file("shapes/gadm41_IDN_2.shp")
bali = gdf[gdf["NAME_1"] == "Bali"].reset_index(drop=True)



# format nama

def format_nama(nama):
    if nama == "Denpasar":
        return "Kota Denpasar"
    else:
        return f"Kabupaten {nama}"


# data
data_kabupaten = {
    "Badung": 80,
    "Gianyar": 65,
    "Denpasar": 90,
    "Tabanan": 50,
    "Buleleng": 70,
    "Karangasem": 40,
    "Jembrana": 30,
    "Bangli": 45,
    "Klungkung": 55
}



# warna

def get_color(value):
    if value >= 75:
        return "#e31a1c"
    elif value >= 50:
        return "#3cfd6f"
    else:
        return "#31a354"



# peta

if "selected_kab" not in st.session_state:
    st.session_state.selected_kab = "NAME_2"



# peta

m = folium.Map(
    location=[-8.4, 115.1],
    zoom_start=10,
    tiles="cartodbpositron"
)

for _, row in bali.iterrows():
    nama = row["NAME_2"]
    nilai = data_kabupaten.get(nama, 0)

    popup_html = f"""
    <b>{format_nama(nama)}</b><br>
    Nilai: {nilai}%<br>
    Ibu Hamil: {1000 + nilai*10}<br>
    Balita: {2000 + nilai*15}
    """

    folium.GeoJson(
        row.geometry,
        style_function=lambda x, val=nilai: {
            "fillColor": get_color(val),
            "color": "white",
            "weight": 2,
            "fillOpacity": 0.9
        },
        tooltip=folium.Tooltip(f"{format_nama(nama)} ({nilai}%)"),
        popup=folium.Popup(popup_html, max_width=250)
    ).add_to(m)


st.title("📊 Dashboard Peta Bali")

col1, col2 = st.columns([3, 1])

# kiri 
with col1:
    html(m._repr_html_(), height=550)



# kanan = 
 
with col2:
    st.subheader("📈 Detail Kabupaten")

    kab = st.session_state.selected_kab
    nilai = data_kabupaten.get(kab, 0)

    st.markdown(f"### {format_nama(kab)}")
    st.markdown(f"**Nilai:** {nilai}%")
    st.markdown(f"**Ibu Hamil:** {1000 + nilai*10}")
    st.markdown(f"**Balita:** {2000 + nilai*15}")