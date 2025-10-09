# %%
# verifica mediane

import pandas as pd
import os

cwd = "C:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/Elaborazioni/E_AnalisiChimiche/Mediane_2019-2023_DEF/"
df_data = pd.read_excel(os.path.join(cwd, "Check/Verifica/CrTOT/Cromo_TOT_verifica.xlsx"), sheet_name="Selezione")
classif = pd.read_csv(os.path.join(cwd, "Check/Verifica/CrTOT/Classificazione_acquiferi_DEF_02102025.csv"))
df_remove = pd.read_csv(os.path.join(cwd, "Check/Verifica/CrTOT/Esclusi_CrTOT_DEF.csv"))
df_outliers = pd.read_excel(os.path.join(cwd, "Outliers_daescludere.xlsx"))

#setting as string
df_data['ID_PUNTO'] = df_data['ID_PUNTO'].astype(str)
classif['ID_PUNTO'] = classif['ID_PUNTO'].astype(str)
df_remove['ID_PUNTO'] = df_remove['ID_PUNTO'].astype(str)
df_outliers['CrTOT'] = df_outliers['CrTOT'].astype(str)

#deleting white spaces
df_data['ID_PUNTO'] = df_data['ID_PUNTO'].str.strip()
classif['ID_PUNTO'] = classif['ID_PUNTO'].str.strip() 
df_remove['ID_PUNTO'] = df_remove['ID_PUNTO'].str.strip() 
df_outliers['CrTOT'] = df_outliers['CrTOT'].astype(str)

df_median = (
    df_data
    .groupby('ID_PUNTO', as_index=False)['VALORE_MODIFICATO']
    .median()
    .rename(columns={'VALORE_MODIFICATO': 'Mediane'})
)

df_merged = df_median.merge(classif, on='ID_PUNTO', how='left')
ids_to_remove = df_remove['ID_PUNTO'].unique()
outliers_remove = df_outliers["CrTOT"].unique()
df_final1 = df_merged[~df_merged['ID_PUNTO'].isin(ids_to_remove)]
df_final2 = df_final1[~df_final1['ID_PUNTO'].isin(outliers_remove)]

df_final2.to_csv(os.path.join(cwd, "Check/Verifica/CrTOT/recalc_mediane_CrTOT.csv"))

# %%
