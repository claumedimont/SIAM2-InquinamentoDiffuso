'''
GRAFICI

'''

# Load necessary packages and files
import pandas as pd
import os

# Load the Excel files
in_dir = 'C:/Users/user/OneDrive - Politecnico di Milano/04_REGIONE/SIAM2-AggiornamentoSitiMisure/Elaborazioni/' 
main_df = pd.read_excel((os.path.join(in_dir,"tutti_merge_unique.xlsx")))
