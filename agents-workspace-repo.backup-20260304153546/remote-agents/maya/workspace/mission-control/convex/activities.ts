import { query, mutation } from "./_generated/server";
import { v } from "convex/values";

// ==================== ACTIVITIES ====================

export const getActivities = query({
  args: {
    limit: v.optional(v.number()),
    type: v.optional(
      v.union(
        v.literal("task_completed"),
        v.literal("task_created"),
        v.literal("document_created"),
        v.literal("document_updated"),
        v.literal("memory_added"),
        v.literal("search_performed"),
        v.literal("system")
      )
    ),
  },
  handler: async (ctx, args) => {
    let activities = ctx.db.query("activities").order("desc");
    
    if (args.type !== undefined) {
      activities = activities.withIndex("by_type", (q) => q.eq("type", args.type));
    }
    
    const results = await activities.take(args.limit || 50);
    return results;
  },
});

export const createActivity = mutation({
  args: {
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
  },
  handler: async (ctx, args) => {
    const activityId = await ctx.db.insert("activities", {
      ...args,
      timestamp: Date.now(),
    });
    return activityId;
  },
});

// ==================== SCHEDULED TASKS ====================

export const getScheduledTasks = query({
  args: {
    startTime: v.number(),
    endTime: v.number(),
  },
  handler: async (ctx, args) => {
    const tasks = await ctx.db
      .query("scheduledTasks")
      .withIndex("by_startTime", (q) =>
        q.gte("startTime", args.startTime).lte("startTime", args.endTime)
      )
      .order("asc")
      .collect();
    return tasks;
  },
});

export const getTasksByWeek = query({
  args: {
    weekStart: v.number(),
  },
  handler: async (ctx, args) => {
    const weekEnd = args.weekStart + 7 * 24 * 60 * 60 * 1000;
    const tasks = await ctx.db
      .query("scheduledTasks")
      .withIndex("by_startTime", (q) =>
        q.gte("startTime", args.weekStart).lte("startTime", weekEnd)
      )
      .order("asc")
      .collect();
    return tasks;
  },
});

export const createScheduledTask = mutation({
  args: {
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
  },
  handler: async (ctx, args) => {
    const taskId = await ctx.db.insert("scheduledTasks", args);
    
    // Log activity
    await ctx.db.insert("activities", {
      type: "task_created",
      title: `Task created: ${args.title}`,
      description: args.description,
      metadata: { taskId },
      userId: args.userId,
      timestamp: Date.now(),
    });
    
    return taskId;
  },
});

export const updateTaskStatus = mutation({
  args: {
    taskId: v.id("scheduledTasks"),
    status: v.union(
      v.literal("pending"),
      v.literal("in_progress"),
      v.literal("completed"),
      v.literal("cancelled")
    ),
  },
  handler: async (ctx, args) => {
    const task = await ctx.db.get(args.taskId);
    if (!task) throw new Error("Task not found");
    
    await ctx.db.patch(args.taskId, { status: args.status });
    
    // Log activity if completed
    if (args.status === "completed") {
      await ctx.db.insert("activities", {
        type: "task_completed",
        title: `Task completed: ${task.title}`,
        metadata: { taskId: args.taskId },
        userId: task.userId,
        timestamp: Date.now(),
      });
    }
    
    return args.taskId;
  },
});

export const deleteTask = mutation({
  args: {
    taskId: v.id("scheduledTasks"),
  },
  handler: async (ctx, args) => {
    await ctx.db.delete(args.taskId);
    return args.taskId;
  },
});

// ==================== DOCUMENTS ====================

export const getDocuments = query({
  args: {
    limit: v.optional(v.number()),
    type: v.optional(
      v.union(
        v.literal("memory"),
        v.literal("document"),
        v.literal("note"),
        v.literal("task")
      )
    ),
  },
  handler: async (ctx, args) => {
    let documents = ctx.db.query("documents").order("desc");
    
    if (args.type !== undefined) {
      documents = documents.withIndex("by_type", (q) => q.eq("type", args.type));
    }
    
    const results = await documents.take(args.limit || 50);
    return results;
  },
});

export const createDocument = mutation({
  args: {
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
    source: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const now = Date.now();
    const documentId = await ctx.db.insert("documents", {
      ...args,
      createdAt: now,
      updatedAt: now,
    });
    
    // Log activity
    await ctx.db.insert("activities", {
      type: args.type === "memory" ? "memory_added" : "document_created",
      title: `${args.type === "memory" ? "Memory" : "Document"} created: ${args.title}`,
      metadata: { documentId, type: args.type },
      userId: args.userId,
      timestamp: now,
    });
    
    return documentId;
  },
});

export const updateDocument = mutation({
  args: {
    documentId: v.id("documents"),
    title: v.optional(v.string()),
    content: v.optional(v.string()),
    tags: v.optional(v.array(v.string())),
  },
  handler: async (ctx, args) => {
    const { documentId, ...updates } = args;
    await ctx.db.patch(documentId, {
      ...updates,
      updatedAt: Date.now(),
    });
    
    // Log activity
    const doc = await ctx.db.get(documentId);
    await ctx.db.insert("activities", {
      type: "document_updated",
      title: `Document updated: ${doc?.title || "Unknown"}`,
      metadata: { documentId },
      userId: doc?.userId,
      timestamp: Date.now(),
    });
    
    return documentId;
  },
});

// ==================== GLOBAL SEARCH ====================

export const searchAll = query({
  args: {
    query: v.string(),
    limit: v.optional(v.number()),
  },
  handler: async (ctx, args) => {
    const limit = args.limit || 20;
    
    // Search activities
    const activities = await ctx.db
      .query("activities")
      .withSearchIndex("search_title", (q) => q.search("title", args.query))
      .take(limit);
    
    // Search documents
    const documentsByTitle = await ctx.db
      .query("documents")
      .withSearchIndex("search_title", (q) => q.search("title", args.query))
      .take(limit);
    
    const documentsByContent = await ctx.db
      .query("documents")
      .withSearchIndex("search_content", (q) => q.search("content", args.query))
      .take(limit);
    
    // Search tasks
    const tasks = await ctx.db
      .query("scheduledTasks")
      .withSearchIndex("search_title", (q) => q.search("title", args.query))
      .take(limit);
    
    // Combine and deduplicate documents
    const documentIds = new Set();
    const uniqueDocuments = [];
    for (const doc of [...documentsByTitle, ...documentsByContent]) {
      if (!documentIds.has(doc._id)) {
        documentIds.add(doc._id);
        uniqueDocuments.push(doc);
      }
    }
    
    // Log search activity
    await ctx.db.insert("activities", {
      type: "search_performed",
      title: `Search: "${args.query}"`,
      metadata: {
        query: args.query,
        resultsCount: activities.length + uniqueDocuments.length + tasks.length,
      },
      timestamp: Date.now(),
    });
    
    return {
      activities,
      documents: uniqueDocuments,
      tasks,
      totalResults: activities.length + uniqueDocuments.length + tasks.length,
    };
  },
});
