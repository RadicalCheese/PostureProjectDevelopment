import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

file_path = '/home/isabelconaghan/Documents/MPU6050/daily_avg_angles.csv'

#check if file exists
if not os.path.exists(file_path):
    print("CSV file not found.")
    exit()

#load data in from csv file
df = pd.read_csv(file_path)

#converting 'day' column to datetime
#avoids NaN and NaT errors
df['day'] = pd.to_datetime(df['day'], errors='coerce')

#dropping rows with invalid timestamps or angles
df.dropna(subset=['day', 'overall_angle'], inplace=True)
#round figures to 1 decimal place
df = df.round(1)

#keeping only last 24 entries to avoid cluttering graphs
df = df.tail(24)

#plotting
figure, axis = plt.subplots()
ax.plot(df['day'], df['overall_angle'], 'o-', label='Tilt Angle', color='orange')

#formatting x-axis for daily ticks
#identifying days in the time format by using the built-in day locator function
axis.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))  # e.g., Apr 17
axis.xaxis.set_major_locator(mdates.DayLocator(interval=1))

#adding labels and styling details to the graph
axis.set_xlabel("Day")
axis.set_ylabel("Angle in Degrees")
axis.set_title("MPU6050 Daily Tilt Angles")
axis.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# Show plot
plt.show()
