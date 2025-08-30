import { ClerkProvider, useAuth } from '@clerk/clerk-expo'
import { tokenCache } from '@clerk/clerk-expo/token-cache'
import { ConvexReactClient } from 'convex/react'
import { ConvexProviderWithClerk } from 'convex/react-clerk'
import { useFonts } from 'expo-font'
import { Stack, useRouter, useSegments } from 'expo-router'
import * as SplashScreen from 'expo-splash-screen'
import { StatusBar } from 'expo-status-bar'
import { useEffect } from 'react'
import { Loading } from '../components/ui/Loading'
import { ThemeProvider, useTheme } from '../theme/index'

// Prevent the splash screen from auto-hiding before asset loading is complete.
SplashScreen.preventAutoHideAsync()

const convex = new ConvexReactClient(process.env.EXPO_PUBLIC_CONVEX_URL!, {
  unsavedChangesWarning: false,
})

export default function RootLayout() {
  const [loaded] = useFonts({
    SpaceMono: require('../assets/fonts/SpaceMono-Regular.ttf'),
  })

  useEffect(() => {
    if (loaded) {
      SplashScreen.hideAsync()
    }
  }, [loaded])

  if (!loaded) {
    return null
  }

  const publishableKey = process.env.EXPO_PUBLIC_CLERK_PUBLISHABLE_KEY!

  if (!publishableKey) {
    throw new Error(
      'Missing Publishable Key. Please set EXPO_PUBLIC_CLERK_PUBLISHABLE_KEY in your .env',
    )
  }

  return (
    <ClerkProvider publishableKey={publishableKey} tokenCache={tokenCache}>
      <ConvexProviderWithClerk client={convex} useAuth={useAuth}>
        <ThemeProvider>
          <NavigationGuard />
          <StatusBar style="light" />
        </ThemeProvider>
      </ConvexProviderWithClerk>
    </ClerkProvider>
  )
}

function NavigationGuard() {
  const segments = useSegments()
  const router = useRouter()
  const { isLoaded, isSignedIn } = useAuth()
  const { colors } = useTheme()

  useEffect(() => {
    if (!isLoaded) return

    const inAuthGroup = segments[0] === '(auth)'

    if (!isSignedIn && !inAuthGroup) {
      router.replace('/sign-in')
    }
  }, [segments, isLoaded, isSignedIn, router])

  if (!isLoaded) {
    return <Loading />
  }

  return (
    <Stack
      screenOptions={{
        headerStyle: { backgroundColor: colors.surface },
        headerTitleStyle: { color: colors.textPrimary },
        headerTintColor: colors.accent,
        contentStyle: { backgroundColor: colors.background },
      }}
    >
      <Stack.Screen name="(main-tabs)" options={{ title: 'Langtools' }} />
    </Stack>
  )
}
