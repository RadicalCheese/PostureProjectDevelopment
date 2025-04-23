import pandas as pd

#loading in the csv file
df = pd.read_csv('senhat.csv')

#clean column names by removing whitespaces
df.columns = df.columns.str.strip()

#removing rows being repeated mid-file
df = df[df['time'] != 'time']

#clean up types so they're in correct format
df['time'] = pd.to_datetime(df['time'], errors='coerce')
df['angle'] = pd.to_numeric(df['angle'], errors='coerce')

#dropping null values
df.dropna(subset=['time', 'angle'], inplace=True)

#adding hour and day columns
df['hour'] = df['time'].dt.floor('h')
df['day'] = df['time'].dt.floor('d')

#grouping the data by hours and days, averaging them out
#and rounding them to 1 decimal place
hourly_avg = df.groupby('hour')['angle'].mean().reset_index().round(1)
daily_avg = df.groupby('day')['angle'].mean().reset_index().round(1)

#printing to console to test averages are right
print(hourly_avg)
print(daily_avg)

#saving to respective csv files
hourly_avg.to_csv('hourly_avg_angles.csv', index=False)
daily_avg.to_csv('daily_avg_angles.csv', index=False)
