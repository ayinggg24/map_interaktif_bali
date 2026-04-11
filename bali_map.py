import streamlit as st
import geopandas as gpd
import folium
from streamlit.components.v1 import html

st.set_page_config(layout="wide")


# data map

gdf = gpd.read_file("shapes/gadm41_IDN_2.shp")
bali = gdf[gdf["NAME_1"] == "Bali"].reset_index(drop=True)

# format nama

def format_nama(nama):
    if nama == "Denpasar":
        return "Kota Denpasar"
    return f"Kabupaten {nama}"


# data persen 

data_kabupaten = {
    "Badung": 98,
    "Gianyar": 100,
    "Denpasar": 98,
    "Tabanan": 100,
    "Buleleng": 99,
    "Karangasem": 100,
    "Jembrana": 99,
    "Bangli": 95,
    "Klungkung": 100
}


# data detail

data_detail = {
    "Jembrana": {
        "d_s": "99%",
        "stunting": "6.1%",
        "underweight": "4.1%",
        "wasting": "1.6%",
        "total_balita": 917,
        "usia_0_5": 50,
        "usia_6_11": 40,
        "usia_12_23": 158,
        "usia_24_35": 210,
        "usia_36_47": 245,
        "usia_48_59": 214
    },

    "Gianyar": {
        "d_s": "100.0%",
        "stunting": "3.8%",
        "underweight": "2.9%",
        "wasting": "1.2%",
        "total_balita": 974,
        "usia_0_5": 33,
        "usia_6_11": 48,
        "usia_12_23": 210,
        "usia_24_35": 266,
        "usia_36_47": 211,
        "usia_48_59": 206
    },

    "Badung": {
        "d_s": "98.0%",
        "stunting": "2.5%",
        "underweight": "3.2%",
        "wasting": "1.2%",
        "total_balita": 471,
        "usia_0_5": 12,
        "usia_6_11": 15,
        "usia_12_23": 90,
        "usia_24_35": 129,
        "usia_36_47": 104,
        "usia_48_59": 121
    },

    "Tabanan": {
        "d_s": "100%",
        "stunting": "2.8%",
        "underweight": "3.1%",
        "wasting": "1.2%",
        "total_balita": 574,
        "usia_0_5": 31,
        "usia_6_11": 16,
        "usia_12_23": 113,
        "usia_24_35": 146,
        "usia_36_47": 123,
        "usia_48_59": 145
    },

    "Klungkung": {
        "d_s": "100%",
        "stunting": "3.1%",
        "underweight": "3.7%",
        "wasting": "1.1%",
        "total_balita": 314,
        "usia_0_5": 2,
        "usia_6_11": 5,
        "usia_12_23": 49,
        "usia_24_35": 59,
        "usia_36_47": 86,
        "usia_48_59": 113
    },

    "Bangli": {
        "d_s": "95.0%",
        "stunting": "3.9%",
        "underweight": "3.7%",
        "wasting": "1.7%",
        "total_balita": 489,
        "usia_0_5": 24,
        "usia_6_11": 32,
        "usia_12_23": 79,
        "usia_24_35": 122,
        "usia_36_47": 121,
        "usia_48_59": 111
    },

    "Karangasem": {
        "d_s": "100.0%",
        "stunting": "3.5%",
        "underweight": "3.8%",
        "wasting": "2.0%",
        "total_balita": 734,
        "usia_0_5": 33,
        "usia_6_11": 24,
        "usia_12_23": 122,
        "usia_24_35": 186,
        "usia_36_47": 189,
        "usia_48_59": 180
    },

    "Denpasar": {
        "d_s": "98.0%",
        "stunting": "2.1%",
        "underweight": "2.0%",
        "wasting": "0.8%",
        "total_balita": 429,
        "usia_0_5": 10,
        "usia_6_11": 7,
        "usia_12_23": 68,
        "usia_24_35": 122,
        "usia_36_47": 113,
        "usia_48_59": 109
    },

    "Buleleng": {
        "d_s": "99%",
        "stunting": "3.3%",
        "underweight": "4.2%",
        "wasting": "2.2%",
        "total_balita": 1175,
        "usia_0_5": 102,
        "usia_6_11": 86,
        "usia_12_23": 225,
        "usia_24_35": 228,
        "usia_36_47": 246,
        "usia_48_59": 288
    }
}


