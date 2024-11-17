import os
os.environ['NO_MAC_EXTENSIONS'] = '1'

from app import readData, detectHydrateFormation
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Read the data using readData from app.py
file_name = "Valiant_505H-09_22-09_30.csv"
dataPoints = readData(file_name)

# Step 2: Detect hydrate formation and normalization using detectHydrateFormation from app.py
hydrate_times, normal_times = detectHydrateFormation(dataPoints)

# Step 3: Convert dataPoints into a pandas DataFrame for plotting
data_dict = {
    'Time': [dp.time for dp in dataPoints],
    'InstantaneousVolume': [dp.instantaneousVolume for dp in dataPoints],
    'SetpointVolume': [dp.setpointVolume for dp in dataPoints],
    'ValvePercentOpen': [dp.valvePercentOpen for dp in dataPoints]
}
data = pd.DataFrame(data_dict)

# Convert 'Time' to datetime with specified format
data['Time'] = pd.to_datetime(data['Time'], format='%m/%d/%Y %I:%M:%S %p')

# Convert hydrate_times and normal_times to datetime
hydrate_times_dt = pd.to_datetime(hydrate_times, format='%m/%d/%Y %I:%M:%S %p')
normal_times_dt = pd.to_datetime(normal_times, format='%m/%d/%Y %I:%M:%S %p')

# Get the instantaneous volumes at the hydrate and normal times
hydrate_volumes = data.loc[data['Time'].isin(hydrate_times_dt), 'InstantaneousVolume']
normal_volumes = data.loc[data['Time'].isin(normal_times_dt), 'InstantaneousVolume']

# Step 4: Plot the data
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot Instantaneous Volume and Setpoint Volume on primary y-axis
ax1.plot(data['Time'], data['InstantaneousVolume'], label="Instantaneous Volume", color="blue")
ax1.plot(data['Time'], data['SetpointVolume'], label="Setpoint Volume", color="green")
ax1.scatter(hydrate_times_dt, hydrate_volumes, color="red", label="Hydrate Formation", zorder=5)
ax1.scatter(normal_times_dt, normal_volumes, color="green", label="System Normalized", zorder=5)
ax1.set_xlabel("Time")
ax1.set_ylabel("Volume")
ax1.grid()

# Plot Valve Percent Open on secondary y-axis
ax2 = ax1.twinx()
ax2.plot(data['Time'], data['ValvePercentOpen'], label="Valve Percent Open", color="orange")
ax2.set_ylabel("Valve Percent Open (%)")

# Combine legends from both axes
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

# Customize and show the plot
plt.title("Hydrate Formation and Normalization Detection")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()