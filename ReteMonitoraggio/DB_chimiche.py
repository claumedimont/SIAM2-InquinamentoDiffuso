'''
CODE TO MERGE 'ANAGRAFICA' AND 'IDROCHIMICA' PER ID_PUNTO

'''
# %%
# Load necessary packages and files
import pandas as pd
import os

# Load the Excel files
in_dir = 'C:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/Elaborazioni/E_AnalisiChimiche/PerConfronto' 
chimiche_df = pd.read_excel(os.path.join(in_dir,'idrochimica_tutti_step6_SL_31102024.xlsx'), sheet_name='idrochimica_tutt_step6')
#chimiche_df = pd.read_csv(os.path.join(in_dir,'mediane.csv'))
anagrafica_df = pd.read_excel(os.path.join(in_dir, 'Anagarafiche aggregate_tutti_SL_061124.xlsx'))

# %%
#fixing possible sources of error during merge
chimiche_df['ID_PUNTO'] = chimiche_df['ID_PUNTO'].astype(str) #setting as string
anagrafica_df['ID_PUNTO'] = anagrafica_df['ID_PUNTO'].astype(str)
chimiche_df['ID_PUNTO'] = chimiche_df['ID_PUNTO'].str.strip() #deleting white spaces
anagrafica_df['ID_PUNTO'] = anagrafica_df['ID_PUNTO'].str.strip()

# %%
# Merge the DataFrames on the 'ID' column
selected_anagrafica = anagrafica_df[['ID_PUNTO', 'Xn', 'Yn','CLASSIFICAZIONE_POLITECNICO','CLASSIFICAZIONE_EUPOLIS']] #Get only these columns from the anagrafica
merged_df = pd.merge(chimiche_df, selected_anagrafica, on='ID_PUNTO', how='left')

# Display the first few rows of the merged DataFrame
print(merged_df.head())

# %%
# Save the merged DataFrame to a new Excel file (optional)
merged_df.to_excel(os.path.join(in_dir,'Merged_complete_anagrafica.xlsx'), index=False)
# %%
