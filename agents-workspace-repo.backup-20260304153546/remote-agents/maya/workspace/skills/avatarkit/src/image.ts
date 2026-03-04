/**
 * image.ts - Image Generation Module
 */
import { AvatarKitApi } from './api';
import { AvatarManager } from './avatar';
import {
  ImageGenerationOptions,
  ImageGenerationResult,
  SceneGenerationOptions,
} from './types';

export interface ImageManagerOptions {
  api: AvatarKitApi;
  avatarManager: AvatarManager;
  defaultSize?: { width: number; height: number };
}

// Scene templates for natural interaction
const SCENE_TEMPLATES: Record<string, string[]> = {
  happy: [
    '在阳光下微笑',
    '坐在咖啡厅里看书',
    '在公园里散步',
    '和朋友聊天',
    '在做喜欢的事情',
  ],
  calm: [
    '在窗边喝茶',
    '看着窗外的风景',
    '在书房里静坐',
    '听雨声',
    '在花园里发呆',
  ],
  tired: [
    '趴在桌上休息',
    '靠在沙发上',
    '在床边放松',
    '揉着眼睛',
    '伸懒腰',
  ],
  thoughtful: [
    '望着远方思考',
    '托腮发呆',
    '在笔记本上写字',
    '看着夜空',
    '独自散步',
  ],
  excited: [
    '在海边奔跑',
    '举着手欢呼',
    '在夜市里逛',
    '尝试新的事物',
    '开心地笑',
  ],
  sad: [
    '看着雨景',
    '抱着膝盖坐着',
    '看着窗外发呆',
    '一个人走着',
    '低着头',
  ],
};

const LOCATION_TEMPLATES: Record<string, string[]> = {
  home: ['房间', '窗边', '书房', '厨房', '阳台', '客厅'],
  outdoor: ['公园', '街道', '海边', '山顶', '咖啡厅', '图书馆'],
  nature: ['森林', '花田', '湖边', '草地', '樱花树下', '竹林'],
  urban: ['城市夜景', '天桥', '地铁站', '商场', '写字楼', '小巷'],
};

export class ImageManager {
  private api: AvatarKitApi;
  private avatarManager: AvatarManager;
  private defaultSize: { width: number; height: number };

  constructor(options: ImageManagerOptions) {
    this.api = options.api;
    this.avatarManager = options.avatarManager;
    this.defaultSize = options.defaultSize || { width: 1024, height: 1024 };
  }

  /**
   * Generate a custom image
   */
  async generate(options: ImageGenerationOptions): Promise<ImageGenerationResult> {
    const result = await this.api.generateImage({
      width: this.defaultSize.width,
      height: this.defaultSize.height,
      ...options,
    });

    // Wait for completion
    return this.api.waitForImage(result.id);
  }

  /**
   * Generate a scene image with avatar
   */
  async generateScene(options: SceneGenerationOptions): Promise<ImageGenerationResult> {
    const avatar = await this.avatarManager.get();
    const avatarDescription = await this.avatarManager.getDescription();

    // Build scene prompt
    const prompt = this.buildScenePrompt(options, avatarDescription);

    const result = await this.api.generateScene({
      ...options,
      prompt,
      width: options.width || this.defaultSize.width,
      height: options.height || this.defaultSize.height,
    });

    return this.api.waitForImage(result.id);
  }

  /**
   * Generate a random scene
   */
  async generateRandomScene(): Promise<{
    image: ImageGenerationResult;
    scene: SceneGenerationOptions;
  }> {
    const moods = Object.keys(SCENE_TEMPLATES) as Array<keyof typeof SCENE_TEMPLATES>;
    const mood = moods[Math.floor(Math.random() * moods.length)];
    
    const locations = Object.values(LOCATION_TEMPLATES).flat();
    const location = locations[Math.floor(Math.random() * locations.length)];

    const scene: SceneGenerationOptions = {
      mood,
      location,
      activity: this.getRandomActivity(mood),
      timeOfDay: this.getRandomTimeOfDay(),
    };

    const image = await this.generateScene(scene);

    return { image, scene };
  }

  /**
   * Generate scene for a specific context
   */
  async generateContextualScene(
    userMessage: string,
    conversationContext: string[]
  ): Promise<ImageGenerationResult | null> {
    // Analyze user message to determine appropriate scene
    const mood = this.inferMood(userMessage, conversationContext);
    const activity = this.inferActivity(userMessage);
    const location = this.inferLocation(userMessage);
    const timeOfDay = this.inferTimeOfDay();

    const scene: SceneGenerationOptions = {
      mood,
      activity,
      location,
      timeOfDay,
    };

    return this.generateScene(scene);
  }

