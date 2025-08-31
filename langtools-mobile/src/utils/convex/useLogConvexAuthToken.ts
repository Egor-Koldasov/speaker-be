import { useAuth } from '@clerk/clerk-expo'
import { useEffect } from 'react'

export const useLogConvexAuthToken = () => {
  const { getToken } = useAuth()
  useEffect(() => {
    ;(async () => {
      console.log(
        'Convex token',
        await getToken({
          template: 'convex',
          skipCache: true,
        }),
      )
    })()
  }, [])
}
