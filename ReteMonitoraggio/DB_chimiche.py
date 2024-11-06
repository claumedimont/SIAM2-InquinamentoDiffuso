
# %%
# Load necessary packages and files
import pandas as pd
import os

# Load the Excel files
#in_dir = 'C:\\Users\\user\\OneDrive - Politecnico di Milano\\SF2-Inquinamento_diffuso\\Elaborazioni\\E_AnalisiChimiche\\PerConfronto' # Claudia's path
in_dir = 'C:\\Users\\user\\OneDrive - Politecnico di Milano\\Lavori_idrogeo\\SIAM2\\SF2-Inquinamento_diffuso\\Elaborazioni\\E_AnalisiChimiche\\PerConfronto' # Pietro's path
#chimiche_df = pd.read_excel(os.path.join(in_dir,'idrochimica_tutti_step6_SL_31102024.xlsx'), sheet_name='MEDIA_2015-2018')
chimiche_df = pd.read_csv(os.path.join(in_dir,'mediane.csv'))
#chimiche_df.set_index('ID_PUNTO', inplace=True)

#display(chimiche_df)

anagrafica_df = pd.read_excel(os.path.join(in_dir, 'Anagarafiche aggregate_tutti_SL_061124.xlsx'))
anagrafica_df.rename(columns={'id_punto': 'ID_PUNTO'}, inplace=True)
# anagrafica_df.set_index('ID_PUNTO', inplace=True)

#display(anagrafica_df)

print('Done')

# %%
# Merge the DataFrames on the 'ID' column
selected_anagrafica = anagrafica_df[['ID_PUNTO', 'Xn', 'Yn','CLASSIFICAZIONE_POLITECNICO','CLASSIFICAZIONE_EUPOLIS']] 
#display(selected_anagrafica)

merged_df = pd.merge(chimiche_df, selected_anagrafica, on='ID_PUNTO', how='left')

# Display the first few rows of the merged DataFrame
print(merged_df.head())

print('Done')

# %%
# Save the merged DataFrame to a new Excel file (optional)
merged_df.to_excel(os.path.join(in_dir,'Merged_mediane_2019-2023.xlsx'), index=False)
# %%

print('Done')
