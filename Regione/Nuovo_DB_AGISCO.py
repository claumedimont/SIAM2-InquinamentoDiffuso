# %%
# Load necessary packages and files
import pandas as pd
import os

# Directory
path = 'C:/Users/user/OneDrive - Politecnico di Milano/04_REGIONE/SIAM2-AggiornamentoSitiMisure/Elaborazioni/DaCondividire/' 

# Load dataframe
df_main = pd.read_excel(os.path.join(path, 'SIAM2_SelezioneAGISCO_2025.xlsx'), sheet_name="Selezione_SIAM2")
df_tecno = pd.read_excel(os.path.join(path, 'SIAM2_SelezioneAGISCO_2025.xlsx'), sheet_name="Tecnologie")

# merge points with info about the applied remediation tecnology
tec_merge = df_main.merge(df_tecno, on='COD_SITO', how='left')
tec_merge.to_excel(os.path.join(path,"tec_merge.xlsx"))


# %%
# 3) INQUINANTI MERGE
df_tecno_sel = pd.read_excel(os.path.join(path, 'SIAM2_tecnologie_2025.xlsx'), sheet_name="Selezione")
df_inqui = pd.read_excel(os.path.join(path, 'SIAM2_SelezioneAGISCO_2025.xlsx'), sheet_name="Sostanze_selezione")

merged_df = pd.merge(df_tecno_sel, df_inqui, on='COD_SITO', how='left')

merged_df.to_excel(os.path.join(path, "inqui_merge.xlsx"))
# %%
df_inq_2025 = pd.read_excel(os.path.join(path, 'SIAM2_sitifalda_2025.xlsx'))
df_old = pd.read_excel(os.path.join(path, 'SIAM2_Complessivo.xlsx'), sheet_name="sel_aggior")

merged_df = pd.merge(df_inq_2025, df_old, on='COD_SITO', how='left')

merged_df.to_excel(os.path.join(path, "inqui_agg.xlsx"))
# %%
