'''
Code to read a structured concentration file and calculate the median values for each point per year
Input files:
* Idrochimica

Author: Pietro Mazzon

'''
# %%
# import libraries
import os
import pandas as pd
import numpy as np

# set WD
cwd = "c:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/Elaborazioni/E_AnalisiChimiche/" #my directory
df = pd.read_excel(os.path.join(cwd,'idrochimica_tutti_step6_SL_31102024.xlsx'), sheet_name="idrochimica_tutt_step6")

# %%
# drop unwanted cols
df.drop(
    ['COMUNE', 'Descrizione Punto', 'PUNTO_PRELIEVO', 'Tipo di campione', 'Tipologia di analisi', 
     'Nota Prelievo', 'Nota Prelevatore', 'VALORE_ORIGINE', 'UM', 'FONTE'],
    axis=1, 
    inplace=True
)

# %%
# groupby ID_PUNTO and then by YEAR
# create a column "YEAR"
df['ANNO']=df['DATA'].dt.year
df_filtered = df[df['ANNO'].between(2019, 2023)]

# groupby and median values
result_grouped = df_filtered.groupby(['PARAMETRO','ID_PUNTO'])['VALORE_MODIFICATO'].median() #5-year median by PARAMETER & POINT
result_reset_index = result_grouped.reset_index() # make the series "result" a DF and reset of indexes
result_reset_index.rename(columns={'VALORE_MODIFICATO': 'MEDIANA_5ANNI'}, inplace=True)
result_reset_index['MEDIANA_5ANNI'] = result_reset_index['MEDIANA_5ANNI'].round(3)

# %%
result_reset_index.to_csv(os.path.join(cwd, "mediane_5_anagrafica_all.csv")) 
# %%
