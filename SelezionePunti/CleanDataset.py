'''
From the mediane 2019 - 2023:
1. Keep punti_esclusi
2. Remove points where mediane = 0
3. Save new files to plot in GIS
'''

# %%
# Load necessary packages and files
import pandas as pd
import os
import numpy as np

# %%
# Load the Excel files
# Punti esclusi
inq = 'CrTOT'
inq3 = 'Cr_TOT'
in_dir1 = 'c:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/Elaborazioni/E_AnalisiChimiche/' 
in_dir2 = 'C:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/GIS/'

mediane = pd.read_csv(os.path.join(in_dir1, f'PerConfronto/ArcGIS_input/Mediane_2019-2023/{inq}_Mediane2019-2023.csv'))
esclusi = pd.read_csv(os.path.join(in_dir2, f'Confronto/NEW_selection_escludere/Esclusi_{inq3}.csv'))
save_dir = os.path.join(in_dir1,'PerConfronto/ArcGIS_input/DEF')

# %%
inq2 = 'Cromo totale'
# Remove points where mediane = 0 expect if they are in punti esclusi
def_df = mediane[(mediane[f'{inq2}_2019_2023'].notna()) & (mediane[f'{inq2}_2019_2023'] != 0) | (mediane['ID_PUNTO'].isin(esclusi['ID_PUNTO']))]

# %%
def_df.to_csv(os.path.join(save_dir, f"DEF_{inq}_mediane_2019-2023.csv"))

# %%
'''
UPDATE: ADD FONTE INFO
'''

save_dir = 'c:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/Elaborazioni/E_AnalisiChimiche/PerConfronto/ArcGIS_input/DEF/' 
in_dir = 'c:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/Elaborazioni/E_AnalisiChimiche/PerConfronto/Input_files/' 
info_df = pd.read_excel(os.path.join(in_dir,'Anagarafiche_aggregate_tutti_SL_100125.xlsx'))
info_df = info_df.rename({"id_punto_idrochimica":"ID_PUNTO"}, axis=1)

# %%
inq = 'CrTOT'
df = pd.read_csv(os.path.join(save_dir, f"DEF_{inq}_mediane_2019-2023.csv"))
print("n records original:", df.shape)
df_update = pd.merge(df, info_df[["ID_PUNTO", "Fonte"]], on="ID_PUNTO", how="left").reset_index(drop=True)
print("n records update:", df_update.shape)

df_update.to_csv(os.path.join(save_dir, f"ULT_{inq}_mediane_2019-2023.csv"))

# %%
'''
UPDATE: ADD NUMBER OF MEASUREMENTS PER POINT 

'''
cwd1 = 'c:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/Elaborazioni/E_AnalisiChimiche/PerConfronto/ArcGIS_input/DEF/'

# Get number of measurements from the monitoring dataset
inq = 'CrTOT'
monit_df = pd.read_csv(os.path.join(cwd1, f"{inq}_dati_monitoraggio.csv"))
mediane_df = pd.read_csv(os.path.join(cwd1, f"ULT_{inq}_mediane_2019-2023.csv"))

# Count number of records per point in monitoring data
record_counts = monit_df.groupby('ID_PUNTO').size().reset_index(name='numero_misure')
update_df = mediane_df.merge(record_counts, on='ID_PUNTO', how='left')
update_df.to_csv(os.path.join(cwd1, f"LAST_{inq}_mediane_2019-2023.csv"))

# %%
