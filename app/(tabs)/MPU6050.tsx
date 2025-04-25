import React, { useEffect, useState } from 'react';
import { StyleSheet, Text, View, Dimensions, ActivityIndicator, SafeAreaView, ScrollView } from 'react-native';
import axios from 'axios';
import { LineChart } from 'react-native-chart-kit';

//inspiration taken from: https://medium.com/@nuburoojkhattak/connecting-your-react-app-to-your-flask-api-a-step-by-step-guide-3daa8ce9d3f2

//url for flask api server
const API_URL = 'http://192.168.18.32:2000/live'; 
const HOURLY_URL = 'http://192.168.18.32:2000/hourly'; 
const DAILY_URL = 'http://192.168.18.32:3000/daily'; 


export default function App() {
  //labels array and data array
  const [liveData, setLiveData] = useState({ labels: [], datasets: [{ data: [] }] });
  const [hourlyData, setHourlyData] = useState({ labels: [], datasets: [{ data: [] }] });
  const [dailyData, setDailyData] = useState({ labels: [], datasets: [{ data: [] }] });
  //app loads while waiting for live readings
  const [loading, setLoading] = useState(true);
  //serror message set to empty
  const [error, setError] = useState('');

  //getting data from flask api using axios
  const fetchLiveData = async () => {
    try {
      const response = await axios.get(API_URL);
      const { timestamps, angles } = response.data;

      //labels are just times
      const labels = timestamps.map(ts => ts.split(' ')[1].slice(0, 5));

      setLiveData({
        labels,
        datasets: [{ data: angles }]
      });

      //setting the error string to returning a message if no data is fetched
      setError('');
    } catch (err) {
      setError('Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  //getting hourly data from flask api using axios
  const fetchHourlyData = async () => {
    try {
      const response = await axios.get(HOURLY_URL);
      const { timestamps, angles } = response.data;

      //labels are just times
      const labels = timestamps.map(ts => ts.split(' ')[1].slice(0, 5));

      setHourlyData({
        labels,
        datasets: [{ data: angles }]
      });

      //setting the error string to returning a message if no data is fetched
      setError('');
    } catch (err) {
      setError('Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

   //getting daily data from flask api using axios
   const fetchDailyData = async () => {
    try {
      const response = await axios.get(DAILY_URL);
      const { timestamps, angles } = response.data;

      //labels are just times
      const labels = timestamps.map(ts => ts.split(' ')[0]);

      setDailyData({
        labels,
        datasets: [{ data: angles }]
      });

      //setting the error string to returning a message if no data is fetched
      setError('');
    } catch (err) {
      setError('Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  //when not calling to the API
  //use CSV files for historic data
  const loadOfflineCSV = async () => {
    try {
      const asset = Asset.fromModule(require('./assets/data/daily_avg_angles.csv'));
      await asset.downloadAsync();
      const fileUri = asset.localUri || asset.uri;
      const response = await FileSystem.readAsStringAsync(fileUri);
      const parsed = Papa.parse(response, { header: true });
      const cleaned = parsed.data.filter(row => row.date && row.overall_angle);
      const labels = cleaned.map(row => row.date);
      const angles = cleaned.map(row => parseFloat(row.overall_angle));
      setDailyData({ labels, datasets: [{ data: angles }] });
    } catch (error) {
      setError('Failed to load offline CSV');
    }
  };

  //checking to see if the data is being fetched from the flask api
  // useEffect(() => {
  //   fetch('http://192.168.18.32:2000/mpu6050')
  //     .then(response => response.json())
  //     .then(json => console.log('Data from server:', json))
  //     .catch(err => console.log('Error fetching:', err.message));
  // }, []);

  //updating the graphs
  useEffect(() => {
    fetchLiveData();
    fetchHourlyData();
    fetchDailyData();
    const interval = setInterval(fetchLiveData, 10000);
    return () => clearInterval(interval);
  }, []);

  //creating the graphs
  return (
    //live graph
    <ScrollView style={styles.container}>
      <Text style={styles.title}>MPU6050 Data</Text>
      <Text style={styles.subheading}>Live Angle Chart</Text>

      {loading ? (
        <ActivityIndicator size="large" />
      ) : error ? (
        <Text style={styles.error}>{error}</Text>
      ) : (
        
<LineChart
  data={liveData}
  width={Dimensions.get('window').width - 32}
  height={220}
  yAxisSuffix="°"
  chartConfig={{
    backgroundColor: '#003f5c',
    backgroundGradientFrom: '#2f4b7c',
    backgroundGradientTo: '#665191',
    decimalPlaces: 1,
    color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
    labelColor: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
    style: {
      borderRadius: 16
    },
    propsForDots: {
      r: '6',
      strokeWidth: '2',
      stroke: '#a05195'
    }
  }}
  bezier
  style={styles.chart}
/>
)}


<Text style={styles.subheading}>Hourly Angle Chart</Text>
{loading ? (
  <ActivityIndicator size="large" />
) : error ? (
  <Text style={styles.error}>{error}</Text>
) : (
  <LineChart
  data={hourlyData}
  width={Dimensions.get('window').width - 32}
  height={220}
  yAxisSuffix="°"
  chartConfig={{
    backgroundColor: '#1b4332',
    backgroundGradientFrom: '#2d6a4f',
    backgroundGradientTo: '#95d5b2',
    decimalPlaces: 1,
    color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
    labelColor: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
    style: {
      borderRadius: 16
    },
    propsForDots: {
      r: '6',
      strokeWidth: '2',
      stroke: '#74c69d'
    }
  }}
  bezier
  style={styles.chart}
/>

)}

<Text style={styles.subheading}>Daily Angle Chart</Text>
{loading ? (
  <ActivityIndicator size="large" />
) : error ? (
  <Text style={styles.error}>{error}</Text>
) : (
  <LineChart
  data={dailyData}
  width={Dimensions.get('window').width - 32}
  height={220}
  yAxisSuffix="°"
  chartConfig={{
    backgroundColor: '#6a040f',
    backgroundGradientFrom: '#9d0208',
    backgroundGradientTo: '#f48c06',
    decimalPlaces: 1,
    color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
    labelColor: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
    style: {
      borderRadius: 16
    },
    propsForDots: {
      r: '6',
      strokeWidth: '2',
      stroke: '#faa307'
    }
  }}
  bezier
  style={styles.chart}
/>
)}
</ScrollView>

  
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 50,
    paddingHorizontal: 16,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 20
  },
  subheading: {
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'left',
    marginBottom: 20
  },
  error: {
    color: 'red',
    textAlign: 'center',
    marginTop: 20
  },
  chart: {
    marginVertical: 8,
    borderRadius: 16
  }
});



