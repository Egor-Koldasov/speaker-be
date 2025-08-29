import { z } from 'zod'

export const clerkErrorSchema = z.object({
  status: z.number(),
  clerkError: z.boolean(),
  errors: z.array(
    z.object({
      code: z.string(),
      message: z.string(),
      longMessage: z.string(),
      meta: z
        .object({
          paramName: z.string().optional(),
        })
        .optional(),
    }),
  ),
})

export const clerkErrorEmailExistsSchema = clerkErrorSchema.extend({
  status: z.literal(422),
  clerkError: z.literal(true),
  errors: z.array(
    z.object({
      code: z.literal('form_identifier_exists'),
      meta: z.object({
        paramName: z.literal('email_address'),
      }),
    }),
  ),
})
