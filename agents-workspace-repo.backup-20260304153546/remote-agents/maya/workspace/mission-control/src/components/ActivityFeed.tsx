"use client";

import { useQuery, useMutation } from "convex/react";
import { api } from "@/lib/api";
import { formatDistanceToNow } from "date-fns";
import {
  CheckCircle,
  Plus,
  FileText,
  Edit,
  Brain,
  Search,
  Settings,
  Clock,
  Filter,
} from "lucide-react";
import { useState } from "react";

const activityIcons = {
  task_completed: CheckCircle,
  task_created: Plus,
  document_created: FileText,
  document_updated: Edit,
  memory_added: Brain,
  search_performed: Search,
  system: Settings,
};

const activityColors = {
  task_completed: "text-green-500",
  task_created: "text-blue-500",
  document_created: "text-purple-500",
  document_updated: "text-yellow-500",
  memory_added: "text-pink-500",
  search_performed: "text-cyan-500",
  system: "text-gray-500",
};

export function ActivityFeed() {
  const [filter, setFilter] = useState<string | null>(null);
  
  // Only pass type if filter is set
  const activities = useQuery(
    api.activities.getActivities,
    filter ? { limit: 50, type: filter as any } : { limit: 50 }
  );
  const createActivity = useMutation(api.activities.createActivity);

  const handleCreateTestActivity = async () => {
    await createActivity({
      type: "task_completed",
      title: "Test activity created",
      description: "This is a test activity",
    });
  };

  const filterOptions = [
    { value: null, label: "All Activities" },
    { value: "task_completed", label: "Completed Tasks" },
    { value: "task_created", label: "Created Tasks" },
    { value: "document_created", label: "Documents" },
    { value: "memory_added", label: "Memories" },
    { value: "search_performed", label: "Searches" },
    { value: "system", label: "System" },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-[var(--foreground)]">
            Activity Feed
          </h2>
          <p className="text-[var(--muted-foreground)] mt-1">
            Track every action and task in your system
          </p>
        </div>
        <button
          onClick={handleCreateTestActivity}
          className="flex items-center gap-2 px-4 py-2 bg-[var(--primary)] text-white rounded-lg hover:bg-[var(--primary)]/90 transition-colors"
        >
          <Plus size={18} />
          Test Activity
        </button>
      </div>

      {/* Filter */}
      <div className="flex items-center gap-2 flex-wrap">
        <Filter size={18} className="text-[var(--muted-foreground)]" />
        {filterOptions.map((option) => (
          <button
            key={option.label}
            onClick={() => setFilter(option.value)}
            className={`px-3 py-1.5 text-sm rounded-full transition-colors ${
              filter === option.value
                ? "bg-[var(--primary)] text-white"
                : "bg-[var(--secondary)] text-[var(--foreground)] hover:bg-[var(--border)]"
            }`}
          >
            {option.label}
          </button>
        ))}
      </div>

      {/* Timeline */}
      <div className="relative">
        {/* Timeline line */}
        <div className="absolute left-6 top-0 bottom-0 w-px bg-[var(--border)]" />

        <div className="space-y-4">
          {activities?.length === 0 && (
            <div className="text-center py-12">
              <Clock
                size={48}
                className="mx-auto text-[var(--muted-foreground)] mb-4"
              />
              <p className="text-[var(--muted-foreground)]">No activities yet</p>
              <p className="text-sm text-[var(--muted-foreground)] mt-1">
                Activities will appear here as you use the system
              </p>
            </div>
          )}

          {activities?.map((activity: any) => {
            const Icon = activityIcons[activity.type as keyof typeof activityIcons];
            const colorClass = activityColors[activity.type as keyof typeof activityColors];

            return (
              <div
                key={activity._id}
                className="relative flex gap-4 p-4 bg-[var(--card)] rounded-xl border border-[var(--border)] hover:border-[var(--primary)]/50 transition-colors"
              >
                {/* Icon */}
                <div
                  className={`relative z-10 flex-shrink-0 w-12 h-12 rounded-full bg-[var(--secondary)] flex items-center justify-center ${colorClass}`}
                >
                  <Icon size={20} />
                </div>

                {/* Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <h3 className="font-medium text-[var(--foreground)]">
                        {activity.title}
                      </h3>
                      {activity.description && (
                        <p className="text-sm text-[var(--muted-foreground)] mt-1">
                          {activity.description}
                        </p>
                      )}
                      <div className="flex items-center gap-3 mt-2">
                        <span className="text-xs px-2 py-1 bg-[var(--secondary)] rounded-full text-[var(--muted-foreground)]">
                          {activity.type.replace("_", " ")}
                        </span>
                        {activity.metadata && Object.keys(activity.metadata).length > 0 && (
                          <span className="text-xs text-[var(--muted-foreground)]">
                            {Object.keys(activity.metadata).length} metadata fields
                          </span>
                        )}
                      </div>
                    </div>
                    <span className="text-sm text-[var(--muted-foreground)] flex-shrink-0">
                      {formatDistanceToNow(activity.timestamp, {
                        addSuffix: true,
                      })}
                    </span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
