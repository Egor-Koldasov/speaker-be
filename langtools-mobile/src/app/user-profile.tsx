import { useUser } from '@clerk/clerk-expo'
import { Text, View } from 'react-native'

export default function UserProfile() {
  const { user } = useUser()

  if (!user) {
    return null
  }

  return (
    <View>
      <Text>{user.emailAddresses[0].emailAddress}</Text>
    </View>
  )
}
