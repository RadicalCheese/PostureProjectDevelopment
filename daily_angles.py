import pandas as pd
import matplotlib.pyplot as plot
import matplotlib.dates as mdates
import os

file_path = '/home/isabelconaghan/Documents/SenseHAT/daily_avg_angles.csv'

#check if file exists
if not os.path.exists(file_path):
    print("CSV file not found.")
    exit()

#load data from csv file
df = pd.read_csv(file_path)

#converting 'day' column to datetime to avoid NaN and NaT errors
df['day'] = pd.to_datetime(df['day'], errors='coerce')

#dropping rows with null or invalid timestamps or angles
df.dropna(subset=['day', 'angle'], inplace=True)
df = df.round(1)

#keeping only last 7 entries
df = df.tail(7)

#plotting the data
figure, axis = plot.subplots()
axis.plot(df['day'], df['angle'], 'o-', label='Tilt Angle', color='purple')

#formatting the dates and locating the correct day
#graphing the data
axis.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
axis.xaxis.set_major_locator(mdates.DayLocator(interval=1))

#labels and styling
axis.set_xlabel("Time")
axis.set_ylabel("Angle in Degrees")
axis.set_title("SenseHAT Daily Tilt Angles")
axis.legend()
plot.xticks(rotation=45)
plot.tight_layout()

#showing the plot
plot.show()
