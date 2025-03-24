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
def monitoring(inq, inq2, siam_df, mind_df, points_df):
    points_df["ID_PUNTO"] = points_df["ID_PUNTO"].astype(str).str.strip().str.upper()
    # SIAM data
    siam_df["ID_PUNTO"] = siam_df["ID_PUNTO"].astype(str).str.strip().str.upper()
    siam_filtered = siam_df[siam_df['ID_PUNTO'].isin(points_df['ID_PUNTO'])]
    siam_filtered = siam_filtered.drop(['COMUNE', 'PUNTO_PRELIEVO', 'Descrizione Punto',
       'Tipo di campione', 'Tipologia di analisi', 'Nota Prelievo','Nota Prelevatore', 'VALORE_ORIGINE',
       'UM', 'FONTE'],axis=1)
    siam_inq = siam_filtered[siam_filtered['PARAMETRO'] == f'{inq2}']
    siam_inq = siam_inq.drop(["PARAMETRO"], axis=1)
    siam_inq = siam_inq.rename(columns={'VALORE_MODIFICATO': 'VALORE'}).reset_index(drop=True)

    # MIND data
    mind_df["CODICE_PP"] = mind_df["CODICE_PP"].astype(str).str.strip().str.upper()
    mind_df["codice_sif"] = mind_df["codice_sif"].astype(str).str.strip().str.upper()
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
    monit_df = pd.concat([siam_inq, mind_filtered], ignore_index=True).sort_values(["ID_PUNTO", "DATA"]).reset_index(drop=True)

    return monit_df


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
PCE, TCE, TCM
'''

# Get a monitoring dataset per each point for which a mediana has been calculated
inq = 'TCE'
inq2 = "TCE"
points_df = pd.read_csv(os.path.join(cwd1, f"PerConfronto/ArcGIS_input/DEF/ULT_{inq}_mediane_2019-2023.csv"))  #points
mind_df = pd.read_excel(os.path.join(cwd2,'PCE_TCE_E_query dati_MIND_2018.xlsx'), sheet_name=f"{inq}")

monit_df = monitoring(inq, inq2, siam_df, mind_df, points_df)
monit_df.to_csv(os.path.join(cwd1, f"PerConfronto/ArcGIS_input/DEF/{inq}_dati_monitoraggio.csv")) #USE THIS TO UPDATE N MISURE

# update ult files!

# %%
asymptote_values = asymptotes[f"{inq}"].to_list()
output_folder = os.path.join(cwd1, f"PerConfronto/ArcGIS_input/PLOTS/{inq}") # output folder

# %%
#Define lower significant concentration
lowest = 30
selected_points = points_df[points_df[f"{inq2}_2019_2023"] >= lowest]["ID_PUNTO"].tolist() # Points to plot
print (len(selected_points))

# %%

# Plot each monitoring point
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
