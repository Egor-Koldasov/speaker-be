import z from 'zod/v3'
import { requireUserByCtx } from './users'
import { mutation } from './utils/mutation'
import { query } from './utils/query'

export const getLearningLanguage = query({
  async handler(ctx) {
    const user = await requireUserByCtx(ctx)
    const learningLanguage = await ctx.db
      .query('learningLanguage')
      .withIndex('byUserId', (q) => q.eq('userId', user._id))
      .first()
    return learningLanguage ?? null
  },
})

export const setCurrentLearningLanguage = mutation({
  args: {
    selectedLearningLanguage: z.string(),
  },
  async handler(ctx, args) {
    const { selectedLearningLanguage } = args
    const user = await requireUserByCtx(ctx)
    const learningLanguage = await ctx.db
      .query('learningLanguage')
      .withIndex('byUserId', (q) => q.eq('userId', user._id))
      .first()
    let learningLanguageId = learningLanguage?._id
    if (!learningLanguageId) {
      learningLanguageId = await ctx.db.insert('learningLanguage', {
        userId: user._id,
        learningLanguages: [],
        selectedLearningLanguage: '',
      })
    }

    await ctx.db.patch(learningLanguageId, { selectedLearningLanguage })
  },
})
