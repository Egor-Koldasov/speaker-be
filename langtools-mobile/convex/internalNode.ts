'use node'
import { FunctionArgs } from 'convex/server'
import postgres from 'postgres'
import { internal } from './_generated/api'
import { internalAction } from './_generated/server'

type DictionaryEntryJsonData = {
  headword: string
  source_language: string
  meanings: {
    headword: string
    local_id: string
    canonical_form: string
    definition: string
    part_of_speech: string
  }[]
}

type DictionaryEntryPgRow = {
  auth_user_id: string
  dictionary_entry_id: string
  json_data: DictionaryEntryJsonData
  email: string
  is_e2e_test: false
}

export const migratePgDictionaryEntries = internalAction({
  async handler(ctx) {
    const postgresqlUrl = process.env.POSTGRESQL_URL

    if (!postgresqlUrl) {
      throw new Error('POSTGRESQL_URL is not set')
    }

    const sql = postgres(postgresqlUrl)

    let dictionaryEntryPgRows: DictionaryEntryPgRow[] = await sql<
      DictionaryEntryPgRow[]
    >`
SELECT
	auth_user_id,
	dictionary_entry_id,
	json_data,
	email,
	is_e2e_test
FROM
	r_user_dictionary_entry
	LEFT JOIN dictionary_entry ON r_user_dictionary_entry.dictionary_entry_id = dictionary_entry.id
	LEFT JOIN auth_user ON r_user_dictionary_entry.auth_user_id = auth_user.id
WHERE
	auth_user.is_e2e_test = FALSE;
    `
    console.log(dictionaryEntryPgRows)

    dictionaryEntryPgRows = dictionaryEntryPgRows.map(
      (dictionaryEntryPgRow) => ({
        ...dictionaryEntryPgRow,
        json_data: {
          ...dictionaryEntryPgRow.json_data,
          meanings: dictionaryEntryPgRow.json_data.meanings.map((meaning) => ({
            headword: meaning.headword,
            local_id: meaning.local_id,
            canonical_form: meaning.canonical_form,
            definition: meaning.definition,
            part_of_speech: meaning.part_of_speech,
          })),
        },
      }),
    )

    await ctx.runMutation(internal.internal.importPgDictionaryEntries, {
      dictionaryEntryPgRows,
    })
  },
})

type FsrsPgRow = {
  fsrs_id: string
  due: Date
  stability: number | null
  difficulty: number | null
  state: number
  step: number
  last_review: Date | null
  reps: number
  lapses: number
  auth_user_id: string
  dictionary_entry_id: string
  meaning_local_id: string
  dictionary_entry_json_data: DictionaryEntryJsonData
}

export const migratePgFsrsProgress = internalAction({
  async handler(ctx) {
    const postgresqlUrl = process.env.POSTGRESQL_URL

    if (!postgresqlUrl) {
      throw new Error('POSTGRESQL_URL is not set')
    }

    const sql = postgres(postgresqlUrl)

    const fsrsPgRows = await sql<FsrsPgRow[]>`
SELECT
	fsrs.id AS fsrs_id,
	fsrs.due,
	fsrs.stability,
	fsrs.difficulty,
	fsrs.state,
	fsrs.step,
	fsrs.last_review,
	fsrs.reps,
	fsrs.lapses,
	auth_user.id AS auth_user_id,
	r_fsrs_meaning.dictionary_entry_id,
	r_fsrs_meaning.meaning_local_id,
	dictionary_entry.json_data as dictionary_entry_json_data
FROM
	fsrs
	LEFT JOIN r_fsrs_meaning ON fsrs.id = r_fsrs_meaning.fsrs_id
	LEFT JOIN auth_user ON r_fsrs_meaning.auth_user_id = auth_user.id
	LEFT JOIN dictionary_entry ON r_fsrs_meaning.dictionary_entry_id = dictionary_entry.id
WHERE
	auth_user.is_e2e_test = FALSE;
    `

    const fsrsPgRowsForMutation: FunctionArgs<
      typeof internal.internal.importPgFsrsProgress
    >['fsrsPgRows'] = fsrsPgRows.map(
      ({ dictionary_entry_json_data, ...fsrsPgRow }) => ({
        ...fsrsPgRow,
        stability: fsrsPgRow.stability ?? undefined,
        difficulty: fsrsPgRow.difficulty ?? undefined,
        due: fsrsPgRow.due.toISOString(),
        last_review: fsrsPgRow.last_review?.toISOString(),
        dictionary_entry_headword: dictionary_entry_json_data.headword,
        dictionary_entry_source_language:
          dictionary_entry_json_data.source_language,
      }),
    )

    console.log(fsrsPgRowsForMutation)

    await ctx.runMutation(internal.internal.importPgFsrsProgress, {
      fsrsPgRows: fsrsPgRowsForMutation,
    })
  },
})
