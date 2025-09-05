import { useMutation as useMutationConvex } from 'convex/react'
import { FunctionReference } from 'convex/server'
import { useCallback, useState } from 'react'

export const useMutation = <Mutation extends FunctionReference<'mutation'>>(
  mutationFn: Mutation,
) => {
  const [isPending, setIsPending] = useState(false)
  const mutation = useMutationConvex(mutationFn)
  const mutate = useCallback(
    async (...args: Parameters<typeof mutation>) => {
      setIsPending(true)
      const result = await mutation(...args)
      setIsPending(false)
      return result
    },
    [mutation],
  )
  return { mutate, isPending }
}
