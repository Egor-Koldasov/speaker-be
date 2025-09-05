import { z } from 'zod/v3'

export const zStreamCursor = z.object({
  streamId: z.string(),
  cursor: z.number(),
})

export const zStreamArgs = z
  .union([
    z.object({ kind: z.literal('list'), startOrder: z.number().optional() }),
    z.object({ kind: z.literal('deltas'), cursors: z.array(zStreamCursor) }),
  ])
  .optional()
