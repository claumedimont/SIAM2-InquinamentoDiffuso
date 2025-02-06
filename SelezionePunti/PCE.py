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

# Load the Excel files
# Buffer files
in_dir1 = 'C:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/GIS/Confronto/Buffers/Selezione_punti/PCE/' 
NE_L1_df = pd.read_csv(os.path.join(in_dir1,'PCE_NE_L1.csv'))
NE_L5_df = pd.read_csv(os.path.join(in_dir1,'PCE_NE_L5.csv'))
W_L1_df = pd.read_csv(os.path.join(in_dir1,'PCE_W_L1.csv'))
W_L5_df = pd.read_csv(os.path.join(in_dir1,'PCE_W_L5.csv'))
sorg_df = pd.read_csv(os.path.join(in_dir1,'PCE_sorgenti.csv'))

# Monitoring data files
in_dir2 = 'C:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/Elaborazioni/E_AnalisiChimiche/' 
in_dir3 = 'C:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/Dati origine/Analisi chimiche/' 
siam_df = pd.read_excel(os.path.join(in_dir2,'idrochimica_tutti_step6_SL_31102024.xlsx'), sheet_name="idrochimica_tutt_step6")
mind_df = pd.read_excel(os.path.join(in_dir3,'PCE_TCE_E_query dati_MIND_2018.xlsx'), sheet_name="PCE")

# %%
# 1. All buffer files into a single df
points_df = pd.concat([NE_L1_df, NE_L5_df, W_L1_df, W_L5_df], ignore_index=True)
points_df = points_df.drop(['ANNO', 'MEDIANA_AN'], axis=1)
points_df = points_df.drop_duplicates().reset_index(drop=True)

# %%
# 2. Get the data ONLY for the points inside points_df from the monitoring data files
# SIAM data
siam_filtered = siam_df[siam_df['ID_PUNTO'].isin(points_df['ID_PUNTO'])]
siam_filtered = siam_filtered.drop(['COMUNE', 'PUNTO_PRELIEVO', 'Descrizione Punto',
       'Tipo di campione', 'Tipologia di analisi', 'Nota Prelievo','Nota Prelevatore', 'VALORE_ORIGINE',
       'UM', 'FONTE'],axis=1)
siam_pce = siam_filtered[siam_filtered['PARAMETRO'] == 'PCE']
siam_pce = siam_pce.drop(["PARAMETRO"], axis=1)
siam_pce = siam_pce.rename(columns={'VALORE_MODIFICATO': 'VALORE'}).reset_index(drop=True)

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
monit_df = pd.concat([siam_pce, mind_filtered], ignore_index=True).sort_values(["ID_PUNTO", "DATA"]).reset_index(drop=True)

#also consider points with less than 10 measures for the areas of interes
# Count the number of measurements per monitoring point & remove points with fewer than 10 measurements
counts = monit_df.groupby("ID_PUNTO")["VALORE"].count().reset_index()
counts.rename(columns={"VALORE": "MISURE"}, inplace=True)
#counts = counts[counts["MISURE"] >= 10]

# Merge with points_df
points_df = points_df.merge(counts, on="ID_PUNTO", how="inner")

# Replace counts with labels
def categorize_count(value):
    if value > 30:
        return ">30"
    elif value > 20:
        return ">20"
    else:
        return ">10"

points_df["MISURE"] = points_df["MISURE"].apply(categorize_count)

# save files
points_df.to_csv(os.path.join(in_dir1, "PCE_daEscludere.csv"))
#monit_df.to_csv(os.path.join(in_dir1, "PCE_all_data.csv"))

#something wrong to get all points da escludere

# %%
# 4. Plot
output_folder = os.path.join(in_dir2,"PerConfronto/PLOTS/PCE")

# Get the points with more than 30 measurements
selected_points = ['0151160006GRZ']

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
    plt.ylabel("Valore PCE", fontsize=12)
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
    #filename = os.path.join(output_folder, f"{point}.png")
    #plt.savefig(filename, dpi=300, bbox_inches="tight")  # Save with high resolution
    #plt.close()  # Close the figure to free memory
    plt.show()

print(f"Plots saved in '{output_folder}' folder.")
# %%