# warna

def get_color(value):
    if value >= 85:
        return "#e31a1c"
    elif value >= 70:
        return "#ffd500"
    elif value >= 50:
        return "#3cfd6f"
    else:
        return "#4da6ff"


# nama kota

if "selected_kab" not in st.session_state:
    st.session_state.selected_kab = "nama"


# map

m = folium.Map(
    location=[-8.4, 115.1],
    zoom_start=9,
    tiles="cartodbpositron"
)


# nama layer

layer_merah = folium.FeatureGroup(name="🔴 Sangat Tinggi (≥85)", show=True)
layer_kuning = folium.FeatureGroup(name="🟡 Tinggi (70–84)", show=True)
layer_sedang = folium.FeatureGroup(name="🟢 Sedang (50–69)", show=True)
layer_rendah = folium.FeatureGroup(name="🔵 Rendah (<50)", show=True)


# loop geojson

for _, row in bali.iterrows():
    nama = row["NAME_2"]
    nilai = data_kabupaten.get(nama, 0)

    # popup detail semua kabupaten
    d = data_detail.get(nama, None)

    if d:
        popup_html = f"""
        <b>{format_nama(nama)}</b><br><br>

        <b>D/S:</b> {d['d_s']}<br>
        <b>Stunting:</b> {d['stunting']}<br>
        <b>Underweight:</b> {d['underweight']}<br>
        <b>Wasting:</b> {d['wasting']}<br>
        <b>Total Balita:</b> {d['total_balita']}<br><br>

        <b>Stunting per usia:</b><br>
        0–5 bln: {d['usia_0_5']}<br>
        6–11 bln: {d['usia_6_11']}<br>
        12–23 bln: {d['usia_12_23']}<br>
        24–35 bln: {d['usia_24_35']}<br>
        36–47 bln: {d['usia_36_47']}<br>
        48–59 bln: {d['usia_48_59']}<br>
        """
    else:
        popup_html = f"""
        <b>{format_nama(nama)}</b><br>
        Nilai: {nilai}%
        """

    geo = folium.GeoJson(
        row.geometry,
        style_function=lambda x, val=nilai: {
            "fillColor": get_color(val),
            "color": "white",
            "weight": 2,
            "fillOpacity": 0.8
        },
        tooltip=folium.Tooltip(f"{format_nama(nama)} ({nilai}%)"),
        popup=folium.Popup(popup_html, max_width=350)
    )

    # masuk layer
    if nilai >= 85:
        geo.add_to(layer_merah)
    elif nilai >= 70:
        geo.add_to(layer_kuning)
    elif nilai >= 50:
        geo.add_to(layer_sedang)
    else:
        geo.add_to(layer_rendah)


# nambah layer

layer_merah.add_to(m)
layer_kuning.add_to(m)
layer_sedang.add_to(m)
layer_rendah.add_to(m)

folium.LayerControl(collapsed=False).add_to(m)


# judul

st.markdown("""
<h3 style="text-align:left;">
BALITA STUNTING PER KELOMPOK UMUR<br>
HASIL PENGUKURAN SERENTAK BULAN NOVEMBER 2025 DI PROVINSI BALI
</h3>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2.5, 1])

with col1:
    html(m._repr_html_(), height=550)

with col2:
    st.subheader("📈 Detail Kabupaten / Kota")

    kab = st.session_state.selected_kab
    nilai = data_kabupaten[kab]

    st.markdown(f"### {format_nama(kab)}")
    st.markdown(f"**Nilai:** {nilai}%")