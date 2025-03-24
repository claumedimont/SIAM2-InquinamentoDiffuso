'''
PLOTS PER MONITORING POINT PER INQUINANTE

'''

# %%
# Load necessary packages and files
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

# Define function
# Get the data ONLY for the points inside points_df from the monitoring data files
def monitoring(siam_df, amiiga_df, points_df):
    points_df["ID_PUNTO"] = points_df["ID_PUNTO"].astype(str).str.strip().str.upper()
    # SIAM data
    siam_df["ID_PUNTO"] = siam_df["ID_PUNTO"].astype(str).str.strip().str.upper()
    siam_filtered = siam_df[siam_df['ID_PUNTO'].isin(points_df['ID_PUNTO'])]
    siam_filtered = siam_filtered.drop(['COMUNE', 'PUNTO_PRELIEVO', 'Descrizione Punto',
       'Tipo di campione', 'Tipologia di analisi', 'Nota Prelievo','Nota Prelevatore', 'VALORE_ORIGINE',
       'UM', 'FONTE'],axis=1)
    siam_cr6 = siam_filtered[(siam_filtered['PARAMETRO'] == 'Cromo VI')]
    siam_cr6 = siam_cr6.rename(columns={'VALORE_MODIFICATO': 'VALORE'}).reset_index(drop=True)
    siam_crTOT = siam_filtered[(siam_filtered['PARAMETRO'] == 'Cromo totale')]
    siam_crTOT = siam_crTOT.rename(columns={'VALORE_MODIFICATO': 'VALORE'}).reset_index(drop=True)

    # DB AMIIGA
    amiiga_df["CODICE_PP"] = amiiga_df["CODICE_PP"].astype(str).str.strip().str.upper()
    amiiga_df["codice_sif"] = amiiga_df["codice_sif"].astype(str).str.strip().str.upper()
    amiiga_filtered = amiiga_df[(amiiga_df['CODICE_PP'].isin(points_df['ID_PUNTO'])) | (amiiga_df['codice_sif'].isin(points_df['ID_PUNTO']))]
    amiiga_filtered['ID_PUNTO'] = np.where(
        amiiga_filtered['CODICE_PP'].isin(points_df['ID_PUNTO']),
        amiiga_filtered['CODICE_PP'],
        amiiga_filtered['codice_sif']
    )
    amiiga_filtered = amiiga_filtered.drop(['CODICE_PP', 'DESCRIZION', 'PROVINCIA', 'COMUNE','ANNO','DataValida', 
                                            'Fonte', 'ID_CAMPION', 'RgaNaccett', 'UM', 'CAS', 'Segno','VALORE_TES', 
                                            'codice_sif', 'ARPA_Plume', 'X', 'corrispond', 'macro', 'Y', 'tipo_falda', 'classifica'], axis=1)
    amiiga_filtered = amiiga_filtered.rename(columns={'DataCampio': 'DATA', 'VALORE_NUM': 'VALORE',
                                                    'codice_sif':'ID_PUNTO','Parametro_':'PARAMETRO'}).reset_index(drop=True)

    amiiga_Cr6 = amiiga_filtered[(amiiga_filtered['PARAMETRO'] == 'Cromo (VI)')]
    amiiga_CrTOT = amiiga_filtered[(amiiga_filtered['PARAMETRO'] == 'Cromo Totale (Cr)')]
    
    monit_df_Cr6 = pd.concat([siam_cr6, amiiga_Cr6], ignore_index=True).sort_values(["ID_PUNTO", "DATA"]).reset_index(drop=True)
    monit_df_Cr6["PARAMETRO"] = monit_df_Cr6["PARAMETRO"].replace({
    "Cromo VI": "Cr6",
    "Cromo (VI)": "Cr6"})
    monit_df_CrTOT = pd.concat([siam_crTOT, amiiga_CrTOT], ignore_index=True).sort_values(["ID_PUNTO", "DATA"]).reset_index(drop=True)
    monit_df_CrTOT["PARAMETRO"] = monit_df_CrTOT["PARAMETRO"].replace({
    "Cromo totale": "CrTOT",
    "Cromo Totale (Cr)": "CrTOT"})
    return [monit_df_Cr6,monit_df_CrTOT]


# Load the common Excel files
cwd1 = 'c:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/Elaborazioni/E_AnalisiChimiche/'
cwd2 = 'C:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/Dati origine/Analisi chimiche/' 
siam_df = pd.read_excel(os.path.join(cwd1,'idrochimica_tutti_step6_SL_31102024.xlsx'), sheet_name="idrochimica_tutt_step6")
values = {'PCE': [1.1, 10, 30, 70, 100, 200, 500, 1000], 
          'TCE': [1.5, 10, 30, 70, 100, 200, 500, 1000],
          'TCM': [0.15, 1, 10, 30, 50, 100, 200, 500],
          'Cromo': [5, 10, 30, 70, 100, 200, 500, 1000]}
