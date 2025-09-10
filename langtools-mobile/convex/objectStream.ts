import z from 'zod/v3'
import { requireUserByCtx } from './users'
import { internalMutation } from './utils/internalMutation'
import { mutation } from './utils/mutation'
import { query } from './utils/query'
import { requireById } from './utils/requireById'
import { zid } from './utils/schema/zid'

export const createObjectStream = mutation({
  args: {},
  handler: async (ctx) => {
    const user = await requireUserByCtx(ctx)
    const id = await ctx.db.insert('objectStream', {
      jsonStringSoFar: '',
      userId: user._id,
    })

    return id
  },
})

export const updateObjectStream = internalMutation({
  args: {
    id: zid('objectStream'),
    jsonStringSoFar: z.string(),
  },
  handler: async (ctx, { jsonStringSoFar, id }) => {
    const user = await requireUserByCtx(ctx)
    const objectStream = await requireById(ctx.db, id)
    if (objectStream.userId !== user._id) {
      throw new Error('Object stream not found')
    }
    await ctx.db.patch(id, {
      jsonStringSoFar,
      updatedAt: new Date().toISOString(),
    })

    return id
  },
})

export const getObjectStream = query({
  args: {
    id: zid('objectStream'),
  },
  handler: async (ctx, { id }) => {
    return await ctx.db.get(id)
  },
})
