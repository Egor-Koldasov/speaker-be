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
        headword: dictionaryEntryJsonData.headword,
        sourceLanguage: dictionaryEntryJsonData.source_language,
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

export const migrateDictionaryEntriesUserIds = internalMutation({
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
        .withIndex('byUserIdHeadwordSourceLanguage', (q) =>
          q.eq('userId', from),
        )
        .collect()

      for (const dictionaryEntry of dictionaryEntries) {
        await ctx.db.patch(dictionaryEntry._id, { userId: to })
      }

      const fsrsProgressList = await ctx.db
        .query('fsrsProgress')
        .withIndex('byUserIdSenseId', (q) => q.eq('userId', from))
        .collect()

      for (const fsrsProgress of fsrsProgressList) {
        await ctx.db.patch(fsrsProgress._id, { userId: to })
      }
    }
  },
})

export const importPgFsrsProgress = internalMutation({
  args: {
    fsrsPgRows: v.array(
      v.object({
        fsrs_id: v.string(),
        due: v.string(),
        stability: v.optional(v.number()),
        difficulty: v.optional(v.number()),
        state: v.number(),
        step: v.number(),
        last_review: v.optional(v.string()),
        reps: v.number(),
        lapses: v.number(),
        auth_user_id: v.string(),
        dictionary_entry_id: v.string(),
        meaning_local_id: v.string(),
        dictionary_entry_headword: v.string(),
        dictionary_entry_source_language: v.string(),
      }),
    ),
  },
  async handler(ctx, { fsrsPgRows }) {
    for (const fsrsProgressPgRow of fsrsPgRows) {
      const dictionaryEntry = await ctx.db
        .query('dictionaryEntries')
        .withIndex('byUserIdHeadwordSourceLanguage', (q) =>
          q
            .eq('userId', fsrsProgressPgRow.auth_user_id)
            .eq('headword', fsrsProgressPgRow.dictionary_entry_headword)
            .eq(
              'sourceLanguage',
              fsrsProgressPgRow.dictionary_entry_source_language,
            ),
        )
        .unique()
      if (!dictionaryEntry) {
        throw new Error(
          `Dictionary entry not found: ${fsrsProgressPgRow.dictionary_entry_id}`,
        )
      }

      const sense = await ctx.db
        .query('dictionaryEntrySenses')
        .withIndex('byDictionaryEntryIdLocalId', (q) =>
          q
            .eq('dictionaryEntryId', dictionaryEntry._id)
            .eq('localId', fsrsProgressPgRow.meaning_local_id),
        )
        .unique()
      if (!sense) {
        throw new Error(
          `Sense not found: ${fsrsProgressPgRow.meaning_local_id}`,
        )
      }

      await ctx.db.insert('fsrsProgress', {
        due: fsrsProgressPgRow.due,
        stability: fsrsProgressPgRow.stability,
        difficulty: fsrsProgressPgRow.difficulty,
        state: fsrsProgressPgRow.state,
        step: fsrsProgressPgRow.step,
        last_review: fsrsProgressPgRow.last_review,
        reps: fsrsProgressPgRow.reps,
        lapses: fsrsProgressPgRow.lapses,
        senseId: sense._id,
        userId: fsrsProgressPgRow.auth_user_id,
      })
    }
  },
})
