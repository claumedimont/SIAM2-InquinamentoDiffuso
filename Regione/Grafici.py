'''
GRAFICI

'''
# %%
# Load necessary packages and files
import pandas as pd
import os
import plotly.express as px

# Load the Excel files
in_dir = 'C:/Users/user/OneDrive - Politecnico di Milano/04_REGIONE/SIAM2-AggiornamentoSitiMisure/Elaborazioni/' 
main_df = pd.read_excel((os.path.join(in_dir,"SIAM2_PerGrafici.xlsx")))

# %%
# Clean df
#df = main_df.drop_duplicates(subset=['DGR_SITO',"COD_SITO", "ANA_classific_attuale"])
df = main_df.drop_duplicates(subset=["COD_SITO", 'ANA_classific_attuale',"MISE_descrizione"])

# %%
# Count occurrences
df_filtered = df[df["DGR_SITO"] == "Procedimento"]
#df_counts = df_filtered.groupby(['ANA_classific_attuale', 'descClassSuoli']).size().reset_index(name='Count')
df_counts = df_filtered.groupby(['ANA_classific_attuale', 'MISE_descrizione']).size().reset_index(name='Count')
colors_sostanze = {"Altro": "#003f5c",
          "Pesticidi": "#58508d",
          "SIAM2" : "#bc5090",
          "SolventiClorurati":"#ff6361",
          "DiossineFurani" : "#ffa600"
          }
colors_tecno = {"rimozione e smaltimento terreno": "#003f5c",
          "pump and treat": "#ffa600",
          "soil vapour extraction (SVE)" : "#2f4b7c",
          "biorisanamento":"#665191",
          "soil venting (SV)" : "#a05195",
          "air sparging": "#d45087",
          "bioventing (BV)" : "#f95d6a",
          "soil flushing": "#fe9395",
          "barriere reattive":"#ff7c43",
          "altro": "#df676e",
          "nan":"#f1f1f1"
          }
colors_MISE = {"rimozione o svuotamento di bidoni, container": "#003f5c",
          "messa in opera di barriere idrauliche": "#ffa600",
          "rimozione dei rifiuti" : "#2f4b7c",
          "rimozione serbatoi":"#665191",
          "raccolta liquidi sversati" : "#a05195",
          "copertura impermeabile temporanea": "#d45087",
          "altro": "#df676e",
          "nan":"#f1f1f1"
          }
colors_MISP = {"confinamento verticale": "#003f5c",
          "barriere idrauliche": "#ffa600",
          "confinamento orizzontale superficiale" : "#2f4b7c",
          "NO":"#f1f1f1"
          }
# %%
# Create bar plot
fig = px.bar(df_counts, 
             x = 'ANA_classific_attuale', 
             y = 'Count', 
             color = 'MISE_descrizione',
             #facet_col="Matrice", 
             barmode = "group",
             #text_auto = True,
             color_discrete_map = colors_MISE)

# Add text labels manually and position them on top of the bars
#fig.update_traces(texttemplate='%{y}', textposition='inside',
#                  textangle = 0, textfont_size =10,
#                  textfont_color = 'white')

fig.update_layout(
    xaxis_title="Stato Attuale",
    yaxis_title="Numero di siti",
    xaxis_title_font=dict(size=14, family='Arial', weight='bold'),
    yaxis_title_font=dict(size=14, family='Arial', weight='bold'),
    title_font = dict(size=16, family='Arial', weight='bold')
)
fig.update_layout(
    yaxis=dict(
        tickmode='linear',  # Ensures evenly spaced ticks
        dtick=1,            # Forces ticks to be spaced by 1 (integers only)
        tickformat="d"      # Ensures numbers are displayed as whole numbers
    )
)
# fig.update_layout(
#     title=dict(
#         text="MISE siti procedimenti",
#         x=0.5,       # Center the title
#         y=0.95,      # Move title closer to the plot
#         xanchor="center",
#         yanchor="top",
#         font=dict(
#             family="Arial",  # Use a bold font
#             size=18,  # Adjust font size
#             color="black"
#     )
# ))
# Show figure
fig.show()

export_path = os.path.join(in_dir, 'Immagini/MISE_procedi.png')
fig.write_image(export_path, scale=3)  # Save the image as PNG
# %%
