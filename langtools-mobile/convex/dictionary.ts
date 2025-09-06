import { asyncMap } from 'convex-helpers'
import z from 'zod/v3'
import { ApiDictionaryEntry } from '../src/utils/dictionary/ApiDictionaryEntry'
import { normalizeLanguageCode } from '../src/utils/normalizeLanguageCode'
import { requireUserByCtx } from './users'
import { internalMutation } from './utils/internalMutation'
import { query } from './utils/query'
import { aiDictionaryEntrySchema } from './utils/schema/aiDictionaryEntrySchema'
import { zid } from './utils/schema/zid'

export const createDictionaryEntry = internalMutation({
  args: {
    userId: zid('users'),
    aiDictionaryEntry: aiDictionaryEntrySchema,
  },
  handler: async (ctx, { userId, aiDictionaryEntry }) => {
    const dictionaryEntryId = await ctx.db.insert('dictionaryEntries', {
      userId,
      headword: aiDictionaryEntry.headword,
      sourceLanguageFull: aiDictionaryEntry.sourceLanguage,
      sourceLanguage: normalizeLanguageCode(aiDictionaryEntry.sourceLanguage),
    })
    await asyncMap(aiDictionaryEntry.senses, async (sense) => {
      await ctx.db.insert('dictionaryEntrySenses', {
        dictionaryEntryId,
        localId: sense.localId,
        canonicalForm: sense.canonicalForm,
        definition: sense.definition,
        partOfSpeech: sense.partOfSpeech,
      })
    })
  },
})

export const getDictionaryEntriesByHeadword = query({
  args: {
    headword: z.string(),
  },
  async handler(ctx, { headword }) {
    const user = await requireUserByCtx(ctx)
    const dictionaryEntries = await ctx.db
      .query('dictionaryEntries')
      .withIndex('byUserIdHeadwordSourceLanguage', (q) =>
        q.eq('userId', user._id).eq('headword', headword.toLocaleLowerCase()),
      )
      .collect()
    const apiDictionaryEntries: ApiDictionaryEntry[] = await asyncMap(
      dictionaryEntries,
      async (dictionaryEntry) => {
        const dictionaryEntrySenses = await ctx.db
          .query('dictionaryEntrySenses')
          .withIndex('byDictionaryEntryIdLocalId', (q) =>
            q.eq('dictionaryEntryId', dictionaryEntry._id),
          )
          .collect()
        return {
          dictionaryEntry,
          dictionaryEntrySenses,
        }
      },
    )
    return apiDictionaryEntries
  },
})
