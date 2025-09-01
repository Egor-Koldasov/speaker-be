import { createThread as createThreadFunction } from '@convex-dev/agent'
import { v } from 'convex/values'
import { components } from './_generated/api'
import { action, mutation } from './_generated/server'
import { agent } from './ai/agent'
import { requireUserByCtx } from './users'

export const createThread = mutation({
  args: {},
  handler: async (ctx) => {
    const user = await requireUserByCtx(ctx)
    const threadId = await createThreadFunction(ctx, components.agent, {
      userId: user._id,
    })
    return threadId
  },
})

export const sendRegularMessage = action({
  args: {
    threadId: v.string(),
    message: v.string(),
  },
  handler: async (ctx, args) => {
    await agent.generateText(
      ctx,
      { threadId: args.threadId },
      { prompt: args.message },
    )
  },
})
