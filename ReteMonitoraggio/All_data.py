'''
For fun
'''
# %%
import pandas as pd
import os

inq = 'PCE'
cwd = 'C:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/Elaborazioni/E_AnalisiChimiche/PerConfronto/ArcGIS_input/DEF/'
monit_df = pd.read_csv(os.path.join(cwd,f"{inq}_dati_monitoraggio.csv"))
anag_df = pd.read_csv(os.path.join(cwd,f"LAST_{inq}_mediane_2019-2023.csv"))

merge = monit_df.merge(anag_df, on="ID_PUNTO", how='left')
# %%
merge.to_csv(os.path.join(cwd, f"{inq}_tutti_dati.csv"))
# %%
