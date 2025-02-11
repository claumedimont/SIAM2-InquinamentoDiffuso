'''
CODE FOR AGISCO DATA VISUALIZATION

INPUT FILES:
* SIAM2_SelezioneAGISCO

OUTPUT PLOTS:

'''
# %%
import pandas as pd
import os
import plotly.graph_objects as go

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
#class_df.to_excel(os.path.join(in_dir,"class_stato.xlsx"))

# %%

# PLOTLY NESTED DONUT PLOTS!
# Output directory
save_dir = os.path.join(in_dir,"new_output")
os.makedirs(save_dir, exist_ok=True)

# Define colors for each category and subcategory
color_map = {
    "bonificato": "#2ca02c",  # Main Green
    "NoEDMA (bonificato)": "#006400",  # Very Dark Green
    "Sospeso (bonificato)": "#228B22",  # Dark Green
    "EDMA>2022 (bonificato)": "#90EE90",  # Light Green

    "potenzialmente contaminato": "#ff8c00",  # Main Orange
    "NoEDMA (potenzialmente contaminato)": "#8B4000",  # Very Dark Orange
    "Sospeso (potenzialmente contaminato)": "#D2691E",  # Dark Orange
    "EDMA>2022 (potenzialmente contaminato)": "#FFA07A",  # Light Orange

    "contaminato": "#e41a1c",  # Main Red
    "NoEDMA (contaminato)": "#8B0000",  # Very Dark Red
    "Sospeso (contaminato)": "#B22222",  # Dark Red
    "EDMA>2022 (contaminato)": "#FA8072",  # Light Red

    "non contaminato a seguito di adr": "#377eb8",  # Main Blue
    "NoEDMA (non contaminato a seguito di adr)": "#08306b",  # Very Dark Blue
    "Sospeso (non contaminato a seguito di adr)": "#08519c",  # Dark Blue
    "EDMA>2022 (non contaminato a seguito di adr)": "#6baed6"  # Light Blue
}

# Loop through each municipality and generate a separate plot
for municipality in class_df['Comune'].unique():
    df_muni = class_df[class_df['Comune'] == municipality]

    # Aggregate data
    state_counts = df_muni.groupby("ANA_classific_attuale")["count"].sum().reset_index()
    edma_counts = df_muni.groupby(["ANA_classific_attuale", "EDMA"])["count"].sum().reset_index()

    # Compute correct proportions so outer ring segments align with inner ring
    outer_segments = []
    for index, row in state_counts.iterrows():
        main_category = row["ANA_classific_attuale"]
        total_main_category = row["count"]

        # Filter for corresponding EDMA subcategories
        subcategories = edma_counts[edma_counts["ANA_classific_attuale"] == main_category]

        # Compute proportions relative to main category
        for _, sub_row in subcategories.iterrows():
            subcategory_label = sub_row["EDMA"] + f" ({main_category})"
            proportion = sub_row["count"] / total_main_category * row["count"]
            outer_segments.append((subcategory_label, proportion))

    # # Labels and values for inner ring
    labels_inner = state_counts["ANA_classific_attuale"]
    values_inner = state_counts["count"]
    colors_inner = [color_map[label] for label in labels_inner]

    # Labels and values for properly aligned outer ring
    labels_outer, values_outer = zip(*outer_segments)
    colors_outer = [color_map[label] for label in labels_outer]

    # Remove subcategory names from outer ring labels
    labels_outer_clean = [label.split(" (")[0] for label in labels_outer]

    # Create a nested donut pie chart
    fig = go.Figure()

    # Inner ring (Main Categories)
    fig.add_trace(go.Pie(
        labels=labels_inner, 
        values=values_inner, 
        hole=0.4,
        marker=dict(colors=colors_inner),
        textinfo='label+value',
        textposition='inside',
        name="Categoria Principale"
    ))

    # Outer ring (EDMA Classification)
    fig.add_trace(go.Pie(
        labels=labels_outer_clean, 
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
# OPTION 2
# Define color scheme
state_colors = {
    "bonificato": "#2ca02c",  
    "potenzialmente contaminato": "#ff8c00",
    "contaminato": "#e41a1c",
    "non contaminato a seguito di adr": "#377eb8"
}

sub_colors = {
    "bonificato_NoEDMA": "#006400",  
    "bonificato_Sospeso": "#228B22",  
    "bonificato_EDMA>2022": "#90EE90",

    "potenzialmente contaminato_NoEDMA": "#8B4500",
    "potenzialmente contaminato_Sospeso": "#FF8C00",
    "potenzialmente contaminato_EDMA>2022": "#FFD700",

    "contaminato_NoEDMA": "#8B0000",
    "contaminato_Sospeso": "#FF6347",
    "contaminato_EDMA>2022": "#FFB6C1",

    "non contaminato a seguito di adr_NoEDMA": "#00008B",
    "non contaminato a seguito di adr_Sospeso": "#4169E1",
    "non contaminato a seguito di adr_EDMA>2022": "#87CEFA"
}

# Output directory
save_dir = os.path.join(in_dir, "output2")
os.makedirs(save_dir, exist_ok=True)

# Loop through each municipality
for municipality in class_df['Comune'].unique():
    df_muni = class_df[class_df['Comune'] == municipality]

    # Aggregate main categories
    state_counts = df_muni.groupby("ANA_classific_attuale")["count"].sum().reset_index()
    
    # Compute correctly nested outer ring proportions
    outer_segments = []
    for index, row in state_counts.iterrows():
        main_category = row["ANA_classific_attuale"]
        total_main_category = row["count"]

        # Get subcategories only within this main category
        subcategories = df_muni[df_muni["ANA_classific_attuale"] == main_category]

        for _, sub_row in subcategories.iterrows():
            subcategory_label = f"{main_category} ({sub_row['EDMA']})"
            proportion = sub_row["count"] / total_main_category * row["count"]
            color_key = f"{main_category}_{sub_row['EDMA']}"  # Ensure correct shading
            outer_segments.append((subcategory_label, proportion, sub_colors[color_key]))

    # Inner ring (Main categories)
    labels_inner = state_counts["ANA_classific_attuale"]
    values_inner = state_counts["count"]
    colors_inner = [state_colors[label] for label in labels_inner]

    # Outer ring (Properly nested subcategories)
    labels_outer, values_outer, colors_outer = zip(*outer_segments)

    # Clean labels for display
    labels_outer_clean = [label.split(" (")[1].strip(")") for label in labels_outer]

    # Create figure
    fig = go.Figure()

    # Inner ring
    fig.add_trace(go.Pie(
        labels=labels_inner,
        values=values_inner,
        hole=0.4,
        marker=dict(colors=colors_inner),
        textinfo='label+value',
        textposition='inside',
        name="Categoria Principale"
    ))

    # Outer ring
    fig.add_trace(go.Pie(
        labels=labels_outer_clean,  
        values=values_outer,
        hole=0.7,
        marker=dict(colors=colors_outer),
        textinfo='label+value',
        textposition='outside',
        name="Sottocategoria"
    ))

    # Update layout
    fig.update_layout(
        title_text=f"Comune: {municipality}",
        annotations=[dict(text=municipality, x=0.5, y=0.5, font_size=20, showarrow=False)],
        showlegend=True
    )

    # Save figure
    fig.write_image(os.path.join(save_dir, f"pie_{municipality}.png"), engine="kaleido", width=800, height=600)

    # Show plot
    fig.show()
# %%
