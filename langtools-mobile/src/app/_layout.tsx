import { ClerkProvider, useAuth } from '@clerk/clerk-expo'
import { tokenCache } from '@clerk/clerk-expo/token-cache'
import { ConvexQueryCacheProvider } from 'convex-helpers/react/cache'
import { ConvexReactClient, useQuery } from 'convex/react'
import { ConvexProviderWithClerk } from 'convex/react-clerk'
import { useFonts } from 'expo-font'
import { Stack, useRouter, useSegments } from 'expo-router'
import * as SplashScreen from 'expo-splash-screen'
import { useEffect } from 'react'
import { api } from '../../convex/_generated/api'
import { headerScreenOptions } from '../components/styles/headerScreenOptions'
import { Loading } from '../components/ui/Loading'
import { ThemeProvider, useTheme } from '../theme/index'
import { useMutationSerial } from '../utils/convex/useMutationSerial'

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
        <ConvexQueryCacheProvider>
          <ThemeProvider>
            <NavigationGuard />
          </ThemeProvider>
        </ConvexQueryCacheProvider>
      </ConvexProviderWithClerk>
    </ClerkProvider>
  )
}

function NavigationGuard() {
  const segments = useSegments()
  const router = useRouter()
  const { isLoaded, isSignedIn } = useAuth()
  const user = useQuery(api.users.getUser)
  const { mutate: syncAuthUser } = useMutationSerial(api.users.syncAuthUser)
  const { colors } = useTheme()

  useEffect(() => {
    if (!isLoaded) return

    const inAuthGroup = segments[0] === '(auth)'

    if (!isSignedIn && !inAuthGroup) {
      router.replace('/sign-in')
    }
  }, [segments, isLoaded, isSignedIn, router])

  useEffect(() => {
    if (isSignedIn && user === null) {
      syncAuthUser({})
    }
  }, [isSignedIn, syncAuthUser, user])

  // useLogConvexAuthToken()

  if (!isLoaded) {
    return <Loading />
  }

  return (
    <Stack screenOptions={headerScreenOptions({ colors: colors })}>
      <Stack.Screen name="(auth)" options={{ headerShown: false }} />
      <Stack.Screen name="(main-tabs)" options={{ headerShown: false }} />
    </Stack>
  )
}
