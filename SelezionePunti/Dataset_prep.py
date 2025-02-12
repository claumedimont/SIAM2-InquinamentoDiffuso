'''
CODE TO:
1. 

INPUT FILES:
* 
OUTPUT FILES:
* 

'''
# %%
# Load necessary packages and files
import pandas as pd
import os
import numpy as np

# Load the Excel files
inq = 'TCM'
in_dir1 = 'C:/Users/HP/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/Elaborazioni/E_DatasetFinali/Senza_C/' 
in_dir2 = f'C:/Users/HP/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/GIS/Confronto/Buffers/Selezione_punti/{inq}/' 
All_df = pd.read_excel(os.path.join(in_dir1, f'{inq}_all_noC.xlsx'))
Exclude_df = pd.read_excel(os.path.join(in_dir2,f'{inq}_daEscludere_DEF.xlsx'))


# %%
# 1. Remove points in exclude_df from all_df

# Convert ID_PUNTO columns to string type
All_df["ID_PUNTO"] = All_df["ID_PUNTO"].astype(str).str.strip().str.upper()
Exclude_df["ID_PUNTO"] = Exclude_df["ID_PUNTO"].astype(str).str.strip().str.upper()

# Drop duplicates from Exclude_df
Exclude_df = Exclude_df.drop_duplicates(subset="ID_PUNTO", keep="first")

# Filter
final_df = All_df[~All_df["ID_PUNTO"].isin(Exclude_df["ID_PUNTO"])]

# %%
# Save
final_df.to_excel(os.path.join(in_dir1, f'{inq}_dataset_110225.xlsx'))

# %%
duplicates = Exclude_df[Exclude_df["ID_PUNTO"].duplicated(keep=False)]
duplicates = duplicates.sort_values(by="ID_PUNTO", ascending=True)
print(duplicates)

# %%
missing_ids = Exclude_df[~Exclude_df["ID_PUNTO"].isin(All_df["ID_PUNTO"])]
print("IDs that are in Exclude_df but NOT in All_df:", missing_ids["ID_PUNTO"].tolist())
# THEY ARE IN ACQUIFER C!

# %%
