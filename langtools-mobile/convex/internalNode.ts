'use node'
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
