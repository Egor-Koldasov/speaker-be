// import { authTables } from "@convex-dev/auth/server";
import { zodToConvex } from 'convex-helpers/server/zod'
import { defineSchema, defineTable } from 'convex/server'
import { v } from 'convex/values'
import { aiDictionaryEntryStreamSchema } from './utils/schema/aiDictionaryEntrySchema'
import {
  aiDictionaryEntrySenseExtraSchema,
  aiDictionaryEntrySenseExtraTranslationSchema,
} from './utils/schema/aiDictionaryEntrySenseExtraSchema'

const updatedAt = v.optional(v.string())

export default defineSchema({
  // ...authTables,
  users: defineTable({
    updatedAt,
    authUserId: v.string(),
    email: v.string(),
  })
    .index('byAuthUserId', ['authUserId'])
    .index('byEmail', ['email']),
  dictionaryEntries: defineTable({
    headword: v.string(),
    sourceLanguage: v.string(),
    sourceLanguageFull: v.optional(v.string()),
    updatedAt,
    userId: v.string(),
  }).index('byUserIdHeadwordSourceLanguage', [
    'userId',
    'headword',
    'sourceLanguage',
  ]),
  dictionaryEntrySenses: defineTable({
    updatedAt,
    dictionaryEntryId: v.id('dictionaryEntries'),
    localId: v.string(),
    canonicalForm: v.string(),
    definition: v.string(),
    partOfSpeech: v.string(),
  }).index('byDictionaryEntryIdLocalId', ['dictionaryEntryId', 'localId']),
  dictionaryEntrySenseTranslation: defineTable({
    updatedAt,
    userId: v.string(),
    dictionaryEntrySenseId: v.id('dictionaryEntrySenses'),
    translationLanguage: v.string(),
    localId: v.string(),
    canonicalForm: v.string(),
    partOfSpeech: v.string(),
    translations: v.array(v.string()),
    definition: v.string(),
  }).index('byDictionaryEntrySenseId', ['dictionaryEntrySenseId']),
  fsrsProgress: defineTable({
    updatedAt,
    senseId: v.id('dictionaryEntrySenses'),
    userId: v.string(),
    due: v.string(),
    stability: v.optional(v.number()),
    difficulty: v.optional(v.number()),
    state: v.number(),
    step: v.number(),
    last_review: v.optional(v.string()),
    reps: v.number(),
    lapses: v.number(),
  })
    .index('byUserIdSenseId', ['userId', 'senseId'])
    .index('byUserIdDue', ['userId', 'due']),
  aiMessageStream: defineTable({
    updatedAt,
    threadId: v.string(),
    streamId: v.string(),
  })
    .index('byThreadId', ['threadId'])
    .index('byStreamId', ['streamId']),
  aiDictionaryEntryStream: defineTable({
    updatedAt,
    threadId: v.string(),
    ...zodToConvex(aiDictionaryEntryStreamSchema).fields,
    finishedAt: v.optional(v.string()),
  }).index('byThreadIdFinishedAt', ['threadId', 'finishedAt']),
  objectStream: defineTable({
    updatedAt,
    // threadId: v.string(),
    userId: v.string(),
    jsonStringSoFar: v.string(),
    finishedAt: v.optional(v.string()),
  }),
  vocabularyAwareSentence: defineTable({
    updatedAt,
    dictionaryEntrySenseId: v.id('dictionaryEntrySenses'),
    sentence: v.string(),
    wordsUsed: v.array(
      v.object({
        headword: v.string(),
        sentenceForm: v.string(),
      }),
    ),
  }).index('byDictionaryEntrySenseId', ['dictionaryEntrySenseId']),
  vocabularyAwareSentenceTranslation: defineTable({
    updatedAt,
    vocabularyAwareSentenceId: v.id('vocabularyAwareSentence'),
    translationLanguage: v.string(),
    exampleSentence: v.string(),
  }),
  dictionaryEntrySenseExtra: defineTable({
    updatedAt,
    dictionaryEntrySenseId: v.id('dictionaryEntrySenses'),
    ...zodToConvex(aiDictionaryEntrySenseExtraSchema).fields,
  }).index('byDictionaryEntrySenseId', ['dictionaryEntrySenseId']),
  dictionaryEntrySenseExtraTranslation: defineTable({
    updatedAt,
    dictionaryEntrySenseExtraId: v.id('dictionaryEntrySenseExtra'),
    translationLanguage: v.string(),
    ...zodToConvex(aiDictionaryEntrySenseExtraTranslationSchema).fields,
  }).index('byDictionaryEntrySenseExtraIdTranslationLanguage', [
    'dictionaryEntrySenseExtraId',
    'translationLanguage',
  ]),
})
