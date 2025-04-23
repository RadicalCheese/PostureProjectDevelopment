import pandas as pd
import matplotlib.pyplot as plot
import matplotlib.dates as mdates
import os

file_path = '/home/isabelconaghan/Documents/SenseHAT/hourly_avg_angles.csv'

#checking if file exists
if not os.path.exists(file_path):
    print("CSV file not found.")
    exit()

#loading data from csv file
df = pd.read_csv(file_path)

#converting 'hour' column to datetime
df['hour'] = pd.to_datetime(df['hour'], errors='coerce')

#dropping rows with null or invalid timestamps or angles
df.dropna(subset=['hour', 'angle'], inplace=True)
df = df.round(1)

#keeping only last 24 entries to avoid clutter
df = df.tail(24)

#plotting 
figure, axis = plot.subplots()
axis.plot(df['hour'], df['angle'], 'o-', label='Tilt Angle', color='orange')

#formatting time and hour using Matplotlib's DateFormatter 
#and HourLocator modules
axis.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
axis.xaxis.set_major_locator(mdates.HourLocator(interval=1))

#labels and styling
axis.set_xlabel("Time")
axis.set_ylabel("Angle in Degrees")
axis.set_title("SenseHAT Hourly Tilt Angles")
axis.legend()
plot.xticks(rotation=45)
plot.tight_layout()

#showing plot
plot.show()
