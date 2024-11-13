'''
Code to extract data for a selection of targets within a MT3D-USGS model
All targets have already been imported into the model as OBSERVED DATA within a model package.

'''
# %%
import flopy
import pandas as pd
import matplotlib.pyplot as plt
import os

# Define paths to model files
in_dir = "e:/SIAM2-InquinamentoDiffuso/Input_flopy/"
model_ws = os.path.join(in_dir, "PCE/")
ucn_file = f"{model_ws}/pce_tmr_ne1_barri.UCN"

# %%
# Load the MT3D model and UCN file
mt_model = flopy.mt3d.Mt3dms.load("pce_tmr_ne.nam", model_ws=model_ws, verbose=True)
ucn_obj = flopy.utils.UcnFile(ucn_file)

# List all loaded packages in the model to see where targets are stored
print("Loaded Packages:", mt_model.get_package_list())

# %%
# Read the Excel file (assuming a single column named 'ID' with the selected target IDs)
selected_targets_df = pd.read_excel(os.path.join(in_dir, "SelGIS_targets.xlsx"))
selected_targets = selected_targets_df['ID'].tolist()

# Extract observation targets from the model
obs_targets = mt_model.sft.obsdata  # Having checked that observations were loaded into the SFT package

# Extract simulated concentration data
times = ucn_obj.get_times()

# %%
# Initialize lists for storing results
observed = []
simulated = []
target_ids = []

# Loop through the selected target IDs
for target_id in selected_targets:
    if target_id in obs_targets.keys():
        # Get the observation data for the target
        obs_data = obs_targets[target_id]

        # Extract the row, column, and layer of the observation point
        row = obs_data['row']
        col = obs_data['column']
        lay = obs_data['layer']

        # Loop through observation records
        for record in obs_data['data']:
            time = record['time']
            obs_conc = record['value']

            # Find the closest simulation time
            closest_time = min(times, key=lambda x: abs(x - time))

            # Get the simulated concentration
            sim_conc = ucn_obj.get_data(totim=closest_time)[lay, row, col]

            # Append the data for plotting
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
# Plot observed vs simulated concentrations
plt.figure(figsize=(10, 6))
plt.scatter(df_results["Observed_Conc"], df_results["Simulated_Conc"], color='blue', edgecolor='k', alpha=0.7)
plt.plot([df_results["Observed_Conc"].min(), df_results["Observed_Conc"].max()],
         [df_results["Observed_Conc"].min(), df_results["Observed_Conc"].max()], 'r--', label='1:1 Line')
plt.xlabel("Observed Concentration (ug/L)")
plt.ylabel("Simulated Concentration (ug/L)")
plt.title("Observed vs Simulated PCE Concentrations for Selected Targets")
plt.legend()
plt.grid()
plt.show()