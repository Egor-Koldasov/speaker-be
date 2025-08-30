// import { authTables } from "@convex-dev/auth/server";
import { defineSchema, defineTable } from 'convex/server'
import { v } from 'convex/values'

export default defineSchema({
  // ...authTables,
  dictionaryEntries: defineTable({
    updatedAt: v.optional(v.string()),
    userId: v.string(),
  }).index('byUserId', ['userId']),
  dictionaryEntrySenses: defineTable({
    updatedAt: v.optional(v.string()),
    dictionaryEntryId: v.id('dictionaryEntries'),
    localId: v.string(),
    canonicalForm: v.string(),
    definition: v.string(),
    partOfSpeech: v.string(),
  }).index('byDictionaryEntryIdLocalId', ['dictionaryEntryId', 'localId']),
})
