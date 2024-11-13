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

    # Loop through each time step in the observed data
    for _, record in target_data.iterrows():
        time = record['time']
        obs_conc = record['observed_conc']

        # Find the closest matching time step in the UCN file
        closest_time = min(times, key=lambda x: abs(x - time))

        # Get the simulated concentration at the specified location and time step
        sim_conc = ucn_obj.get_data(totim=closest_time)[lay, row, col]

        # Store the observed and simulated concentrations
        observed.append(obs_conc)
        simulated.append(sim_conc)
        target_ids.append(target_id)

# Create a DataFrame for easy plotting and analysis
df_results = pd.DataFrame({
    "Target_ID": target_ids,
    "Observed_Conc": observed,
    "Simulated_Conc": simulated
})

# %%
plt.figure(figsize=(10, 6))
plt.scatter(observed, simulated, color='blue', edgecolor='k', alpha=0.7)
plt.plot([min(observed), max(observed)], [min(observed), max(observed)], 'r--', label='1:1 Line')
plt.xlabel("Observed Concentration (ug/L)")
plt.ylabel("Simulated Concentration (ug/L)")
plt.title("Observed vs Simulated PCE Concentrations")
plt.legend()
plt.grid()
plt.show()

# %%
#Save results dataframe?
df_results.to_excel(os.path.join(in_dir, "results.xlsx"))
# %%
