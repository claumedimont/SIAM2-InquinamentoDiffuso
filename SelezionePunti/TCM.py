'''
CODE TO:
1. 

INPUT FILES:
* 
OUTPUT FILES:
* 

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
in_dir1 = 'C:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/GIS/Confronto/Buffers/Selezione_punti/TCM/' 
L1_df = pd.read_csv(os.path.join(in_dir1,'TCM_L1.csv'))
L5_df = pd.read_csv(os.path.join(in_dir1,'TCM_L5.csv'))
NON_df = pd.read_excel(os.path.join(in_dir1,'TCM_daNONescludere.xlsx'))
sorg_df = pd.read_csv(os.path.join(in_dir1,'TCM_sorgenti.csv'))

# Monitoring data files
in_dir2 = 'C:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/Elaborazioni/E_AnalisiChimiche/' 
in_dir3 = 'C:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/Dati origine/Analisi chimiche/' 
siam_df = pd.read_excel(os.path.join(in_dir2,'idrochimica_tutti_step6_SL_31102024.xlsx'), sheet_name="idrochimica_tutt_step6")
mind_df = pd.read_excel(os.path.join(in_dir3,'PCE_TCE_E_query dati_MIND_2018.xlsx'), sheet_name="TCM")

# %%
# 1. All buffer files into a single df
points_df = pd.concat([L1_df, L5_df, sorg_df], ignore_index=True)
points_df = points_df.drop(['ANNO', 'MEDIANA_AN'], axis=1)
points_df = points_df.drop_duplicates().reset_index(drop=True)

# Remove points "da non escludere"
# Ensure ID_PUNTO columns are strings, stripped of spaces, and in uppercase for consistency
points_df["ID_PUNTO"] = points_df["ID_PUNTO"].astype(str).str.strip().str.upper()
NON_df["ID_PUNTO"] = NON_df["ID_PUNTO"].astype(str).str.strip().str.upper()
points_df = points_df[~points_df['ID_PUNTO'].isin(NON_df['ID_PUNTO'])]

# %%
# 2. Get the data ONLY for the points inside points_df from the monitoring data files
# SIAM data
siam_filtered = siam_df[siam_df['ID_PUNTO'].isin(points_df['ID_PUNTO'])]
siam_filtered = siam_filtered.drop(['COMUNE', 'PUNTO_PRELIEVO', 'Descrizione Punto',
       'Tipo di campione', 'Tipologia di analisi', 'Nota Prelievo','Nota Prelevatore', 'VALORE_ORIGINE',
       'UM', 'FONTE'],axis=1)
siam_tcm = siam_filtered[siam_filtered['PARAMETRO'] == 'Cloroformio']
siam_tcm = siam_tcm.drop(["PARAMETRO"], axis=1)
siam_tcm = siam_tcm.rename(columns={'VALORE_MODIFICATO': 'VALORE'}).reset_index(drop=True)

# MIND data
mind_filtered = mind_df[mind_df['CODICE_PP'].isin(points_df['ID_PUNTO']) | mind_df['codice_sif'].isin(points_df['ID_PUNTO'])]
mind_filtered['ID_PUNTO'] = np.where(
    mind_filtered['CODICE_PP'].isin(points_df['ID_PUNTO']),
    mind_filtered['CODICE_PP'],
    mind_filtered['codice_sif'])
mind_filtered = mind_filtered.drop(['CODICE_PP', 'DESCRIZIONE_PUNTO_PRELIEVO', 'PROVINCIA', 'COMUNE',
       'ANNO', 'DataValidazione', 'Fonte', 'ID_CAMPIONE',
       'RgaNaccettazione', 'Parametro_unificato', 'UM', 'CAS', 'Segno',
       'VALORE_TESTO', 'codice_sif', 'ARPA_Plumes', 'X',
       'Y', 'tipo_falda', 'class_poli'],axis=1)
mind_filtered = mind_filtered.rename(columns={'DataCampionamento': 'DATA', 
                                              'VALORE_NUMERICO': 'VALORE'}).reset_index(drop=True)

# %%
# 3. Get unique monitoring dataset
monit_df = pd.concat([siam_tcm, mind_filtered], ignore_index=True).sort_values(["ID_PUNTO", "DATA"]).reset_index(drop=True)

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

# save files
points_sel.to_csv(os.path.join(in_dir1, "TCM_n_misure.csv"))
points_df.to_csv(os.path.join(in_dir1, "TCM_daEscludere.csv"))
monit_df.to_csv(os.path.join(in_dir1, "TCM_all_data.csv"))


# %%
# 4. Plot
in_dir1 = 'C:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/GIS/Confronto/Buffers/Selezione_punti/TCM/' 
monit_df = pd.read_csv(os.path.join(in_dir1, "TCM_all_data.csv")).reset_index(drop=True)
output_folder = os.path.join(in_dir1,"Plots")
os.makedirs(output_folder, exist_ok=True)
monit_df["DATA"] = pd.to_datetime(monit_df["DATA"], format="%Y-%m-%d", errors="coerce")

# %%
# Points to plot
selected_points = ['PO0151460U0405']

# Plot each monitoring point
# Set Seaborn style
sns.set_style("darkgrid")
for point in selected_points:
    df_point = monit_df[monit_df['ID_PUNTO'] == point]  # Filter data for the point
    df_point = df_point.sort_values(by="DATA")  # Ensure the dates are sorted

    # Create figure
    plt.figure(figsize=(10, 6))
    
    # Seaborn lineplot with markers
    sns.lineplot(data=df_point, x="DATA", y="VALORE", marker="o", color="royalblue", linewidth=2.5)

    # Formatting the plot
    plt.xlabel("Data", fontsize=12)
    plt.ylabel("Valore TCM", fontsize=12)
    plt.title(f"Concentrazione vs Tempo\n{point}", fontsize=14, fontweight="bold")

    # Rotate x-axis labels and format dates nicely
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))  # Show Year-Month
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))  # Show every 6 months

    # Improve layout
    plt.grid(True, linestyle="--", alpha=0.6)  # Dotted grid
    plt.tight_layout()

    # Save the plot as a PNG file
    # filename = os.path.join(output_folder, f"{point}.png")
    # plt.savefig(filename, dpi=300, bbox_inches="tight")  # Save with high resolution
    # plt.close()  # Close the figure to free memory
    plt.show()

print(f"Plots saved in '{output_folder}' folder.")
# %%
