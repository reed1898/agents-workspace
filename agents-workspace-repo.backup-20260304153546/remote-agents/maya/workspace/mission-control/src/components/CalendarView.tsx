"use client";

import { useQuery, useMutation } from "convex/react";
import { api } from "@/lib/api";
import {
  startOfWeek,
  endOfWeek,
  addDays,
  format,
  isSameDay,
  startOfDay,
  addWeeks,
  subWeeks,
  isToday,
} from "date-fns";
import { useState } from "react";
import {
  ChevronLeft,
  ChevronRight,
  Plus,
  Clock,
  CheckCircle,
  Circle,
  AlertCircle,
  X,
} from "lucide-react";

export function CalendarView() {
  const [currentWeek, setCurrentWeek] = useState(new Date());
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedSlot, setSelectedSlot] = useState<{
    date: Date;
    hour: number;
  } | null>(null);

  const weekStart = startOfWeek(currentWeek, { weekStartsOn: 1 });
  const weekEnd = endOfWeek(currentWeek, { weekStartsOn: 1 });

  const tasks = useQuery(api.activities.getTasksByWeek, {
    weekStart: weekStart.getTime(),
  });

  const createTask = useMutation(api.activities.createScheduledTask);
  const updateTaskStatus = useMutation(api.activities.updateTaskStatus);

  const weekDays = Array.from({ length: 7 }, (_, i) => addDays(weekStart, i));
  const hours = Array.from({ length: 24 }, (_, i) => i);

  const handlePrevWeek = () => setCurrentWeek(subWeeks(currentWeek, 1));
  const handleNextWeek = () => setCurrentWeek(addWeeks(currentWeek, 1));
  const handleToday = () => setCurrentWeek(new Date());

  const getTasksForSlot = (date: Date, hour: number) => {
    const slotStart = new Date(date);
    slotStart.setHours(hour, 0, 0, 0);
    const slotEnd = new Date(date);
    slotEnd.setHours(hour + 1, 0, 0, 0);

    return (
      tasks?.filter((task: any) => {
        const taskStart = new Date(task.startTime);
        return taskStart >= slotStart && taskStart < slotEnd;
      }) || []
    );
  };

  const getTasksForDay = (date: Date) => {
    return (
      tasks?.filter((task: any) => {
        const taskStart = new Date(task.startTime);
        return isSameDay(taskStart, date);
      }) || []
    );
  };

  const handleAddTask = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!selectedSlot) return;

    const formData = new FormData(e.currentTarget);
    const title = formData.get("title") as string;
    const description = formData.get("description") as string;
    const priority = formData.get("priority") as "low" | "medium" | "high";

    const startTime = new Date(selectedSlot.date);
    startTime.setHours(selectedSlot.hour, 0, 0, 0);

    await createTask({
      title,
      description,
      startTime: startTime.getTime(),
      endTime: startTime.getTime() + 60 * 60 * 1000,
      status: "pending",
      priority,
      tags: [],
      recurrence: "none",
    });

    setShowAddModal(false);
    setSelectedSlot(null);
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "high":
        return "bg-red-500/20 text-red-400 border-red-500/30";
      case "medium":
        return "bg-yellow-500/20 text-yellow-400 border-yellow-500/30";
      case "low":
        return "bg-green-500/20 text-green-400 border-green-500/30";
      default:
        return "bg-gray-500/20 text-gray-400 border-gray-500/30";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "completed":
        return <CheckCircle size={14} className="text-green-400" />;
      case "in_progress":
        return <Clock size={14} className="text-yellow-400" />;
      case "cancelled":
        return <X size={14} className="text-red-400" />;
      default:
        return <Circle size={14} className="text-gray-400" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-[var(--foreground)]">
            Calendar
          </h2>
          <p className="text-[var(--muted-foreground)] mt-1">
            Weekly view of your scheduled tasks
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={handleToday}
            className="px-4 py-2 bg-[var(--secondary)] text-[var(--foreground)] rounded-lg hover:bg-[var(--border)] transition-colors"
          >
            Today
          </button>
          <div className="flex items-center bg-[var(--secondary)] rounded-lg">
            <button
              onClick={handlePrevWeek}
              className="p-2 hover:bg-[var(--border)] transition-colors rounded-l-lg"
            >
              <ChevronLeft size={20} />
            </button>
            <span className="px-4 text-sm font-medium">
              {format(weekStart, "MMM d")} - {format(weekEnd, "MMM d, yyyy")}
            </span>
            <button
              onClick={handleNextWeek}
              className="p-2 hover:bg-[var(--border)] transition-colors rounded-r-lg"
            >
              <ChevronRight size={20} />
            </button>
          </div>
        </div>
      </div>

      {/* Calendar Grid */}
      <div className="bg-[var(--card)] rounded-xl border border-[var(--border)] overflow-hidden">
        {/* Days Header */}
        <div className="grid grid-cols-8 border-b border-[var(--border)]">
          <div className="p-4 text-sm font-medium text-[var(--muted-foreground)] border-r border-[var(--border)]">
            Time
          </div>
          {weekDays.map((day) => (
            <div
              key={day.toISOString()}
              className={`p-4 text-center border-r border-[var(--border)] last:border-r-0 ${
                isToday(day) ? "bg-[var(--primary)]/10" : ""
              }`}
            >
              <div className="text-sm font-medium text-[var(--foreground)]">
                {format(day, "EEE")}
              </div>
              <div
                className={`text-lg font-bold ${
                  isToday(day)
                    ? "text-[var(--primary)]"
                    : "text-[var(--foreground)]"
                }`}
              >
                {format(day, "d")}
              </div>
              <div className="mt-2 space-y-1">
                {getTasksForDay(day)
                  .slice(0, 3)
                  .map((task: any) => (
                    <div
                      key={task._id}
                      className={`text-xs px-2 py-1 rounded border ${getPriorityColor(
                        task.priority
                      )} truncate`}
                    >
                      {getStatusIcon(task.status)}
                      <span className="ml-1">{task.title}</span>
                    </div>
                  ))}
                {getTasksForDay(day).length > 3 && (
                  <div className="text-xs text-[var(--muted-foreground)]">
                    +{getTasksForDay(day).length - 3} more
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Time Grid */}
        <div className="max-h-[500px] overflow-y-auto">
          {hours.map((hour) => (
            <div key={hour} className="grid grid-cols-8 min-h-[60px]">
              <div className="p-2 text-xs text-[var(--muted-foreground)] border-r border-[var(--border)] border-b flex items-start justify-center">
                {format(new Date().setHours(hour, 0, 0, 0), "h a")}
              </div>
              {weekDays.map((day) => {
                const slotTasks = getTasksForSlot(day, hour);
                return (
                  <div
                    key={`${day.toISOString()}-${hour}`}
                    className="border-r border-b border-[var(--border)] last:border-r-0 p-1 relative hover:bg-[var(--secondary)]/50 transition-colors cursor-pointer"
                    onClick={() => {
                      setSelectedSlot({ date: day, hour });
                      setShowAddModal(true);
                    }}
                  >
                    <button className="absolute top-1 right-1 opacity-0 hover:opacity-100 transition-opacity">
                      <Plus size={14} className="text-[var(--primary)]" />
                    </button>
                    <div className="space-y-1">
                      {slotTasks.map((task: any) => (
                        <div
                          key={task._id}
                          className={`text-xs px-2 py-1 rounded border ${getPriorityColor(
                            task.priority
                          )} truncate flex items-center gap-1`}
                          onClick={(e) => {
                            e.stopPropagation();
                            if (task.status !== "completed") {
                              updateTaskStatus({
                                taskId: task._id,
                                status: "completed",
                              });
                            }
                          }}
                        >
                          {getStatusIcon(task.status)}
                          <span className="truncate">{task.title}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>
          ))}
        </div>
      </div>

      {/* Legend */}
      <div className="flex items-center gap-6 text-sm">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-red-500/20 border border-red-500/30" />
          <span className="text-[var(--muted-foreground)]">High Priority</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-yellow-500/20 border border-yellow-500/30" />
          <span className="text-[var(--muted-foreground)]">Medium Priority</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-green-500/20 border border-green-500/30" />
          <span className="text-[var(--muted-foreground)]">Low Priority</span>
        </div>
        <div className="flex items-center gap-2">
          <CheckCircle size={14} className="text-green-400" />
          <span className="text-[var(--muted-foreground)]">Completed</span>
        </div>
      </div>

      {/* Add Task Modal */}
      {showAddModal && selectedSlot && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-[var(--card)] rounded-xl border border-[var(--border)] p-6 w-full max-w-md">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-[var(--foreground)]">
                Add Task
              </h3>
              <button
                onClick={() => {
                  setShowAddModal(false);
                  setSelectedSlot(null);
                }}
                className="p-1 hover:bg-[var(--secondary)] rounded transition-colors"
              >
                <X size={20} />
              </button>
            </div>

            <form onSubmit={handleAddTask} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-[var(--foreground)] mb-1">
                  Date & Time
                </label>
                <div className="text-sm text-[var(--muted-foreground)]">
                  {format(selectedSlot.date, "EEEE, MMMM d")} at{" "}
                  {format(
                    new Date().setHours(selectedSlot.hour, 0, 0, 0),
                    "h:mm a"
                  )}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-[var(--foreground)] mb-1">
                  Title
                </label>
                <input
                  name="title"
                  type="text"
                  required
                  className="w-full px-3 py-2 bg-[var(--background)] border border-[var(--border)] rounded-lg text-[var(--foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
                  placeholder="Enter task title"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-[var(--foreground)] mb-1">
                  Description
                </label>
                <textarea
                  name="description"
                  rows={3}
                  className="w-full px-3 py-2 bg-[var(--background)] border border-[var(--border)] rounded-lg text-[var(--foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)] resize-none"
                  placeholder="Enter task description"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-[var(--foreground)] mb-1">
                  Priority
                </label>
                <select
                  name="priority"
                  defaultValue="medium"
                  className="w-full px-3 py-2 bg-[var(--background)] border border-[var(--border)] rounded-lg text-[var(--foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>

              <button
                type="submit"
                className="w-full px-4 py-2 bg-[var(--primary)] text-white rounded-lg hover:bg-[var(--primary)]/90 transition-colors font-medium"
              >
                Add Task
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
