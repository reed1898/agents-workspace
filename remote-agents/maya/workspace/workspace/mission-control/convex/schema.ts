import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  // Activities - records of actions and tasks completed
  activities: defineTable({
    type: v.union(
      v.literal("task_completed"),
      v.literal("task_created"),
      v.literal("document_created"),
      v.literal("document_updated"),
      v.literal("memory_added"),
      v.literal("search_performed"),
      v.literal("system")
    ),
    title: v.string(),
    description: v.optional(v.string()),
    metadata: v.optional(v.record(v.string(), v.any())),
    userId: v.optional(v.string()),
    timestamp: v.number(),
  })
    .index("by_timestamp", ["timestamp"])
    .index("by_type", ["type"])
    .searchIndex("search_title", {
      searchField: "title",
    }),

  // Scheduled tasks for calendar view
  scheduledTasks: defineTable({
    title: v.string(),
    description: v.optional(v.string()),
    startTime: v.number(),
    endTime: v.optional(v.number()),
    status: v.union(
      v.literal("pending"),
      v.literal("in_progress"),
      v.literal("completed"),
      v.literal("cancelled")
    ),
    priority: v.union(v.literal("low"), v.literal("medium"), v.literal("high")),
    userId: v.optional(v.string()),
    tags: v.optional(v.array(v.string())),
    recurrence: v.optional(
      v.union(
        v.literal("daily"),
        v.literal("weekly"),
        v.literal("monthly"),
        v.literal("none")
      )
    ),
  })
    .index("by_startTime", ["startTime"])
    .index("by_status", ["status"])
    .searchIndex("search_title", {
      searchField: "title",
    }),

  // Searchable documents/memories
  documents: defineTable({
    title: v.string(),
    content: v.string(),
    type: v.union(
      v.literal("memory"),
      v.literal("document"),
      v.literal("note"),
      v.literal("task")
    ),
    tags: v.optional(v.array(v.string())),
    userId: v.optional(v.string()),
    createdAt: v.number(),
    updatedAt: v.number(),
    source: v.optional(v.string()),
  })
    .index("by_createdAt", ["createdAt"])
    .index("by_type", ["type"])
    .searchIndex("search_content", {
      searchField: "content",
    })
    .searchIndex("search_title", {
      searchField: "title",
    }),
});
