import { query } from './_generated/server'

export const getUserProfile = query({
  args: {},
  handler: async (ctx) => {
    const userIdentity = await ctx.auth.getUserIdentity()

    console.log('userIdentity', userIdentity)
    // if (!userIdentity) {
    //   throw new Error('Unauthorized')
    // }
    return userIdentity
  },
})
