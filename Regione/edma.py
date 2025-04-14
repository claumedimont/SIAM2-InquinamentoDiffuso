# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from itertools import product

# Load the Excel files
in_dir = 'C:/Users/user/OneDrive - Politecnico di Milano/04_REGIONE/SIAM2-AggiornamentoSitiMisure/Elaborazioni/DaCondividire/' 
df = pd.read_excel((os.path.join(in_dir,"SIAM2_ClassifEDMA.xlsx")),sheet_name="Complessivo")

# %%
# Agregamos combinaciones faltantes (ejemplo, Non Sospeso o Potenzialmente Contaminato)
comuni = df['Comune'].unique()
classificazioni = ['Contaminato', 'Potenzialmente contaminato']
edma_stati = ['Sospeso', 'Non sospeso']
full_index = pd.DataFrame(product(comuni, classificazioni, edma_stati),
                          columns=['Comune','Classificazione Attuale', 'EDMA'])

# Unir con los datos reales y rellenar los NaNs con 0
df_full = pd.merge(full_index, df, how='left',
                   on=['Comune','Classificazione Attuale', 'EDMA']).fillna(0)

# Pivot para gráfico apilado
pivot = df_full.pivot_table(index=['Comune', 'Classificazione Attuale'],
                               columns='EDMA', values='count').fillna(0)

# %%
# Prepare plot
comuni_order = sorted(comuni)
x = np.arange(len(comuni_order))  # the label locations
width = 0.35  # width of the bars

# Split by classification
contaminato = pivot.xs('Contaminato', level=1)
potenzialmente = pivot.xs('Potenzialmente contaminato', level=1)

# Define colors
colors = {
    'Contaminato': {'Sospeso': '#8B0000', 'Non sospeso': '#FF7F7F'},  # dark red, light red
    'Potenzialmente contaminato': {'Sospeso': '#FF8C00', 'Non sospeso': '#FFD580'}  # dark orange, light orange
}

# %%
fig, ax = plt.subplots(figsize=(14, 6))

# Bar plots for each classification
ax.bar(x - width/2, contaminato['Non sospeso'], width=width,
       label='Contaminato - Non sospeso', color=colors['Contaminato']['Non sospeso'])
ax.bar(x - width/2, contaminato['Sospeso'], width=width,
       bottom=contaminato['Non sospeso'], label='Contaminato - Sospeso', color=colors['Contaminato']['Sospeso'])

ax.bar(x + width/2, potenzialmente['Non sospeso'], width=width,
       label='Potenzialmente contaminato - Non sospeso', color=colors['Potenzialmente contaminato']['Non sospeso'])
ax.bar(x + width/2, potenzialmente['Sospeso'], width=width,
       bottom=potenzialmente['Non sospeso'], label='Potenzialmente contaminato - Sospeso', color=colors['Potenzialmente contaminato']['Sospeso'])

# Aesthetics
ax.set_xticks(x)
ax.set_xticklabels(comuni_order, rotation=45, ha='right')
ax.set_xlabel('Comune', fontsize=12, weight='bold')
ax.set_ylabel('Numero di siti',fontsize=12, weight='bold')
ax.set_title('Stato EDMA per Comune',fontsize=16, weight='bold')
ax.legend(title='Classificazione / EDMA', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

export_path = os.path.join(in_dir, 'EDMA.png')
plt.savefig(export_path, dpi=300, bbox_inches='tight')

plt.show()


# %%
