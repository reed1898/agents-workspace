/**
 * memory.ts - Memory Management Module
 */
import { MemoryEntry, ConversationContext, AvatarKitConfig } from './types';

export interface MemoryManagerOptions {
  storage?: MemoryStorage;
  contextWindow?: number;
  maxEntries?: number;
}

export interface MemoryStorage {
  getEntries(type?: string): Promise<MemoryEntry[]>;
  addEntry(entry: MemoryEntry): Promise<void>;
  updateEntry(id: string, updates: Partial<MemoryEntry>): Promise<void>;
  deleteEntry(id: string): Promise<void>;
  getContext(userId: string): Promise<ConversationContext>;
  updateContext(userId: string, context: Partial<ConversationContext>): Promise<void>;
}

// In-memory storage implementation
class MemoryStorageImpl implements MemoryStorage {
  private entries: Map<string, MemoryEntry> = new Map();
  private contexts: Map<string, ConversationContext> = new Map();

  async getEntries(type?: string): Promise<MemoryEntry[]> {
    const entries = Array.from(this.entries.values());
    if (type) {
      return entries.filter(e => e.type === type);
    }
    return entries;
  }

  async addEntry(entry: MemoryEntry): Promise<void> {
    this.entries.set(entry.id, entry);
  }

  async updateEntry(id: string, updates: Partial<MemoryEntry>): Promise<void> {
    const entry = this.entries.get(id);
    if (entry) {
      this.entries.set(id, { ...entry, ...updates });
    }
  }

  async deleteEntry(id: string): Promise<void> {
    this.entries.delete(id);
  }

  async getContext(userId: string): Promise<ConversationContext> {
    return this.contexts.get(userId) || {
      userId,
      messages: [],
    };
  }

  async updateContext(userId: string, context: Partial<ConversationContext>): Promise<void> {
    const existing = this.contexts.get(userId) || { userId, messages: [] };
    this.contexts.set(userId, { ...existing, ...context });
  }
}

export class MemoryManager {
  private storage: MemoryStorage;
  private contextWindow: number;
  private maxEntries: number;

  constructor(options: MemoryManagerOptions = {}) {
    this.storage = options.storage || new MemoryStorageImpl();
    this.contextWindow = options.contextWindow || 10;
    this.maxEntries = options.maxEntries || 100;
  }

  /**
   * Add a memory entry
   */
  async remember(
    type: MemoryEntry['type'],
    key: string,
    value: string,
    confidence: number = 1.0,
    context?: string
  ): Promise<MemoryEntry> {
    // Check if entry already exists
    const existing = await this.findEntry(type, key);
    
    if (existing) {
      // Update existing entry
      await this.storage.updateEntry(existing.id, {
        value,
        confidence: Math.max(existing.confidence, confidence),
        timestamp: new Date(),
        context,
      });
      return { ...existing, value, confidence, timestamp: new Date(), context };
    }

    // Create new entry
    const entry: MemoryEntry = {
      id: this.generateId(),
      type,
      key,
      value,
      confidence,
      timestamp: new Date(),
      context,
    };

    await this.storage.addEntry(entry);
    await this.pruneIfNeeded();

    return entry;
  }

  /**
   * Recall a memory entry
   */
  async recall(type?: string, key?: string): Promise<MemoryEntry | null> {
    if (key) {
      return this.findEntry(type, key);
    }

    const entries = await this.storage.getEntries(type);
    // Return most recent high-confidence entry
    return entries
      .sort((a, b) => b.confidence - a.confidence || b.timestamp.getTime() - a.timestamp.getTime())[0] || null;
  }

