# %%
import pandas as pd
import os

wd = "C:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/Elaborazioni/E_Prelievi/"
df = pd.read_excel(os.path.join(wd, "sipiui_selezione.xlsx"), sheet_name="Origine-2022")

# municipalities
comuni = [
"SENAGO",
"BARANZATE",
"NOVATE MILANESE",
"MILANO",
"BRESSO",
"LAINATE",
"PERO",
"MONZA",
"ARESE",
"PADERNO DUGNANO",
"CUSANO MILANINO",
"GARBAGNATE MILANESE",
"MUGGIO'",
"CINISELLO BALSAMO",
"SETTIMO MILANESE",
"BRUGHERIO",
"SESTO SAN GIOVANNI",
"CARONNO PERTUSELLA",
"COLOGNO MONZESE",
"ORIGGIO",
"RHO",
"NOVA MILANESE",
"CORMANO",
"BOLLATE"]


# Filter rows where column value is in the list
filtered_df = df[df['COMUNEOPERA'].isin(comuni)]
filtered_df.to_csv(os.path.join(wd, "sel_2022.csv"))
# %%
