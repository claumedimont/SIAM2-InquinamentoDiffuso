'''
GRAFICI

'''
# %%
# Load necessary packages and files
import pandas as pd
import os
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Load the Excel files
in_dir = 'C:/Users/user/OneDrive - Politecnico di Milano/04_REGIONE/SIAM2-AggiornamentoSitiMisure/Elaborazioni/' 
main_df = pd.read_excel((os.path.join(in_dir,"SIAM2_PerGrafici.xlsx")))

# %%
# Clean df
#df = main_df.drop_duplicates(subset=['DGR_SITO',"COD_SITO", "ANA_classific_attuale", 'MISE_descrizione'])
#df = main_df.drop_duplicates(subset=["COD_SITO", 'ANA_classific_attuale',"Matrice", "tipo_sostanza"])
df = main_df.drop_duplicates(subset=["COD_SITO", 'ANA_classific_attuale',"Matrice", "TecnologieDescrizione"])

# Count occurrences
df_filtered = df[(df["DGR_SITO"] == "Prioritario")|(df["DGR_SITO"] == "Sorgenti")]
#df_filtered = df[df["DGR_SITO"] == "Procedimento"]
#df_counts = df_filtered.groupby(['ANA_classific_attuale', 'MISE_descrizione']).size().reset_index(name='Count')
df_counts = df_filtered.groupby(['ANA_classific_attuale', 'Matrice','TecnologieDescrizione'], dropna=False).size().reset_index(name='Count')

label_map = {
    "bonificato": "B",
    "contaminato": "C",
    "potenzialmente contaminato": "PC",
    "non contaminato": "N",
    "non contaminato a seguito di AdR": "AdR"
}

df_counts["ANA_classific_attuale"] = df_counts["ANA_classific_attuale"].map(label_map)

# %%
'''
PLOT
'''
colors_sostanze = {"Altro": "#005F73",
          "Pesticidi": "#94D2BD",
          "SolventiClorurati+Cromo" : "#0A9396",
          "AltriSolventiClorurati":"#E9D8A6",
          "DiossineFurani" : "#EE9B00",
          "SenzaDati": "#dddddd"
          }

colors_tecno = {"rimozione e smaltimento terreno": "#005F73",
          "pump and treat": "#EE9B00",
          "soil vapour extraction (SVE)" : "#0A9396",
          "biorisanamento":"#AE2012",
          "soil venting (SV)" : "#219ebc",
          "air sparging": "#94D2BD",
          "bioventing (BV)" : "#8ecae6",
          "soil flushing": "#97D89B",
          "barriere reattive":"#CA6702",
          "altro": "#E9D8A6",
          "SenzaDati": "#dddddd"
          }
colors_MISE = {"rimozione o svuotamento di bidoni, container": "#005F73",
          "messa in opera di barriere idrauliche": "#EE9B00",
          "rimozione dei rifiuti" : "#0A9396",
          "rimozione serbatoi":"#AE2012",
          "raccolta liquidi sversati" : "#219ebc",
          "copertura impermeabile temporanea": "#94D2BD",
          "altro": "#E9D8A6",
          }
colors_MISP = {"confinamento verticale": "#005F73",
          "barriere idrauliche": "#0A9396",
          "confinamento orizzontale superficiale" : "#94D2BD",
          "NO":"#E9D8A6"
          }

#ATTENTION
titulo = "Siti prioritari: Tecnologie di bonifica"
image = 'Priori_tenco'
hue = 'TecnologieDescrizione'
leyenda = "Tecnologia di bonifica"
palette = colors_tecno



plot_df = df_counts.copy()

# %%
# Add senza dati to the plots
plot_df['ANA_classific_attuale'] = plot_df['ANA_classific_attuale'].fillna('SenzaDati')
plot_df['Matrice'] = plot_df['Matrice'].fillna('SenzaDati')
plot_df['TecnologieDescrizione'] = plot_df['TecnologieDescrizione'].fillna('SenzaDati')


# %%
# DO THIS TO SPLIT PER MATRICE

# Initialize FacetGrid for 'Matrice'
g = sns.FacetGrid(
    plot_df,
    col="Matrice",
    height=5,
    aspect=1,
    sharey=True
)

# Map the barplot on the FacetGrid
g.map_dataframe(
    sns.barplot,
    x="ANA_classific_attuale",
    y="Count",
    hue=hue,
    palette=palette,
    estimator=sum,
    dodge = True,
    errorbar=None,
    width = 0.8
)
# Set axis labels and titles
g.set_axis_labels("Stato attuale del sito", "Numero di siti", weight='bold')
g.set_titles(col_template="{col_name}")
g.figure.subplots_adjust(top=0.85)
g.figure.suptitle(titulo, fontsize=16, weight='bold')

# Customize legends
g.add_legend(title=leyenda)
g._legend.set_bbox_to_anchor((1.015, 0.6)) 

#add label box
label_det = (
    "B = bonificato\n"
    "C = contaminato\n"
    "PC = potenzialmente contaminato\n"
    "N = non contaminato\n"
    "AdR = non contaminato a seguito di AdR"
)

# Add label map explanation under the legend
g.figure.text(
    0.8,  # x position (tweak depending on layout)
    0.4,   # y position
    label_det,
    ha='left',
    va='top',
    fontsize=9,
    bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.5')
)

# Optional: customize axis
for ax in g.axes.flat:
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

for ax in g.axes.flat:
    for container in ax.containers:
        ax.bar_label(container, fmt='%d', label_type='edge', fontsize=9, color='black')

export_path = os.path.join(in_dir, f'Immagini/Nuove/{image}.png')
plt.savefig(export_path, dpi=300, bbox_inches='tight')
plt.show()

# %%
# DO THIS TO NOT SPLIT BY MATRICE

fig = plt.figure(figsize=(10, 6))
# Create the barplot (no FacetGrid)
sns.barplot(
    data=plot_df,
    x="ANA_classific_attuale",
    y="Count",
    hue=hue,
    palette=palette,
    estimator=sum,
    dodge=True,
    errorbar=None,
    width=0.8
)
# Titles and labels
plt.xlabel("Stato attuale del sito", weight='bold')
plt.ylabel("Numero di siti", weight='bold')
plt.title(titulo, fontsize=16, weight='bold')

# Legend customization
plt.legend(
    title=leyenda,
    bbox_to_anchor=(1.02, 0.8),  # Push legend to the right
    loc='upper left',
    borderaxespad=0,
    frameon=False  # Optional: remove legend border
)
#add label box
label_det = (
    "B = bonificato\n"
    "C = contaminato\n"
    "PC = potenzialmente contaminato\n"
    "N = non contaminato\n"
    "AdR = non contaminato a seguito di AdR"
)

# Add label map explanation under the legend
fig.text(
    0.93,  # x position (tweak depending on layout)
    0.4,   # y position
    label_det,
    ha='left',
    va='top',
    fontsize=9,
    bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.5')
)
# Y axis: only integer ticks
plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

# Add labels on bars
ax = plt.gca()
for container in ax.containers:
    ax.bar_label(container, fmt='%d', label_type='edge', fontsize=9, color='black')

export_path = os.path.join(in_dir, f'Immagini/Nuove/{image}.png')
plt.savefig(export_path, dpi=300, bbox_inches='tight')
plt.show()
# %%
