/**
 * Mock API for development without Convex authentication
 * This will be replaced by actual Convex codegen when connected
 */
export const api = {
  activities: {
    getActivities: "activities:getActivities" as any,
    createActivity: "activities:createActivity" as any,
    getScheduledTasks: "activities:getScheduledTasks" as any,
    getTasksByWeek: "activities:getTasksByWeek" as any,
    createScheduledTask: "activities:createScheduledTask" as any,
    updateTaskStatus: "activities:updateTaskStatus" as any,
    deleteTask: "activities:deleteTask" as any,
    getDocuments: "activities:getDocuments" as any,
    createDocument: "activities:createDocument" as any,
    updateDocument: "activities:updateDocument" as any,
    searchAll: "activities:searchAll" as any,
  },
};
