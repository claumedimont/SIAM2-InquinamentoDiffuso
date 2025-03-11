'''
CODE TO:
1. 

INPUT FILES:
* 
OUTPUT FILES:
* 
NEW VERSION: INCLUDING DB AMIIGA AND SELECTION OF POINTS = ALL POINTS OF DATI MONITORAGGIO --> MEDIANE ANNUALE IN ARCGIS
IN ACQ A, B, AND AB.
MONIT_ALL DOES NOT HAVE ANY SELECTION OF POINTS. SHOULD INCLUDE ALL OF THEM

'''
# %%
# Load necessary packages and files
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# %%
# Load the Excel files
# Buffer files
in_dir1 = 'C:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/GIS/Confronto/ReteMonitoraggio/Selezione_A_AB_B/' 
punti_df = pd.read_csv(os.path.join(in_dir1,'Cromo.csv'))
#L1_df = pd.read_csv(os.path.join(in_dir1,'TCM_L1.csv'))
#L5_df = pd.read_csv(os.path.join(in_dir1,'TCM_L5.csv'))
#NON_df = pd.read_excel(os.path.join(in_dir1,'TCM_daNONescludere.xlsx'))
#sorg_df = pd.read_csv(os.path.join(in_dir1,'TCM_sorgenti.csv'))

# Monitoring data files
in_dir2 = 'C:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/Elaborazioni/E_AnalisiChimiche/' 
in_dir3 = 'C:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/Dati origine/Analisi chimiche/' 
siam_df = pd.read_excel(os.path.join(in_dir2,'idrochimica_tutti_step6_SL_31102024.xlsx'), sheet_name="idrochimica_tutt_step6")
amiiga_df = pd.read_excel(os.path.join(in_dir3, 'Progetti_vecchi/AMIIGA/DB_AMIIGA.xlsx'))

# %%
# 1. All buffer files into a single df
# points_df = pd.concat([L1_df, L5_df, sorg_df], ignore_index=True)
points_df = punti_df.drop(['ANNO', 'MEDIANA_AN'], axis=1)
points_df = punti_df.drop_duplicates().reset_index(drop=True)

# Remove points "da non escludere"
# Ensure ID_PUNTO columns are strings, stripped of spaces, and in uppercase for consistency
# points_df["ID_PUNTO"] = points_df["ID_PUNTO"].astype(str).str.strip().str.upper()
# NON_df["ID_PUNTO"] = NON_df["ID_PUNTO"].astype(str).str.strip().str.upper()
# points_df = points_df[~points_df['ID_PUNTO'].isin(NON_df['ID_PUNTO'])]

# %%
# 2. Get the data ONLY for the points inside points_df from the monitoring data files
# SIAM Data
siam_filtered = siam_df[siam_df['ID_PUNTO'].isin(points_df['ID_PUNTO'])]
siam_filtered = siam_filtered.drop(['COMUNE', 'PUNTO_PRELIEVO', 'Descrizione Punto',
       'Tipo di campione', 'Tipologia di analisi', 'Nota Prelievo','Nota Prelevatore', 'VALORE_ORIGINE',
       'UM', 'FONTE'], axis=1)

siam_cr = siam_filtered[(siam_filtered['PARAMETRO'] == 'Cromo totale') | (siam_filtered['PARAMETRO'] == 'Cromo VI')]
#siam_cr = siam_cr.drop(["PARAMETRO"], axis=1)
siam_cr = siam_cr.rename(columns={'VALORE_MODIFICATO': 'VALORE'}).reset_index(drop=True)

siam_all = siam_df.drop(['COMUNE', 'PUNTO_PRELIEVO', 'Descrizione Punto',
       'Tipo di campione', 'Tipologia di analisi', 'Nota Prelievo','Nota Prelevatore', 'VALORE_ORIGINE',
       'UM', 'FONTE'], axis=1)
