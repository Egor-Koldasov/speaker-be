import { createTool, ToolCtx } from '@convex-dev/agent'
import z from 'zod/v3'
import { api, internal } from '../_generated/api'
import { PromptParameter } from '../types/PromptParameter'

export const suggestNewWordsTool = createTool({
  description: `
Activate this tool when suggesting new words for the user to learn. It will load the related user training data and return it along with the detailed intructions about how to proceed.`,
  args: z.object({}),
  handler: async (ctx: ToolCtx, args) => {
    const { threadId, userId } = ctx
    if (!threadId) {
      throw new Error('No thread ID in context')
    }
    ctx.runQuery(api.aiChat.getExistingThread, { threadId })

    const learningLanguage = await ctx.runQuery(
      api.learningLanguage.getLearningLanguage,
      {},
    )

    const vocabularyContext = await ctx.runQuery(
      internal.dictionary.getVocabularyContext,
      {
        extendedInfoLimit: 500,
      },
    )

    const trainingData: PromptParameter[] = [
      {
        name: 'selectedLearningLanguage',
        description: `
The language the user has selected to learn, in BCP 47 format.
`,
        value: learningLanguage?.selectedLearningLanguage,
      },
      {
        name: 'vocabularyContextItemsExtended',
        description: `
A list of the most recent words from the user's training vocabulary.
`,
        value: vocabularyContext.vocabularyContextItemsExtended,
      },
      {
        name: 'vocabularyContextItemsShort',
        description: `
The rest of the words from the user's training vocabulary.
`,
        value: vocabularyContext.vocabularyContextItemsShort,
      },
    ]

    const instructionPrompt = `
Analyze the user's saved vocabulary words and estimate the user's language proficiency level of the selected language.
The returned vocabulary data contains words from all the languages that the user learns, so make sure to only consider the words from the selected learning language.

Create an educational lesson. The goal of the lesson is to discover new word meanings to add to the user’s vocabulary.

Answer in a brief and strict format:

1. Write an example sentence that combines words from the user's vocabulary with the new words. Avoid using too many new words in the example sentence. Example sentence should aim to include only such new words that match the user's language proficiency, prioritizing the most often used words in a language. If the user is using a different language from the one that they are learning, add a translation.

2. Write a list of new words in the example sentence that are not present in the user's vocabulary. The list should include every new word used in the example sentence that doesn't exist in the user's vocabulary.
`

    return {
      trainingData,
      instructionPrompt,
    }
  },
})
