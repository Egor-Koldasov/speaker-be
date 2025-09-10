import { parsePartialJson } from 'ai'
import { useQuery } from 'convex/react'
import { useCallback, useEffect, useMemo, useState } from 'react'
import z, { ZodObject, ZodRawShape } from 'zod/v3'
import { api } from '../../../convex/_generated/api'
import { Id } from '../../../convex/_generated/dataModel'

export const useObjectStream = <PartialSchema extends ZodObject<ZodRawShape>>(
  objectStreamId: Id<'objectStream'> | null,
  schema: PartialSchema,
) => {
  const objectStream = useQuery(
    api.objectStream.getObjectStream,
    !objectStreamId
      ? 'skip'
      : {
          id: objectStreamId,
        },
  )
  const [partialUnknownObject, setPartialUnknownObject] = useState<Awaited<
    ReturnType<typeof parsePartialJson>
  > | null>(null)
  const updatePartialObject = useCallback(async () => {
    if (!objectStream?.jsonStringSoFar) return null
    const partialUnknownObject_ = await parsePartialJson(
      objectStream.jsonStringSoFar,
    )
    setPartialUnknownObject(partialUnknownObject_)
    return partialUnknownObject_
  }, [objectStream])
  useEffect(() => {
    updatePartialObject()
  }, [updatePartialObject])

  const partialObject = useMemo(async () => {
    if (!partialUnknownObject?.value) {
      return { data: null, validationError: null }
    }
    const validation = schema.safeParse(partialUnknownObject.value)
    if (!validation.success) {
      console.error(
        'objectStream validation error',
        validation.error,
        partialUnknownObject.value,
      )
      return { data: null, validationError: validation.error }
    }
    return {
      data: validation.data as z.output<PartialSchema>,
      validationError: null,
    }
  }, [partialUnknownObject, schema])
  return { objectStream, partialObject }
}
