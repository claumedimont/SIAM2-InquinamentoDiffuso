'''

'''
# %%
# Load necessary packages and files
import pandas as pd
import os

# Load the Excel files
in_dir = 'C:/Users/user/OneDrive - Politecnico di Milano/04_REGIONE/SIAM2-AggiornamentoSitiMisure/Elaborazioni/' 
tutti_df = pd.read_excel(os.path.join(in_dir, 'SIAM2_EstrazioneAGISCO.xlsx'), sheet_name="Tutti_comuni_SIAM2")
siti_df = pd.read_excel(os.path.join(in_dir, 'SIAM2_Siti_Aggiornati.xlsx'), sheet_name="SITI_GIS")

# %%
df_coords = siti_df.merge(tutti_df[['COD_SITO', 'ANA_CX', 'ANA_CY']], on='COD_SITO', how='left')
# %%
df_coords.to_excel(os.path.join(in_dir,"coords.xlsx"))
# %%