  /**
   * Build a complete scene prompt
   */
  private buildScenePrompt(options: SceneGenerationOptions, avatarDescription: string): string {
    const parts: string[] = [];

    // Avatar description
    if (avatarDescription) {
      parts.push(avatarDescription);
    }

    // Activity
    if (options.activity) {
      parts.push(`正在${options.activity}`);
    }

    // Location
    if (options.location) {
      parts.push(`在${options.location}`);
    }

    // Time of day
    if (options.timeOfDay) {
      const timeMap: Record<string, string> = {
        morning: '早晨',
        afternoon: '下午',
        evening: '傍晚',
        night: '夜晚',
      };
      parts.push(timeMap[options.timeOfDay]);
    }

    // Mood
    if (options.mood) {
      const moodMap: Record<string, string> = {
        happy: '开心的表情',
        sad: '难过的表情',
        calm: '平静的表情',
        excited: '兴奋的表情',
        tired: '疲惫的表情',
        thoughtful: '沉思的表情',
      };
      parts.push(moodMap[options.mood]);
    }

    // Add quality modifiers
    parts.push('高质量', '精美细节', '柔和光线');

    return parts.join('，');
  }

  /**
   * Infer mood from message context
   */
  private inferMood(message: string, context: string[]): SceneGenerationOptions['mood'] {
    const text = (message + ' ' + context.join(' ')).toLowerCase();

    const moodKeywords: Record<string, string[]> = {
      happy: ['开心', '高兴', '快乐', '棒', '好', '喜欢', '爱', '哈哈', '嘻嘻'],
      sad: ['难过', '伤心', '哭', '累', '痛苦', '不好', '糟', '郁闷'],
      tired: ['累', '疲惫', '困', '睡觉', '休息', '倦'],
      excited: ['兴奋', '激动', '期待', '哇', '太棒了', ' amazing'],
      calm: ['平静', '安静', '放松', '舒服', '惬意'],
      thoughtful: ['想', '思考', '考虑', '也许', '可能', '担心'],
    };

    for (const [mood, keywords] of Object.entries(moodKeywords)) {
      if (keywords.some(kw => text.includes(kw))) {
        return mood as SceneGenerationOptions['mood'];
      }
    }

    return 'calm'; // Default mood
  }

  /**
   * Infer activity from message
   */
  private inferActivity(message: string): string {
    const activityPatterns: Record<string, string[]> = {
      '工作': ['工作', '加班', '写代码', '开会', '忙'],
      '学习': ['学习', '看书', '上课', '复习', '考试'],
      '休息': ['休息', '睡觉', '躺', '放松'],
      '吃饭': ['吃', '饭', '餐厅', '饿'],
      '运动': ['运动', '跑步', '健身', '瑜伽'],
      '逛街': ['逛街', '买东西', '购物', '商场'],
    };

    for (const [activity, keywords] of Object.entries(activityPatterns)) {
      if (keywords.some(kw => message.includes(kw))) {
        return activity;
      }
    }

    // Default activities
    const defaults = ['发呆', '看着窗外', '思考', '放松', '享受时光'];
    return defaults[Math.floor(Math.random() * defaults.length)];
  }

  /**
   * Infer location from message
   */
  private inferLocation(message: string): string {
    const locationPatterns: Record<string, string[]> = {
      '房间': ['家', '房间', '床上', '沙发'],
      '咖啡厅': ['咖啡', '咖啡厅', '咖啡馆'],
      '公园': ['公园', '户外', '散步'],
      '海边': ['海', '沙滩', '海边'],
      '图书馆': ['图书馆', '书店', '看书'],
    };

    for (const [location, keywords] of Object.entries(locationPatterns)) {
      if (keywords.some(kw => message.includes(kw))) {
        return location;
      }
    }

    // Random location
    const allLocations = Object.values(LOCATION_TEMPLATES).flat();
    return allLocations[Math.floor(Math.random() * allLocations.length)];
  }

  /**
   * Infer time of day
   */
  private inferTimeOfDay(): SceneGenerationOptions['timeOfDay'] {
    const hour = new Date().getHours();
    
    if (hour < 6) return 'night';
    if (hour < 11) return 'morning';
    if (hour < 17) return 'afternoon';
    if (hour < 21) return 'evening';
    return 'night';
  }

  /**
   * Get random activity for mood
   */
  private getRandomActivity(mood: string): string {
    const activities = SCENE_TEMPLATES[mood] || SCENE_TEMPLATES.calm;
    return activities[Math.floor(Math.random() * activities.length)];
  }

  /**
   * Get random time of day
   */
  private getRandomTimeOfDay(): SceneGenerationOptions['timeOfDay'] {
    const times: SceneGenerationOptions['timeOfDay'][] = ['morning', 'afternoon', 'evening', 'night'];
    return times[Math.floor(Math.random() * times.length)];
  }
}

export default ImageManager;
