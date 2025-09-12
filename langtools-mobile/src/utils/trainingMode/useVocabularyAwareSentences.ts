import { useCallback, useEffect, useMemo } from 'react'
import { proxy, useSnapshot } from 'valtio'
import { api } from '../../../convex/_generated/api'
import { Id } from '../../../convex/_generated/dataModel'
import { NextFsrsItemWithExtra } from '../../../convex/types/NextFsrsItemWithTranslations'
import { aiVocabularyAwareSentenceStreamSchema } from '../../../convex/utils/schema/aiVocabularyAwareSentenceSchema'
import { useAction } from '../convex/useAction'
import { useMutation } from '../convex/useMutation'
import { withRetry } from '../convex/withRetry'
import { getRandomItem } from '../data/getRandomItem'
import { useObjectStream } from '../objectStream/useObjectStream'

type UseVocabularyAwareSentencesOpts = {
  nextFsrsItem: NextFsrsItemWithExtra | undefined
}

const state = proxy({
  senseIdToObjectStreamId: {} as Record<
    Id<'dictionaryEntrySenses'>,
    Id<'objectStream'>
  >,
  generationAttempt: 0,
})

export const useVocabularyAwareSentences = (
  opts: UseVocabularyAwareSentencesOpts,
) => {
  const { nextFsrsItem } = opts
  const generateAction = useAction(
    api.vocabularyAwareSentence.generateVocabularyAwareSentences,
  )
  const createObjectStream = useMutation(api.objectStream.createObjectStream)

  const snap = useSnapshot(state)

  const objectStreamId = !nextFsrsItem
    ? null
    : (snap.senseIdToObjectStreamId[nextFsrsItem.sense._id] ?? null)

  const { partialObject } = useObjectStream(
    objectStreamId,
    aiVocabularyAwareSentenceStreamSchema,
  )

  const vocabularyAwareSentences = useMemo(() => {
    if (partialObject.data && nextFsrsItem) {
      return partialObject.data.sentences ?? []
    }
    return nextFsrsItem?.vocabularyAwareSentences
  }, [partialObject.data, nextFsrsItem])

  const generateWithRetry = useCallback(
    async (dictionaryEntrySenseId: Id<'dictionaryEntrySenses'>) => {
      if (!nextFsrsItem) {
        console.error('nextFsrsItem not found', nextFsrsItem)
        return
      }
      state.generationAttempt = 0
      await withRetry({
        fn: async () => {
          const objectStreamId = await createObjectStream.mutate()
          state.senseIdToObjectStreamId[nextFsrsItem.sense._id] = objectStreamId
          generateAction.exec({
            dictionaryEntrySenseId,
            objectStreamId,
          })
        },
        onRetry: (error, attempt) => {
          state.generationAttempt = attempt + 1
        },
      })
    },
    [createObjectStream, generateAction, nextFsrsItem],
  )

  const requireGeneration =
    !!nextFsrsItem && nextFsrsItem.vocabularyAwareSentences.length === 0

  useEffect(() => {
    if (!nextFsrsItem || !requireGeneration || generateAction.isPending) {
      return
    }
    generateWithRetry(nextFsrsItem.sense._id)
  }, [requireGeneration])

  const vocabularyAwareSentence = useMemo(() => {
    return getRandomItem(vocabularyAwareSentences ?? [])
  }, [vocabularyAwareSentences])

  return {
    vocabularyAwareSentences,
    vocabularyAwareSentence,
    generateVocabularyAwareSentences: generateAction,
  }
}
