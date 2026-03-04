/**
 * index.ts - AvatarKit Skill Main Entry Point
 * 
 * AI 伴侣形象系统 - 让你的 Agent 拥有专属外貌、声音和动态表达
 * 
 * 支持配置：
 * - 自建后端 API
 * - 第三方模型提供商（FAL、ElevenLabs 等）
 * - 混合模式
 */
import { AvatarKitApi, ProviderConfig } from './api';
import { AvatarManager, AvatarStorage } from './avatar';
import { ImageManager } from './image';
import { VoiceManager } from './voice';
import { MemoryManager, MemoryStorage } from './memory';
import { NaturalInteraction } from './natural';
import {
  AvatarKitConfig,
  AvatarConfig,
  AvatarCreateOptions,
  ImageGenerationOptions,
  SceneGenerationOptions,
  VoiceSynthesisOptions,
  VoiceCloneOptions,
  NaturalResponse,
  QuotaInfo,
  QuotaUsage,
  MemoryEntry,
} from './types';
import { manifest } from './SKILL';

// Re-export all modules
export * from './api';
export * from './avatar';
export * from './image';
export * from './voice';
export * from './memory';
export * from './natural';
export * from './types';
export { manifest } from './SKILL';

/**
 * Extended configuration with provider options
 */
export interface AvatarKitFullConfig extends AvatarKitConfig {
  /**
   * 自定义后端 API 地址
   * 默认: https://api.avatarkit.com/v1
   */
  baseUrl?: string;
  
  /**
   * 模型提供商配置
   * 用于直接连接第三方服务，绕过自建后端
   */
  providers?: ProviderConfig;
  
  /**
   * 超时设置（毫秒）
   * 默认: 30000
   */
  timeout?: number;
}

/**
 * Main AvatarKit class - 主类
 */
export class AvatarKit {
  // Core components
  public readonly api: AvatarKitApi;
  public readonly avatar: AvatarManager;
  public readonly image: ImageManager;
  public readonly voice: VoiceManager;
  public readonly memory: MemoryManager;
  public readonly natural: NaturalInteraction;

  // Configuration
  private config: AvatarKitFullConfig;

  constructor(config: AvatarKitFullConfig) {
    this.config = config;

    // Initialize API client with custom configuration
    this.api = new AvatarKitApi(
      {
        apiKey: config.apiKey,
        baseUrl: config.baseUrl || 'https://api.avatarkit.com/v1',
        timeout: config.timeout || 30000,
      },
      config.providers
    );

    // Initialize managers
    this.avatar = new AvatarManager({
      api: this.api,
    });

    this.image = new ImageManager({
      api: this.api,
      avatarManager: this.avatar,
    });

    this.voice = new VoiceManager({
      api: this.api,
      avatarManager: this.avatar,
      config: config.voice,
    });

    this.memory = new MemoryManager({
      contextWindow: config.memory?.contextWindow || 10,
    });

    this.natural = new NaturalInteraction({
      api: this.api,
      avatarManager: this.avatar,
      imageManager: this.image,
      voiceManager: this.voice,
      memoryManager: this.memory,
      behavior: config.behavior,
    });

    // Initialize with config
    this.initialize();
  }

  /**
   * Initialize AvatarKit with configuration
   */
  private async initialize(): Promise<void> {
    // Create default avatar if specified in config
    if (this.config.avatar && !(await this.avatar.exists())) {
      try {
        await this.avatar.create(this.config.avatar as AvatarCreateOptions);
      } catch (error) {
        console.error('Failed to create default avatar:', error);
      }
    }

    // Apply voice configuration
    if (this.config.voice) {
      this.voice.updateConfig(this.config.voice);
    }
  }

  /**
   * 自然对话模式 - Natural Conversation Mode
   * 
   * 核心方法：处理用户消息，自然融入图片/语音
   */
  async chat(
    message: string,
    userId: string = 'default'
  ): Promise<NaturalResponse> {
    return this.natural.respond(message, userId);
  }

  /**
   * 快速回复 - Quick Reply
   */
  async reply(message: string, userId: string = 'default'): Promise<string> {
    const response = await this.chat(message, userId);
    return response.text;
  }

  /**
   * 生成场景图片 - Generate Scene Image
   */
  async scene(
    description: string,
    mood?: SceneGenerationOptions['mood']
  ): Promise<string | null> {
    try {
      const result = await this.image.generateScene({
        prompt: description,
        mood,
      });
      return result.url;
    } catch (error) {
      console.error('Failed to generate scene:', error);
      return null;
    }
  }

  /**
   * 语音回复 - Voice Reply
   */
  async speak(text: string): Promise<Buffer | null> {
    return this.voice.speak(text);
  }

  /**
   * 获取配额信息 - Get Quota Information
   */
  async quota(): Promise<QuotaInfo> {
    return this.api.getQuota();
  }

  /**
   * 获取配额使用情况 - Get Quota Usage
   */
  async usage(): Promise<QuotaUsage> {
    return this.api.getQuotaUsage();
  }

  /**
   * 检查是否已创建形象 - Check if avatar exists
   */
  async hasAvatar(): Promise<boolean> {
    return this.avatar.exists();
  }

