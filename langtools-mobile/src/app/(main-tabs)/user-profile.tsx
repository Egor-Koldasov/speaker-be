import { useAuth } from '@clerk/clerk-expo'
import { api } from '@convex/_generated/api'
import { useQuery } from 'convex/react'
import { Button } from '../../components/ui/Button'
import { Loading } from '../../components/ui/Loading'
import { Screen } from '../../components/ui/Screen'
import { Text } from '../../components/ui/Text'
import { View as ThemedView } from '../../components/ui/View'
import { useTheme } from '../../theme/index'

export default function UserProfile() {
  const { signOut } = useAuth()
  const userProfile = useQuery(api.users.getUserProfile)

  const { spacing } = useTheme()
  return (
    <Screen>
      {!userProfile ? (
        <Loading />
      ) : (
        <ThemedView
          background="elevated"
          rounded="lg"
          padded
          style={{ gap: spacing.md }}
        >
          <Text variant="title">Profile</Text>
          <Text color="secondary">{userProfile?.email ?? '—'}</Text>
          <Button title="Log out" onPress={() => signOut()} />
        </ThemedView>
      )}
    </Screen>
  )
}
