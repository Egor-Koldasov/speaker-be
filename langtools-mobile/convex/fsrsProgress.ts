import { asyncMap } from 'convex-helpers'
import { getManyFrom } from 'convex-helpers/server/relationships'
import { convexToZod } from 'convex-helpers/server/zod'
import z from 'zod/v3'
import { matchDictionaryEntryLanguage } from '../src/utils/dictionary/matchDictionaryEntryLanguage'
import { isNonNullable } from '../src/utils/isNonNullable'
import { api, internal } from './_generated/api'
import { Doc } from './_generated/dataModel'
import schema from './schema'
import { NextFsrsItemWithExtra } from './types/NextFsrsItemWithTranslations'
import { RegisteredQueryReturnType } from './types/utils/RegisteredQueryReturnType'
import { requireUserByActionCtx, requireUserByCtx } from './users'
import { action } from './utils/action'
import { internalMutation } from './utils/internalMutation'
import { internalQuery } from './utils/internalQuery'
import { mutation } from './utils/mutation'
import { query } from './utils/query'
import { requireById } from './utils/requireById'
import { processReviewApiResponseSchema } from './utils/schema/fsrsApiItemSchema'
import {
  FsrsProgressState,
  fsrsProgressStateSchema,
} from './utils/schema/FsrsProgressState'
import { zid } from './utils/schema/zid'
import { getVocabularyAwareSentecesBySenseId } from './vocabularyAwareSentence'

export const getFsrsProgressList = query({
  args: {
    sourceLanguage: z.string().optional(),
  },
  async handler(ctx, args) {
    const user = await requireUserByCtx(ctx)
    const fsrsProgressList = await getManyFrom(
      ctx.db,
      'fsrsProgress',
      'byUserIdSenseId',
      user._id,
      'userId',
    )
    const fsrsProgressListLoaded = await asyncMap(
      fsrsProgressList,
      async (fsrsProgress) => {
        const sense = await requireById(ctx.db, fsrsProgress.senseId)

        const dictionaryEntry = await requireById(
          ctx.db,
          sense.dictionaryEntryId,
        )

        return {
          fsrsProgress,
          sense,
          dictionaryEntry,
        }
      },
    )

    const { sourceLanguage } = args

    const fsrsProgressListLoadedFiltered = !sourceLanguage
      ? fsrsProgressListLoaded
      : fsrsProgressListLoaded.filter((fsrsProgress) =>
          matchDictionaryEntryLanguage(
            fsrsProgress.dictionaryEntry,
            sourceLanguage,
          ),
        )

    return fsrsProgressListLoadedFiltered
  },
})

export const createFsrsProgress = mutation({
  args: {
    senseId: zid('dictionaryEntrySenses'),
  },
  handler: async (ctx, { senseId }) => {
    const user = await requireUserByCtx(ctx)
    const sense = await requireById(ctx.db, senseId)
    const dictionaryEntry = await requireById(ctx.db, sense.dictionaryEntryId)
    if (dictionaryEntry.userId !== user._id) {
      throw new Error('Sense does not belong to user')
    }
    const fsrsProgress = await ctx.db
      .query('fsrsProgress')
      .withIndex('byUserIdSenseId', (q) =>
        q.eq('userId', user._id).eq('senseId', senseId),
      )
      .unique()
    if (fsrsProgress) {
      throw new Error('FSRS progress already exists')
    }
    const fsrsProgressId = await ctx.db.insert('fsrsProgress', {
      due: new Date().toISOString(),
      state: 1,
      step: 0,
      reps: 0,
      lapses: 0,
      userId: user._id,
      senseId,
    })
    return { fsrsProgressId }
  },
})

export const getNextFsrsItems = query({
  args: {
    limit: z.number(),
    sourceLanguage: z.string().optional(),
  },
  handler: async (ctx, { limit, sourceLanguage }) => {
    const user = await requireUserByCtx(ctx)
    const fsrsProgressList = await ctx.db
      .query('fsrsProgress')
      .withIndex('byUserIdDue', (q) => q.eq('userId', user._id))
      .order('asc')
      .collect()
    const fsrsProgressListLoaded = (
      await asyncMap(fsrsProgressList, async (fsrsProgress) => {
        const sense = await requireById(ctx.db, fsrsProgress.senseId)
        const dictionaryEntry = await requireById(
          ctx.db,
          sense.dictionaryEntryId,
        )
        if (
          !!sourceLanguage &&
          !matchDictionaryEntryLanguage(dictionaryEntry, sourceLanguage)
            .isMatching
        ) {
          return null
        }
        return { fsrsProgress, sense, dictionaryEntry }
      })
    )
      .filter(isNonNullable)
      .slice(0, limit)
    return fsrsProgressListLoaded
  },
})

export type NextFsrsItem = Awaited<
  RegisteredQueryReturnType<typeof getNextFsrsItems>
>[number]

