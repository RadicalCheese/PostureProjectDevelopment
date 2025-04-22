import pandas as pd

#loading in the CSV file storing the sensor data
df = pd.read_csv('get_mpu6050_data.csv')

#removing unnecessary whitespace from column names
df.columns = df.columns.str.strip()

#removing rows where the title does not match the values in the csv file
df = df[df['time'] != 'time']

#cleaning up time and angle columns to avoid NaN and NaT errors
df['time'] = pd.to_datetime(df['time'], errors='coerce')
df['overall_angle'] = pd.to_numeric(df['overall_angle'], errors='coerce')

#drop rows with null values
df.dropna(subset=['time', 'overall_angle'], inplace=True)

#adding hour/day columns to the csv data
df['hour'] = df['time'].dt.floor('h')
df['day'] = df['time'].dt.floor('d')

#grouping angles by hours and days
#calculating mean averages of the angles
#rounding the angles to 1 decimal place
hourly_avg = df.groupby('hour')['overall_angle'].mean().reset_index().round(1)
daily_avg = df.groupby('day')['overall_angle'].mean().reset_index().round(1)

#printing the averages to console
#ensuring the maths is being recognised
print(hourly_avg)
print(daily_avg)

#saving the new data to new csv files
hourly_avg.to_csv('hourly_avg_angles.csv', index=False)
daily_avg.to_csv('daily_avg_angles.csv', index=False)
