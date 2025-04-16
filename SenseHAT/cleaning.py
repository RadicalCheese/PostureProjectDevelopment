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
axis.set_title("Sense HAT Live Angles")
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

#cleaning data
    df = pd.read_csv(file_path)
    df = df[df['time'].apply(lambda x: isinstance(x, str))]
    df['time'] = df['time'].apply(parse_time)
    df.dropna(subset=['time', 'angle'], inplace=True)
    df = df.round(1)
    df.sort_values(by='time', inplace=True)

    #graphs only last 10 readings- saves clutter
    df = df.tail(10)

    #clears and then actively repopulates graph readings
    axis.clear()
    axis.plot(df['time'], df['angle'], 'o-', label='Tilt Angle')
    axis.set_xlabel("Time")
    axis.set_ylabel("Angle in Degrees")
    axis.set_title("Sense HAT Live Angles")
    axis.legend()
    plot.xticks(rotation=45)
    plot.tight_layout()
    
    

#runs animation
animation = FuncAnimation(figure, update, interval=refresh_interval)
plot.show()

