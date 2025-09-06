import { Doc } from '../../../convex/_generated/dataModel'

export type ApiDictionaryEntry = {
  dictionaryEntry: Doc<'dictionaryEntries'>
  dictionaryEntrySenses: Doc<'dictionaryEntrySenses'>[]
}
