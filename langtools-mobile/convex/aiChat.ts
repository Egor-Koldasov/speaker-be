import {
  createThread as createThreadFunction,
  getThreadMetadata,
  listMessages,
  syncStreams,
  ThreadDoc,
  vStreamArgs,
} from '@convex-dev/agent'
import { PersistentTextStreaming } from '@convex-dev/persistent-text-streaming'
import { paginationOptsValidator } from 'convex/server'
import { v } from 'convex/values'
import { api, components } from './_generated/api'
import { action, mutation, query } from './_generated/server'
import { agent } from './ai/agent'
import { TransactionCtx } from './types/TransactionCtx'
import { requireUserByCtx } from './users'

const persistentTextStreaming = new PersistentTextStreaming(
  components.persistentTextStreaming,
)

export const createThread = mutation({
  args: {},
  handler: async (ctx) => {
    const user = await requireUserByCtx(ctx)
    const threadId = await createThreadFunction(ctx, components.agent, {
      userId: user._id,
    })

    const streamId = await persistentTextStreaming.createStream(ctx)
    await ctx.db.insert('aiMessageStream', {
      threadId,
      streamId,
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
    await ctx.runQuery(api.aiChat.getExistingThread, {
      threadId: args.threadId,
    })
    await agent.streamText(
      ctx,
      { threadId: args.threadId },
      { prompt: args.message },
      { saveStreamDeltas: { throttleMs: 100 } },
    )
  },
})

// export const streamMessage = httpAction(async (ctx, request) => {
//   const body = (await request.json()) as { streamId: string }
//   await agent.streamText(
//     ctx,
//     { threadId: args.threadId },
//     { prompt: args.message },
//     { saveStreamDeltas: { throttleMs: 100 } },
//   )
// })

export const listThreads = query({
  args: {},
  handler: async (ctx) => {
    const user = await requireUserByCtx(ctx)
    const result = await ctx.runQuery(
      components.agent.threads.listThreadsByUserId,
      {
        userId: user._id,
        order: 'desc',
        paginationOpts: { numItems: 50, cursor: null },
      },
    )
    return result.page
  },
})

export const listThreadMessages = query({
  args: {
    threadId: v.string(),
    streamArgs: vStreamArgs,
    paginationOpts: paginationOptsValidator,
  },
  handler: async (ctx, args) => {
    await requireThread(ctx, args.threadId)
    const streams = await syncStreams(ctx, components.agent, args)
    const paginated = await listMessages(ctx, components.agent, args)
    return { ...paginated, streams }
  },
})

export type AuthorizedThreadDoc = ThreadDoc & { userId: string }

const isAuthorizedThread = (
  thread: ThreadDoc,
): thread is AuthorizedThreadDoc => {
  return !!thread.userId
}

export const requireThread = async (ctx: TransactionCtx, threadId: string) => {
  const user = await requireUserByCtx(ctx)
  const thread = await getThreadMetadata(ctx, components.agent, {
    threadId,
  })
  if (!isAuthorizedThread(thread) || thread.userId !== user._id) {
    console.error('Access denied to thread', threadId)
    throw new Error('Thread not found')
  }
  return thread
}

export const getExistingThread = query({
  args: { threadId: v.string() },
  handler: async (ctx, { threadId }) => {
    const thread = await requireThread(ctx, threadId)
    return thread
  },
})
