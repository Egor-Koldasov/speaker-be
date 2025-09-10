import z from 'zod/v3'

export const aiVocabularyAwareSentenceSchema = z.object({
  sentences: z
    .array(
      z
        .object({
          sentence: z
            .string()
            .describe('The regular sentence text for reading practice.'),
          sentenceWithoutHeadword: z
            .string()
            .describe(
              'The exact same sentence text, but with the target word replaced exactly with \`___\`.',
            ),
          wordsUsed: z.array(
            z.object({
              sentenceForm: z
                .string()
                .describe(
                  'The word in the exact same form as it appears in the sentence.',
                ),
              headword: z.string().describe(`
If the word was taken from the user's vocabulary parameters and its shape was changed \
the headword should match the shape from the parameters. Otherwise, it should be the same \
as the word in the sentence.
`),
            }),
          ).describe(`
A property \
that contains every word used in the sentence in the same order \
as they appear in the sentence. If the same word is used multiple times in the sentence, \
it should be included multiple times in the array.
`),
        })
        .describe('An example sentence object.'),
    )
    .describe('List of example sentences.'),
})

export type AiVocabularyAwareSentence = z.output<
  typeof aiVocabularyAwareSentenceSchema
>

export const aiVocabularyAwareSentenceStreamSchema =
  aiVocabularyAwareSentenceSchema.partial().extend({
    sentences: z
      .array(aiVocabularyAwareSentenceSchema.shape.sentences.element.partial())
      .optional(),
  })

export type AiVocabularyAwareSentenceStream = z.output<
  typeof aiVocabularyAwareSentenceStreamSchema
>
