import { defineSchema, defineTable } from "convex/server";
import { authTables } from "@convex-dev/auth/server";
import { v } from "convex/values";

// The schema is entirely optional.
// You can delete this file (schema.ts) and the
// app will continue to work.
// The schema provides more precise TypeScript types.
export default defineSchema({
  // Auth tables for @convex-dev/auth
  ...authTables,
  
  // Custom user profile table
  users: defineTable({
    name: v.optional(v.string()),
    email: v.string(),
    image: v.optional(v.string()),
    // Add other user profile fields as needed
  }).index("by_email", ["email"]),
  
  // Example table for future expansion
  preferences: defineTable({
    userId: v.id("users"),
    language: v.optional(v.string()),
    theme: v.optional(v.string()),
    notifications: v.optional(v.boolean()),
  }).index("by_user", ["userId"]),
});