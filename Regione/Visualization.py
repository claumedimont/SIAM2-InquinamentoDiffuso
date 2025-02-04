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

# Load the Excel files
in_dir = 'C:/Users/HP/OneDrive - Politecnico di Milano/PhD_Claudia/Period_Regione/Elaborazioni/' 
sel_df = pd.read_excel(os.path.join(in_dir, 'SIAM2_SelezioneAGISCO.xlsx'), sheet_name="Tutti")

# %%
# Identify sites with last EDMA before 2022
sel_df['EDMA'] = sel_df['anno_ultimo_edma'].apply(
    lambda x: 'NoEDMA' if pd.isna(x) else ('Sospeso' if x < 2022 else 'EDMA>2022'))
sel_df['ANA_classific_attuale'] = sel_df['ANA_classific_attuale'].str.lower()

# Aggregate data: Count sites per comune, state, and split by EDMA
class_df = sel_df.groupby(['Provincia','Comune', 'ANA_classific_attuale', 'EDMA']).size().reset_index(name='count')
class_df.to_excel(os.path.join(in_dir,"class_stato.xlsx"))

# %%
# # Pivot the DataFrame to prepare for stacking
# df_pivot = class_df.pivot_table(index=['Provincia', 'Comune'], 
#                                   columns='ANA_classific_attuale', 
#                                   values='count', 
#                                   fill_value=0).reset_index()

# CHANGE THIS FOR PLOTLY NESTED DONUT PLOTS!

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
    state_counts = df_muni.groupby("ANA_classific_attuale")["count"].sum()
    edma_counts = df_muni.groupby("EDMA")["count"].sum()

    fig, ax = plt.subplots(figsize=(6, 6))

    # Inner pie (site states)
    wedges1, texts1, autotexts1 = ax.pie(
        state_counts, labels=state_counts.index, autopct='%1.1f%%',
        colors=[state_colors[s] for s in state_counts.index],
        wedgeprops=dict(width=0.4, edgecolor='w'), startangle=140
    )

    # Outer pie (EDMA classification)
    wedges2, texts2, autotexts2 = ax.pie(
        edma_counts, labels=edma_counts.index, autopct='%1.1f%%',
        colors=[edma_colors[e] for e in edma_counts.index],
        radius=0.7, wedgeprops=dict(width=0.3, edgecolor='w'), startangle=140
    )

    # Adjust text size
    plt.setp(autotexts1, size=10, weight="bold")
    plt.setp(autotexts2, size=8, weight="bold")

    ax.set_title(f"{municipality}", fontsize=14)
    plt.tight_layout()

    # Save each figure separately
    plt.savefig(os.path.join(in_dir, f"/output/nested_pie_{municipality}.png"), dpi=300)

# %%
