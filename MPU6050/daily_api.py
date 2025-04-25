from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
CORS(app) 
daily_path = '/home/isabelconaghan/Documents/MPU6050/daily_avg_angles.csv'

#parses time
def parse_time(time):
    try:
        return pd.to_datetime(time)
    except:
        return pd.NaT

#takes in csv file as file_path
def get_clean_data(file_path):
    if not os.path.exists(file_path):
        return pd.DataFrame()

    #reads in respective CSV files, declared in methods
    df = pd.read_csv(file_path)
    
    #gets rid of whitespaces
    df.columns = df.columns.str.strip()

#cleans data again
    df['day'] = pd.to_datetime(df['day'], errors='coerce')
    df['overall_angle'] = pd.to_numeric(df['overall_angle'], errors='coerce')
    df.dropna(subset=['day', 'overall_angle'], inplace=True)
    df = df.round(1)
    df.sort_values(by='day', inplace=True)
    return df.tail(10)

#to get daily data from API
@app.route('/daily')
def daily_data():
    df = get_clean_data(daily_path)
    #checks if data is not being passed in
    if df.empty:
        return jsonify({'error': 'No data available'}), 404

    #converting to json
    #listing values
    response = {
        "timestamps": df['day'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist(),
        "angles": df['overall_angle'].tolist()
    }
    #jsonifies data
    return jsonify(response)

#different port to avoid overloading
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
