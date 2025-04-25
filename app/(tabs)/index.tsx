import { Image, StyleSheet, Platform } from 'react-native';

import { HelloWave } from '@/components/HelloWave';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';

export default function HomeScreen() {
  return (
    <ParallaxScrollView
    headerBackgroundColor={{ light: '#F72585', dark: '#7209B7' }} // hot pink to purple
    headerImage={
      <Image
        source={require('@/assets/images/partial-react-logo.png')}
        style={styles.reactLogo}
      />  
      }>
      <ThemedView style={styles.titleContainer}>
        <ThemedText type="title" style={styles.headingText}>
          Welcome to BackTalk
        </ThemedText>
      </ThemedView>

      <ThemedView style={styles.subheadingContainer}>
        <ThemedText type="subtitle" style={styles.subheadingText}>
          Your Posture, Monitored
        </ThemedText>
      </ThemedView>

      {/* Optional: keep or remove the guide steps below */}
      <ThemedView style={styles.stepContainer}>
  <ThemedText type="subtitle">How To Use</ThemedText>
  <ThemedText>
    Navigate to the sensor pages using the tabs.
  </ThemedText>
</ThemedView>
    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  titleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 4,
  },
  subheadingContainer: {
    marginBottom: 20,
    paddingHorizontal: 12,
  },
  headingText: {
    color: '#ff69b4', // brighter blush pink
  },
  subheadingText: {
    color: '#ffb6c1', // light pink
    fontSize: 18,
    fontStyle: 'italic',
  },
  stepContainer: {
    gap: 8,
    marginBottom: 8,
  },
  reactLogo: {
    height: 178,
    width: 290,
    bottom: 0,
    left: 0,
    position: 'absolute',
  },
});
