import { asyncMap } from 'convex-helpers'
import { getManyFrom } from 'convex-helpers/server/relationships'
import z from 'zod/v3'
import { matchDictionaryEntryLanguage } from '../src/utils/dictionary/matchDictionaryEntryLanguage'
import { isNonNullable } from '../src/utils/isNonNullable'
import { internal } from './_generated/api'
import { requireUserByActionCtx, requireUserByCtx } from './users'
import { action } from './utils/action'
import { internalQuery } from './utils/internalQuery'
import { mutation } from './utils/mutation'
import { query } from './utils/query'
import { requireById } from './utils/requireById'
import { zid } from './utils/schema/zid'

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

export const getFsrsProgressById = internalQuery({
  args: {
    fsrsProgressId: zid('fsrsProgress'),
  },
  handler: async (ctx, { fsrsProgressId }) => {
    return await ctx.db.get(fsrsProgressId)
  },
})

export const processReview = action({
  args: {
    fsrsProgressId: zid('fsrsProgress'),
    rating: z.number(),
  },
  handler: async (ctx, { fsrsProgressId, rating }) => {
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

    console.log('processReview response', response)
  },
})
