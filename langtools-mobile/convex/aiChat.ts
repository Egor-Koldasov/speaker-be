import {
  createThread as createThreadFunction,
  getThreadMetadata,
  listMessages,
  syncStreams,
  ThreadDoc,
  vStreamArgs,
} from '@convex-dev/agent'
import { paginationOptsValidator } from 'convex/server'
import { v } from 'convex/values'
import { z } from 'zod/v4'
import { api, components } from './_generated/api'
import { action, mutation, query } from './_generated/server'
import { agent } from './ai/agent'
import { PromptParameter } from './types/PromptParameter'
import { TransactionCtx } from './types/TransactionCtx'
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

export const generateDictionaryEntry = action({
  args: {
    headword: v.string(),
    forceLanguage: v.string(),
    threadId: v.string(),
  },
  async handler(ctx, { headword, forceLanguage, threadId }) {
    await ctx.runQuery(api.aiChat.getExistingThread, {
      threadId,
    })
    const prompt = `
You are a professional linguist and lexicographer tasked with writing a comprehensive
dictionary entry in the original language of the provided term.
All JSON values should be in original language.

You will be given a set of input parameters.

Focus on:

- Detecting the correct source language based on the term and user preferences
- Including all meanings known ordered from most to least common
- Writing detailed definitions that reflect each meaning and their distinctions
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
        value: forceLanguage,
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
        schema: z.object({
          headword: z
            .string()
            .describe(
              'Word form as users encounter it (can be inflected, variant spelling, etc.)',
            ),
          sourceLanguage: z
            .string()
            .describe(
              'Original language in BCP 47 format, guessed from word and user preferences',
            ),
          meanings: z.array(
            z.object({
              localId: z
                .string()
                .describe(
                  'Unique identifier for the meaning in format {headword}-{index} starting from 1',
                ),
              canonicalForm: z
                .string()
                .describe(
                  'Standard dictionary form - base/citation form (infinitive, nominative, etc.)',
                ),
              definition: z
                .string()
                .describe(
                  'Clear, comprehensive definition in original language',
                ),
              partOfSpeech: z
                .string()
                .describe('Part of speech in original language'),
            }),
          ),
        }),
      },
    )

    for await (const part of stream.partialObjectStream) {
      console.log(part)
    }
  },
})
