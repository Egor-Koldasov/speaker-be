import { StreamObjectResult } from 'ai'
import { throttleAsync } from '../../../src/utils/data/throttle'
import { internal } from '../../_generated/api'
import { Id } from '../../_generated/dataModel'
import { ActionCtx } from '../../_generated/server'

export type ProcessObjectStreamOpts = {
  ctx: ActionCtx
  objectStreamId: Id<'objectStream'>
  stream: StreamObjectResult<unknown, unknown, unknown>
}

export const processObjectStream = async (opts: ProcessObjectStreamOpts) => {
  const { ctx, stream, objectStreamId } = opts

  let jsonStringSoFar = ''

  const updateDbThrottle = throttleAsync(async (jsonStringSoFarArg: string) => {
    await ctx.runMutation(internal.objectStream.updateObjectStream, {
      id: objectStreamId,
      jsonStringSoFar: jsonStringSoFarArg,
    })
  }, 1000)

  for await (const part of stream.textStream) {
    jsonStringSoFar += part
    await updateDbThrottle(jsonStringSoFar)
  }

  return {}
}
