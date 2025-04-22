from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os
from datetime import datetime

#instantiates the Flask API server
app = Flask(__name__)
#implements CORS for data broadcasting
#data now accessible by mobile application 
CORS(app) 

#filepaths
mpu6050_path = '/home/isabelconaghan/Documents/MPU6050/get_mpu6050_data.csv'
hourly_path = '/home/isabelconaghan/Documents/MPU6050/hourly_avg_angles.csv'
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

    #renaming 'hour' to 'time' 
    #hourly data purposes
    if 'hour' in df.columns:
        df.rename(columns={'hour': 'time'}, inplace=True)

    if 'angle' in df.columns and 'overall_angle' not in df.columns:
        df.rename(columns={'angle': 'overall_angle'}, inplace=True)

#cleans data again
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df['overall_angle'] = pd.to_numeric(df['overall_angle'], errors='coerce')
    df.dropna(subset=['time', 'overall_angle'], inplace=True)
    df = df.round(1)
    df.sort_values(by='time', inplace=True)
    return df.tail(10)

#API endpoint for live data
@app.route('/live')
def live_data():
    #gets data from the correct csv file
    df = get_clean_data(mpu6050_path)
    
    #checks if data is not being passed in
    if df.empty:
        return jsonify({'error': 'No data available'}), 404

    #converts data to json format
    #lists values
    response = {
        #using datetime format to keep values clean and in the right order
        "timestamps": df['time'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist(),
        "angles": df['overall_angle'].tolist()
    }
    
    #jsonifies data
    return jsonify(response)

#API endpoint for hourly data
@app.route('/hourly')
def hourly_data():
    #cleans data from the hourly average csv file
    df = get_clean_data(hourly_path)
    
    #checks if data is not being passed in
    if df.empty:
        return jsonify({'error': 'No data available'}), 404

    #converting values to json format
    #listing values
    response = {
        #using datetime format to keep values clean and in the right order
        "timestamps": df['time'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist(),
        "angles": df['overall_angle'].tolist()
    }
    #jsonifies data
    return jsonify(response)

#when more than two endpoints are declared server becomes overloaded
#throws 500: Internal Server error
#@app.route('/daily')
#def daily_data():
   # df = get_clean_data(daily_path)
   # #checks if data is not being passed in
   # if df.empty:
     #   return jsonify({'error': 'No data available'}), 404

    #converting to json
    #listing values
    #response = {
       # "timestamps": df['time'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist(),
       # "angles": df['overall_angle'].tolist()
   # }
    #jsonifies data
   # return jsonify(response)

#host the endpoints on port 2000
#http://192.18.32.0:2000/
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2000)
