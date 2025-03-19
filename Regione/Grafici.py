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
#df = main_df.drop_duplicates(subset=["COD_SITO", "Matrice"])
df = main_df.drop_duplicates(subset=["COD_SITO", "Matrice", "tipo_sostanza"])

# %%
# Count occurrences
#df_counts = df.groupby(['ANA_classific_attuale', 'Matrice']).size().reset_index(name='Count')
df_counts = df.groupby(['ANA_classific_attuale', 'Matrice', "tipo_sostanza"]).size().reset_index(name='Count')

# %%
# Create bar plot
fig = px.bar(df_counts, 
             x='ANA_classific_attuale', 
             y='Count', 
             color='Matrice',
             #facet_col="Matrice", 
             barmode="group")

fig.update_layout(
    xaxis_title="Stato Attuale",
    yaxis_title="Numero di siti",
    xaxis_title_font=dict(size=14, family='Arial', weight='bold'),
    yaxis_title_font=dict(size=14, family='Arial', weight='bold')
)
# Show figure
fig.show()

export_path = os.path.join(in_dir, 'siti_matrici.png')
fig.write_image(export_path)  # Save the image as PNG
# %%
