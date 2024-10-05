# %%
import geopandas as gpd
import os
# %%
# Load the shapefile
folder = 'd:/Claudia/SIAM2_Inquinamento-diffuso/Historical/Results_CrVI_TMR/'
output = 'd:/Claudia/SIAM2_Inquinamento-diffuso/Historical/Results_CrVI_TMR/ToImport'
os.makedirs(output, exist_ok=True)
subs = ['ZoneA', 'ZoneB', 'ZoneC', 'ZoneD']

# %%
for i in subs:
    folder_path = os.path.join(folder, subs[i])
    # Loop through all the shapefiles in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".shp"):  # Ensure we are only working with shapefiles
            shapefile_path = os.path.join(folder_path, filename)
            
            # Load the shapefile
            gdf = gpd.read_file(shapefile_path)
            
            # Assuming the concentration values are in a column named 'concentration'
            # Filter the rows where concentration is greater than 0.1
            gdf_filtered = gdf[gdf['concentrat'] > 0.1]
            
            # Define output path for the filtered shapefile
            filtered_shapefile_path = os.path.join(output_folder, f"{filtered}_{i}.shp")
            
            # Save the filtered shapefile
            gdf_filtered.to_file(filtered_shapefile_path)