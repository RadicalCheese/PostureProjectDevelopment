from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__) 
CORS(app)

live_path = '/home/isabelconaghan/Documents/SenseHAT/senhat.csv'
hourly_path = '/home/isabelconaghan/Documents/SenseHAT/hourly_avg_angles.csv'

def parse_time(time):
    try:
        return pd.to_datetime(time)
    except:
        return pd.NaT

def get_clean_data(file_path):
    #returns empty DataFrame if file not found
    if not os.path.exists(file_path):
        return pd.DataFrame()  
        
    #cleaning data for json parsing
    df = pd.read_csv(file_path)
    
    #renaming 'hour' to 'time' 
    #hourly data purposes
    if 'hour' in df.columns:
        df.rename(columns={'hour': 'time'}, inplace=True)
        
    df = df[df['time'].apply(lambda x: isinstance(x, str))]
    df['time'] = df['time'].apply(parse_time)
    df.dropna(subset=['time', 'angle'], inplace=True)
    df = df.round(1)
    df.sort_values(by='time', inplace=True)
    df = df.tail(10)
    return df

@app.route('/live')
def data():
    df = get_clean_data(live_path)
    if df.empty:
        return jsonify({'error': 'No data available'}), 404

    #converting to json
    response = {
        "timestamps": df['time'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist(),
        "angles": df['angle'].tolist()
    }
    return jsonify(response)
    
    
#to get hourly data from API
@app.route('/hourly')
def hourly_data():
    df = get_clean_data(hourly_path)
    
    #checks if data is not being passed in
    if df.empty:
        return jsonify({'error': 'No data available'}), 404

    #converting values to json format
    #listing values
    response = {
        "timestamps": df['time'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist(),
        "angles": df['angle'].tolist()
    }
    #jsonifies data
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
