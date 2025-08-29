import { useAuth } from '@clerk/clerk-expo'
import { api } from '@convex/_generated/api'
import { useQuery } from 'convex/react'
import { Text, TouchableOpacity, View } from 'react-native'

export default function UserProfile() {
  const { signOut } = useAuth()
  const userProfile = useQuery(api.users.getUserProfile)

  return (
    <View>
      <Text>{userProfile?.email}</Text>
      <TouchableOpacity onPress={() => signOut()}>
        <Text>Log out</Text>
      </TouchableOpacity>
    </View>
  )
}
