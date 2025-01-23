'''
CODE TO:
1. COMPARE COORDS BETWEEN 'ANAGRAFICA' AND 'ASSEGNAZIONE ACQUIFERO'
2. GET ANNUAL MEDIAN VALUES OF HYDROCHEMICAL DATA 'MEDIANA ANNUALE DATI IDROCHIMICI'
3. MERGE BOTH FILES

INPUT FILES:
* Anagarafiche_aggregate_tutti
* Assegnazione_acquifero
* idrochimica_tutti

OUTPUT FILES:
* Merged_idrochimica

'''
# %%
# Load necessary packages and files
import pandas as pd
import os

# Load the Excel files
in_dir = 'C:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/Elaborazioni/E_AnalisiChimiche/PerConfronto/Input_files/' 
acquiferi_df = pd.read_excel(os.path.join(in_dir,'Assegnazione_acquifero_230125.xlsx'), sheet_name="Confronti_classifica")
idrochimica_df = pd.read_excel(os.path.join(in_dir,'idrochimica_tutti_step6_SL_31102024.xlsx'))
anagrafica_df = pd.read_excel(os.path.join(in_dir, 'Anagarafiche_aggregate_tutti_SL_100125.xlsx'))


# %%
# 1. COMPARE COORDS BETWEEN 'ANAGRAFICA' AND 'ASSEGNAZIONE ACQUIFERO'
# Keep only the columns 'ID_point', 'X', and 'Y'
df1 = acquiferi_df[['id_punto_idrochimica', 'X', 'Y', 'CLASSIFICA_DEF']]
df1['X'] = df1['X'].round(0)
df1['Y'] = df1['Y'].round(0)
df2 = anagrafica_df[['id_punto_idrochimica', 'Xn', 'Yn']]
df2['Xn'] = df2['Xn'].round(0)
df2['Yn']= df2['Yn'].round(0)

# Merge the dataframes on 'ID_point' to compare coordinates
merged_df = pd.merge(df1, df2, on='id_punto_idrochimica')
merged_df.rename(columns={'id_punto_idrochimica': 'ID_PUNTO'}, inplace=True)

# Add a flag column where inconsistencies between the coordinates are found
merged_df['Flag'] = (merged_df['X'] != merged_df['Xn']) | (merged_df['Y'] != merged_df['Yn'])

# Filter only the points where there is a flag
flagged_points = merged_df[merged_df['Flag']]

# %%
# 2. GET ANNUAL MEDIAN VALUES OF HYDROCHEMICAL DATA 'MEDIANA ANNUALE DATI IDROCHIMICI'
# drop unnecesary cols
df3 = idrochimica_df[['ID_PUNTO', 'DATA', 'VALORE_MODIFICATO', 'PARAMETRO', 'FONTE']]

# create a column "YEAR"
df3['ANNO']=df3['DATA'].dt.year

# group by PARAMETER, point and by year, then calculates the median of the column valore modificato
df3_result = df3.groupby(['PARAMETRO','ID_PUNTO','ANNO'])['VALORE_MODIFICATO'].median() 
df3_result = df3_result.reset_index()
df3_result.rename(columns={'VALORE_MODIFICATO': 'MEDIANA_ANNO'}, inplace=True)

# %%
# 3. MERGE FILES
# Preparing files to merge
merged_df = merged_df.drop(['X', 'Y', 'Flag'], axis=1)

#fixing possible sources of error during merge
#setting as string
merged_df['ID_PUNTO'] = merged_df['ID_PUNTO'].astype(str)
df3_result['ID_PUNTO'] = df3_result['ID_PUNTO'].astype(str)

#deleting white spaces
merged_df['ID_PUNTO'] = merged_df['ID_PUNTO'].str.strip() 
df3_result['ID_PUNTO'] = df3_result['ID_PUNTO'].str.strip()

# Merge the DataFrames on the 'ID' column
final_df = pd.merge(merged_df, df3_result, on='ID_PUNTO', how='left')

# Display the first few rows of the merged DataFrame
print(final_df.head())

# %%
# Save the merged DataFrame to a new Excel file
final_df.to_excel(os.path.join(in_dir,'Merged_idrochimica.xlsx'), index=False)


# %%
'''
NEW PART: GET MEDIAN VALUES FOR PERIODS 2015-2019 AND 2020-2023 PER EACH COMPONENT

'''
# Run STEP 1. first
# 2. GET ANNUAL MEDIAN VALUES OF HYDROCHEMICAL DATA 'MEDIANA ANNUALE DATI IDROCHIMICI'
# drop unnecesary cols
df3 = idrochimica_df[['ID_PUNTO', 'DATA', 'VALORE_MODIFICATO', 'PARAMETRO', 'FONTE']]

# create a column "YEAR"
df3['ANNO']=df3['DATA'].dt.year

# Define the periods
period1 = range(2015, 2020)
period2 = range(2020, 2024)

# Preparing files to merge
merged_df = merged_df.drop(['X', 'Y', 'Flag'], axis=1)
#fixing possible sources of error during merge
#setting as string
merged_df['ID_PUNTO'] = merged_df['ID_PUNTO'].astype(str)
#deleting white spaces
merged_df['ID_PUNTO'] = merged_df['ID_PUNTO'].str.strip() 

# Process the data to calculate medians for each parameter and period
# Initialize an empty list to store results for all parameters
parameters = df3['PARAMETRO'].unique()

for param in parameters:
    # Filter data for the current parameter
    param_data = df3[df3['PARAMETRO'] == param]

    # Calculate medians for each period
    median_2015_2019 = param_data[param_data['ANNO'].isin(period1)] \
        .groupby(['ID_PUNTO'], as_index=False)['VALORE_MODIFICATO'].median()
    median_2015_2019.rename(columns={'VALORE_MODIFICATO': f'{param}_2015_2019'}, inplace=True)

    median_2020_2023 = param_data[param_data['ANNO'].isin(period2)] \
        .groupby(['ID_PUNTO'], as_index=False)['VALORE_MODIFICATO'].median()
    median_2020_2023.rename(columns={'VALORE_MODIFICATO': f'{param}_2020_2023'}, inplace=True)

    # Merge the results for both periods
    medians = pd.merge(median_2015_2019, median_2020_2023, 
                           on=['ID_PUNTO'], how='outer')

    #fixing possible sources of error during merge
    #setting as string
    medians['ID_PUNTO'] = medians['ID_PUNTO'].astype(str)
    #deleting white spaces
    medians['ID_PUNTO'] = medians['ID_PUNTO'].str.strip()

    # Merge the DataFrames on the 'ID' column
    final_meds = pd.merge(merged_df, medians, on='ID_PUNTO', how='left')

    # Save the result to a file for the current parameter
    final_meds.to_excel(os.path.join(in_dir,f'Mediane_{param}.xlsx'), index=False)

    # Print confirmation
    print(f"Saved results for {param} to {final_meds}")

# %%
