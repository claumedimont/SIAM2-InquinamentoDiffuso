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


# Working directory
in_dir = 'C:/Users/user/OneDrive - Politecnico di Milano/04_REGIONE/SIAM2-AggiornamentoSitiMisure/Elaborazioni/' 

# %%
# Get file SIAM2_ClassifEDMA (done)
sel_df = pd.read_excel(os.path.join(in_dir, 'SIAM2_SelezioneAGISCO.xlsx'), sheet_name="Tutti")
# Identify sites with last EDMA before 2022
sel_df['EDMA'] = sel_df['anno_ultimo_edma'].apply(
    lambda x: 'NoEDMA' if pd.isna(x) else ('Sospeso' if x < 2022 else 'NonSospeso'))
sel_df['ANA_classific_attuale'] = sel_df['ANA_classific_attuale'].str.lower()
# Aggregate data: Count sites per comune, state, and split by EDMA
class_df = sel_df.groupby(['Provincia','Comune', 'ANA_classific_attuale', 'EDMA']).size().reset_index(name='count')
#class_df.to_excel(os.path.join(in_dir,"SIAM2_ClassifEDMA.xlsx"))

# %%
# PLOTLY NESTED DONUT PLOTS!
# Load file
class_df = pd.read_excel(os.path.join(in_dir, "SIAM2_ClassifEDMA.xlsx"), sheet_name="Selezione")

# Output directory
save_dir = os.path.join(in_dir,"new_output")
os.makedirs(save_dir, exist_ok=True)


# %%
import plotly.express as px
# %%
# Get unique Comuni
comuni = class_df["Comune"].unique()

for comune in comuni:
    df_comune = class_df[class_df["Comune"] == comune]
    # Define custom colors
    color_map = {
        "P.C.": "#facb65",
        "C.": "#fa8065"
    }

    # Replace long labels with short ones
    df_comune = df_comune.replace({
        "ANA_classific_attuale": {
            "potenzialmente contaminato": "P.C.",
            "contaminato": "C."
        }
    })

    # Create the figure
    fig = px.sunburst(df_comune, 
        path=["ANA_classific_attuale", "EDMA"], 
        values='count',
        color="ANA_classific_attuale",
        color_discrete_map=color_map
        )
    fig.update_traces(textinfo="label+value", 
    insidetextorientation="horizontal",
    insidetextfont=dict(family="Arial Black", size=14))
    fig.update_layout(title_text=f"Stato EDMA siti contaminati e potenzialmente contaminati (01/2025)<br>{comune}", title_x=0.5, title_font=dict(size=15, family="Arial Black"))
    #fig.show()
   
    # fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    
    # # Save the figure as PNG
    file_path = os.path.join(save_dir, f"{comune}_donut.png")
    fig.write_image(file_path, engine="kaleido")
    print(f"Saved: {file_path}")
          
# %%
