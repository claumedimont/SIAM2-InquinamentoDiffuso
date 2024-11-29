'''
Code to extract data for a selection of targets within a MT3D-USGS model
All targets have already been imported into the model as ANALYTIC ELEMENTS.

Target file should include columns:
ID, row, col, layer, time (n days from start of simulation), obs_values
'''
# %%
import flopy
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from datetime import datetime, timedelta

# Define the paths to your model files
in_dir = "e:/SIAM2-InquinamentoDiffuso/Input_flopy/"
model_ws = os.path.join(in_dir, "Cr6/")
ucn_file = f"{model_ws}/tmr_ce_crvi_ext1.UCN"
obs_file = os.path.join(model_ws, "targets/per_confronto.csv")
modello_nam = "tmr_ce_crvi_ext.nam"
inquinante = "Cr6"

# %%
# Load the MT3D model and UCN file
mt_model = flopy.mt3d.Mt3dms.load(modello_nam, model_ws=model_ws, verbose=True)
ucn_obj = flopy.utils.UcnFile(ucn_file)

# %%
# Extract simulated concentration data from the UCN file
times = ucn_obj.get_times()  # Get all time steps from the UCN file

# Define the simulation start date
start_date = datetime.strptime("2014-01-01", "%Y-%m-%d")
# Convert simulation times to actual dates
dates = [start_date + timedelta(days=int(t)) for t in times]

# Load the observed data from the CSV file
obs_df = pd.read_csv(obs_file)

# %%
# Iterate through the unique target IDs in the observed data
for target_id in obs_df['id'].unique():
    # Get the observed data for this target
    target_data = obs_df[obs_df['id'] == target_id]

    # Extract the target location (row, col, layer)
    row = int(target_data.iloc[0]['row'])
    col = int(target_data.iloc[0]['col'])
    lay = int(target_data.iloc[0]['layer'])

    # Extract the observed concentrations for this target
    observed_concs = target_data['observed_conc'].values  # Assumes column is named 'observed_conc'
    observed_dates = [start_date + timedelta(days=int(t)) for t in target_data['time'].values]

    # Extract the simulated concentrations for this target location over all time steps
    simulated_concs = []
    for time in times:
        sim_conc = ucn_obj.get_data(totim=time)[lay, row, col]
        simulated_concs.append(sim_conc)

    # Create a plot for this target showing observed vs simulated concentrations over time
    plt.figure(figsize=(10, 6))
    plt.plot(observed_dates, observed_concs, 'bo-', label="Dati osservati")
    plt.plot(dates, simulated_concs, 'r^-', label="Dati simulati")
    plt.xlabel("Anno") 
    plt.ylabel("Concentrazione (ug/L)")
    plt.title(f"Confronto {inquinante} - Target {target_id}")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save or show the plot
    plt.savefig(os.path.join(in_dir, inquinante, "confronto", f"target_{target_id}.png"))  # Save plot as image
   
# %%
