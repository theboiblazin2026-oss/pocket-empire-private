---
name: React Native
description: Components, navigation, native modules, Expo
---

# React Native Skill

## Components

```jsx
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';

export default function MyComponent({ onPress }) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Hello</Text>
      <TouchableOpacity onPress={onPress}>
        <Text>Press Me</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  title: { fontSize: 24, fontWeight: 'bold' },
});
```

## Navigation

```jsx
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

const Stack = createStackNavigator();

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Details" component={DetailsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

// Navigate
navigation.navigate('Details', { id: 123 });
```

## Expo CLI

```bash
npx create-expo-app myapp
cd myapp
npx expo start
```

## When to Apply
Use when building cross-platform mobile apps with React Native.
