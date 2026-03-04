import { httpAction } from "./_generated/server";
import { api } from "./_generated/api";
import { v } from "convex/values";

// HTTP endpoint for OpenClaw to push activities
export const pushActivity = httpAction(async (ctx, request) => {
  // Only accept POST requests
  if (request.method !== "POST") {
    return new Response("Method not allowed", { status: 405 });
  }

  try {
    const body = await request.json();
    
    // Validate required fields
    if (!body.type || !body.title) {
      return new Response(
        JSON.stringify({ error: "Missing required fields: type, title" }),
        { status: 400, headers: { "Content-Type": "application/json" } }
      );
    }

    // Validate type
    const validTypes = [
      "task_completed",
      "task_created",
      "document_created",
      "document_updated",
      "memory_added",
      "search_performed",
      "system",
    ];
    
    if (!validTypes.includes(body.type)) {
      return new Response(
        JSON.stringify({ error: `Invalid type. Must be one of: ${validTypes.join(", ")}` }),
        { status: 400, headers: { "Content-Type": "application/json" } }
      );
    }

    // Create the activity
    const activityId = await ctx.runMutation(api.activities.createActivity, {
      type: body.type,
      title: body.title,
      description: body.description,
      metadata: body.metadata || {},
      userId: body.userId || "openclaw",
    });

    return new Response(
      JSON.stringify({ success: true, activityId }),
      { status: 200, headers: { "Content-Type": "application/json" } }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({ error: "Failed to create activity", details: String(error) }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
});
