import { useAuth } from '@clerk/clerk-expo'
import { Redirect, Stack } from 'expo-router'
import { useTheme } from '../../theme'

export default function AuthRoutesLayout() {
  const { isSignedIn } = useAuth()
  const { colors } = useTheme()
  if (isSignedIn) {
    return <Redirect href={'/'} />
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
      <Stack.Screen name="sign-in" options={{ title: 'Sign in' }} />
    </Stack>
  )
}
