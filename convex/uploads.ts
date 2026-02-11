import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

export const createUpload = mutation({
  args: {
    userId: v.id("users"),
    imagePath: v.string(),
    createdAt: v.float64(),
  },
  handler: async (ctx, args) => {
    const id = await ctx.db.insert("uploads", {
      userId: args.userId,
      imagePath: args.imagePath,
      createdAt: args.createdAt,
    });
    const upload = await ctx.db.get(id);
    return upload!;
  },
});

export const getUploadById = query({
  args: { uploadId: v.id("uploads") },
  handler: async (ctx, args) => {
    const upload = await ctx.db.get(args.uploadId);
    return upload ?? null;
  },
});

export const getUploadsByUser = query({
  args: { userId: v.id("users") },
  handler: async (ctx, args) => {
    const uploads = await ctx.db
      .query("uploads")
      .withIndex("by_user", (q) => q.eq("userId", args.userId))
      .order("desc")
      .collect();
    return uploads;
  },
});

