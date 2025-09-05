import { useAction as useActionConvex } from 'convex/react'
import { FunctionReference } from 'convex/server'
import { useCallback, useState } from 'react'

export const useAction = <Action extends FunctionReference<'action'>>(
  actionFn: Action,
) => {
  const [isPending, setIsPending] = useState(false)
  const action = useActionConvex(actionFn)
  const exec = useCallback(
    async (...args: Parameters<typeof action>) => {
      setIsPending(true)
      const result = await action(...args)
      setIsPending(false)
      return result
    },
    [action],
  )
  return { exec, isPending }
}
