'''
Code to assign categories to substances listed in AGISCO database.

'''
# %%
# Load necessary packages and files
import pandas as pd
import os

in_dir = 'C:/Users/user/OneDrive - Politecnico di Milano/04_REGIONE/SIAM2-AggiornamentoSitiMisure/Elaborazioni/' 
df_map = pd.read_excel(os.path.join(in_dir,'sostanze_classificate.xlsx'))
df_sites = pd.read_excel(os.path.join(in_dir,'SIAM2_agg_ALL1.xlsx'))

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

df_sites['tipo_sostanza_suolo'] = df_sites['sostanze_suolo'].apply(
    lambda x: get_tipi_sostanza(x, mapping)
)

df_sites['tipo_sostanza_acque'] = df_sites['sostanze_acqua'].apply(
    lambda x: get_tipi_sostanza(x, mapping)
)

df_sites.to_excel(os.path.join(in_dir,"SIAM2_agg_ALL2.xlsx"))
# %%
