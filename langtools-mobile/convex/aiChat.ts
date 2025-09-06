import {
  createThread as createThreadFunction,
  getThreadMetadata,
  listMessages,
  syncStreams,
  ThreadDoc,
} from '@convex-dev/agent'
import { parsePartialJson } from 'ai'
import { convexToZod } from 'convex-helpers/server/zod'
import { paginationOptsValidator } from 'convex/server'
import { v } from 'convex/values'
import { z } from 'zod/v3'
import { throttleAsync } from '../src/utils/data/throttle'
import { api, components, internal } from './_generated/api'
import { action } from './_generated/server'
import { agent } from './ai/agent'
import { PromptParameter } from './types/PromptParameter'
import { TransactionCtx } from './types/TransactionCtx'
import { requireUserByCtx } from './users'
import { internalMutation } from './utils/internalMutation'
import { mutation } from './utils/mutation'
import { query } from './utils/query'
import {
  aiDictionaryEntrySchema,
  AiDictionaryEntryStream,
  aiDictionaryEntryStreamSchema,
} from './utils/schema/aiDictionaryEntrySchema'
import { zStreamArgs } from './utils/zStreamArgs'

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
    await ctx.runQuery(api.aiChat.getExistingThread, {
      threadId: args.threadId,
    })
    await agent.streamText(
      ctx,
      { threadId: args.threadId },
      {
        prompt: args.message,
      },
      { saveStreamDeltas: { throttleMs: 100 } },
    )

    // for await (const part of stream.fullStream) {
    //   console.log(part)
    // }
  },
})

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

export const getDictionaryEntry = query({
  args: {
    threadId: z.string(),
    streamArgs: zStreamArgs,
  },
  handler: async (ctx, { threadId, streamArgs }) => {
    await requireThread(ctx, threadId)
    const streams = await syncStreams(ctx, components.agent, {
      streamArgs,
      threadId,
    })
    return { streams }
  },
})

export const listThreadMessages = query({
  args: {
    threadId: z.string(),
    streamArgs: zStreamArgs,
    paginationOpts: convexToZod(paginationOptsValidator),
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
  return { thread, userId: user._id }
}

export const getExistingThread = query({
  args: { threadId: z.string() },
  handler: async (ctx, { threadId }) => {
    const thread = await requireThread(ctx, threadId)
    return thread
  },
})

export const generateDictionaryEntry = action({
  args: {
    headword: v.string(),
    forceLanguage: v.optional(v.string()),
    threadId: v.string(),
  },
  async handler(ctx, { headword, forceLanguage, threadId }) {
    const thread = await ctx.runQuery(api.aiChat.getExistingThread, {
      threadId,
    })
    const prompt = `
You are a professional linguist and lexicographer tasked with writing a comprehensive
dictionary entry in the original language of the provided term.
All JSON values should be in original language.

You will be given a set of input parameters.

Focus on:

- Detecting the correct source language based on the term and user preferences
- Including all senses known ordered from most to least common
- Writing detailed definitions that reflect each sense and their distinctions
`
    const parameters: PromptParameter[] = [
      {
        name: 'headword',
        description: 'A word or phrase to define',
        value: headword,
      },
      {
        name: 'forceLanguage',
        description: 'The language to force the definition to be in',
        value: forceLanguage ?? '',
      },
    ].filter((p) => !!p.value)

    // const { messages } = await saveMessages(ctx, components.agent, {
    //   threadId,
    //   userId: user._id,
    //   messages: [
    //     {
    //       role: 'system',
    //       content: prompt,
    //     },
    //     {
    //       role: 'user',
    //       content: JSON.stringify(parameters, null, 2),
    //     },
    //   ],
    // })
    const stream = await agent.streamObject(
      ctx,
      { threadId },
      {
        messages: [
          {
            role: 'system',
            content: prompt,
          },
          {
            role: 'user',
            content: JSON.stringify(parameters, null, 2),
          },
        ],
        schema: aiDictionaryEntrySchema,
      },
    )

    let jsonStringSoFar = ''

    const updateDbThrottle = throttleAsync(
      async (aiDictionaryEntryStream: AiDictionaryEntryStream) => {
        await ctx.runMutation(internal.aiChat.updateAiDictionaryEntryStream, {
          threadId,
          aiDictionaryEntryStream,
        })
      },
      1000,
    )

    for await (const part of stream.textStream) {
      jsonStringSoFar += part
      const partialObject = await parsePartialJson(jsonStringSoFar)
      const validationResult = aiDictionaryEntryStreamSchema.safeParse(
        partialObject.value,
      )
      if (validationResult.success) {
        await updateDbThrottle(validationResult.data)
      }
    }
    const aiDictionaryEntry = await stream.object

    await ctx.runMutation(internal.dictionary.createDictionaryEntry, {
      userId: thread.userId,
      aiDictionaryEntry,
    })

    await ctx.runMutation(internal.aiChat.finishAiDictionaryEntryStream, {
      threadId,
    })
  },
})

export const updateAiDictionaryEntryStream = internalMutation({
  args: {
    threadId: z.string(),
    aiDictionaryEntryStream: aiDictionaryEntryStreamSchema,
  },
  handler: async (ctx, { aiDictionaryEntryStream, threadId }) => {
    const dbRow = await ctx.db
      .query('aiDictionaryEntryStream')
      .withIndex('byThreadIdFinishedAt', (q) =>
        q.eq('threadId', threadId).eq('finishedAt', undefined),
      )
      .unique()

    let id = dbRow?._id

    if (!id) {
      id = await ctx.db.insert('aiDictionaryEntryStream', {
        ...aiDictionaryEntryStream,
        threadId,
      })
    }

    await ctx.db.patch(id, {
      ...aiDictionaryEntryStream,
      updatedAt: new Date().toISOString(),
    })
  },
})

export const finishAiDictionaryEntryStream = internalMutation({
  args: { threadId: z.string() },
  handler: async (ctx, { threadId }) => {
    const dbRow = await ctx.db
      .query('aiDictionaryEntryStream')
      .withIndex('byThreadIdFinishedAt', (q) =>
        q.eq('threadId', threadId).eq('finishedAt', undefined),
      )
      .unique()
    if (!dbRow) {
      throw new Error('AiDictionaryEntryStream not found')
    }
    await ctx.db.patch(dbRow._id, { finishedAt: new Date().toISOString() })
  },
})

export const getAiDictionaryEntryStream = query({
  args: { threadId: z.string() },
  handler: async (ctx, { threadId }) => {
    const dbRow = await ctx.db
      .query('aiDictionaryEntryStream')
      .withIndex('byThreadIdFinishedAt', (q) =>
        q.eq('threadId', threadId).eq('finishedAt', undefined),
      )
      .unique()
    return dbRow
  },
})
