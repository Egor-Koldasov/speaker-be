import { query } from "./_generated/server";

export const getUserProfile = query({
  args: {},
  handler: async (ctx) => {
    const userIdentity = await ctx.auth.getUserIdentity()
    if (!userIdentity) {
      throw new Error('Unauthorized')
    }
    return await ctx.db.query("users").collect();
  },
})