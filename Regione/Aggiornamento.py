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
in_dir = 'C:/Users/user/OneDrive - Politecnico di Milano/04_REGIONE/SIAM2-AggiornamentoSitiMisure/Elaborazioni/' 
sel_df = pd.read_excel(os.path.join(in_dir, 'SIAM2_ComplessivoNuovo.xlsx'))
agg_df = pd.read_excel(os.path.join(in_dir, 'SIAM2_Siti_Aggiornati.xlsx'), sheet_name="SITI_PRIORITARI")


# %%
#merge points with info about the applied remediation tecnology
agg_merge = pd.merge(agg_df, sel_df, on='COD_SITO', how='left')
#agg_merge = agg_merge.drop(['Provincia', 'Comune'], axis=1)

# %%
#agg_merge.to_excel(os.path.join(in_dir,"priori_merge.xlsx"))
# %%
# ultimate aggregation
# Group by 'COD_SITO' and aggregate multiple values as lists
aggregated_df = agg_merge.groupby('COD_SITO').agg({
    'Provincia':'first',
    'Comune':'first',
    'Area':'first',
    'Stato2017-2019': 'first',
    'ANA_classific_attuale': 'first',
    'descClassSuoli': 'first',
    'descClassAcque': 'first',
    'Stato': 'first',
    'anno_ultimo_edma': 'first',
    'Tipologia_sito': 'first',
    'ANA_denom_sito': 'first',
    'ANA_anno_apertura': 'first',
    'PRAT_anno_chiusura': 'first',
    
    # Aggregate these as lists
    'Matrice': lambda x: list(set(x.dropna())),  # Remove duplicates & NaN
    'tipo_sostanza': lambda x: list(set(x.dropna())),
    'sostanze': lambda x: list(set(x.dropna())),
    'conc_max': lambda x: list(set(x.dropna())),
    'TecnologieDescrizione': lambda x: list(set(x.dropna())),
    'TipoTecnologiaDescrizione': lambda x: list(set(x.dropna())),
    'note_tecnologia': lambda x: list(set(x.dropna())),
    'MISE_descrizione': lambda x: list(set(x.dropna())),
    'MISP_descrizione': lambda x: list(set(x.dropna())),
    'Simulato_SIAM2':'first'
}).reset_index()

# %%
aggregated_df.to_excel(os.path.join(in_dir,"priori_merge_unique.xlsx"))
# %%
