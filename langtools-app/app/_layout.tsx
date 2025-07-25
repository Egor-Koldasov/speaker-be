import { useEffect, useState } from 'react';
import { Stack } from 'expo-router';
import { useFonts } from 'expo-font';
import * as SplashScreen from 'expo-splash-screen';
import { StatusBar } from 'expo-status-bar';
import { ConvexProvider, ConvexReactClient } from 'convex/react';
import { ConvexAuthProvider } from '@convex-dev/auth/react';
import Constants from 'expo-constants';
import { Text, View } from 'react-native';
import * as SecureStore from 'expo-secure-store';

// Keep the splash screen visible while we fetch resources
SplashScreen.preventAutoHideAsync();

// Create storage adapter for Convex Auth using Expo SecureStore
const authStorage = {
  getItem: async (key: string): Promise<string | null> => {
    try {
      return await SecureStore.getItemAsync(key);
    } catch {
      return null;
    }
  },
  setItem: async (key: string, value: string): Promise<void> => {
    try {
      await SecureStore.setItemAsync(key, value);
    } catch {
      // Handle storage errors silently
    }
  },
  removeItem: async (key: string): Promise<void> => {
    try {
      await SecureStore.deleteItemAsync(key);
    } catch {
      // Handle storage errors silently
    }
  },
};

export default function RootLayout(): JSX.Element {
  const [loaded] = useFonts({
    // Add custom fonts here if needed
  });
  const [convexClient, setConvexClient] = useState<ConvexReactClient | null>(null);

  // Initialize Convex client safely in useEffect to avoid C++ bridge issues
  useEffect(() => {
    try {
      const convexUrl = Constants.expoConfig?.extra?.convexUrl || process.env.EXPO_PUBLIC_CONVEX_URL || 'http://127.0.0.1:3210';
      const client = new ConvexReactClient(convexUrl, {
        unsavedChangesWarning: false,
      });
      setConvexClient(client);
    } catch {
      // Failed to initialize Convex client - will retry on next render
    }
  }, []);

  useEffect(() => {
    if (loaded) {
      SplashScreen.hideAsync();
    }
  }, [loaded]);

  // Show loading until both fonts and Convex are ready
  if (!loaded || !convexClient) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <Text>Loading...</Text>
      </View>
    );
  }

  return (
    <ConvexProvider client={convexClient}>
      <ConvexAuthProvider client={convexClient} storage={authStorage}>
        <Stack
          screenOptions={{
            headerShown: false,
          }}
        >
          <Stack.Screen name="index" />
          <Stack.Screen name="(auth)" options={{ headerShown: false }} />
          <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        </Stack>
        <StatusBar style="auto" />
      </ConvexAuthProvider>
    </ConvexProvider>
  );
}