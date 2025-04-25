import pandas as pd
import matplotlib.pyplot as plot
import matplotlib.dates as mdates
import os

file_path = '/home/isabelconaghan/Documents/SenseHAT/hourly_avg_angles.csv'

# Check if file exists
if not os.path.exists(file_path):
    print("CSV file not found.")
    exit()

# Load data
df = pd.read_csv(file_path)

# Convert 'hour' column to datetime
df['hour'] = pd.to_datetime(df['hour'], errors='coerce')

# Drop rows with invalid timestamps or angles
df.dropna(subset=['hour', 'angle'], inplace=True)
df = df.round(1)

# Optional: keep only last 24 entries
df = df.tail(24)

# Plotting
figure, axis = plt.subplots()
axis.plot(df['hour'], df['angle'], 'o-', label='Tilt Angle', color='orange')

# Time formatting
axis.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
axis.xaxis.set_major_locator(mdates.HourLocator(interval=1))

# Labels and styling
axis.set_xlabel("Time")
axis.set_ylabel("Angle in Degrees")
axis.set_title("SenseHAT Hourly Tilt Angles")
axis.legend()
plot.xticks(rotation=45)
plot.tight_layout()

# Show plot
plot.show()
