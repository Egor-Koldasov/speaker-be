import { FunctionReference } from 'convex/server'
import { useCallback } from 'react'
import { useMutation } from './useMutation'

export const useMutationSerial = <
  Mutation extends FunctionReference<'mutation'>,
>(
  mutationFn: Mutation,
) => {
  const { mutate, isPending } = useMutation(mutationFn)
  const mutateSerial = useCallback(
    (...args: Parameters<typeof mutate>) => {
      if (isPending) {
        return
      }
      mutate(...args)
    },
    [isPending, mutate],
  )
  return { mutate: mutateSerial, isPending }
}
