import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

export const get = query({
  args: {},
  handler: async (ctx) => {
    return await ctx.db.query("publicMessages").collect();
  },
});

export const send = mutation({
  args: { text: v.string() },
  handler: async (ctx, { text }) => {
    const message = { text };
    return await ctx.db.insert("publicMessages", message);
  },
});