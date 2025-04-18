import pandas as pd

# Load the CSV
df = pd.read_csv('get_mpu6050_data.csv')

# Clean column names
df.columns = df.columns.str.strip()

# Remove bad rows (e.g. headers repeated mid-file)
df = df[df['time'] != 'time']

# Clean up types
df['time'] = pd.to_datetime(df['time'], errors='coerce')
df['overall_angle'] = pd.to_numeric(df['overall_angle'], errors='coerce')

# Drop rows with bad values
df.dropna(subset=['time', 'overall_angle'], inplace=True)

# Add hour/day columns
df['hour'] = df['time'].dt.floor('h')
df['day'] = df['time'].dt.floor('d')

# Group and average
hourly_avg = df.groupby('hour')['overall_angle'].mean().reset_index().round(1)
daily_avg = df.groupby('day')['overall_angle'].mean().reset_index().round(1)

# Print to console
print(hourly_avg)
print(daily_avg)

# Save to CSVs
hourly_avg.to_csv('hourly_avg_angles.csv', index=False)
daily_avg.to_csv('daily_avg_angles.csv', index=False)
