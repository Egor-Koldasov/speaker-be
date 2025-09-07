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
          leewayInSeconds: 60 * 60 * 24 * 30 * 12, // 12 months
        }),
      )
    })()
  }, [])
}
