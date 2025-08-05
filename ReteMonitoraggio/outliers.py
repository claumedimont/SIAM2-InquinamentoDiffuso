'''
Aggiornametno selezione siti agisco con outliers

'''
# %%
# Load necessary packages and files
import pandas as pd
import os

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
