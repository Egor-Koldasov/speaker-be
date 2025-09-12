import { Doc } from '../_generated/dataModel'
import { NextFsrsItem } from '../fsrsProgress'

export type NextFsrsItemWithExtra = NextFsrsItem & {
  senseTranslations: Doc<'dictionaryEntrySenseTranslation'>[]
  vocabularyAwareSentences: Doc<'vocabularyAwareSentence'>[]
}
