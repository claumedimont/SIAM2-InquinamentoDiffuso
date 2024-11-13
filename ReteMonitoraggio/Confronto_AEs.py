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

# Define the paths to your model files
in_dir = "e:/SIAM2-InquinamentoDiffuso/Input_flopy/"
model_ws = os.path.join(in_dir, "PCE/")
ucn_file = f"{model_ws}/pce_tmr_ne1_barri.UCN"
obs_file = os.path.join(in_dir, "PCE/targets/per_confronto.csv")

# %%
# Load the MT3D model and UCN file
mt_model = flopy.mt3d.Mt3dms.load("pce_tmr_ne.nam", model_ws=model_ws, verbose=True)
ucn_obj = flopy.utils.UcnFile(ucn_file)

# %%
# Extract simulated concentration data from the UCN file
times = ucn_obj.get_times()  # Get all time steps from the UCN file

# Load the observed data from the CSV file
obs_df = pd.read_csv(obs_file)

# %%
# Initialize lists for storing results
observed = []
simulated = []
target_ids = []

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

    # Extract the simulated concentrations for this target location over all time steps
    simulated_concs = []
    for time in times:
        sim_conc = ucn_obj.get_data(totim=time)[lay, row, col]
        simulated_concs.append(sim_conc)

    # Create a plot for this target showing observed vs simulated concentrations over time
    plt.figure(figsize=(10, 6))
    plt.plot(target_data['time'], observed_concs, 'bo-', label="Observed Concentration")
    plt.plot(times, simulated_concs, 'r^-', label="Simulated Concentration")
    plt.xlabel("Time (years)")  # Adjust the x-axis label if necessary
    plt.ylabel("Concentration (ug/L)")
    plt.title(f"Observed vs Simulated PCE Concentrations for Target {target_id}")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)  # Rotate x-axis labels if needed
    plt.tight_layout()

    # Save or show the plot
    plt.savefig(os.path.join(in_dir, "PCE", "confronto", f"target_{target_id}.png"))  # Save plot as image
   
#     # Store the observed and simulated concentrations
#     observed.append(observed_concs)
#     simulated.append(sim_conc)
#     target_ids.append(target_id)

# # Create a DataFrame for easy plotting and analysis
# df_results = pd.DataFrame({
#     "Target_ID": target_ids,
#     "Observed_Conc": observed,
#     "Simulated_Conc": simulated
# })
