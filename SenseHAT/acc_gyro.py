from sense_hat import SenseHat
from datetime import datetime
import time
import numpy as np
from csv import writer

sense = SenseHat()
sense.color.gain = 64
sense.color.integration_cycles = 64


def get_sense_data():
    sense_data = []
    
    #date and time variable
    current_time = datetime.now()
    
    #get date and time
    #use only time
    sense_data.append(current_time.time())
    
    #get environmental data from sensors
    sense_data.append(sense.get_temperature())
    sense_data.append(sense.get_pressure())
    sense_data.append(sense.get_humidity())
    
    #get accelerometer data from x, y and z axes
    acc = sense.get_accelerometer_raw()
    sense_data.append(acc["x"])
    sense_data.append(acc["y"])
    sense_data.append(acc["z"])
    
    #get gyroscope data from x, y and z axes
    gyro = sense.get_gyroscope_raw()
    sense_data.append(gyro["x"])
    sense_data.append(gyro["y"])
    sense_data.append(gyro["z"])

    #get angle data from complementary filter
    #code and general understanding from https://www.hibit.dev/posts/92/complementary-filter-and-relative-orientation-with-mpu6050
    dt = 0.01  #time increase in seconds
    alpha = 0.98  #constant for filtering, makes it so "98% of the weight lays on the gyroscope measurements"

    #1: calculating "pitch and roll" angles from accelerometer data
    pitchAccel = np.arctan2(acc["y"], np.sqrt(acc["x"]**2 + acc["z"]**2))
    rollAccel = np.arctan2(-acc["x"], np.sqrt(acc["y"]**2 + acc["z"]**2))

    #2: integrating gyroscopic data to get angles
    #assuming initial angles are zero
    pitchGyro = gyro["x"] * dt
    rollGyro = gyro["y"] * dt

    #3: fusing accelerometer and gyroscope data by use of complementary filter
    pitch = alpha * (pitchAccel) + (1 - alpha) * (pitchGyro)
    roll = alpha * (rollAccel) + (1 - alpha) * (rollGyro)

    #printing the angles in degrees for pitch and roll
    pitchDegree = np.degrees(pitch)
    rollDegree = np.degrees(roll)
    
    #convert the degrees to radians
    #radians used for specific degrees in regard to a circle
    pitchRadians = np.radians(pitchDegree)
    rollRadians = np.radians(rollDegree)

    #calculating the overall angle from pitch and roll
    overallRadianAngle = np.sqrt(pitchRadians**2 + rollRadians**2)  #combines pitch and roll
    overallDegreeAngle = np.degrees(overallRadianAngle)  #converts angle back to degrees
    
    sense_data.append(overallDegreeAngle)
    
    return sense_data

with open('senhat.csv', 'w', buffering=1, newline='') as f:
    data_writer = writer(f)
    data_writer.writerow(['time','temp','pres','hum','acc_x','acc_y','acc_z','gyro_x','gyro_y','gyro_z',
                          'angle'])
    
    while True:
        data = get_sense_data()
        data_writer.writerow(data)
        print(data)
        #creating a delay
        time.sleep(10)

