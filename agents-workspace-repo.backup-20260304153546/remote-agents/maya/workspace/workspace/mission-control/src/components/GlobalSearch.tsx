"use client";

import { useQuery, useMutation } from "convex/react";
import { api } from "@/lib/api";
import { useState, useEffect } from "react";
import {
  Search,
  FileText,
  CheckCircle,
  Brain,
  Clock,
  Plus,
  X,
  Filter,
  Loader2,
} from "lucide-react";
import { formatDistanceToNow } from "date-fns";

const typeIcons = {
  memory: Brain,
  document: FileText,
  note: FileText,
  task: CheckCircle,
  activity: Clock,
};

const typeColors = {
  memory: "text-pink-500 bg-pink-500/10",
  document: "text-purple-500 bg-purple-500/10",
  note: "text-yellow-500 bg-yellow-500/10",
  task: "text-blue-500 bg-blue-500/10",
  activity: "text-cyan-500 bg-cyan-500/10",
};

export function GlobalSearch() {
  const [query, setQuery] = useState("");
  const [debouncedQuery, setDebouncedQuery] = useState("");
  const [activeFilters, setActiveFilters] = useState<string[]>([]);
  const [showAddModal, setShowAddModal] = useState(false);
  const [addType, setAddType] = useState<"memory" | "document" | "note">(
    "memory"
  );

  // Debounce search query
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedQuery(query);
    }, 300);
    return () => clearTimeout(timer);
  }, [query]);

  const searchResults = useQuery(
    api.activities.searchAll,
    debouncedQuery.length >= 2
      ? { query: debouncedQuery, limit: 20 }
      : "skip"
  );

  const createDocument = useMutation(api.activities.createDocument);

  const filters = [
    { id: "activities", label: "Activities" },
    { id: "documents", label: "Documents" },
    { id: "tasks", label: "Tasks" },
  ];

  const handleAddDocument = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const title = formData.get("title") as string;
    const content = formData.get("content") as string;
    const tags = (formData.get("tags") as string)
      .split(",")
      .map((t) => t.trim())
      .filter(Boolean);

    await createDocument({
      title,
      content,
      type: addType,
      tags,
    });

    setShowAddModal(false);
  };

  const filteredResults = () => {
    if (!searchResults) return null;

    let results: any[] = [];

    if (
      activeFilters.length === 0 ||
      activeFilters.includes("activities")
    ) {
      results = [...results, ...searchResults.activities.map((a: any) => ({ ...a, resultType: "activity" }))];
    }

    if (activeFilters.length === 0 || activeFilters.includes("documents")) {
      results = [...results, ...searchResults.documents.map((d: any) => ({ ...d, resultType: "document" }))];
    }

    if (activeFilters.length === 0 || activeFilters.includes("tasks")) {
      results = [...results, ...searchResults.tasks.map((t: any) => ({ ...t, resultType: "task" }))];
    }

    return results.sort((a, b) => {
      const aTime = a.timestamp || a.createdAt || 0;
      const bTime = b.timestamp || b.createdAt || 0;
      return bTime - aTime;
    });
  };

  const toggleFilter = (filterId: string) => {
    setActiveFilters((prev) =>
      prev.includes(filterId)
        ? prev.filter((f) => f !== filterId)
        : [...prev, filterId]
    );
  };

  const highlightText = (text: string, query: string) => {
    if (!query) return text;
    const regex = new RegExp(`(${query})`, "gi");
    const parts = text.split(regex);
    return parts.map((part, i) =>
      regex.test(part) ? (
        <span key={i} className="bg-[var(--primary)]/30 text-[var(--primary)]">
          {part}
        </span>
      ) : (
        part
      )
    );
  };

  const results = filteredResults();

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-[var(--foreground)]">
            Global Search
          </h2>
          <p className="text-[var(--muted-foreground)] mt-1">
            Search across all memories, documents, and tasks
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => {
              setAddType("memory");
              setShowAddModal(true);
            }}
            className="flex items-center gap-2 px-4 py-2 bg-[var(--secondary)] text-[var(--foreground)] rounded-lg hover:bg-[var(--border)] transition-colors"
          >
            <Brain size={18} />
            Add Memory
          </button>
          <button
            onClick={() => {
              setAddType("document");
              setShowAddModal(true);
            }}
            className="flex items-center gap-2 px-4 py-2 bg-[var(--secondary)] text-[var(--foreground)] rounded-lg hover:bg-[var(--border)] transition-colors"
          >
            <FileText size={18} />
            Add Doc
          </button>
        </div>
      </div>

      {/* Search Bar */}
      <div className="relative">
        <Search
          className="absolute left-4 top-1/2 -translate-y-1/2 text-[var(--muted-foreground)]"
          size={20}
        />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search anything..."
          className="w-full pl-12 pr-4 py-4 bg-[var(--card)] border border-[var(--border)] rounded-xl text-[var(--foreground)] placeholder:text-[var(--muted-foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)] text-lg"
        />
        {query && (
          <button
            onClick={() => setQuery("")}
            className="absolute right-4 top-1/2 -translate-y-1/2 p-1 hover:bg-[var(--secondary)] rounded transition-colors"
          >
            <X size={18} className="text-[var(--muted-foreground)]" />
          </button>
        )}
      </div>

      {/* Filters */}
      <div className="flex items-center gap-2 flex-wrap">
        <Filter size={18} className="text-[var(--muted-foreground)]" />
        {filters.map((filter) => (
          <button
            key={filter.id}
            onClick={() => toggleFilter(filter.id)}
            className={`px-3 py-1.5 text-sm rounded-full transition-colors ${
              activeFilters.includes(filter.id)
                ? "bg-[var(--primary)] text-white"
                : "bg-[var(--secondary)] text-[var(--foreground)] hover:bg-[var(--border)]"
            }`}
          >
            {filter.label}
          </button>
        ))}
      </div>

      {/* Results */}
      <div className="space-y-4">
        {query.length > 0 && query.length < 2 && (
          <div className="text-center py-12">
            <Search
              size={48}
              className="mx-auto text-[var(--muted-foreground)] mb-4"
            />
            <p className="text-[var(--muted-foreground)]">
              Type at least 2 characters to search
            </p>
          </div>
        )}

        {query.length >= 2 && !searchResults && (
          <div className="text-center py-12">
            <Loader2
              size={48}
              className="mx-auto text-[var(--primary)] mb-4 animate-spin"
            />
            <p className="text-[var(--muted-foreground)]">Searching...</p>
          </div>
        )}

        {searchResults && results?.length === 0 && (
          <div className="text-center py-12">
            <Search
              size={48}
              className="mx-auto text-[var(--muted-foreground)] mb-4"
            />
            <p className="text-[var(--muted-foreground)]">No results found</p>
            <p className="text-sm text-[var(--muted-foreground)] mt-1">
              Try a different search term
            </p>
          </div>
        )}

        {results?.map((result: any) => {
          const Icon = typeIcons[result.resultType as keyof typeof typeIcons] || FileText;
          const colorClass = typeColors[result.resultType as keyof typeof typeColors] || typeColors.document;
          const title = result.title || "Untitled";
          const content = result.content || result.description || "";
          const timestamp = result.timestamp || result.createdAt || Date.now();

          return (
            <div
              key={`${result.resultType}-${result._id}`}
              className="p-4 bg-[var(--card)] rounded-xl border border-[var(--border)] hover:border-[var(--primary)]/50 transition-colors"
            >
              <div className="flex items-start gap-4">
                <div
                  className={`flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center ${colorClass}`}
                >
                  <Icon size={20} />
                </div>

                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <h3 className="font-medium text-[var(--foreground)]">
                        {highlightText(title, debouncedQuery)}
                      </h3>
                      {content && (
                        <p className="text-sm text-[var(--muted-foreground)] mt-1 line-clamp-2">
                          {highlightText(content, debouncedQuery)}
                        </p>
                      )}
                      <div className="flex items-center gap-3 mt-2">
                        <span
                          className={`text-xs px-2 py-1 rounded-full ${colorClass}`}
                        >
                          {result.resultType}
                        </span>
                        {result.type && result.type !== result.resultType && (
                          <span className="text-xs px-2 py-1 bg-[var(--secondary)] rounded-full text-[var(--muted-foreground)]">
                            {result.type}
                          </span>
                        )}
                        {result.tags?.map((tag: string) => (
                          <span
                            key={tag}
                            className="text-xs px-2 py-1 bg-[var(--secondary)] rounded-full text-[var(--muted-foreground)]"
                          >
                            {tag}
                          </span>
                        ))}
                        <span className="text-xs text-[var(--muted-foreground)]">
                          {formatDistanceToNow(timestamp, { addSuffix: true })}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          );
        })}

        {searchResults && results && results.length > 0 && (
          <div className="text-center py-4 text-sm text-[var(--muted-foreground)]">
            Found {searchResults.totalResults} results
          </div>
        )}
      </div>

      {/* Add Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
        >
          <div className="bg-[var(--card)] rounded-xl border border-[var(--border)] p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-[var(--foreground)]">
                Add {addType === "memory" ? "Memory" : addType === "document" ? "Document" : "Note"}
              </h3>
              <button
                onClick={() => setShowAddModal(false)}
                className="p-1 hover:bg-[var(--secondary)] rounded transition-colors"
              >
                <X size={20} />
              </button>
            </div>

            <form onSubmit={handleAddDocument} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-[var(--foreground)] mb-1">
                  Type
                </label>
                <select
                  value={addType}
                  onChange={(e) =>
                    setAddType(e.target.value as "memory" | "document" | "note")
                  }
                  className="w-full px-3 py-2 bg-[var(--background)] border border-[var(--border)] rounded-lg text-[var(--foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
                >
                  <option value="memory">Memory</option>
                  <option value="document">Document</option>
                  <option value="note">Note</option>
                </select>
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
                  placeholder={`Enter ${addType} title`}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-[var(--foreground)] mb-1">
                  Content
                </label>
                <textarea
                  name="content"
                  rows={6}
                  required
                  className="w-full px-3 py-2 bg-[var(--background)] border border-[var(--border)] rounded-lg text-[var(--foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)] resize-none"
                  placeholder={`Enter ${addType} content`}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-[var(--foreground)] mb-1">
                  Tags (comma-separated)
                </label>
                <input
                  name="tags"
                  type="text"
                  className="w-full px-3 py-2 bg-[var(--background)] border border-[var(--border)] rounded-lg text-[var(--foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
                  placeholder="tag1, tag2, tag3"
                />
              </div>

              <button
                type="submit"
                className="w-full px-4 py-2 bg-[var(--primary)] text-white rounded-lg hover:bg-[var(--primary)]/90 transition-colors font-medium"
              >
                Add {addType === "memory" ? "Memory" : addType === "document" ? "Document" : "Note"}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
