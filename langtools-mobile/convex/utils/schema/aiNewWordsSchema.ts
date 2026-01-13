import z from 'zod/v3'

export const aiNewWordsSchema = z.object({
  suggestedWords: z.array(
    z.object({
      headword: z.string(),
    }),
  ),
})
