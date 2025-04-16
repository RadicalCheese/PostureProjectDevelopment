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
    sense_data.append(current_time.time())
    
    #get environmental data
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
    
    #alright ok let's do this
    #complementary filter time
    #calculating angles n all that jazz
    
    dt = 0.01  # Time step in seconds
    alpha = 0.98  # Filter constant

    # Step 1: Calculate pitch and roll angles from accelerometer data
    pitch_accel = np.arctan2(acc["y"], np.sqrt(acc["x"]**2 + acc["z"]**2))
    roll_accel = np.arctan2(-acc["x"], np.sqrt(acc["y"]**2 + acc["z"]**2))

    # Step 2: Integrate gyroscope data to get angles
    # Assuming initial angles are zero (for simplicity)
    pitch_gyro = gyro["x"] * dt
    roll_gyro = gyro["y"] * dt

    # Step 3: Apply complementary filter to fuse accelerometer and gyroscope data
    pitch = alpha * (pitch_accel) + (1 - alpha) * (pitch_gyro)
    roll = alpha * (roll_accel) + (1 - alpha) * (roll_gyro)

    # Print the final angles
    pitchDegree = np.degrees(pitch)
    rollDegree = np.degrees(roll)
    
    # Assuming you have pitch and roll in degrees, you can convert them to radians first
    pitchRadians = np.radians(pitchDegree)  # Convert pitch from degrees to radians
    rollRadians = np.radians(rollDegree)    # Convert roll from degrees to radians

    # Calculate the overall tilt (overall angle) from pitch and roll
    overallRadianAngle = np.sqrt(pitchRadians**2 + rollRadians**2)  # Combine pitch and roll
    overallDegreeAngle = np.degrees(overallRadianAngle)  # Convert back to degrees
    
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

