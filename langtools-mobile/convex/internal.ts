import { WithoutSystemFields } from 'convex/server'
import { v } from 'convex/values'
import { Doc } from './_generated/dataModel'
import { internalMutation } from './_generated/server'

export const importPgDictionaryEntries = internalMutation({
  args: {
    dictionaryEntryPgRows: v.array(
      v.object({
        auth_user_id: v.string(),
        dictionary_entry_id: v.string(),
        json_data: v.object({
          headword: v.string(),
          source_language: v.string(),
          meanings: v.array(
            v.object({
              headword: v.string(),
              local_id: v.string(),
              canonical_form: v.string(),
              definition: v.string(),
              part_of_speech: v.string(),
            }),
          ),
        }),
        email: v.string(),
        is_e2e_test: v.boolean(),
      }),
    ),
  },
  async handler(ctx, { dictionaryEntryPgRows }) {
    for (const dictionaryEntryPgRow of dictionaryEntryPgRows) {
      const dictionaryEntryJsonData = dictionaryEntryPgRow.json_data

      const dictionaryEntry: WithoutSystemFields<Doc<'dictionaryEntries'>> = {
        userId: dictionaryEntryPgRow.auth_user_id,
      }

      const dictionaryEntryId = await ctx.db.insert(
        'dictionaryEntries',
        dictionaryEntry,
      )

      const dictionaryEntrySenses = dictionaryEntryJsonData.meanings.map(
        (meaning): WithoutSystemFields<Doc<'dictionaryEntrySenses'>> => ({
          canonicalForm: meaning.canonical_form,
          definition: meaning.definition,
          partOfSpeech: meaning.part_of_speech,
          localId: meaning.local_id,
          dictionaryEntryId,
        }),
      )

      for (const dictionaryEntrySense of dictionaryEntrySenses) {
        await ctx.db.insert('dictionaryEntrySenses', dictionaryEntrySense)
      }
    }
  },
})

export const migrateUserIds = internalMutation({
  args: {
    userIds: v.array(
      v.object({
        from: v.string(),
        to: v.string(),
      }),
    ),
  },
  async handler(ctx, { userIds }) {
    for (const { from, to } of userIds) {
      const dictionaryEntries = await ctx.db
        .query('dictionaryEntries')
        .withIndex('byUserId', (q) => q.eq('userId', from))
        .collect()

      for (const dictionaryEntry of dictionaryEntries) {
        await ctx.db.patch(dictionaryEntry._id, { userId: to })
      }
    }
  },
})
