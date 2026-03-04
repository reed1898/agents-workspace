/**
 * avatar.ts - Avatar Management Module
 */
import { AvatarKitApi } from './api';
import {
  AvatarConfig,
  AvatarCreateOptions,
} from './types';

export interface AvatarManagerOptions {
  api: AvatarKitApi;
  storage?: AvatarStorage;
}

export interface AvatarStorage {
  get(): Promise<AvatarConfig | null>;
  set(avatar: AvatarConfig): Promise<void>;
  delete(): Promise<void>;
}

// Default in-memory storage
class MemoryStorage implements AvatarStorage {
  private avatar: AvatarConfig | null = null;

  async get(): Promise<AvatarConfig | null> {
    return this.avatar;
  }

  async set(avatar: AvatarConfig): Promise<void> {
    this.avatar = avatar;
  }

  async delete(): Promise<void> {
    this.avatar = null;
  }
}

export class AvatarManager {
  private api: AvatarKitApi;
  private storage: AvatarStorage;
  private cachedAvatar: AvatarConfig | null = null;

  constructor(options: AvatarManagerOptions) {
    this.api = options.api;
    this.storage = options.storage || new MemoryStorage();
  }

  /**
   * Create a new avatar
   */
  async create(options: AvatarCreateOptions): Promise<AvatarConfig> {
    // Merge with defaults
    const defaults: Partial<AvatarCreateOptions> = {
      name: '小晴',
      gender: 'female',
      style: 'anime',
      personality: '温柔、喜欢分享生活',
    };

    const mergedOptions = { ...defaults, ...options };
    
    // Create via API
    const avatar = await this.api.createAvatar(mergedOptions as AvatarCreateOptions);
    
    // Store locally
    await this.storage.set(avatar);
    this.cachedAvatar = avatar;

    return avatar;
  }

  /**
   * Get current avatar (from cache or storage)
   */
  async get(): Promise<AvatarConfig | null> {
    if (this.cachedAvatar) {
      return this.cachedAvatar;
    }

    const avatar = await this.storage.get();
    if (avatar) {
      this.cachedAvatar = avatar;
    }

    return avatar;
  }

  /**
   * Get avatar by ID from API
   */
  async getById(id: string): Promise<AvatarConfig> {
    const avatar = await this.api.getAvatar(id);
    this.cachedAvatar = avatar;
    await this.storage.set(avatar);
    return avatar;
  }

  /**
   * Update avatar settings
   */
  async update(updates: Partial<Omit<AvatarConfig, 'id' | 'createdAt' | 'updatedAt'>>): Promise<AvatarConfig> {
    const current = await this.get();
    if (!current?.id) {
      throw new Error('No avatar exists. Create one first.');
    }

    const updated = await this.api.updateAvatar(current.id, updates);
    this.cachedAvatar = updated;
    await this.storage.set(updated);

    return updated;
  }

  /**
   * Delete current avatar
   */
  async delete(): Promise<void> {
    const current = await this.get();
    if (current?.id) {
      await this.api.deleteAvatar(current.id);
    }
    
    this.cachedAvatar = null;
    await this.storage.delete();
  }

  /**
   * Check if avatar exists
   */
  async exists(): Promise<boolean> {
    const avatar = await this.get();
    return avatar !== null;
  }

  /**
   * Get avatar description for prompts
   */
  async getDescription(): Promise<string> {
    const avatar = await this.get();
    if (!avatar) {
      return '';
    }

    const parts: string[] = [];
    
    if (avatar.name) {
      parts.push(`名字是${avatar.name}`);
    }
    
    if (avatar.gender) {
      const genderMap: Record<string, string> = {
        male: '男性',
        female: '女性',
        neutral: '中性',
      };
      parts.push(`${genderMap[avatar.gender]}角色`);
    }
    
    if (avatar.style) {
      const styleMap: Record<string, string> = {
        anime: '动漫风格',
        realistic: '写实风格',
        '3d': '3D风格',
        pixel: '像素风格',
      };
      parts.push(styleMap[avatar.style] || avatar.style);
    }
    
    if (avatar.personality) {
      parts.push(`性格${avatar.personality}`);
    }

    return parts.join('，');
  }

  /**
   * Clear cache
   */
  clearCache(): void {
    this.cachedAvatar = null;
  }
}

export default AvatarManager;
