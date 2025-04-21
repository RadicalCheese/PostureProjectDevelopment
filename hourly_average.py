import pandas as pd
import matplotlib.pyplot as plot
import matplotlib.dates as mdates
import os

file_path = '/home/isabelconaghan/Documents/MPU6050/hourly_avg_angles.csv'

#checking if file exists
if not os.path.exists(file_path):
    print("CSV file not found.")
    exit()

#loading data from hourly averages CSV file
df = pd.read_csv(file_path)

#converting the 'hour' column to datetime
#avoids NaN and NaT errors
df['hour'] = pd.to_datetime(df['hour'], errors='coerce')

#dropping rows with invalid timestamps or angles
df.dropna(subset=['hour', 'overall_angle'], inplace=True)
df = df.round(1)

#keep only the last 24 entries to avoid clutter
df = df.tail(24)

#plotting the data
figure, axis = plt.subplots()
axis.plot(df['hour'], df['overall_angle'], 'o-', label='Tilt Angle', color='orange')

#formatting the time to show the hour and minutes
#using the hour function to identify and update the hours
axis.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
axis.xaxis.set_major_locator(mdates.HourLocator(interval=1))

#adding labels and styling the graph
axis.set_xlabel("Time")
axis.set_ylabel("Angle in Degrees")
axis.set_title("MPU6050 Hourly Tilt Angles")
axis.legend()
plot.xticks(rotation=45)
plot.tight_layout()

#showing the plot
plot.show()
