'''
CODE FOR AGISCO DATA VISUALIZATION

INPUT FILES:
* SIAM2_SelezioneAGISCO

OUTPUT PLOTS:

'''
# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import plotly.graph_objects as go

# Load the Excel files
in_dir = 'C:/Users/user/OneDrive - Politecnico di Milano/PhD_Claudia/Period_Regione/Elaborazioni/' 
sel_df = pd.read_excel(os.path.join(in_dir, 'SIAM2_SelezioneAGISCO.xlsx'), sheet_name="Tutti")

# %%
# Identify sites with last EDMA before 2022
sel_df['EDMA'] = sel_df['anno_ultimo_edma'].apply(
    lambda x: 'NoEDMA' if pd.isna(x) else ('Sospeso' if x < 2022 else 'EDMA>2022'))
sel_df['ANA_classific_attuale'] = sel_df['ANA_classific_attuale'].str.lower()

# Aggregate data: Count sites per comune, state, and split by EDMA
class_df = sel_df.groupby(['Provincia','Comune', 'ANA_classific_attuale', 'EDMA']).size().reset_index(name='count')
#class_df.to_excel(os.path.join(in_dir,"class_stato.xlsx"))

# %%
# # Pivot the DataFrame to prepare for stacking
# df_pivot = class_df.pivot_table(index=['Provincia', 'Comune'], 
#                                   columns='ANA_classific_attuale', 
#                                   values='count', 
#                                   fill_value=0).reset_index()

# CHANGE THIS FOR PLOTLY NESTED DONUT PLOTS!
save_dir = os.path.join(in_dir,"output")

# Define colors for each state
state_colors = {
    "contaminato": "#e41a1c",  # Red
    "non contaminato a seguito di adr": "#377eb8",  # Blue
    "bonificato": "#4daf4a",  # Green
    "potenzialmente contaminato": "#ff7f00"  # Orange
}

edma_colors = {
    "EDMA>2022": "#a6cee3",  # Light Blue
    "Sospeso": "#fb9a99",  # Light Red
    "NoEDMA": "#b2df8a"  # Light Green
}

# Loop through each municipality and generate a separate plot
for municipality in class_df['Comune'].unique():
    df_muni = class_df[class_df['Comune'] == municipality]

    # Aggregate data
    state_counts = df_muni.groupby("ANA_classific_attuale")["count"].sum().reset_index()
    edma_counts = df_muni.groupby(["ANA_classific_attuale", "EDMA"])["count"].sum().reset_index()

    # Define labels and values for both rings
    labels_inner = state_counts["ANA_classific_attuale"]
    values_inner = state_counts["count"]
    colors_inner = [state_colors[s] for s in labels_inner]

    labels_outer = edma_counts["EDMA"] + " (" + edma_counts["ANA_classific_attuale"] + ")"
    values_outer = edma_counts["count"]
    colors_outer = [edma_colors[e] for e in edma_counts["EDMA"]]

    # Create a nested donut pie chart
    fig = go.Figure()

    # Inner ring (State Categories)
    fig.add_trace(go.Pie(
        labels=labels_inner, 
        values=values_inner, 
        hole=0.4,
        marker=dict(colors=colors_inner),
        textinfo='label+value',
        textposition='inside',
        name="ANA_classific_attuale"
    ))

    # Outer ring (EDMA Classification)
    fig.add_trace(go.Pie(
        labels=labels_outer, 
        values=values_outer, 
        hole=0.7,
        marker=dict(colors=colors_outer),
        textinfo='label+value',
        textposition='outside',
        name="EDMA"
    ))

    # Layout settings
    fig.update_layout(
        title_text=f"Comune: {municipality}",
        annotations=[dict(text=municipality, x=0.5, y=0.5, font_size=20, showarrow=False)],
        showlegend=True
    )

    # Save each figure as a PNG
    fig.write_image(f"{save_dir}/pie_{municipality}.png", engine="kaleido", width=800, height=600)

    # Show the figure
    fig.show()

# %%
