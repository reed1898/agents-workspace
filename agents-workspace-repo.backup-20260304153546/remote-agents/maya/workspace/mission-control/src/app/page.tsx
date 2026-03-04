"use client";

import { useState } from "react";
import { ActivityFeed } from "@/components/ActivityFeed";
import { CalendarView } from "@/components/CalendarView";
import { GlobalSearch } from "@/components/GlobalSearch";
import { Activity, Calendar, Search } from "lucide-react";

type Tab = "activity" | "calendar" | "search";

export default function Home() {
  const [activeTab, setActiveTab] = useState<Tab>("activity");

  const tabs = [
    { id: "activity" as Tab, label: "Activity Feed", icon: Activity },
    { id: "calendar" as Tab, label: "Calendar", icon: Calendar },
    { id: "search" as Tab, label: "Global Search", icon: Search },
  ];

  return (
    <main className="min-h-screen bg-[var(--background)]">
      {/* Header */}
      <header className="border-b border-[var(--border)] bg-[var(--card)]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-[var(--primary)] rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">M</span>
              </div>
              <h1 className="text-xl font-bold text-[var(--foreground)]">
                Mission Control
              </h1>
            </div>
            <div className="text-sm text-[var(--muted-foreground)]">
              Your personal command center
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="border-b border-[var(--border)] bg-[var(--card)]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-1">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-4 py-3 text-sm font-medium transition-colors border-b-2 ${
                    activeTab === tab.id
                      ? "border-[var(--primary)] text-[var(--primary)]"
                      : "border-transparent text-[var(--muted-foreground)] hover:text-[var(--foreground)]"
                  }`}
                >
                  <Icon size={18} />
                  {tab.label}
                </button>
              );
            })}
          </div>
        </div>
      </nav>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {activeTab === "activity" && <ActivityFeed />}
        {activeTab === "calendar" && <CalendarView />}
        {activeTab === "search" && <GlobalSearch />}
      </div>
    </main>
  );
}