  /**
   * Get all memories of a type
   */
  async getMemories(type?: string): Promise<MemoryEntry[]> {
    const entries = await this.storage.getEntries(type);
    return entries.sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime());
  }

  /**
   * Get user preferences
   */
  async getPreferences(): Promise<Record<string, string>> {
    const entries = await this.storage.getEntries('preference');
    const preferences: Record<string, string> = {};
    
    for (const entry of entries) {
      preferences[entry.key] = entry.value;
    }

    return preferences;
  }

  /**
   * Remember user preference
   */
  async rememberPreference(key: string, value: string, context?: string): Promise<void> {
    await this.remember('preference', key, value, 1.0, context);
  }

  /**
   * Add message to conversation context
   */
  async addMessage(
    userId: string,
    role: 'user' | 'assistant',
    content: string,
    hasImage?: boolean,
    hasVoice?: boolean
  ): Promise<void> {
    const context = await this.storage.getContext(userId);
    
    context.messages.push({
      role,
      content,
      timestamp: new Date(),
      hasImage,
      hasVoice,
    });

    // Keep only recent messages
    if (context.messages.length > this.contextWindow) {
      context.messages = context.messages.slice(-this.contextWindow);
    }

    context.lastInteractionAt = new Date();
    await this.storage.updateContext(userId, context);
  }

  /**
   * Get conversation context
   */
  async getConversationContext(userId: string): Promise<ConversationContext> {
    return this.storage.getContext(userId);
  }

  /**
   * Get recent messages
   */
  async getRecentMessages(userId: string, count?: number): Promise<ConversationContext['messages']> {
    const context = await this.storage.getContext(userId);
    const limit = count || this.contextWindow;
    return context.messages.slice(-limit);
  }

  /**
   * Detect user mood from conversation
   */
  async detectMood(userId: string): Promise<string> {
    const messages = await this.getRecentMessages(userId, 5);
    const text = messages.map(m => m.content).join(' ');

    const moodPatterns: Record<string, string[]> = {
      happy: ['开心', '高兴', '快乐', '喜欢', '棒', '好', '哈哈'],
      sad: ['难过', '伤心', '哭', '痛苦', '不好', '糟'],
      angry: ['生气', '烦', '讨厌', '愤怒', '气死'],
      tired: ['累', '疲惫', '困', '倦'],
      excited: ['兴奋', '激动', '期待', '太棒了'],
      anxious: ['担心', '焦虑', '紧张', '害怕'],
    };

    for (const [mood, patterns] of Object.entries(moodPatterns)) {
      if (patterns.some(p => text.includes(p))) {
        return mood;
      }
    }

    return 'neutral';
  }

  /**
   * Get favorite interactions
   */
  async getFavoriteInteractions(): Promise<MemoryEntry[]> {
    const entries = await this.storage.getEntries('interaction');
    return entries
      .filter(e => e.confidence >= 0.8)
      .sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime())
      .slice(0, 10);
  }

  /**
   * Extract preferences from message
   */
  async extractPreferences(message: string): Promise<Array<{ key: string; value: string }>> {
    const preferences: Array<{ key: string; value: string }> = [];

    // Pattern matching for preferences
    const patterns: Array<{ regex: RegExp; key: string; extractor: (match: RegExpMatchArray) => string }> = [
      { 
        regex: /喜欢(.+)/, 
        key: 'likes', 
        extractor: (m) => m[1].trim() 
      },
      { 
        regex: /不喜欢(.+)/, 
        key: 'dislikes', 
        extractor: (m) => m[1].trim() 
      },
      { 
        regex: /经常(.+)/, 
        key: 'habits', 
        extractor: (m) => m[1].trim() 
      },
      { 
        regex: /讨厌(.+)/, 
        key: 'dislikes', 
        extractor: (m) => m[1].trim() 
      },
      { 
        regex: /爱(.+)/, 
        key: 'loves', 
        extractor: (m) => m[1].trim() 
      },
    ];

    for (const pattern of patterns) {
      const match = message.match(pattern.regex);
      if (match) {
        preferences.push({
          key: pattern.key,
          value: pattern.extractor(match),
        });
      }
    }

    return preferences;
  }

  /**
   * Clear all memories
   */
  async clear(): Promise<void> {
    const entries = await this.storage.getEntries();
    for (const entry of entries) {
      await this.storage.deleteEntry(entry.id);
    }
  }

  /**
   * Find entry by type and key
   */
  private async findEntry(type?: string, key?: string): Promise<MemoryEntry | null> {
    const entries = await this.storage.getEntries(type);
    return entries.find(e => e.key === key) || null;
  }

  /**
   * Generate unique ID
   */
  private generateId(): string {
    return `mem_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Prune old entries if exceeding max
   */
  private async pruneIfNeeded(): Promise<void> {
    const entries = await this.storage.getEntries();
    
    if (entries.length > this.maxEntries) {
      // Sort by confidence and recency
      const sorted = entries.sort(
        (a, b) => a.confidence - b.confidence || a.timestamp.getTime() - b.timestamp.getTime()
      );

      // Remove lowest confidence oldest entries
      const toRemove = sorted.slice(0, entries.length - this.maxEntries);
      for (const entry of toRemove) {
        await this.storage.deleteEntry(entry.id);
      }
    }
  }
}

export default MemoryManager;
