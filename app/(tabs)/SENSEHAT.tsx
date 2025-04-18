// import React, { useEffect, useState } from 'react';
// import { StyleSheet, Text, View, Dimensions, ActivityIndicator, SafeAreaView } from 'react-native';
// import axios from 'axios';
// import { LineChart } from 'react-native-chart-kit';

// //inspiration taken from: https://medium.com/@nuburoojkhattak/connecting-your-react-app-to-your-flask-api-a-step-by-step-guide-3daa8ce9d3f2

// //url for flask api server
// const API_URL = 'http://192.168.18.32:5000/senseHAT'; 

// export default function App() {
//   //labels array and data array
//   const [data, setData] = useState({ labels: [], datasets: [{ data: [] }] });
//   //app loads while waiting for live readings
//   const [loading, setLoading] = useState(true);
//   //serror message set to empty
//   const [error, setError] = useState('');

//   //getting data from flask api using axios
//   const fetchData = async () => {
//     try {
//       const response = await axios.get(API_URL);
//       const { timestamps, angles } = response.data;

//       //labels are just times
//       const labels = timestamps.map(ts => ts.split(' ')[1].slice(0, 5));

//       setData({
//         labels,
//         datasets: [{ data: angles }]
//       });

//       //setting the error string to returning a message if no data is fetched
//       setError('');
//     } catch (err) {
//       setError('Failed to fetch data');
//     } finally {
//       setLoading(false);
//     }
//   };

//   //checking to see if the data is being fetched from the flask api
//   // useEffect(() => {
//   //   fetch('http://192.168.18.32:2000/mpu6050')
//   //     .then(response => response.json())
//   //     .then(json => console.log('Data from server:', json))
//   //     .catch(err => console.log('Error fetching:', err.message));
//   // }, []);

//   //updating the graph live
//   useEffect(() => {
//     fetchData();
//     const interval = setInterval(fetchData, 10000);
//     return () => clearInterval(interval);
//   }, []);

//   //creating the graph
//   return (
//     <SafeAreaView style={styles.container}>
//       <Text style={styles.title}>Live Angle Chart</Text>

//       {loading ? (
//         <ActivityIndicator size="large" />
//       ) : error ? (
//         <Text style={styles.error}>{error}</Text>
//       ) : (
//         <LineChart
//           data={data}
//           width={Dimensions.get('window').width - 32}
//           height={220}
//           yAxisSuffix="°"
//           chartConfig={{
//             backgroundColor: '#e26a00',
//             backgroundGradientFrom: '#fb8c00',
//             backgroundGradientTo: '#ffa726',
//             decimalPlaces: 1,
//             color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
//             labelColor: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
//             style: {
//               borderRadius: 16
//             },
//             propsForDots: {
//               r: '6',
//               strokeWidth: '2',
//               stroke: '#ffa726'
//             }
//           }}
//           bezier
//           style={styles.chart}
//         />
//       )}
//     </SafeAreaView>
//   );
// }

// const styles = StyleSheet.create({
//   container: {
//     flex: 1,
//     paddingTop: 50,
//     paddingHorizontal: 16,
//     backgroundColor: '#fff',
//   },
//   title: {
//     fontSize: 22,
//     fontWeight: 'bold',
//     textAlign: 'center',
//     marginBottom: 20
//   },
//   error: {
//     color: 'red',
//     textAlign: 'center',
//     marginTop: 20
//   },
//   chart: {
//     marginVertical: 8,
//     borderRadius: 16
//   }
// });