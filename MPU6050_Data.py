#import time
#import mpu6050
#from csv import writer

#mpu6050 = mpu6050.mpu6050(0x68)

#def read_data():
    #acc_data = mpu6050.get_accel_data()
    #gyro_data = mpu6050.get_gyro_data()
    
    #return acc_data, gyro_data

#with open('mpu6050_data.csv', 'w', buffering=1, newline='') as f:
    #data_writer = writer(f)
    #data_writer.writerow(['acc','gyro'])
    
   #while True:
        #data = read_data()
        #data_writer.writerow(data)
    
    #time.sleep(20)
    
import time
import numpy as np
from mpu6050 import mpu6050
from csv import writer
from datetime import datetime

mpu = mpu6050(0x68)

def read_data():
    acc_data = mpu.get_accel_data()
    gyro_data = mpu.get_gyro_data()
    #date and time variable
    current_time = datetime.now()
    
    #get date and time
    return acc_data, gyro_data, current_time

sense_data = []

with open('get_mpu6050_data.csv', 'a', buffering=1, newline='') as f:
    data_writer = writer(f)
    data_writer.writerow(['accelerometer', 'gyroscope', 'overall_angle', 'time'])

    dt = 0.01  # Time step in seconds
    alpha = 0.98  # Complementary filter constant

    pitch = 0
    roll = 0

    while True:
        acc, gyro, current_time = read_data()

        # Step 1: Calculate pitch and roll from accelerometer
        pitch_accel = np.arctan2(acc["y"], np.sqrt(acc["x"]**2 + acc["z"]**2))
        roll_accel = np.arctan2(-acc["x"], np.sqrt(acc["y"]**2 + acc["z"]**2))

        # Step 2: Integrate gyro data
        pitch_gyro = pitch + gyro["x"] * dt
        roll_gyro = roll + gyro["y"] * dt

        # Step 3: Complementary filter
        pitch = alpha * pitch_gyro + (1 - alpha) * pitch_accel
        roll = alpha * roll_gyro + (1 - alpha) * roll_accel

        # Final angles
        pitch_deg = np.degrees(pitch)
        roll_deg = np.degrees(roll)

        # Combine pitch and roll into overall tilt angle
        pitch_rad = np.radians(pitch_deg)
        roll_rad = np.radians(roll_deg)
        overall_rad = np.sqrt(pitch_rad**2 + roll_rad**2)
        overall_deg = np.degrees(overall_rad)

        sense_data.append(acc)
        sense_data.append(gyro)
        sense_data.append(overall_deg)
        sense_data.append(current_time)
        
        data_writer.writerow([acc, gyro, overall_deg, current_time])

        time.sleep(10)

