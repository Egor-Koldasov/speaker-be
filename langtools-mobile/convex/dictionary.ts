import { asyncMap } from 'convex-helpers'
import z from 'zod/v3'
import { ApiDictionaryEntry } from '../src/utils/dictionary/ApiDictionaryEntry'
import { apiToAiDictionaryEntry } from '../src/utils/dictionary/apiToAiDictionaryEntry'
import { normalizeLanguageCode } from '../src/utils/normalizeLanguageCode'
import { internal } from './_generated/api'
import { Doc } from './_generated/dataModel'
import { DatabaseReader } from './_generated/server'
import { agent } from './ai/agent'
import { PromptParameter } from './types/PromptParameter'
import { requireUserByActionCtx, requireUserByCtx } from './users'
import { action } from './utils/action'
import { sortSensesByLocalId } from './utils/dictionary/sortSensesByLocalId'
import { internalMutation } from './utils/internalMutation'
import { internalQuery } from './utils/internalQuery'
import { query } from './utils/query'
import { requireById } from './utils/requireById'
import { aiDictionaryEntrySchema } from './utils/schema/aiDictionaryEntrySchema'
import { aiDictionaryEntryTranslationSchema } from './utils/schema/aiDictionaryEntryTranslationSchema'
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
    return dictionaryEntryId
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
        return dictionaryEntryToApiDictionaryEntry(ctx.db, dictionaryEntry)
      },
    )
    return apiDictionaryEntries
  },
})

const dictionaryEntryToApiDictionaryEntry = async (
  db: DatabaseReader,
  dictionaryEntry: Doc<'dictionaryEntries'>,
) => {
  const dictionaryEntrySenses = await db
    .query('dictionaryEntrySenses')
    .withIndex('byDictionaryEntryIdLocalId', (q) =>
      q.eq('dictionaryEntryId', dictionaryEntry._id),
    )
    .collect()
  return {
    dictionaryEntry,
    dictionaryEntrySenses,
  }
}

export const getApiDictionaryEntryById = internalQuery({
  args: {
    dictionaryEntryId: zid('dictionaryEntries'),
  },
  handler: async (ctx, { dictionaryEntryId }) => {
    const dictionaryEntry = await ctx.db.get(dictionaryEntryId)
    if (!dictionaryEntry) {
      return { apiDictionaryEntry: null }
    }
    const apiDictionaryEntry = await dictionaryEntryToApiDictionaryEntry(
      ctx.db,
      dictionaryEntry,
    )
    return { apiDictionaryEntry }
  },
})

export const generateDictionaryEntryTranslation = action({
  args: {
    dictionaryEntryId: zid('dictionaryEntries'),
    translationLanguage: z.string(),
  },
  async handler(ctx, { dictionaryEntryId, translationLanguage }) {
    const user = await requireUserByActionCtx(ctx)
    const { apiDictionaryEntry } = await ctx.runQuery(
      internal.dictionary.getApiDictionaryEntryById,
      {
        dictionaryEntryId,
      },
    )
    if (!apiDictionaryEntry) {
      throw new Error('Dictionary entry not found')
    }

    const prompt = `
You are a professional linguist and lexicographer tasked with writing a comprehensive
dictionary entry designed for the language learners.

You will be given a dictionary entry in the original language and a target \
language that the user is proficient in. Create a dictionary entry in the target \
language provided that is designed for the language learners. The translated \
dictionary entry can differ from the original dictionary entry to make the definition \
more accessible and understandable for the language learners.

Translate all dictionary entry senses.
    `
    const parameters: PromptParameter[] = [
      {
        name: 'dictionaryEntry',
        description: 'A dictionary entry in the original language',
        value: apiToAiDictionaryEntry(apiDictionaryEntry),
      },
      {
        name: 'translationLanguage',
        description: 'The target language for the dictionary entry',
        value: translationLanguage,
      },
    ]

    const result = await agent.generateObject(
      ctx,
      { userId: user._id },
      {
        schema: aiDictionaryEntryTranslationSchema,
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
      },
    )
    const aiDictionaryEntryTranslation = result.object
    await ctx.runMutation(
      internal.dictionary.createDictionaryEntryTranslation,
      {
        dictionaryEntryId,
        translationLanguage,
        aiDictionaryEntryTranslation,
      },
    )
  },
})

export const createDictionaryEntryTranslation = internalMutation({
  args: {
    dictionaryEntryId: zid('dictionaryEntries'),
    translationLanguage: z.string(),
    aiDictionaryEntryTranslation: aiDictionaryEntryTranslationSchema,
  },
  handler: async (
    ctx,
    { dictionaryEntryId, translationLanguage, aiDictionaryEntryTranslation },
  ) => {
    const user = await requireUserByCtx(ctx)
    await requireById(ctx.db, dictionaryEntryId)

    const dictionaryEntrySenses = (
      await ctx.db
        .query('dictionaryEntrySenses')
        .withIndex('byDictionaryEntryIdLocalId', (q) =>
          q.eq('dictionaryEntryId', dictionaryEntryId),
        )
        .collect()
    ).sort(sortSensesByLocalId)

    await asyncMap(
      aiDictionaryEntryTranslation.senses,
      async (senseTranslation, index) => {
        const senseOriginal = dictionaryEntrySenses[index]
        if (!senseOriginal) {
          throw new Error(
            `Sense original not found: ${senseTranslation.localId}`,
          )
        }
        if (senseOriginal.localId !== senseTranslation.localId) {
          throw new Error(
            `Sense local id mismatch: ${senseOriginal.localId} !== ${senseTranslation.localId}`,
          )
        }
        await ctx.db.insert('dictionaryEntrySenseTranslation', {
          dictionaryEntrySenseId: senseOriginal._id,
          localId: senseTranslation.localId,
          canonicalForm: senseTranslation.canonicalForm,
          partOfSpeech: senseTranslation.partOfSpeech,
          definition: senseTranslation.definition,
          translationLanguage,
          userId: user._id,
        })
      },
    )
  },
})
