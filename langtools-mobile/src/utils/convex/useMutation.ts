import { useMutation as useMutationConvex } from 'convex/react'
import { FunctionReference } from 'convex/server'
import { useCallback, useTransition } from 'react'

export const useMutation = <Mutation extends FunctionReference<'mutation'>>(
  mutationFn: Mutation,
) => {
  const [isPending, startTransition] = useTransition()
  const mutation = useMutationConvex(mutationFn)
  const mutate = useCallback(
    (...args: Parameters<typeof mutation>) => {
      startTransition(() => {
        mutation(...args)
      })
    },
    [mutation],
  )
  return { mutate, isPending }
}
