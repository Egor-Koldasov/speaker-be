import { useCallback, useEffect, useMemo } from 'react'
import { proxy, useSnapshot } from 'valtio'
import { api } from '../../../convex/_generated/api'
import { Id } from '../../../convex/_generated/dataModel'
import { aiVocabularyAwareSentenceStreamSchema } from '../../../convex/utils/schema/aiVocabularyAwareSentenceSchema'
import { useAction } from '../convex/useAction'
import { useMutation } from '../convex/useMutation'
import { withRetry } from '../convex/withRetry'
import { getRandomItem } from '../data/getRandomItem'
import { useObjectStream } from '../objectStream/useObjectStream'
import { useQuery } from 'convex/react'

type UseDictionaryEntrySenseExtraOpts = {
  dictionaryEntrySenseId: Id<'dictionaryEntrySenses'> | null
}

const state = proxy({
  senseIdToObjectStreamId: {} as Record<
    Id<'dictionaryEntrySenses'>,
    Id<'objectStream'>
  >,
  generationAttempt: 0,
})

export const useDictionaryEntrySenseExtra = (
  opts: UseDictionaryEntrySenseExtraOpts,
) => {
  const { dictionaryEntrySenseId } = opts
  const generateAction = useAction(
    api.vocabularyAwareSentence.generateVocabularyAwareSentences,
  )
  const createObjectStream = useMutation(api.objectStream.createObjectStream)

  const dictionaryEntrySenseExtraSaved = useQuery(
    api.dictionary.getDictionaryEntrySenseExtra,
    !dictionaryEntrySenseId
      ? 'skip'
      : {
          dictionaryEntrySenseId,
          translationLanguage: 'en',
        },
  )

  const snap = useSnapshot(state)

  const objectStreamId = !dictionaryEntrySenseId
    ? null
    : (snap.senseIdToObjectStreamId[dictionaryEntrySenseId] ?? null)

  const { partialObject } = useObjectStream(
    objectStreamId,
    aiVocabularyAwareSentenceStreamSchema,
  )

  const dictionaryEntrySenseExtra = useMemo(() => {
    if (partialObject.data && !!dictionaryEntrySenseId) {
      return partialObject.data.sentences ?? []
    }
    return dictionaryEntrySenseExtraSaved?.dictionaryEntrySenseExtra ?? null
  }, [
    partialObject.data,
    dictionaryEntrySenseId,
    dictionaryEntrySenseExtraSaved,
  ])

  const generateWithRetry = useCallback(
    async (dictionaryEntrySenseId: Id<'dictionaryEntrySenses'>) => {
      state.generationAttempt = 0
      await withRetry({
        fn: async () => {
          const objectStreamId = await createObjectStream.mutate()
          state.senseIdToObjectStreamId[dictionaryEntrySenseId] = objectStreamId
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
    [createObjectStream, generateAction],
  )

  const requireGeneration =
    !!dictionaryEntrySenseExtraSaved &&
    !dictionaryEntrySenseExtraSaved.dictionaryEntrySenseExtra

  useEffect(() => {
    if (
      !dictionaryEntrySenseId ||
      !requireGeneration ||
      generateAction.isPending
    ) {
      return
    }
    generateWithRetry(dictionaryEntrySenseId)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [requireGeneration])

  return {
    dictionaryEntrySenseExtra,
    generate: generateAction,
  }
}
