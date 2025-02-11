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
sel_df = pd.read_excel(os.path.join(in_dir, 'SIAM2_SelezioneAGISCO.xlsx'), sheet_name="UniTecno")
agg_df = pd.read_excel(os.path.join(in_dir, 'SIAM2_Siti_Agg.xlsx'), sheet_name="SITI_PROCEDIMENTO")


# %%
#merge points with info about the applied remediation tecnology
agg_merge = agg_df.merge(sel_df, on='COD_SITO', how='left')
agg_merge = agg_merge.drop(['Provincia', 'Comune'], axis=1)

# %%
agg_merge.to_excel(os.path.join(in_dir,"procedi_merge.xlsx"))
# %%
