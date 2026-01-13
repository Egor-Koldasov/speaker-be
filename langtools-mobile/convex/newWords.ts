import { internal } from './_generated/api'
import { PromptParameter } from './types/PromptParameter'
import { requireUserByActionCtx } from './users'
import { action } from './utils/action'
import { zid } from './utils/schema/zid'

export const generateNewWords = action({
  args: {
    objectStreamId: zid('objectStream'),
  },
  async handler(ctx, { objectStreamId }) {
    const user = await requireUserByActionCtx(ctx)

    const vocabularyContext = await ctx.runQuery(
      internal.dictionary.getVocabularyContext,
      {
        extendedInfoLimit: 500,
      },
    )

    const prompt = `
    
    `

    const params: PromptParameter[] = [
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
  },
})
