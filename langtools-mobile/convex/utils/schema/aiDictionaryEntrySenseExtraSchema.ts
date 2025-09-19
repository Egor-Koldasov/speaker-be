import z from 'zod/v3'

export const aiDictionaryEntrySenseExtraSchema = z.object({
  pronunciation: z
    .array(z.string())
    .describe('List of pronunciations in IPA format.'),
  toneNotation: z
    .string()
    .describe(
      'Tone markers for tone languages (Mandarin: xuéxí, Vietnamese: học tập).',
    ),
  morphology: z.string().describe('List of all the morphological features.'),
  etymology: z
    .string()
    .describe("A detailed explanation of the word's etymology."),
  synonyms: z.array(z.string()).describe('List of synonyms.'),
  antonyms: z.array(z.string()).describe('List of antonyms.'),
})

export type AiDictionaryEntrySenseExtra = z.output<
  typeof aiDictionaryEntrySenseExtraSchema
>

export const aiDictionaryEntrySenseExtraTranslationSchema =
  aiDictionaryEntrySenseExtraSchema.extend({
    pronunciationTips: z
      .string()
      .describe(
        'Pronunciation tips in translation language in beginner-friendly way.',
      ),
    toneTips: z
      .string()
      .describe(
        'Include for tonal languages: tone tips in translation language in beginner-friendly way.',
      ),
  })
