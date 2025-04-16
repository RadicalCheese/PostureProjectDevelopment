from flask import Flask, jsonify
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
file_path = '/home/isabelconaghan/Documents/SenseHAT/senhat.csv'

def parse_time(time):
    try:
        return pd.to_datetime(time)
    except:
        return pd.NaT

def get_clean_data():
    if not os.path.exists(file_path):
        return pd.DataFrame()  # return empty DataFrame if file not found

    df = pd.read_csv(file_path)
    df = df[df['time'].apply(lambda x: isinstance(x, str))]
    df['time'] = df['time'].apply(parse_time)
    df.dropna(subset=['time', 'angle'], inplace=True)
    df = df.round(1)
    df.sort_values(by='time', inplace=True)
    df = df.tail(10)  # return only the last 10 readings
    return df

@app.route('/data')
def data():
    df = get_clean_data()
    if df.empty:
        return jsonify({'error': 'No data available'}), 404

    #converting to json
    response = {
        "timestamps": df['time'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist(),
        "angles": df['angle'].tolist()
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
