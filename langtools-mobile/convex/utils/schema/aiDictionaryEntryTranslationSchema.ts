import { z } from 'zod/v3'

export const aiDictionaryEntryTranslationSchema = z.object({
  senses: z
    .array(
      z.object({
        localId: z.string().describe('Sense local id of the original meaning.'),
        canonicalForm: z
          .string()
          .describe(
            'Standard dictionary form - base/citation form (infinitive, nominative, etc.)',
          ),
        partOfSpeech: z.string().describe('Part of speech.'),
        translations: z
          .array(z.string())
          .describe(
            'Direct translations of the word, ordered by the best fit.',
          ),
        definition: z
          .string()
          .describe(
            'Clear, comprehensive definition of a particular sense of the word.',
          ),
      }),
    )
    .describe('List of all senses ordered from most to least common usage.'),
})

export type AiDictionaryEntryTranslation = z.infer<
  typeof aiDictionaryEntryTranslationSchema
>

export const aiDictionaryEntryTranslationStreamSchema =
  aiDictionaryEntryTranslationSchema.partial().extend({
    senses: z
      .array(aiDictionaryEntryTranslationSchema.shape.senses.element.partial())
      .optional(),
  })

export type AiDictionaryEntryTranslationStream = z.infer<
  typeof aiDictionaryEntryTranslationStreamSchema
>