siam_all = siam_all[(siam_all['PARAMETRO'] == 'Cromo totale') | (siam_all['PARAMETRO'] == 'Cromo VI')]
#siam_all = siam_all.drop(["PARAMETRO"], axis=1)
siam_all = siam_all.rename(columns={'VALORE_MODIFICATO': 'VALORE'}).reset_index(drop=True)

# DB AMIIGA
amiiga_filtered = amiiga_df[(amiiga_df['CODICE_PP'].isin(points_df['ID_PUNTO'])) | (amiiga_df['codice_sif'].isin(points_df['ID_PUNTO']))]
amiiga_filtered['ID_PUNTO'] = np.where(
    amiiga_filtered['CODICE_PP'].isin(points_df['ID_PUNTO']),
    amiiga_filtered['CODICE_PP'],
    amiiga_filtered['codice_sif']
)

amiiga_filtered = amiiga_filtered[(amiiga_filtered['Parametro_'] == 'Cromo (VI)') | (amiiga_filtered['Parametro_'] == 'Cromo Totale (Cr)')]
amiiga_filtered = amiiga_filtered.drop(['CODICE_PP', 'DESCRIZION', 'PROVINCIA', 'COMUNE',
       'ANNO','DataValida', 'Fonte', 'ID_CAMPION',
       'RgaNaccett', 'UM', 'CAS', 'Segno',
       'VALORE_TES', 'codice_sif', 'ARPA_Plume', 'X', 'corrispond', 'macro', 
       'Y', 'tipo_falda', 'classifica'], axis=1)
amiiga_filtered = amiiga_filtered.rename(columns={'DataCampio': 'DATA', 'VALORE_NUM': 'VALORE',
                                                  'codice_sif':'ID_PUNTO','Parametro_':'PARAMETRO'}).reset_index(drop=True)

amiiga_all = amiiga_df[(amiiga_df['Parametro_'] == 'Cromo (VI)') | (amiiga_df['Parametro_'] == 'Cromo Totale (Cr)')]
amiiga_all = amiiga_all.drop(['CODICE_PP', 'DESCRIZION', 'PROVINCIA', 'COMUNE',
       'ANNO','DataValida', 'Fonte', 'ID_CAMPION',
       'RgaNaccett', 'UM', 'CAS', 'Segno',
       'VALORE_TES', 'ARPA_Plume', 'X', 'corrispond', 'macro', 
       'Y', 'tipo_falda', 'classifica'], axis=1)
amiiga_all = amiiga_all.rename(columns={'DataCampio': 'DATA', 
                                              'VALORE_NUM': 'VALORE',
                                              'codice_sif':'ID_PUNTO',
                                              'Parametro_':'PARAMETRO'}).reset_index(drop=True)


# %%
# 3. Get unique monitoring dataset
monit_df = pd.concat([siam_cr, amiiga_filtered], ignore_index=True).sort_values(["ID_PUNTO", "DATA"]).reset_index(drop=True)
monit_all = pd.concat([siam_all, amiiga_all], ignore_index=True).sort_values(["ID_PUNTO", "DATA"]).reset_index(drop=True)
#also consider points with less than 10 measures for the areas of interes
# Count the number of measurements per monitoring point & remove points with fewer than 10 measurements
counts = monit_df.groupby("ID_PUNTO")["VALORE"].count().reset_index()
counts.rename(columns={"VALORE": "N_MISURE"}, inplace=True)
counts_sel = counts[counts["N_MISURE"] >= 10]

# Merge with points_df
points_sel = points_df.merge(counts_sel, on="ID_PUNTO", how="inner")
points_df = points_df.merge(counts, on="ID_PUNTO", how="inner")

# Replace counts with labels
def categorize_count(value):
     if value > 30:
         return ">30"
     elif value > 20:
         return ">20"
     else:
         return ">10"

points_sel["N_MISURE"] = points_sel["N_MISURE"].apply(categorize_count)

