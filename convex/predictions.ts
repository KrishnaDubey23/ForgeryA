import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

export const createPrediction = mutation({
  args: {
    uploadId: v.id("uploads"),
    densenetScore: v.float64(),
    mobilenetScore: v.float64(),
    ensembleScore: v.float64(),
    severity: v.string(),
    tamperedRatio: v.float64(),
    heatmapPaths: v.array(v.string()),
    createdAt: v.float64(),
  },
  handler: async (ctx, args) => {
    const id = await ctx.db.insert("predictions", {
      uploadId: args.uploadId,
      densenetScore: args.densenetScore,
      mobilenetScore: args.mobilenetScore,
      ensembleScore: args.ensembleScore,
      severity: args.severity,
      tamperedRatio: args.tamperedRatio,
      heatmapPaths: args.heatmapPaths,
      createdAt: args.createdAt,
    });
    const prediction = await ctx.db.get(id);
    return prediction!;
  },
});

export const getPredictionsByUpload = query({
  args: { uploadId: v.id("uploads") },
  handler: async (ctx, args) => {
    const predictions = await ctx.db
      .query("predictions")
      .withIndex("by_upload", (q) => q.eq("uploadId", args.uploadId))
      .order("desc")
      .collect();
    return predictions;
  },
});

export const getHistoryByUser = query({
  args: { userId: v.id("users") },
  handler: async (ctx, args) => {
    // Fetch uploads for this user
    const uploads = await ctx.db
      .query("uploads")
      .withIndex("by_user", (q) => q.eq("userId", args.userId))
      .order("desc")
      .collect();

    const history = [];
    for (const upload of uploads) {
      const preds = await ctx.db
        .query("predictions")
        .withIndex("by_upload", (q) => q.eq("uploadId", upload._id))
        .order("desc")
        .collect();
      if (preds.length === 0) continue;
      const latest = preds[0];
      history.push({
        upload,
        prediction: latest,
      });
    }
    return history;
  },
});

