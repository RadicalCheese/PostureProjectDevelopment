import pandas as pd
import matplotlib.pyplot as plot
from datetime import datetime, date
from matplotlib.animation import FuncAnimation
import os

file_path = '/home/isabelconaghan/Documents/SenseHAT/senhat.csv'
refresh_interval = 2000 

#establishing scatter plot
#code from
#https://medium.com/intel-student-ambassadors/live-graph-simulation-using-python-matplotlib-and-pandas-30ea4e50f883
figure, axis = plot.subplots()
line, = axis.plot([], [], 'o-', label='Tilt Angle')
axis.set_xlabel("Time")
axis.set_ylabel("Angle in Degrees")
axis.set_title("SenseHAT Live Angles")
plot.xticks(rotation=45)
plot.tight_layout()
axis.legend()

#time parser
#ensures date is in datetime format
#otherwise returns it as a NaT (Not a Time) label
#NaTs get cleaned further on
def parse_time(time):
    try:
        return pd.to_datetime(time)
    except:
            return pd.NaT

#animates plot
#updates using csv file reloads
def update(frame):
    if not os.path.exists(file_path):
        return

    #reads in the csv file
    df = pd.read_csv(file_path)
    #removes whitespaces
    df.columns = df.columns.str.strip()

    #renaming columns if needed
    if 'angle' in df.columns and 'angle' not in df.columns:
        df.rename(columns={'angle': 'angle'}, inplace=True)
    if 'time' in df.columns and 'time' not in df.columns:
        df.rename(columns={'time': 'time'}, inplace=True)

    #cleans the data by making sure the data is in the right formats
    #if time or angle data can't be parsed, return as NaN or NaT
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df['angle'] = pd.to_numeric(df['angle'], errors='coerce')
    #drops null values
    df.dropna(subset=['time', 'angle'], inplace=True)
    #rounds values to one decimal place
    df = df.round(1)
    #only graph last 10 entries to prevent clutter
    df = df.tail(10)
    
    #writing to a new csv file
    cleaned_file_path = '/home/isabelconaghan/Documents/SenseHAT/cleaned_sensehat_data.csv'
    df.to_csv(cleaned_file_path, index=False)

    #plotting the updated data
    axis.clear()
    axis.plot(df['time'], df['angle'], 'o-', label='Tilt Angle')
    axis.set_xlabel("Time")
    axis.set_ylabel("Angle in Degrees")
    axis.set_title("SenseHAT Live Angles")
    axis.legend()
    plot.xticks(rotation=45)
    plot.tight_layout()
    
    

#runs animation to update live data
animation = FuncAnimation(figure, update, interval=refresh_interval, cache_frame_data=False)
plot.show()
