'''
CODE TO CLEAN & PREPARE THE AGISCO DATABASE

INPUT FILES:
* Estrazione AGISCO

OUTPUT FILES:
* Clean file

'''
# %%
# Load necessary packages and files
import pandas as pd
import os

# Load the Excel files
in_dir = 'C:/Users/HP/OneDrive - Politecnico di Milano/PhD_Claudia/Period_Regione/Elaborazioni/' 
agisco_df = pd.read_excel(os.path.join(in_dir,'SIAM2_EstrazioneAGISCO.xlsx'), sheet_name="Tutti_comuni_SIAM2", dtype={"ANA_civico_sito": str})

# %%
# Check for duplicates based on column 'COD_SITO'
dups = agisco_df[agisco_df.duplicated(subset=['COD_SITO'], keep=False)]
dups.to_excel(os.path.join(in_dir,"dups.xlsx"))

# get year from column 'data ultimo edma associato al sito'
agisco_df['data ultimo edma associato al sito'] = agisco_df['data ultimo edma associato al sito'].replace("NULL", pd.NA)
agisco_df['data ultimo edma associato al sito'] = pd.to_datetime(agisco_df['data ultimo edma associato al sito'], errors='coerce')
agisco_df['anno_ultimo_edma'] = agisco_df['data ultimo edma associato al sito'].dt.year

#remove dups by keeping the most recent row
agisco_clean = agisco_df.sort_values(by='data ultimo edma associato al sito', ascending=False).drop_duplicates(subset=['COD_SITO'], keep='first')

# %%
# Save clean df
agisco_clean.to_excel(os.path.join(in_dir,"AGISCO_clean.xlsx"))
# %%
