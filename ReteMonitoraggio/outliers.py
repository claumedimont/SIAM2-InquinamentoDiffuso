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
siti_df = pd.read_csv(os.path.join(dir2, 'Outliers_SitiAGISCO.CSV'))

filtered_df = info_df[info_df['COD_SITO'].isin(siti_df['Codice'])]

# %%
filtered_df.to_excel(os.path.join(dir2, 'Outliers_SitiInfo.xlsx'))
# %%
