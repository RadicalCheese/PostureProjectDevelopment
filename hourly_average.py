import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

file_path = '/home/isabelconaghan/Documents/MPU6050/hourly_avg_angles.csv'

# Check if file exists
if not os.path.exists(file_path):
    print("CSV file not found.")
    exit()

# Load data
df = pd.read_csv(file_path)

# Convert 'hour' column to datetime
df['hour'] = pd.to_datetime(df['hour'], errors='coerce')

# Drop rows with invalid timestamps or angles
df.dropna(subset=['hour', 'overall_angle'], inplace=True)
df = df.round(1)

# Optional: keep only last 24 entries
df = df.tail(24)

# Plotting
fig, ax = plt.subplots()
ax.plot(df['hour'], df['overall_angle'], 'o-', label='Tilt Angle', color='orange')

# Time formatting
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))

# Labels and styling
ax.set_xlabel("Time")
ax.set_ylabel("Angle in Degrees")
ax.set_title("MPU6050 Hourly Tilt Angles")
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# Show plot
plt.show()
