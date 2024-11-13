'''
Code to prepare input file for ArcGIS
from previously filtered target csv file (by npoints)
'''
# %%
import pandas as pd
import os

# Load files
in_dir1 = "C:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/Elaborazioni/E_AnalisiChimiche/Target_concentrazione_modello/ArcGIS_input/"
in_dir2 = "C:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/Elaborazioni/E_AnalisiChimiche/PerConfronto/ArcGIS_input/"
targets_filtered = pd.read_csv(os.path.join(in_dir1,"Cr6_filtered_10.csv"))
mediane_anag = pd.read_csv(os.path.join(in_dir2,"Cr6_mediane_anagrafica.csv"))

# %%
# Extract the 'id' column 
target_ids = targets_filtered['name'].unique()  
# Filter the larger DataFrame based on observation point IDs
target_anag = mediane_anag[mediane_anag['ID_PUNTO'].isin(target_ids)]  # Assuming 'id' is the column with IDs
print(target_anag.head(5))

# %%
# Save the filtered DataFrame if needed
target_anag.to_csv(os.path.join(in_dir2,"Selected_npoints/Cr6_np10_anag.csv"), index=False)

print(f"Filtered points: {len(target_anag)} points found.")

# %%
