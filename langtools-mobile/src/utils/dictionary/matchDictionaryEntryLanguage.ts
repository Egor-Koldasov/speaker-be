import { Doc } from '../../../convex/_generated/dataModel'

export const matchDictionaryEntryLanguage = (
  dictionaryEntry: Doc<'dictionaryEntries'>,
  language: string,
) => {
  const isMatching =
    dictionaryEntry.sourceLanguage === language ||
    dictionaryEntry.sourceLanguageFull === language
  return { isMatching }
}