asymptotes = pd.DataFrame(values)

# %%
'''
CROMO
'''

# Get a monitoring dataset per each point for which a mediana has been calculated
inq1 = 'Cr6'
inq2 = "CrTOT"
points1_df = pd.read_csv(os.path.join(cwd1, f"PerConfronto/ArcGIS_input/DEF/ULT_{inq1}_mediane_2019-2023.csv"))  #points
points2_df = pd.read_csv(os.path.join(cwd1, f"PerConfronto/ArcGIS_input/DEF/ULT_{inq2}_mediane_2019-2023.csv"))  #points
amiiga_df = pd.read_excel(os.path.join(cwd2, 'Progetti_vecchi/AMIIGA/DB_AMIIGA.xlsx'))
monit_cr6 = monitoring(siam_df, amiiga_df, points1_df)
monit_cr6 = monit_cr6[0]
monit_cr6.to_csv(os.path.join(cwd1, f"PerConfronto/ArcGIS_input/DEF/{inq1}_dati_monitoraggio.csv"))
monit_crTOT = monitoring(siam_df, amiiga_df, points2_df)
monit_crTOT = monit_crTOT[1]
monit_crTOT.to_csv(os.path.join(cwd1, f"PerConfronto/ArcGIS_input/DEF/{inq2}_dati_monitoraggio.csv"))

# %%
#Add counts
counts_cr6 = monit_cr6.groupby('ID_PUNTO').size().reset_index(name='numero_misure')
update1_df = points1_df.merge(counts_cr6, on='ID_PUNTO', how='left')
update1_df.to_csv(os.path.join(cwd1, f"LAST_{inq1}_mediane_2019-2023.csv"))
counts_crTOT = monit_crTOT.groupby('ID_PUNTO').size().reset_index(name='numero_misure')
update2_df = points2_df.merge(counts_crTOT, on='ID_PUNTO', how='left')
update2_df.to_csv(os.path.join(cwd1, f"LAST_{inq2}_mediane_2019-2023.csv"))

asymptote_values = asymptotes["Cromo"].to_list()
output_folder_cr6 = os.path.join(cwd1, f"PerConfronto/ArcGIS_input/PLOTS/{inq1}") # output folder
output_folder_crTOT = os.path.join(cwd1, f"PerConfronto/ArcGIS_input/PLOTS/{inq2}") # output folder

# %%
#Define lower significant concentration
inq = "CrTOT"
points_df = points2_df
output_folder = output_folder_crTOT
monitoring_df = monit_crTOT
lowest = 25
selected_points = points_df[points_df[f"Cromo totale_2019_2023"] >= lowest]["ID_PUNTO"].tolist() # Points to plot
print (len(selected_points))

# %%
monitoring_df["DATA"] = pd.to_datetime(monitoring_df["DATA"], format="%Y-%m-%d", errors="coerce")
# Plot each monitoring point
sns.set_style("darkgrid")
for point in selected_points:
    df_point = monitoring_df[monitoring_df['ID_PUNTO'] == point]  # Filter data for the point
    df_point = df_point.sort_values(by="DATA")  # Ensure the dates are sorted

    # Create figure
    plt.figure(figsize=(10, 6))
    
    # Seaborn lineplot with markers
    sns.lineplot(data=df_point, x="DATA", y="VALORE", marker="o", color="royalblue", linewidth=2.5)

    # Formatting the plot
    plt.xlabel("Data", fontsize=12)
    plt.ylabel(f"Valore {inq} (ug/L)", fontsize=12)
    plt.title(f"{point}", fontsize=14, fontweight="bold")
    max_y = df_point["VALORE"].max()  # Get max value from data
    # If max_y is NaN or Inf, set a default upper limit
    if not np.isfinite(max_y):  
        max_y = 10 
    plt.ylim(0, max_y + 5) 

    # Rotate x-axis labels and format dates nicely
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))  # Show Year-Month
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))  # Show every 6 months
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(integer=True)) # just integers on y axis

    # Add reference horizontal lines (asymptotes)
    for y_value in asymptote_values:
        plt.axhline(y=y_value, color="black", linestyle="--", linewidth=1, alpha=0.7)

    # Improve layout
    plt.grid(True, linestyle="--", alpha=0.6)  # Dotted grid
    plt.tight_layout()

    # Save the plot as a PNG file
    filename = os.path.join(output_folder, f"{point}.png")
    plt.savefig(filename, dpi=300, bbox_inches="tight")  # Save with high resolution
    plt.show()
    plt.close()  # Close the figure to free memory
    

print(f"Plots saved in '{output_folder}' folder.")
# %%
