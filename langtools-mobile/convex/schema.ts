// import { authTables } from "@convex-dev/auth/server";
import { defineSchema, defineTable } from 'convex/server'
import { v } from 'convex/values'

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
    updatedAt,
    userId: v.string(),
  })
    .index('byUserId', ['userId'])
    .index('byHeadwordSourceLanguage', ['headword', 'sourceLanguage']),
  dictionaryEntrySenses: defineTable({
    updatedAt,
    dictionaryEntryId: v.id('dictionaryEntries'),
    localId: v.string(),
    canonicalForm: v.string(),
    definition: v.string(),
    partOfSpeech: v.string(),
  }).index('byDictionaryEntryIdLocalId', ['dictionaryEntryId', 'localId']),
  fsrsProgress: defineTable({
    updatedAt,
    due: v.string(),
    stability: v.optional(v.number()),
    difficulty: v.optional(v.number()),
    state: v.number(),
    step: v.number(),
    last_review: v.optional(v.string()),
    reps: v.number(),
    lapses: v.number(),
  }),
  relSenseFsrsProgress: defineTable({
    updatedAt,
    fsrsProgressId: v.id('fsrsProgress'),
    senseId: v.id('dictionaryEntrySenses'),
    userId: v.string(),
  }).index('byUserIdSenseId', ['userId', 'senseId']),
  aiMessageStream: defineTable({
    updatedAt,
    threadId: v.string(),
    streamId: v.string(),
  })
    .index('byThreadId', ['threadId'])
    .index('byStreamId', ['streamId']),
})
