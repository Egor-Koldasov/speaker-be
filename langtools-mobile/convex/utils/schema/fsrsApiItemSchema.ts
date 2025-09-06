import z from 'zod/v3'

export const fsrsApiItemSchema = z.object({
  due: z.string(),
  stability: z.number().nullable(),
  difficulty: z.number().nullable(),
  state: z.number(),
  step: z.number(),
  last_review: z.string().nullable(),
  reps: z.number(),
  lapses: z.number(),
})

export const processReviewApiResponseSchema = z.object({
  updated_training_data: fsrsApiItemSchema,
})