points_sel["PARAMETRO"] = points_sel["PARAMETRO"].replace({
    "Cromo totale": "CrTotale",
    "Cromo Totale (Cr)": "CrTotale",
    "Cromo VI": "CrVI",
    "Cromo (VI)": "CrVI"
})

monit_df["PARAMETRO"] = monit_df["PARAMETRO"].replace({
    "Cromo totale": "CrTotale",
    "Cromo Totale (Cr)": "CrTotale",
    "Cromo VI": "CrVI",
    "Cromo (VI)": "CrVI"
})

monit_all["PARAMETRO"] = monit_all["PARAMETRO"].replace({
    "Cromo totale": "CrTotale",
    "Cromo Totale (Cr)": "CrTotale",
    "Cromo VI": "CrVI",
    "Cromo (VI)": "CrVI"
})

# save files
points_sel.to_csv(os.path.join(in_dir1, "Cromo_n_misure.csv"))
#points_df.to_csv(os.path.join(in_dir1, "TCM_daEscludere.csv"))
monit_df.to_csv(os.path.join(in_dir1, "Cromo_sel_data.csv"))
monit_all.to_csv(os.path.join(in_dir1, "Cromo_all_points.csv"))

# %%
# 4. Plot
in_dir1 = 'C:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/GIS/Confronto/ReteMonitoraggio/Selezione_A_AB_B/'
monit_df = pd.read_csv(os.path.join(in_dir1, "Cromo_sel_data.csv")).reset_index(drop=True)
output_folder = os.path.join(in_dir1,"Plots")
os.makedirs(output_folder, exist_ok=True)
monit_df["DATA"] = pd.to_datetime(monit_df["DATA"], format="%Y-%m-%d", errors="coerce")

# %%
# output_folder = os.path.join(in_dir1,"Plots")
# os.makedirs(output_folder, exist_ok=True)
monit_all = pd.read_csv(os.path.join(in_dir1,"Cromo_all_points.csv")).reset_index(drop=True)
# monit_df["DATA"] = pd.to_datetime(monit_df["DATA"], format="%Y-%m-%d", errors="coerce")
monit_all["DATA"] = pd.to_datetime(monit_all["DATA"], format="%Y-%m-%d", errors="coerce")

# sel df
data_df = monit_all

# %%
# Points to plot
#param = 'Cromo VI'
selected_points = ['151460402']
# check data for a monitoring point
#monit_df.loc[monit_df['ID_PUNTO']==selected_points]

# Plot each monitoring point
# Set Seaborn style
sns.set_style("darkgrid")
for point in selected_points:
    #df_point = data_df[(data_df['ID_PUNTO'] == point) & (data_df['PARAMETRO']== param)]  # Filter data for the point and param
    df_point = data_df[data_df['ID_PUNTO'] == point]
    df_point = df_point.sort_values(by="DATA")  # Ensure the dates are sorted

    # Create figure
    plt.figure(figsize=(10, 6))
    
    # Seaborn lineplot with markers
    sns.lineplot(data=df_point, x="DATA", y="VALORE", hue="PARAMETRO", marker="o", linewidth=2.5)

    # Formatting the plot
    plt.xlabel("Data", fontsize=12)
    plt.ylabel(f"Valore Cromo (ug/L)", fontsize=12)
    plt.title(f"{point}", fontsize=14, fontweight="bold")
    plt.ylim(0, 250)

    # Rotate x-axis labels and format dates nicely
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))  # Show Year-Month
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))  # Show every 6 months

    # Improve layout
    plt.grid(True, linestyle="--", alpha=0.6)  # Dotted grid
    plt.tight_layout()

    # Save the plot as a PNG file
    filename = os.path.join(output_folder, f"{point}.png")
    plt.savefig(filename, dpi=300, bbox_inches="tight")  # Save with high resolution
    plt.close()  # Close the figure to free memory
    plt.show()

print(f"Plots saved in '{output_folder}' folder.")
# %%
