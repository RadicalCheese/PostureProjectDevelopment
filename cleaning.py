import pandas as pd
import matplotlib.pyplot as plot
from datetime import datetime, date
from matplotlib.animation import FuncAnimation
import os

file_path = '/home/isabelconaghan/Documents/MPU6050/get_mpu6050_data.csv'
refresh_interval = 2000 

#establishing scatter plot
#code from
#https://medium.com/intel-student-ambassadors/live-graph-simulation-using-python-matplotlib-and-pandas-30ea4e50f883
figure, axis = plot.subplots()
line, = axis.plot([], [], 'o-', label='Tilt Angle')
axis.set_xlabel("Time")
axis.set_ylabel("Angle in Degrees")
axis.set_title("MPU6050 Live Angles")
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

    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    # Rename if needed
    if 'angle' in df.columns and 'overall_angle' not in df.columns:
        df.rename(columns={'angle': 'overall_angle'}, inplace=True)
    if 'timestamp' in df.columns and 'time' not in df.columns:
        df.rename(columns={'timestamp': 'time'}, inplace=True)

    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df['overall_angle'] = pd.to_numeric(df['overall_angle'], errors='coerce')
    df.dropna(subset=['time', 'overall_angle'], inplace=True)
    df = df.round(1)
    df = df.tail(10)

    axis.clear()
    axis.plot(df['time'], df['overall_angle'], 'o-', label='Tilt Angle')
    axis.set_xlabel("Time")
    axis.set_ylabel("Angle in Degrees")
    axis.set_title("MPU6050 Live Angles")
    axis.legend()
    plot.xticks(rotation=45)
    plot.tight_layout()
    
    

#runs animation
animation = FuncAnimation(figure, update, interval=refresh_interval, cache_frame_data=False)
plot.show()
