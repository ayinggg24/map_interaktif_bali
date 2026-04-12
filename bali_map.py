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
    if nama == "Bali":
        return "Provinsi Bali"
    elif nama == "Denpasar":
        return "Kota Denpasar"
    else:
        return f"Kabupaten {nama}"
    

data_kabupaten = {
    
    "Badung": 2.5, "Gianyar": 3.8, "Denpasar": 2.1,
    "Tabanan": 2.8, "Buleleng": 3.3, "Karangasem": 3.5,
    "Jembrana": 6.1, "Bangli": 3.9, "Klungkung": 3.1
}

data_detail = {
       "Bali": {
        "d_s": "99%",
        "stunting": "3.4%",
        "underweight": "3.4%",
        "wasting": "1.5%",
        "total_balita": 6077,
        "usia_0_5": 297,
        "usia_6_11": 273,
        "usia_12_23": 1114,
        "usia_24_35": 1468,
        "usia_36_47": 1438,
        "usia_48_59": 1487
    },
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

# =========================
# WARNA
# =========================
def get_color(value):
    if value >= 30:
        return "#e31a1c"
    elif value >= 20:
        return "#ffd500"
    elif value >= 10:
        return "#3cfd6f"
    else:
        return "#4da6ff"

# =========================
# SESSION
# =========================
if "selected_kab" not in st.session_state:
    st.session_state.selected_kab = "Bali"
    

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
    <div style="font-size:15px; line-height:1.4;">
    <b>{format_nama(nama)}</b><br><br>
    D/S: <b>{d['d_s']}</b><br>
    Stunting: <b>{d['stunting']}</b><br>
    Underweight: <b>{d['underweight']}</b><br>
    Wasting: <b>{d['wasting']}</b><br>
    </div>
    <div style="font-size:15px; line-height:1.4;">
    0–5 bln: <b>{d['usia_0_5']}</b><br>
    6–11 bln: <b>{d['usia_6_11']}</b><br>
    12–23 bln: <b>{d['usia_12_23']}</b><br>
    24–35 bln: <b>{d['usia_24_35']}</b><br>
    36–47 bln: <b>{d['usia_36_47']}</b><br>
    48–59 bln: <b>{d['usia_48_59']}</b><br>
        """
    else:
        popup_html = f"<b>{format_nama(nama)}</b><br>Nilai: {nilai}%"

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
       tooltip=folium.Tooltip(f"{format_nama(nama)} (<b>{nilai}%</b>)"),
        popup=folium.Popup(popup_html, max_width=300)
    )

    geo.add_to(m)

    folium.Marker(
    location=[row.geometry.centroid.y, row.geometry.centroid.x],
    icon=folium.DivIcon(
        html=f"""
        <div style="
            font-size:12px;
            color:black;
            font-weight:bold;
            text-align:left;
            white-space:nowrap;
            text-shadow: 2px 2px 2px white;
        ">
        {nama}
        </div>
        """
    )
).add_to(m)

# =========================
# LEGEND STATIS (FIX)
# =========================
legend_html = """
<div style="
position: fixed; 
bottom: 25px; left: 20px; width: 200px; 
background-color: rgba(255,255,255,0.95);
border-radius: 12px;
padding: 14px;
box-shadow: 0 4px 15px rgba(0,0,0,0.3);
font-size: 14px;
color: black;
z-index: 99999;
border: 1px solid #ddd;
">

<b>Kategori Presentase Stunting</b><br><br>

<div><span style="background:#4da6ff;width:18px;height:18px;display:inline-block;"></span> Rendah <b>(2.5%–10%)</b></div>
<div><span style="background:#3cfd6f;width:18px;height:18px;display:inline-block;"></span> Sedang <b>(10%–19%)</b></div>
<div><span style="background:#ffd500;width:18px;height:18px;display:inline-block;"></span> Tinggi <b>(20%–29%)</b></div>
<div><span style="background:#e31a1c;width:18px;height:18px;display:inline-block;"></span> Sangat Tinggi <b>(≥30%)</b></b></div>

</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# =========================
# UI
# =========================


st.markdown("""
<h3>BALITA STUNTING PER KELOMPOK UMUR<br>
HASIL PENGUKURAN  NOVEMBER 2025 DI PROVINSI BALI</h3>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2.5, 1])

with col1:
    map_data = st_folium(m, width=700, height=550, key="map")

    if map_data and map_data.get("last_active_drawing"):
        props = map_data["last_active_drawing"].get("properties", {})
        nama_kab = props.get("NAME_2")
        if nama_kab and nama_kab in data_kabupaten:
            if st.session_state.selected_kab != nama_kab:
                st.session_state.selected_kab = nama_kab
                st.rerun()

                st.markdown("""


""", unsafe_allow_html=True)

with col2:
    st.subheader("📈Hasil Pengukuran Balita Stunting Kabupaten / Kota")

    kab = st.session_state.selected_kab
    nilai = data_kabupaten.get(kab, 0)

    st.markdown(f"### {format_nama(kab)}")
    st.markdown(f"**Presentase :**")

    

    d = data_detail.get(kab)

    # fungsi bar dinamis
    def bar(val, max_val=100):
        try:
            num = float(str(val).replace("%", ""))
        except:
            num = 0
        width = (num / max_val) * 100
        return f"""
        <div style='flex:1; background:#eee; margin:0 10px; height:6px;'>
            <div style='width:{width}%; background:#4da6ff; height:6px;'></div>
        </div>
        """

    if d:
         st.markdown(f"""
<div style="margin-top:-20px; padding-top:0;">

<div style="display:flex; justify-content:space-between; align-items:center;">
<span>D/S</span>
<div style="flex:1; height:6px; background:#eee; margin:0 10px; border-radius:5px;">
<div style="width:{int(d['d_s'].replace('%',''))}%; height:6px; background:#4da6ff; border-radius:5px;"></div>
</div>
<span>{d['d_s']}</span>
</div>

<div style="display:flex; justify-content:space-between; align-items:center;">
<span>Stunting</span>
<div style="flex:1; height:6px; background:#eee; margin:0 10px; border-radius:5px;">
<div style="width:{float(d['stunting'].replace('%',''))*10}%; height:6px; background:#4da6ff; border-radius:5px;"></div>
</div>
<span>{d['stunting']}</span>
</div>

<div style="display:flex; justify-content:space-between; align-items:center;">
<span>Underweight</span>
<div style="flex:1; height:6px; background:#eee; margin:0 10px; border-radius:5px;">
<div style="width:{float(d['underweight'].replace('%',''))*10}%; height:6px; background:#4da6ff; border-radius:5px;"></div>
</div>
<span>{d['underweight']}</span>
</div>

<div style="display:flex; justify-content:space-between; align-items:center;">
<span>Wasting</span>
<div style="flex:1; height:6px; background:#eee; margin:0 10px; border-radius:5px;">
<div style="width:{float(d['wasting'].replace('%',''))*10}%; height:6px; background:#4da6ff; border-radius:5px;"></div>
</div>
<span>{d['wasting']}</span>
</div>

<div style="display:flex; justify-content:space-between; align-items:center;">
<span>Total</span>
<div style="flex:1; height:6px; background:#eee; margin:0 10px; border-radius:5px;">
<div style="width:{d['total_balita']/6000*100}%; height:6px; background:#4da6ff; border-radius:5px;"></div>
</div>
<span>{d['total_balita']}</span>
</div>


<div style="margin-top:15px;">
<b>Kelompok Umur Balita Stunting : </b>
</div>

<div style="display:flex; justify-content:space-between; align-items:center; ,margin-top: ">
<span>Usia 0-5</span>
<div style="flex:1; height:6px; background:#eee; margin:0 10px; border-radius:5px;">
<div style="width:{d['usia_0_5']/1500*100}%; height:6px; background:#4da6ff; border-radius:5px;"></div>
</div>
<span><b>{d['usia_0_5']}</b></span>
</div>

<div style="display:flex; justify-content:space-between; align-items:center; ,margin-top: ">
<span>Usia 6-11</span>
<div style="flex:1; height:6px; background:#eee; margin:0 10px; border-radius:5px;">
<div style="width:{d['usia_6_11']/1500*100}%; height:6px; background:#4da6ff; border-radius:5px;"></div>
</div>
<span><b>{d['usia_6_11']}</b></span>
</div>

<div style="display:flex; justify-content:space-between; align-items:center; ,margin-top: ">
<span>Usia 12-23</span>
<div style="flex:1; height:6px; background:#eee; margin:0 10px; border-radius:5px;">
<div style="width:{d['usia_12_23']/1500*100}%; height:6px; background:#4da6ff; border-radius:5px;"></div>
</div>
<span><b>{d['usia_12_23']}</b></span>
</div>

<div style="display:flex; justify-content:space-between; align-items:center; ,margin-top: ">
<span>Usia 24-35</span>
<div style="flex:1; height:6px; background:#eee; margin:0 10px; border-radius:5px;">
<div style="width:{d['usia_24_35']/1500*100}%; height:6px; background:#4da6ff; border-radius:5px;"></div>
</div>
<span><b>{d['usia_24_35']}</b></span>
</div>

<div style="display:flex; justify-content:space-between; align-items:center; ,margin-top: ">
<span>Usia 36-47</span>
<div style="flex:1; height:6px; background:#eee; margin:0 10px; border-radius:5px;">
<div style="width:{d['usia_36_47']/1500*100}%; height:6px; background:#4da6ff; border-radius:5px;"></b></div>
</div>
<span><b>{d['usia_36_47']}</b></span>
</div>

<div style="display:flex; justify-content:space-between; align-items:center; ,margin-top: ">
<span>Usia 48-59</span>
<div style="flex:1; height:6px; background:#eee; margin:0 10px; border-radius:5px;">
<div style="width:{d['usia_48_59']/1500*100}%; height:6px; background:#4da6ff; border-radius:5px;"></div>
</div>
<span><b>{d['usia_48_59']}</b></span>
</div>


</div>
""", unsafe_allow_html=True)