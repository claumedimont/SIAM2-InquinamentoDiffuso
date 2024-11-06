
# %%
# Load necessary packages and files
import pandas as pd
import os

# Load the Excel files
in_dir = 'C:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/Elaborazioni/E_AnalisiChimiche/PerConfronto' 
#chimiche_df = pd.read_excel(os.path.join(in_dir,'idrochimica_tutti_step6_SL_31102024.xlsx'), sheet_name='MEDIA_2015-2018')
chimiche_df = pd.read_excel(os.path.join(in_dir,'idrochimica_tutti_step6_SL_31102024.xlsx'), sheet_name='MEDIA_2019-2023')

anagrafica_df = pd.read_excel(os.path.join(in_dir, 'AnagaraficheAggregate_tutti_SL_291024.xlsx'))

# %%
# Merge the DataFrames on the 'ID' column
selected_anagrafica = anagrafica_df[['ID_PUNTO', 'Xn', 'Yn','CLASSIFICAZIONE_POLITECNICO','CLASSIFICAZIONE_EUPOLIS']] 
merged_df = pd.merge(chimiche_df, selected_anagrafica, on='ID_PUNTO', how='left')

# Display the first few rows of the merged DataFrame
print(merged_df.head())

# %%
# Save the merged DataFrame to a new Excel file (optional)
merged_df.to_excel(os.path.join(in_dir,'Merged_2019-2023.xlsx'), index=False)
# %%
