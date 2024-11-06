# %%
import pandas as pd
import os
# %%
# Load files
folder_1 = 'd:/Claudia/SIAM2_Inquinamento-diffuso/Confronto/'
folder_2 = 'C:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/Elaborazioni/E_Sorgenti/'

coords_1 = pd.read_csv(os.path.join(folder_1, "anagrafica_ARPA.csv"))
coords_2 = pd.read_csv(os.path.join(folder_1, "anagrafica_MM_CAP_ALFA.csv"))

data_Cr = pd.read_excel(os.path.join(folder_2, "Rete_Cr.xlsx"))

# %%
# Prepare first coords file
coords_1 = coords_1.rename(columns={"Codice_PP":"ID_PUNTO"})

to_modify = 'CAP'
data_Cr.loc[data_Cr['FONTE'] == to_modify, 'ID_PUNTO'] = \
    data_Cr.loc[data_Cr['FONTE'] == to_modify, 'ID_PUNTO'].str[:-3]

# %%
# Merge with first coords file
merged_1 = pd.merge(data_Cr, coords_1[['ID_PUNTO', 'X', 'Y']], 
                       on='ID_PUNTO', how='left')
# %%
#coords_2 = coords_2.rename(columns={"COD":"ID_PUNTO"})
#coords_2['ID_PUNTO'] = coords_2['ID_PUNTO'].apply(
#    lambda x: '0' + x if x.startswith('15') else x)
merged_2 = pd.merge(merged_1, coords_2[['ID_PUNTO', 'X', 'Y']], 
                       on='ID_PUNTO', how='left', suffixes=('', '_new'))
merged_2['X'] = merged_2['X'].combine_first(merged_2['X_new'])
merged_2['Y'] = merged_2['Y'].combine_first(merged_2['Y_new'])
merged_2.drop(['X_new', 'Y_new'], axis=1, inplace=True)

# %%
#without adding a zero for MM in coords 2
coords_3 = pd.read_csv(os.path.join(folder_1, "anagrafica_MM_CAP_ALFA.csv"))
coords_3 = coords_3.rename(columns={"COD":"ID_PUNTO"})
# %%
merged_2['ID_PUNTO'] = merged_2['ID_PUNTO'].astype(str)
coords_3['ID_PUNTO'] = coords_3['ID_PUNTO'].astype(str)

# Step 4: Strip any leading/trailing whitespace (in case of formatting issues)
merged_2['ID_PUNTO'] = merged_2['ID_PUNTO'].str.strip()
coords_3['ID_PUNTO'] = coords_3['ID_PUNTO'].str.strip()

# %%
merged_3 = pd.merge(merged_2, coords_3[['ID_PUNTO', 'X', 'Y']],
                       on='ID_PUNTO', how='left', suffixes=('', '_new'))
# %%
merged_3['X'] = merged_3['X'].combine_first(merged_3['X_new'])
merged_3['Y'] = merged_3['Y'].combine_first(merged_3['Y_new'])
merged_3.drop(['X_new', 'Y_new'], axis=1, inplace=True)

# %%
merged_3.to_excel(os.path.join(folder_2,"Cr_ReteCoords.xlsx"))
# %%
