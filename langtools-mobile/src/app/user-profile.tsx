import { useAuth } from '@clerk/clerk-expo'
import { useQuery } from 'convex/react'
import { Text, TouchableOpacity, View } from 'react-native'
import { api } from '../../convex/_generated/api'

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
