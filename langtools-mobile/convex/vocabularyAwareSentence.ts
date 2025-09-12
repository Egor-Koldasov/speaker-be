import { asyncMap } from 'convex-helpers'
import { api, internal } from './_generated/api'
import { Doc, Id } from './_generated/dataModel'
import { agent } from './ai/agent'
import {
  requireDictionaryEntry,
  requireDictionaryEntrySense,
} from './dictionary'
import { PromptParameter } from './types/PromptParameter'
import { TransactionCtx } from './types/TransactionCtx'
import { requireUserByActionCtx } from './users'
import { action } from './utils/action'
import { internalMutation } from './utils/internalMutation'
import { processObjectStream } from './utils/objectStream/processObjectStream'
import { query } from './utils/query'
import { aiVocabularyAwareSentenceSchema } from './utils/schema/aiVocabularyAwareSentenceSchema'
import { zid } from './utils/schema/zid'

export const generateVocabularyAwareSentences = action({
  args: {
    dictionaryEntrySenseId: zid('dictionaryEntrySenses'),
    objectStreamId: zid('objectStream').optional(),
  },
  async handler(ctx, { dictionaryEntrySenseId, objectStreamId }) {
    const user = await requireUserByActionCtx(ctx)
    const { dictionaryEntrySense, dictionaryEntry } = await ctx.runQuery(
      internal.dictionary.requireDictionaryEntrySenseQuery,
      {
        dictionaryEntrySenseId,
      },
    )
    const vocabularyContext = await ctx.runQuery(
      internal.dictionary.getVocabularyContext,
      {
        extendedInfoLimit: 500,
      },
    )
    if (!objectStreamId) {
      objectStreamId = await ctx.runMutation(
        api.objectStream.createObjectStream,
      )
    }
    const prompt = `
You are a professional linguist and lexicographer tasked with writing sentences that \
will help the user learn the word in a foreign language.

You will be given a list of words from the user's training vocabulary and a target word definition. \
Create example sentences using the target headword and the words from the user's vocabulary. \
The sentences should always include the target headword, and it should be used in the same \
sense that is provided in the parameters.
If the vocabulary is insufficient to generate \
example sentences, use other words, prioritizing the most frequently used words in the language.

Every sentence item should be an object containing a sentence text itself and a property \
that contains every word used in the sentence in the same order \
as they appear in the sentence. If the same word is used multiple times in the sentence, \
it should be included multiple times in the array.
    `

    const promptParameters: PromptParameter[] = [
      {
        name: 'numberOfSentences',
        description: `The number of example sentences to generate.`,
        value: 10,
      },
      {
        name: 'targetWordDefinition',
        description: `The definition object of the target word to train.`,
        value: {
          headword: dictionaryEntry.headword,
          sourceLanguage: dictionaryEntry.sourceLanguage,
          sense: {
            partOfSpeech: dictionaryEntrySense.partOfSpeech,
            canonicalForm: dictionaryEntrySense.canonicalForm,
            definition: dictionaryEntrySense.definition,
          },
        },
      },
      {
        name: 'vocabularyContextItemsExtended',
        description: `
A prioritized list of the words from the user's training vocabulary. These words are \
the best candidates to be included in the example sentences.
          `,
        value: vocabularyContext.vocabularyContextItemsExtended,
      },
      {
        name: 'vocabularyContextItemsShort',
        description: `
The rest of the words from the user's training vocabulary. These words have lower priority \
to be included in the example sentences, but still more preferred than non-vocabulary words.
          `,
        value: vocabularyContext.vocabularyContextItemsShort,
      },
    ]

    const stream = await agent.streamObject(
      ctx,
      { userId: user._id },
      {
        schema: aiVocabularyAwareSentenceSchema,
        messages: [
          {
            role: 'system',
            content: prompt,
          },
          {
            role: 'user',
            content: JSON.stringify(promptParameters, null, 2),
          },
        ],
      },
    )

    await processObjectStream({
      ctx,
      objectStreamId,
      stream,
    })

    const aiVocabularyAwareSentence = await stream.object

    await ctx.runMutation(
      internal.vocabularyAwareSentence.createAiVocabularyAwareSentence,
      {
        dictionaryEntrySenseId,
        aiVocabularyAwareSentence,
      },
    )
  },
})

export const createAiVocabularyAwareSentence = internalMutation({
  args: {
    dictionaryEntrySenseId: zid('dictionaryEntrySenses'),
    aiVocabularyAwareSentence: aiVocabularyAwareSentenceSchema,
  },
  async handler(ctx, args) {
    const { aiVocabularyAwareSentence, dictionaryEntrySenseId } = args

    // Check permissions
    await requireDictionaryEntrySense(ctx, dictionaryEntrySenseId)

    await asyncMap(
      aiVocabularyAwareSentence.sentences,
      async (sentenceItem) => {
        await ctx.db.insert('vocabularyAwareSentence', {
          dictionaryEntrySenseId,
          sentence: sentenceItem.sentence,
          wordsUsed: sentenceItem.wordsUsed,
        })
      },
    )
  },
})

export const getVocabularyAwareSentecesBySenseId = async (
  ctx: TransactionCtx,
  opts: { dictionaryEntrySenseId: Id<'dictionaryEntrySenses'> },
) => {
  const { dictionaryEntrySenseId } = opts
  const vocabularyAwareSentences = await ctx.db
    .query('vocabularyAwareSentence')
    .withIndex('byDictionaryEntrySenseId', (q) =>
      q.eq('dictionaryEntrySenseId', dictionaryEntrySenseId),
    )
    .collect()
  return { vocabularyAwareSentences }
}

export const getVocabularyAwareSentecesByDictionaryEntry = query({
  args: {
    dictionaryEntryId: zid('dictionaryEntries'),
  },
  async handler(ctx, args) {
    const { dictionaryEntryId } = args

    await requireDictionaryEntry(ctx, dictionaryEntryId)

    const dictionaryEntrySenses = await ctx.db
      .query('dictionaryEntrySenses')
      .withIndex('byDictionaryEntryIdLocalId', (q) =>
        q.eq('dictionaryEntryId', dictionaryEntryId),
      )
      .collect()

    const vocabularyAwareSentencesBySenseId: Record<
      Id<'dictionaryEntrySenses'>,
      {
        vocabularyAwareSentences: Doc<'vocabularyAwareSentence'>[]
      }
    > = {}

    for (const dictionaryEntrySense of dictionaryEntrySenses) {
      const { vocabularyAwareSentences } =
        await getVocabularyAwareSentecesBySenseId(ctx, {
          dictionaryEntrySenseId: dictionaryEntrySense._id,
        })
      vocabularyAwareSentencesBySenseId[dictionaryEntrySense._id] = {
        vocabularyAwareSentences,
      }
    }

    return { vocabularyAwareSentencesBySenseId }
  },
})
