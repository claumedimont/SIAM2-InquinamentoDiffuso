'''
CODE to prepare target file for input to Confronto_AEs.py
Files needed:
- Targets exported from GWV: get location per row & col --> grid_locations.csv
- Dataframe with cols ID, X, Y, layer, time (n days from start of simulation), obs_values --> obs_data.csv
- List of selected targets after applying the npoints and spatial location criteria --> selected_targets.csv

'''
# %%
import pandas as pd
import os

# File paths
in_dir = "e:/SIAM2-InquinamentoDiffuso/Input_flopy/TCM/targets/"
obs_file = os.path.join(in_dir, "obs_data.xlsx")
grid_file = os.path.join(in_dir, "grid_locations.csv")
selected_file = os.path.join(in_dir, "selected_targets.csv")

# %%
# Step 1: Get obs_data in format
obs_df = pd.read_excel(obs_file)
long_df = pd.melt(obs_df, 
                  id_vars=['ID', 'X', 'Y', 'group', 'weight', 'layer'], 
                  var_name='time', 
                  value_name='value')
long_df = long_df.dropna(subset=['value'])
print(long_df.head())

# %%
# Step 2: add row & column info from grid_file
grid_df = pd.read_csv(grid_file)
merged_df = pd.merge(long_df, grid_df[['ID', 'row', 'column']], on='ID', how='left')
merged_df = merged_df.dropna(subset=['row'])

# %%
# Step 3: extract selected targets
selected_df = pd.read_csv(selected_file)
selected_ids = selected_df['ID']
final_df = merged_df[merged_df['ID'].isin(selected_ids)]

# %%
# Save file
final_df = final_df.drop(columns=['X', 'Y', 'group'])
final_df = final_df[['ID', 'row', 'column', 'layer', 'weight', 'time', 'value']]
final_df.to_csv(os.path.join(in_dir,"per_confronto.csv"))
# %%
