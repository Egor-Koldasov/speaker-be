import { z } from 'zod/v3'

export const aiDictionaryEntrySchema = z.object({
  headword: z
    .string()
    .describe(
      'Word form as users encounter it (can be inflected, variant spelling, etc.)',
    ),
  sourceLanguage: z
    .string()
    .describe(
      'Original language in BCP 47 format, guessed from word and user preferences',
    ),
  senses: z
    .array(
      z.object({
        localId: z
          .string()
          .describe(
            'Unique identifier for the sense in format {headword}-{index} starting from 1',
          ),
        canonicalForm: z
          .string()
          .describe(
            'Standard dictionary form - base/citation form (infinitive, nominative, etc.)',
          ),
        partOfSpeech: z
          .string()
          .describe('Part of speech in original language'),
        definition: z
          .string()
          .describe('Clear, comprehensive definition in original language'),
      }),
    )
    .describe('List of all senses ordered from most to least common usage'),
})

export const aiDictionaryEntryStreamSchema = aiDictionaryEntrySchema
  .partial()
  .extend({
    senses: z
      .array(aiDictionaryEntrySchema.shape.senses.element.partial())
      .optional(),
  })

export type AiDictionaryEntryStream = z.infer<
  typeof aiDictionaryEntryStreamSchema
>
