'''
CODE TO CLEAN & PREPARE THE AGISCO DATABASE AND MERGE WITH INFO
ABOUT REMEDIATION TECNOLOGIES PER SITE

INPUT FILES:
* Estrazione AGISCO
* Tecnica_tipo_bonifica

OUTPUT FILES:
* Selezione AGISCO
* Merge con tecnologie

'''
# %%
# Load necessary packages and files
import pandas as pd
import os

# Load the Excel files
in_dir = 'C:/Users/HP/OneDrive - Politecnico di Milano/PhD_Claudia/Period_Regione/Elaborazioni/' 
#agisco_df = pd.read_excel(os.path.join(in_dir,'SIAM2_EstrazioneAGISCO.xlsx'), sheet_name="Tutti_comuni_SIAM2", dtype={"ANA_civico_sito": str})
sel_df = pd.read_excel(os.path.join(in_dir, 'SIAM2_SelezioneAGISCO.xlsx'), sheet_name= 'TuttiTecnologie')
#tecnica_df = pd.read_excel(os.path.join(in_dir, 'tecnica_tipo_bonifica.xlsx'))

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

# Save clean df
agisco_clean.to_excel(os.path.join(in_dir,"AGISCO_clean.xlsx"))

# %%
#merge points with info about the applied remediation tecnology
tec_merge = sel_df.merge(tecnica_df, on='COD_SITO', how='left')
tec_merge = tec_merge.drop(['ANA_anno_apertura_y'], axis=1)
tec_merge.to_excel(os.path.join(in_dir,"tec_merge.xlsx"))

# %%
# dealing with duplicates (multiple tecnologies for the same site)
# A) Group by 'COD_SITO' and aggregate remediation techniques and matrices
df_grouped = sel_df.groupby(['Provincia', 'Comune', 'COD_SITO', 'ANA_classific_attuale', 
                         'descClassSuoli', 'descClassAcque', 'anno_ultimo_edma', 
                         'Tipologia_sito', 'ANA_denom_sito', 'ANA_anno_apertura_x', 
                         'PRAT_anno_chiusura']) \
               .agg({
                   'TecnologieDescrizione': lambda x: ', '.join(x.dropna().unique()), 
                   'MatriceDescrizione': lambda x: ', '.join(x.dropna().unique())
               }).reset_index()

# Split technologies into separate columns
techniques = df_grouped['TecnologieDescrizione'].str.get_dummies(sep=', ')
matrices = df_grouped['MatriceDescrizione'].str.get_dummies(sep=', ')

# Merge back into the main dataframe
df_final = pd.concat([df_grouped.drop(columns=['TecnologieDescrizione', 'MatriceDescrizione']), techniques, matrices], axis=1)
df_final.to_excel(os.path.join(in_dir,'tecno_split.xlsx'))

# %%
# B) Group by unique site ID while keeping other attributes
# Fill NaN values in all columns that might affect grouping
sel_df.fillna('NoInfo', inplace=True)  # Replace NaN with empty strings (or choose a specific default)

# Define columns to group by (excluding `TecnologieDescrizione` & `MatriceDescrizione`)
group_cols = [
    'Provincia', 'Comune', 'COD_SITO', 'ANA_classific_attuale', 
    'descClassSuoli', 'descClassAcque', 'anno_ultimo_edma', 
    'Tipologia_sito', 'ANA_denom_sito', 'ANA_anno_apertura_x', 
    'PRAT_anno_chiusura'
]

# Group by key columns and aggregate technologies and matrices
df_grouped = sel_df.groupby(group_cols, dropna=False).agg({
    'TecnologieDescrizione': lambda x: ', '.join(sorted(x.dropna().unique())), 
    'MatriceDescrizione': lambda x: ', '.join(sorted(x.dropna().unique()))
}).reset_index()

# Convert lists into One-Hot Encoded columns
techniques = df_grouped['TecnologieDescrizione'].str.get_dummies(sep=', ')
matrices = df_grouped['MatriceDescrizione'].str.get_dummies(sep=', ')

# Merge back into the dataframe
df_final = pd.concat([df_grouped.drop(columns=['TecnologieDescrizione', 'MatriceDescrizione']), techniques, matrices], axis=1)

# Display row count for debugging
print(f"Initial rows: {sel_df.shape[0]}, Final rows: {df_final.shape[0]}")
#df_final.to_excel(os.path.join(in_dir,'tecno_splitC.xlsx'))

# %%
df_final.to_excel(os.path.join(in_dir,'tecno_splitD.xlsx'))
# %%
