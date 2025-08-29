import { useAuth, useUser } from '@clerk/clerk-expo'
import { useQuery } from 'convex/react'
import { useEffect } from 'react'
import { Text, View } from 'react-native'
import { api } from '../../convex/_generated/api'

export default function UserProfile() {
  const userProfile = useQuery(api.users.getUserProfile)
  const { user } = useUser()
  const { getToken } = useAuth()

  useEffect(() => {
    ;(async () => {
      const token = await getToken({ template: 'convex' })
      console.log(token)
    })()
  }, [])

  return (
    <View>
      <Text>{userProfile?.email}</Text>
      <Text>{user?.emailAddresses[0].emailAddress}</Text>
    </View>
  )
}
