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
sel_df = pd.read_excel(os.path.join(in_dir, 'DaCondividire/SIAM2_Complessivo.xlsx'), sheet_name="TuttiRecords")
priori_df = pd.read_excel(os.path.join(in_dir, 'DaCondividire/SIAM2_Siti_Aggiornati.xlsx'), sheet_name="SITI_PRIORITARI")
proced_df = pd.read_excel(os.path.join(in_dir, 'DaCondividire/SIAM2_Siti_Aggiornati.xlsx'), sheet_name="SITI_PROCEDIMENTO")


# %%
#merge info no agregation
cods_priori = priori_df[['COD_SITO','Stato2017-2019','Simulato_SIAM2']]
cods_proced = proced_df[['COD_SITO', 'Stato_2017','Simulato_SIAM2', 'Note']]
agg_merge = pd.merge(cods_priori, sel_df, on='COD_SITO', how='left')
agg_merge["DGR_SITO"] = 'Prioritario'
agg_merge = agg_merge.rename({'Stato2017-2019':'Stato_iniziale', 'Stato':'Stato_attuale'}, axis=1)
agg_merge2 = pd.merge(cods_proced, sel_df, on='COD_SITO', how='left')
agg_merge2["DGR_SITO"] = 'Procedimento'
agg_merge2 = agg_merge2.rename({'Stato_2017':'Stato_iniziale', 'Stato':'Stato_attuale'}, axis=1)
siti_siam = pd.concat([agg_merge, agg_merge2], ignore_index = True)
#agg_merge = agg_merge.drop(['Provincia', 'Comune'], axis=1)

# %%
siti_siam.to_excel(os.path.join(in_dir,"solo_siti_comp.xlsx"))

# %%
# ultimate aggregation
# Group by 'COD_SITO' and aggregate multiple values as lists
aggregated_df = sel_df.groupby('COD_SITO').agg({
    'Provincia':'first',
    'Comune':'first',
    'Stato': 'first',
    'ANA_denom_sito': 'first',
    'ANA_classific_attuale': 'first',
    'descClassSuoli': 'first',
    'descClassAcque': 'first',
    'anno_ultimo_edma': 'first',
    'Tipologia_sito': 'first',
    'ANA_anno_apertura': 'first',
    'PRAT_anno_chiusura': 'first',
    
    # Aggregate these as lists
    'Matrice': lambda x: list(set(x.dropna())),  # Remove duplicates & NaN
    'tipo_sostanza': lambda x: list(set(x.dropna())),
    'sostanze': lambda x: list(set(x.dropna())),
    #'conc_max': lambda x: list(set(x.dropna())),
    'TecnologieDescrizione': lambda x: list(set(x.dropna())),
    'TipoTecnologiaDescrizione': lambda x: list(set(x.dropna())),
    'note_tecnologia': lambda x: list(set(x.dropna())),
    'MISE_descrizione': lambda x: list(set(x.dropna())),
    'MISP_descrizione': lambda x: list(set(x.dropna())),
}).reset_index()

# %%
aggregated_df.to_excel(os.path.join(in_dir,"tutti_merge_unique.xlsx"))
# %%