export const getNextFsrsItemWithExtra = query({
  args: {
    limit: z.number(),
    sourceLanguage: z.string().optional(),
  },
  handler: async (
    ctx,
    { limit, sourceLanguage },
  ): Promise<NextFsrsItemWithExtra[]> => {
    await requireUserByCtx(ctx)
    const nextFsrsItems = await ctx.runQuery(
      api.fsrsProgress.getNextFsrsItems,
      {
        limit,
        sourceLanguage,
      },
    )
    const nextFsrsItemsWithExtra = await asyncMap(
      nextFsrsItems,
      async (nextFsrsItem) => {
        const senseTranslations = await ctx.db
          .query('dictionaryEntrySenseTranslation')
          .withIndex('byDictionaryEntrySenseId', (q) =>
            q.eq('dictionaryEntrySenseId', nextFsrsItem.sense._id),
          )
          .collect()
        const { vocabularyAwareSentences } =
          await getVocabularyAwareSentecesBySenseId(ctx, {
            dictionaryEntrySenseId: nextFsrsItem.sense._id,
          })
        return {
          ...nextFsrsItem,
          senseTranslations,
          vocabularyAwareSentences,
        }
      },
    )
    return nextFsrsItemsWithExtra
  },
})

export const getFsrsProgressById = internalQuery({
  args: {
    fsrsProgressId: zid('fsrsProgress'),
  },
  handler: async (ctx, { fsrsProgressId }) => {
    return await ctx.db.get(fsrsProgressId)
  },
})

export const updateFsrsProgress = internalMutation({
  args: {
    fsrsProgressId: zid('fsrsProgress'),
    fsrsProgress: convexToZod(schema.tables.fsrsProgress.validator).partial(),
  },
  handler: async (ctx, { fsrsProgressId, fsrsProgress }) => {
    await ctx.db.patch(fsrsProgressId, fsrsProgress)
  },
})

export const processReview = action({
  args: {
    fsrsProgressId: zid('fsrsProgress'),
    rating: z.number(),
  },
  handler: async (
    ctx,
    { fsrsProgressId, rating },
  ): Promise<Doc<'fsrsProgress'>> => {
    const user = await requireUserByActionCtx(ctx)
    const fsrsProgress = await ctx.runQuery(
      internal.fsrsProgress.getFsrsProgressById,
      {
        fsrsProgressId,
      },
    )
    if (!fsrsProgress) {
      throw new Error('FSRS progress not found')
    }
    if (fsrsProgress.userId !== user._id) {
      throw new Error('FSRS progress does not belong to user')
    }

    const fsrsApiUrl = new URL(process.env.FSRS_API_URL ?? '')
    fsrsApiUrl.pathname = `/fsrs/process_review`

    const response = await fetch(fsrsApiUrl.toString(), {
      headers: {
        'Content-Type': 'application/json',
      },
      method: 'POST',
      body: JSON.stringify({
        fsrs: {
          due: fsrsProgress.due,
          stability: fsrsProgress.stability ?? null,
          difficulty: fsrsProgress.difficulty ?? null,
          state: fsrsProgress.state,
          step: fsrsProgress.step,
          last_review: fsrsProgress.last_review ?? null,
          reps: fsrsProgress.reps,
          lapses: fsrsProgress.lapses,
        },
        rating,
        review_time: new Date().toISOString(),
      }),
    })

    if (!response.ok) {
      console.error('processReview request error', await response.text())
      throw new Error('Failed to process review')
    }

    const processReviewApiResponse = processReviewApiResponseSchema.parse(
      await response.json(),
    )

    await ctx.runMutation(internal.fsrsProgress.updateFsrsProgress, {
      fsrsProgressId,
      fsrsProgress: {
        ...processReviewApiResponse.updated_training_data,
        stability:
          processReviewApiResponse.updated_training_data.stability ?? undefined,
        difficulty:
          processReviewApiResponse.updated_training_data.difficulty ??
          undefined,
        last_review:
          processReviewApiResponse.updated_training_data.last_review ??
          undefined,
      },
    })
    const nextFsrsProgress = await ctx.runQuery(
      internal.fsrsProgress.getFsrsProgressById,
      {
        fsrsProgressId,
      },
    )
    if (!nextFsrsProgress) {
      throw new Error('FSRS progress not found')
    }
    return nextFsrsProgress
  },
})

type FsrsProgressStateToCount = Record<FsrsProgressState, number>
type FsrsDueStats = {
  fsrsProgressStateToCount: FsrsProgressStateToCount
}

export const getFsrsDueStats = query({
  args: {
    sourceLanguage: z.string().optional(),
  },
  handler: async (ctx, { sourceLanguage }) => {
    const user = await requireUserByCtx(ctx)
    const fsrsProgressList = await ctx.db
      .query('fsrsProgress')
      .withIndex('byUserIdDue', (q) => q.eq('userId', user._id))
      .order('asc')
      .collect()

    const fsrsDueStats: FsrsDueStats = {
      fsrsProgressStateToCount: {
        [FsrsProgressState.Learning]: 0,
        [FsrsProgressState.Review]: 0,
        [FsrsProgressState.Relearning]: 0,
      },
    }
    for (const fsrsProgress of fsrsProgressList) {
      const sense = await requireById(ctx.db, fsrsProgress.senseId)
      const dictionaryEntry = await requireById(ctx.db, sense.dictionaryEntryId)
      if (
        !!sourceLanguage &&
        !matchDictionaryEntryLanguage(dictionaryEntry, sourceLanguage)
          .isMatching
      ) {
        continue
      }
      const fsrsProgressState = fsrsProgressStateSchema.parse(
        fsrsProgress.state,
      )
      fsrsDueStats.fsrsProgressStateToCount[fsrsProgressState]++
    }
    return fsrsDueStats
  },
})
