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

# Directory
in_dir = 'C:/Users/user/OneDrive - Politecnico di Milano/04_REGIONE/SIAM2-AggiornamentoSitiMisure/Elaborazioni/' 
#sel_df = pd.read_excel(os.path.join(in_dir, 'SIAM2_SelezioneAGISCO.xlsx'), sheet_name= 'Tutti')

# %%
# 1) INITIAL MERGE

# Load dataframe
agisco_df = pd.read_excel(os.path.join(in_dir,'SIAM2_EstrazioneAGISCO.xlsx'), sheet_name="Tutti_comuni_SIAM2", dtype={"ANA_civico_sito": str})

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
#agisco_clean.to_excel(os.path.join(in_dir,"AGISCO_clean.xlsx"))

# %%
# 2) TECNOLOGY MERGE

# Load dataframe
tecnica_df = pd.read_excel(os.path.join(in_dir, 'tecnica_tipo_bonifica.xlsx'))

# merge points with info about the applied remediation tecnology
tec_merge = sel_df.merge(tecnica_df, on='COD_SITO', how='left')
tec_merge = tec_merge.drop(['ANA_anno_apertura_y'], axis=1)
tec_merge.to_excel(os.path.join(in_dir,"tec_merge.xlsx"))

# %%
# 2.1) Dealing with duplicates (multiple tecnologies for the same site)
# OPTION A) Group by 'COD_SITO' and aggregate remediation techniques and matrices

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
#df_final.to_excel(os.path.join(in_dir,'tecno_split.xlsx'))

# %%
# OPTION B) Group by unique site ID while keeping other attributes

# Fill NaN values in all columns that might affect grouping
sel_df.fillna('NoInfo', inplace=True)  # Replace NaN with empty strings (or choose a specific default)

# target matrices
target_mat = ['suolo/sottosuolo', 'acque sotterranee', 'NoInfo']
sel_df = sel_df[sel_df["MatriceDescrizione"].isin(target_mat)]

# Define columns to group by (excluding `TecnologieDescrizione` & `MatriceDescrizione`)
group_cols = [
    'Provincia', 'Comune', 'COD_SITO', 'ANA_classific_attuale', 
    'descClassSuoli', 'descClassAcque', 'Stato', 'anno_ultimo_edma', 
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

# Display row count for debugging & save
print(f"Initial rows: {sel_df.shape[0]}, Final rows: {df_final.shape[0]}")
df_final.to_excel(os.path.join(in_dir,'tecno_splitE.xlsx'))


# %%
# 3) INQUINANTI MERGE

# Load dataframe
inqui_df = pd.read_excel(os.path.join(in_dir,('Supporto/InquinantiXmatrice.xlsx')))

# Select only the sites of interest
# Ensure ID_PUNTO columns are strings, stripped of spaces, and in uppercase for consistency
sel_df["COD_SITO"] = sel_df["COD_SITO"].astype(str).str.strip().str.upper()
inqui_df["COD_SITO"] = inqui_df["COD_SITO"].astype(str).str.strip().str.upper()
inqui_df = inqui_df[inqui_df['COD_SITO'].isin(sel_df['COD_SITO'])]

# target matrices
target_mat = ['Suolo/Sottosuolo', 'Falda contaminata']
filter1_df = inqui_df[inqui_df["Matrice_inquinante"].isin(target_mat)]

# classificazione sostanze
# Define classification categories as dictionaries
categories = {
    "Pesticidi": {
        "Aldrin", "Alaclor", "Atrazina", "Beta - Esacloroesano", "Clordano", 
        "Dieldrin", "Gamma - Esacloroesano (Lindano)", "Alfa - Esacloroesano",
        "Sommatoria fitofarmaci", "FITOFARMACI"
    },
    "DiossineFurani": {
        "DIOSSINE E FURANI", "Esaclorobenzene"
    },
    "SolventiClorurati": {
        "Tetracloroetilene (PCE)", "Tricloroetilene", "Triclorometano",
        "Diclorometano", "Cloruro di vinile", "Esaclorobutadiene"
    },
    "SIAM2": {
        "Tetracloroetilene (PCE)", "Tricloroetilene", "Triclorometano",
        "Cromo totale", "Cromo Totale", "Cromo VI"
    }
}

# Function to classify substances (SIAM2 first priority)
def classify_tipo_sostanza(substance):
    if substance in categories["SIAM2"]:  # Prioritize SIAM2
        return "SIAM2"
    for category, substances in categories.items():
        if category != "SIAM2" and substance in substances:  # Assign another category if not SIAM2
            return category
    return "Altro"  # Default category for unclassified substances

# Apply the classification function to create the "tipo_sostanza" column
# and list the sostanze in a single column per matrice and tipo
filter1_df["tipo_sostanza"] = filter1_df["sostanze"].apply(classify_tipo_sostanza)

# tutti inquinanti merge
tuttinq_merge = sel_df.merge(filter1_df, on='COD_SITO', how='left')
#tuttinq_merge.to_excel(os.path.join(in_dir,"tuttinq_merge.xlsx"))

# %%
# 4) SIAM2 selezione inquinante + selezione tecnologie
SELinqui_df = pd.read_excel(os.path.join(in_dir, 'SIAM2_SelezioneAGISCO.xlsx'), sheet_name= 'TuttiInquinanti')
SELtecno_df = pd.read_excel(os.path.join(in_dir, 'SIAM2_SelezioneAGISCO.xlsx'), sheet_name= 'TuttiTecnologie')

SELinqui_df['Matrice_inquinante'] = SELinqui_df['Matrice_inquinante'].replace('Falda contaminata', 'acque sotterranee')
SELinqui_df['Matrice_inquinante'] = SELinqui_df['Matrice_inquinante'].replace('Suolo/Sottosuolo', 'suolo/sottosuolo')
#SELinqui_df = SELinqui_df.drop(['tipo_sostanza'], axis=1)

# merge with sel_df
# Ensure both DataFrames have 'Matrice' instead of different names
SELtecno_df = SELtecno_df.rename(columns={'Matrice_tecnologie': 'Matrice'})
SELinqui_df = SELinqui_df.rename(columns={'Matrice_inquinante': 'Matrice'})
# merge both DataFrames on 'COD_SITO' and 'Matrice'
merged_df = pd.merge(SELinqui_df, SELtecno_df, on=['COD_SITO', 'Matrice'], how='left')
#merged_df.to_excel(os.path.join(in_dir,"SIAM2_Complessivo.xlsx"))

# %%
# 5) Merge tecnologie MISE e MISP
mise_df = pd.read_excel(os.path.join(in_dir, "Supporto/Tecniche_MISE.xlsx"))
misp_df = pd.read_excel(os.path.join(in_dir, "Supporto/Tecniche_MISP.xlsx"))
comp_df = pd.read_excel(os.path.join(in_dir, "DaCondividire/SIAM2_Complessivo.xlsx"))

mise_df = mise_df[['COD_SITO', 'codDescrizione']].rename(columns={'codDescrizione': 'MISE_descrizione'})
misp_df = misp_df[['COD_SITO', 'codDescrizione']].rename(columns={'codDescrizione': 'MISP_descrizione'})

merged1_df = pd.merge(comp_df, mise_df, on=['COD_SITO'], how="left")
merged2_df = pd.merge(merged1_df, misp_df, on=['COD_SITO'], how="left")

#merged2_df.to_excel(os.path.join(in_dir, "SIAM2_ComplessivoNuovo.xlsx"))
# %%
