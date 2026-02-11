import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

export const createModelMetric = mutation({
  args: {
    name: v.string(),
    version: v.string(),
    accuracy: v.float64(),
    f1Score: v.float64(),
    createdAt: v.float64(),
  },
  handler: async (ctx, args) => {
    const id = await ctx.db.insert("models", {
      name: args.name,
      version: args.version,
      accuracy: args.accuracy,
      f1Score: args.f1Score,
      createdAt: args.createdAt,
    });
    const model = await ctx.db.get(id);
    return model!;
  },
});

export const getModelMetrics = query({
  args: {},
  handler: async (ctx) => {
    const models = await ctx.db.query("models").order("desc").collect();
    return models;
  },
});

export const triggerRetrain = mutation({
  args: {
    adminId: v.id("users"),
    triggeredAt: v.float64(),
  },
  handler: async (ctx, args) => {
    const id = await ctx.db.insert("retrainTriggers", {
      adminId: args.adminId,
      triggeredAt: args.triggeredAt,
    });
    const trigger = await ctx.db.get(id);
    return trigger!;
  },
});

