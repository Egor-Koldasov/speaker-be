import { useAuth } from '@clerk/clerk-expo'
import { api } from '@convex/_generated/api'
import { useQuery } from 'convex/react'
import { Button } from '../../components/ui/Button'
import { Loading } from '../../components/ui/Loading'
import { Screen } from '../../components/ui/Screen'
import { Text } from '../../components/ui/Text'
import { View } from '../../components/ui/View'
import { useTheme } from '../../theme/index'
import { LearningLanguageSelector } from '../../components/settings/LearningLanguageSelector'

export default function UserProfile() {
  const { signOut } = useAuth()
  const user = useQuery(api.users.getUser)

  const { spacing } = useTheme()
  console.log('user.id', user?._id)
  return (
    <Screen style={{ gap: spacing.sm }}>
      {!user ? (
        <Loading />
      ) : (
        <>
          <View
            background="elevated"
            rounded="lg"
            padded
            style={{ gap: spacing.md }}
          >
            <Text variant="title">Profile</Text>
            <Text color="secondary">{user?.email ?? '—'}</Text>
            <Button onPress={() => signOut()}>Log out</Button>
          </View>
          <View
            background="elevated"
            rounded="lg"
            padded
            style={{ gap: spacing.md }}
          >
            <Text variant="title">Learning language</Text>
            <LearningLanguageSelector />
          </View>
        </>
      )}
    </Screen>
  )
}
