'''
Aggiornamento selezione siti agisco con outliers

'''
# %%
# Load necessary packages and files
import pandas as pd
import os


# %%
# Load the Excel files
dir1 = 'C:/Users/user/OneDrive - Politecnico di Milano/04_REGIONE/SIAM2-AggiornamentoSitiMisure/Elaborazioni/' 
dir2 = 'C:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/Elaborazioni/E_AnalisiChimiche/Dataset_interpolazione/Outliers' 
info_df = pd.read_excel(os.path.join(dir1, 'DaCondividire/SIAM2_Complessivo.xlsx'), sheet_name="RigaUnica")
siti_df = pd.read_excel(os.path.join(dir2, 'Outliers_SitiAGISCO_DEF.xlsx'), sheet_name="Siti")
piezo_df = pd.read_excel(os.path.join(dir2, 'Outliers_SitiAGISCO_DEF.xlsx'), sheet_name="Punti")

# %%
filtered_df = info_df[info_df['COD_SITO'].isin(siti_df['Codice'])]
#filtered_df.to_excel(os.path.join(dir2, 'Outliers_SitiInfo.xlsx'))

df_grouped = piezo_df.groupby('COD_Sito1')['ID_PUNTO'].apply(list).reset_index()
df_grouped = df_grouped.rename(columns = {'COD_Sito1':'COD_SITO'})

df_merged = siti_df.merge(df_grouped, on='COD_SITO', how='left')
#df_merged.to_excel(os.path.join(dir2, 'Outliers_PiezoxSiti.xlsx'))

# %%
# ---------------
# REMOVE HOTSPOTS (MONOPARAMETRO) FROM MEDIANE DATASET
# ---------------
wd = "C:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/Elaborazioni/E_AnalisiChimiche/Mediane_2019-2022_DEF/"

pce_df = pd.read_csv(os.path.join(wd, "DEF/", "LAST_PCE_mediane_2019-2023.csv"))
tce_df = pd.read_csv(os.path.join(wd, "DEF/", "LAST_TCE_mediane_2019-2023.csv"))
tcm_df = pd.read_csv(os.path.join(wd, "DEF/", "LAST_TCM_mediane_2019-2023.csv"))
cr6_df = pd.read_csv(os.path.join(wd, "DEF/", "LAST_Cr6_mediane_2019-2023.csv"))
crTOT_df = pd.read_csv(os.path.join(wd, "DEF/", "LAST_CrTOT_mediane_2019-2023.csv"))

out_df = pd.read_excel(os.path.join(wd, "Outliers_daescludere.xlsx"))

# IDs to remove
pce_remove = out_df["PCE"].dropna().unique().astype(str)
tce_remove = out_df["TCE"].dropna().unique().astype(str)
tcm_remove = out_df["TCM"].dropna().unique().astype(str)
cr6_remove = out_df["Cr6"].dropna().unique().astype(str)
crtot_remove = out_df["CrTOT"].dropna().unique().astype(str)

def normalize_ids(series):
    return (series.astype(str)
                  .str.strip()          # remove leading/trailing spaces
                  .str.replace(r"\s+", "", regex=True)  # remove ALL whitespace
                  .str.upper())         # make uppercase for consistency

# Apply to datasets
for df in [pce_df, tce_df, tcm_df, cr6_df, crTOT_df]:
    df["ID_PUNTO"] = normalize_ids(df["ID_PUNTO"])

# Apply to removal lists
pce_remove = normalize_ids(pd.Series(pce_remove)).unique()
tce_remove = normalize_ids(pd.Series(tce_remove)).unique()
tcm_remove = normalize_ids(pd.Series(tcm_remove)).unique()
cr6_remove = normalize_ids(pd.Series(cr6_remove)).unique()
crtot_remove = normalize_ids(pd.Series(crtot_remove)).unique()

# %%
# filter datasets
pce_df["ID_PUNTO"] = pce_df["ID_PUNTO"].astype(str)
pce_clean = pce_df[~pce_df["ID_PUNTO"].isin(pce_remove)]

tce_df["ID_PUNTO"] = tce_df["ID_PUNTO"].astype(str)
tce_clean = tce_df[~tce_df["ID_PUNTO"].isin(tce_remove)]

tcm_df["ID_PUNTO"] = tcm_df["ID_PUNTO"].astype(str)
tcm_clean = tcm_df[~tcm_df["ID_PUNTO"].isin(tcm_remove)]

cr6_df["ID_PUNTO"] = cr6_df["ID_PUNTO"].astype(str)
cr6_clean = cr6_df[~cr6_df["ID_PUNTO"].isin(cr6_remove)]

crTOT_df["ID_PUNTO"] = crTOT_df["ID_PUNTO"].astype(str)
crtot_clean = crTOT_df[~crTOT_df["ID_PUNTO"].isin(crtot_remove)]

print(f"original: {len(pce_df)} after: {len(pce_clean)}, to remove: {pce_remove.size}, actually removed: {len(pce_df)-len(pce_clean)}")
print(f"original: {len(tce_df)} after: {len(tce_clean)}, to remove: {tce_remove.size}, actually removed: {len(tce_df)-len(tce_clean)}")
print(f"original: {len(tcm_df)} after: {len(tcm_clean)}, to remove: {tcm_remove.size}, actually removed: {len(tcm_df)-len(tcm_clean)}")
print(f"original: {len(cr6_df)} after: {len(cr6_clean)}, to remove: {cr6_remove.size}, actually removed: {len(cr6_df)-len(cr6_clean)}")
print(f"original: {len(crTOT_df)} after: {len(crtot_clean)}, to remove: {crtot_remove.size}, actually removed: {len(crTOT_df)-len(crtot_clean)}")

# %%
# save
pce_clean.to_csv(os.path.join(wd, "DEF", "CLEAN_PCE_mediane_2019-2023.csv"))
tce_clean.to_csv(os.path.join(wd, "DEF", "CLEAN_TCE_mediane_2019-2023.csv"))
tcm_clean.to_csv(os.path.join(wd, "DEF", "CLEAN_TCM_mediane_2019-2023.csv"))
cr6_clean.to_csv(os.path.join(wd, "DEF", "CLEAN_Cr6_mediane_2019-2023.csv"))
crtot_clean.to_csv(os.path.join(wd, "DEF", "CLEAN_CrTOT_mediane_2019-2023.csv"))

# %%