  /**
   * 创建形象 - Create Avatar
   */
  async createAvatar(options: AvatarCreateOptions): Promise<AvatarConfig> {
    return this.avatar.create(options);
  }

  /**
   * 更新形象 - Update Avatar
   */
  async updateAvatar(updates: Partial<AvatarConfig>): Promise<AvatarConfig> {
    return this.avatar.update(updates);
  }

  /**
   * 获取形象信息 - Get Avatar Info
   */
  async getAvatar(): Promise<AvatarConfig | null> {
    return this.avatar.get();
  }

  /**
   * 设置记忆 - Set Memory
   */
  async remember(
    type: MemoryEntry['type'],
    key: string,
    value: string
  ): Promise<void> {
    await this.memory.remember(type, key, value);
  }

  /**
   * 获取记忆 - Get Memory
   */
  async recall(type?: string, key?: string): Promise<MemoryEntry | null> {
    return this.memory.recall(type, key);
  }

  /**
   * 设置用户偏好 - Set User Preference
   */
  async setPreference(key: string, value: string): Promise<void> {
    await this.memory.rememberPreference(key, value);
  }

  /**
   * 获取用户偏好 - Get User Preferences
   */
  async getPreferences(): Promise<Record<string, string>> {
    return this.memory.getPreferences();
  }

  // ==================== OpenClaw Integration ====================

  /**
   * OpenClaw Skill Interface - onMessage handler
   */
  async onMessage(message: {
    content: string;
    userId: string;
    channel: string;
  }): Promise<{
    text?: string;
    image?: string;
    voice?: Buffer;
    actions?: Array<{ type: string; data?: unknown }>;
  }> {
    const response = await this.chat(message.content, message.userId);

    const result: {
      text?: string;
      image?: string;
      voice?: Buffer;
      actions?: Array<{ type: string; data?: unknown }>;
    } = {
      text: response.text,
    };

    if (response.image?.url) {
      result.image = response.image.url;
    }

    if (response.voice) {
      result.voice = response.voice;
    }

    return result;
  }

  /**
   * OpenClaw Skill Interface - onCommand handler
   */
  async onCommand(
    command: string,
    args: string[],
    context: { userId: string; channel: string }
  ): Promise<{
    text?: string;
    image?: string;
    voice?: Buffer;
  }> {
    switch (command) {
      case 'avatar':
        return this.handleAvatarCommand(args);
      
      case 'scene':
        return this.handleSceneCommand(args);
      
      case 'voice':
        return this.handleVoiceCommand(args);
      
      case 'quota':
        return this.handleQuotaCommand();
      
      default:
        return { text: `Unknown command: ${command}` };
    }
  }

  // ==================== Command Handlers ====================

  private async handleAvatarCommand(args: string[]): Promise<{ text: string }> {
    const subcommand = args[0];

    switch (subcommand) {
      case 'create':
        return { text: 'Use the SDK to create an avatar programmatically.' };
      
      case 'show':
      case 'get': {
        const avatar = await this.avatar.get();
        if (avatar) {
          return {
            text: `当前形象：${avatar.name}\n风格：${avatar.style}\n性格：${avatar.personality}`,
          };
        }
        return { text: '还没有创建形象，使用 avatar.create() 创建。' };
      }
      
      default:
        return { text: 'Usage: /avatar [create|show]' };
    }
  }

  private async handleSceneCommand(args: string[]): Promise<{ text: string; image?: string }> {
    const description = args.join(' ');
    if (!description) {
      return { text: 'Usage: /scene [description]' };
    }

    try {
      const result = await this.image.generateScene({ prompt: description });
      return {
        text: `生成了场景：${description}`,
        image: result.url,
      };
    } catch (error) {
      return { text: '生成图片失败，请稍后重试。' };
    }
  }

  private async handleVoiceCommand(args: string[]): Promise<{ text: string; voice?: Buffer }> {
    const subcommand = args[0];

    switch (subcommand) {
      case 'speak': {
        const text = args.slice(1).join(' ');
        if (!text) {
          return { text: 'Usage: /voice speak [text]' };
        }
        const voice = await this.voice.speak(text);
        return { text: `语音消息：${text}`, voice: voice || undefined };
      }
      
      case 'list': {
        const voices = await this.voice.listVoices();
        const voiceList = voices.map(v => `- ${v.name}: ${v.description}`).join('\n');
        return { text: `可用声音：\n${voiceList}` };
      }
      
      default:
        return { text: 'Usage: /voice [speak|list]' };
    }
  }

  private async handleQuotaCommand(): Promise<{ text: string }> {
    try {
      const quota = await this.api.getQuota();
      return {
        text: `配额状态：\n- 总配额：${quota.total}\n- 已使用：${quota.used}\n- 剩余：${quota.remaining}\n- 等级：${quota.tier}`,
      };
    } catch (error) {
      return { text: '获取配额信息失败。' };
    }
  }
}

/**
 * Create AvatarKit instance
 */
export function createAvatarKit(config: AvatarKitFullConfig): AvatarKit {
  return new AvatarKit(config);
}

/**
 * Default export
 */
export default AvatarKit;
