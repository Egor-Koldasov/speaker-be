import { v } from "convex/values";
import { mutation, query } from "./_generated/server.js";
import { auth } from "./auth";

/**
 * Get the current authenticated user
 */
export const getCurrentUser = query({
  args: {},
  handler: async (ctx) => {
    const userId = await auth.getUserId(ctx);
    if (!userId) {
      return null;
    }

    const user = await ctx.db.get(userId);
    return user;
  },
});

/**
 * Update user profile
 */
export const updateProfile = mutation({
  args: {
    name: v.optional(v.string()),
  },
  handler: async (ctx, { name }) => {
    const userId = await auth.getUserId(ctx);
    if (!userId) {
      throw new Error("Not authenticated");
    }

    const user = await ctx.db.get(userId);
    if (!user) {
      throw new Error("User not found");
    }

    if (name !== undefined) {
      await ctx.db.patch(userId, { name });
    }

    return { success: true };
  },
});

/**
 * Delete user account
 */
export const deleteAccount = mutation({
  args: {},
  handler: async (ctx) => {
    const userId = await auth.getUserId(ctx);
    if (!userId) {
      throw new Error("Not authenticated");
    }

    // Delete user preferences
    const preferences = await ctx.db
      .query("preferences")
      .withIndex("by_user", (q) => q.eq("userId", userId))
      .collect();
    
    for (const pref of preferences) {
      await ctx.db.delete(pref._id);
    }

    // Delete user account
    await ctx.db.delete(userId);

    return { success: true };
  },
});
