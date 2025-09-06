import { AiDictionaryEntry } from '../../../convex/utils/schema/aiDictionaryEntrySchema'
import { ApiDictionaryEntry } from './ApiDictionaryEntry'

// Normalize the ApiDictionaryEntry to the AiDictionaryEntry.
// For functions that work with partial data.
export const apiToAiDictionaryEntry = (
  apiDictionaryEntry: ApiDictionaryEntry,
): AiDictionaryEntry => {
  return {
    headword: apiDictionaryEntry.dictionaryEntry.headword,
    sourceLanguage: apiDictionaryEntry.dictionaryEntry.sourceLanguage,
    senses: apiDictionaryEntry.dictionaryEntrySenses,
  }
}
