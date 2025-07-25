import React from 'react';
import { View, ActivityIndicator } from 'react-native';
import { Redirect } from 'expo-router';
import { useConvexAuth } from 'convex/react';

export default function IndexScreen(): JSX.Element {
  const { isLoading, isAuthenticated } = useConvexAuth();

  // Monitor auth state changes for debugging

  // Show loading spinner while checking authentication
  if (isLoading) {
    // Showing loading spinner while checking auth state
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size="large" color="#007AFF" />
      </View>
    );
  }

  // Redirect based on authentication state
  if (isAuthenticated) {
    // User is authenticated, redirecting to main app
    return <Redirect href="/(tabs)" />;
  } else {
    // User is not authenticated, redirecting to login
    return <Redirect href="/(auth)/login" />;
  }
}