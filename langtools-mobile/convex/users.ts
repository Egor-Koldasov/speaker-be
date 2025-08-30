import { query, QueryCtx } from './_generated/server'
import { User } from './types/User'

export const getUserByCtx = async (ctx: QueryCtx): Promise<User | null> => {
  const userIdentity = await ctx.auth.getUserIdentity()

  if (!userIdentity) {
    return null
  }

  if (!userIdentity.email) {
    console.error('User email is not set')
    return null
  }

  return {
    id: userIdentity.subject,
    email: userIdentity.email,
  }
}

export const getUser = query({
  args: {},
  handler: async (ctx): Promise<User | null> => {
    return await getUserByCtx(ctx)
  },
})
