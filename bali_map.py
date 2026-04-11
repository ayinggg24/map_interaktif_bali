import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

# =========================
# LOAD DATA SEK
# =========================
gdf = gpd.read_file("shapes/gadm41_IDN_2.shp")
bali = gdf[gdf["NAME_1"] == "Bali"].reset_index(drop=True)

def format_nama(nama):
    if nama == "Denpasar":
        return "Kota Denpasar"
    return f"Kabupaten {nama}"

data_kabupaten = {
    "Badung": 98, "Gianyar": 100, "Denpasar": 98,
    "Tabanan": 100, "Buleleng": 99, "Karangasem": 100,
    "Jembrana": 99, "Bangli": 95, "Klungkung": 100
}

data_detail = {
    "Jembrana": {
        "d_s": "99%", "stunting": "6.1%", "underweight": "4.1%", "wasting": "1.6%",
        "total_balita": 917, "usia_0_5": 50, "usia_6_11": 40, "usia_12_23": 158,
        "usia_24_35": 210, "usia_36_47": 245, "usia_48_59": 214
    },
    "Gianyar": {
        "d_s": "100%", "stunting": "3.8%", "underweight": "2.9%", "wasting": "1.2%",
        "total_balita": 974, "usia_0_5": 33, "usia_6_11": 48, "usia_12_23": 210,
        "usia_24_35": 266, "usia_36_47": 211, "usia_48_59": 206
    },
    "Badung": {
        "d_s": "98%", "stunting": "2.5%", "underweight": "3.2%", "wasting": "1.2%",
        "total_balita": 471, "usia_0_5": 12, "usia_6_11": 15, "usia_12_23": 90,
        "usia_24_35": 129, "usia_36_47": 104, "usia_48_59": 121
    },
    "Tabanan": {
        "d_s": "100%", "stunting": "2.8%", "underweight": "3.1%", "wasting": "1.2%",
        "total_balita": 574, "usia_0_5": 31, "usia_6_11": 16, "usia_12_23": 113,
        "usia_24_35": 146, "usia_36_47": 123, "usia_48_59": 145
    },
    "Klungkung": {
        "d_s": "100%", "stunting": "3.1%", "underweight": "3.7%", "wasting": "1.1%",
        "total_balita": 314, "usia_0_5": 2, "usia_6_11": 5, "usia_12_23": 49,
        "usia_24_35": 59, "usia_36_47": 86, "usia_48_59": 113
    },
    "Bangli": {
        "d_s": "95%", "stunting": "3.9%", "underweight": "3.7%", "wasting": "1.7%",
        "total_balita": 489, "usia_0_5": 24, "usia_6_11": 32, "usia_12_23": 79,
        "usia_24_35": 122, "usia_36_47": 121, "usia_48_59": 111
    },
    "Karangasem": {
        "d_s": "100%", "stunting": "3.5%", "underweight": "3.8%", "wasting": "2.0%",
        "total_balita": 734, "usia_0_5": 33, "usia_6_11": 24, "usia_12_23": 122,
        "usia_24_35": 186, "usia_36_47": 189, "usia_48_59": 180
    },
    "Denpasar": {
        "d_s": "98%", "stunting": "2.1%", "underweight": "2.0%", "wasting": "0.8%",
        "total_balita": 429, "usia_0_5": 10, "usia_6_11": 7, "usia_12_23": 68,
        "usia_24_35": 122, "usia_36_47": 113, "usia_48_59": 109
    },
    "Buleleng": {
        "d_s": "99%", "stunting": "3.3%", "underweight": "4.2%", "wasting": "2.2%",
        "total_balita": 1175, "usia_0_5": 102, "usia_6_11": 86, "usia_12_23": 225,
        "usia_24_35": 228, "usia_36_47": 246, "usia_48_59": 288
    }
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

# =========================
# SESSION STATE
# =========================
if "selected_kab" not in st.session_state:
    st.session_state.selected_kab = list(data_kabupaten.keys())[0]

# =========================
# MAP
# =========================
m = folium.Map(location=[-8.4, 115.1], zoom_start=9, tiles="cartodbpositron")

for _, row in bali.iterrows():
    nama = row["NAME_2"]
    nilai = data_kabupaten.get(nama, 0)
    d = data_detail.get(nama)

    if d:
        popup_html = f"""
        <b>{format_nama(nama)}</b><br><br>
        <b>D/S:</b> {d['d_s']}<br>
        <b>Stunting:</b> {d['stunting']}<br>
        <b>Underweight:</b> {d['underweight']}<br>
        <b>Wasting:</b> {d['wasting']}<br>
        """
    else:
        popup_html = f"<b>{format_nama(nama)}</b><br>Nilai: {nilai}%"

    geo = folium.GeoJson(
        data={
            "type": "Feature",
            "geometry": row.geometry.__geo_interface__,
            "properties": {
                "NAME_2": nama
            }
        },
        style_function=lambda x, val=nilai: {
            "fillColor": get_color(val),
            "color": "white",
            "weight": 2,
            "fillOpacity": 0.8
        },
        tooltip=folium.Tooltip(f"{format_nama(nama)} ({nilai}%)"),
        popup=folium.Popup(popup_html, max_width=300)
    )

    geo.add_to(m)

# =========================
# UI
# =========================
st.markdown("""
<h3>BALITA STUNTING PER KELOMPOK UMUR<br>
HASIL PENGUKURAN NOVEMBER 2025 - BALI</h3>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2.5, 1])

# =========================
# MAP + CLICK HANDLER (FIXED)
# =========================
with col1:
    map_data = st_folium(m, width=700, height=550, key="map")

    # Ambil NAME_2 langsung dari last_active_drawing -> properties
    if map_data and map_data.get("last_active_drawing"):
        props = map_data["last_active_drawing"].get("properties", {})
        nama_kab = props.get("NAME_2")
        if nama_kab and nama_kab in data_kabupaten:
            if st.session_state.selected_kab != nama_kab:
                st.session_state.selected_kab = nama_kab
                st.rerun()

# =========================
# SIDEBAR DETAIL
# =========================
with col2:
    st.subheader("📈 Detail Kabupaten / Kota")

    kab = st.session_state.selected_kab
    nilai = data_kabupaten.get(kab, 0)

    st.markdown(f"### {format_nama(kab)}")
    st.markdown(f"**Nilai:** {nilai}%")

    d = data_detail.get(kab)

    if d:
        st.markdown(f"""
        **D/S:** {d['d_s']}  
        **Stunting:** {d['stunting']}  
        **Underweight:** {d['underweight']}  
        **Wasting:** {d['wasting']}  
        **Total Balita:** {d['total_balita']}  

        **Stunting per usia:**
        - 0–5 bln: {d['usia_0_5']}
        - 6–11 bln: {d['usia_6_11']}
        - 12–23 bln: {d['usia_12_23']}
        - 24–35 bln: {d['usia_24_35']}
        - 36–47 bln: {d['usia_36_47']}
        - 48–59 bln: {d['usia_48_59']}
        """)
# =========================
# GREY LUCUUU
# =========================