# %%
# Load necessary packages and files
import pandas as pd
import os

# Directory
path = 'C:/Users/user/OneDrive - Politecnico di Milano/04_REGIONE/SIAM2-AggiornamentoSitiMisure/Elaborazioni/' #/DaCondividire/

# %%
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
# Load dataframe
df_main = pd.read_excel(os.path.join(path, 'SIAM2_falda_contaminata_agg.xlsx'))
df_inqui = pd.read_excel(os.path.join(path, 'Sel_inquinanti_2024.xlsx'))

merged_df = pd.merge(df_main, df_inqui, on='COD_SITO', how='left')

# %%
merged_df.to_excel(os.path.join(path,"inqui_agg_falda.xlsx"))
# %%

df_map = pd.read_excel(os.path.join(path,'sostanze_classificate.xlsx'))
mapping = (
    df_map
    .set_index('sostanze')['tipo_sostanza']
    .to_dict()
)

def get_tipi_sostanza(sostanze_cell, mapping):
    if pd.isna(sostanze_cell):
        return None

    # handle list or string
    if isinstance(sostanze_cell, list):
        sostanze = sostanze_cell
    else:
        sostanze = [s.strip() for s in sostanze_cell.split(',')]

    tipi = {
        mapping[s]
        for s in sostanze
        if s in mapping and pd.notna(mapping[s])
    }

    return ', '.join(sorted(tipi)) if tipi else None

merged_df['tipo_sostanze'] = merged_df['Sostanze'].apply(
    lambda x: get_tipi_sostanza(x, mapping)
)

merged_df.to_excel(os.path.join(path,"SIAM2_sostanze_agg.xlsx"))
# %%
# Load dataframe
df_main = pd.read_excel(os.path.join(path, 'SIAM2_sostanze_agg.xlsx'), sheet_name="Selezione_siti")
df_tecno = pd.read_excel(os.path.join(path, 'SIAM2_sostanze_agg.xlsx'), sheet_name="Tecnologie_dettaglio")

merged_df = pd.merge(df_main, df_tecno, on='COD_SITO', how='left')

merged_df.to_excel(os.path.join(path,"SIAM2_selezione_siti_2025.xlsx"))
# %%
