import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  users: defineTable({
    email: v.string(),
    passwordHash: v.string(),
    isAdmin: v.boolean(),
  }).index("by_email", ["email"]),

  uploads: defineTable({
    userId: v.id("users"),
    imagePath: v.string(),
    createdAt: v.float64(),
  }).index("by_user", ["userId"]),

  predictions: defineTable({
    uploadId: v.id("uploads"),
    densenetScore: v.float64(),
    mobilenetScore: v.float64(),
    ensembleScore: v.float64(),
    severity: v.string(),
    tamperedRatio: v.float64(),
    heatmapPaths: v.array(v.string()),
    createdAt: v.float64(),
  }).index("by_upload", ["uploadId"]),

  models: defineTable({
    name: v.string(),
    version: v.string(),
    accuracy: v.float64(),
    f1Score: v.float64(),
    createdAt: v.float64(),
  }).index("by_name", ["name"]),

  retrainTriggers: defineTable({
    adminId: v.id("users"),
    triggeredAt: v.float64(),
  }).index("by_admin", ["adminId"]),
});

