import geopandas as gpd

# load shapefile
gdf = gpd.read_file("shapes/gadm41_IDN_2.shp")

# ambil Bali saja
bali = gdf[gdf["NAME_1"] == "Bali"]

# simpan jadi geojson
bali.to_file("bali_only.geojson", driver="GeoJSON")

print("DONE -> bali_only.geojson berhasil dibuat")