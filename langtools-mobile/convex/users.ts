import { api } from './_generated/api'
import { Doc } from './_generated/dataModel'
import { ActionCtx, mutation, query } from './_generated/server'
import { AuthUser } from './types/AuthUser'
import { TransactionCtx } from './types/TransactionCtx'
import { UnknownCtx } from './types/UnknownCtx'

export const getAuthUserByCtx = async (
  ctx: UnknownCtx,
): Promise<AuthUser | null> => {
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

export const requireAuthUserByCtx = async (
  ctx: UnknownCtx,
): Promise<AuthUser> => {
  const authUser = await getAuthUserByCtx(ctx)
  if (!authUser) {
    throw new Error('Auth user not found')
  }
  return authUser
}

export const requireUserByCtx = async (
  ctx: TransactionCtx,
): Promise<Doc<'users'>> => {
  const user = await getUserByCtx(ctx)
  if (!user) {
    throw new Error('User not found')
  }
  return user
}

export const getUserByCtx = async (
  ctx: TransactionCtx,
): Promise<Doc<'users'> | null> => {
  const authUser = await getAuthUserByCtx(ctx)
  if (!authUser) {
    return null
  }
  return await ctx.db
    .query('users')
    .withIndex('byAuthUserId', (q) => q.eq('authUserId', authUser.id))
    .unique()
}

export const getUser = query({
  args: {},
  handler: async (ctx) => {
    return await getUserByCtx(ctx)
  },
})

export const syncAuthUser = mutation({
  async handler(ctx, args) {
    const authUser = await requireAuthUserByCtx(ctx)
    const user = await getUserByCtx(ctx)
    if (!user) {
      await ctx.db.insert('users', {
        authUserId: authUser.id,
        email: authUser.email,
      })
    }
  },
})

export const requireUserByActionCtx = async (
  ctx: ActionCtx,
): Promise<Doc<'users'>> => {
  const user = await ctx.runQuery(api.users.getUser)
  if (!user) {
    throw new Error('User not found')
  }
  return user
}
