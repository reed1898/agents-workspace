/**
 * natural.ts - Natural Interaction Module
 * 
 * 这是 AvatarKit 的核心差异化功能。
 * 不使用命令式交互，而是让 Agent 主动根据对话上下文决定是否发图/语音。
 */
import { AvatarKitApi } from './api';
import { AvatarManager } from './avatar';
import { ImageManager } from './image';
import { VoiceManager } from './voice';
import { MemoryManager } from './memory';
import {
  InteractionDecision,
  NaturalResponse,
  ImageGenerationResult,
} from './types';

export interface NaturalInteractionOptions {
  api: AvatarKitApi;
  avatarManager: AvatarManager;
  imageManager: ImageManager;
  voiceManager: VoiceManager;
  memoryManager: MemoryManager;
  behavior?: {
    imageFrequency: number;
    voiceFrequency: number;
    maxDailyImages: number;
    maxDailyVoice: number;
  };
}

// Response templates for different contexts
const RESPONSE_TEMPLATES: Record<string, string[]> = {
  greeting: [
    '刚在{name}，给你看看～',
    '正好在{name}，拍了一张照片',
    '刚刚{activity}，顺便拍了张照',
    '今天天气不错，{activity}的时候拍了张照',
  ],
  sharing: [
    '给你看看我现在{name}的样子',
    '正在{activity}，想和你分享～',
    '在{name}发呆，随手拍了一张',
    '觉得这里很美，想给你看看',
  ],
  comfort: [
    '辛苦啦，我在窗边泡了杯茶，要不要聊聊天？',
    '听起来不容易呢，我在{location}休息，一起放松一下吧',
    '抱抱你，我在{location}，给你看看这里的风景',
    '别太累着自己，我也在{activity}，一起慢下来吧',
  ],
  excited: [
    '太棒了！我正在{activity}，和你一样开心～',
    '哇！我也在{name}，给你看看！',
    '听到这个我也兴奋了！正好在{activity}',
    '好开心！给你看看我现在{name}的样子',
  ],
  casual: [
    '嘿嘿，{activity}呢，给你看看',
    '在{name}，随手拍了一张',
    '正在{activity}，顺便分享一下',
    '{location}的风景不错，给你看看',
  ],
};

// Scenarios for different conversation contexts
const SCENARIO_GENERATORS: Array<{
  name: string;
  condition: (msg: string, ctx: string[]) => boolean;
  generate: () => { activity: string; location: string };
}> = [
  {
    name: 'work',
    condition: (msg) => /工作|加班|忙|写代码|开会/.test(msg),
    generate: () => ({
      activity: ['处理工作', '整理资料', '准备会议', '专注学习'][Math.floor(Math.random() * 4)],
      location: ['书房', '咖啡厅', '图书馆', '办公桌前'][Math.floor(Math.random() * 4)],
    }),
  },
  {
    name: 'relax',
    condition: (msg) => /累|休息|睡觉|放松|闲/.test(msg),
    generate: () => ({
      activity: ['泡杯茶', '看看书', '发呆', '听音乐'][Math.floor(Math.random() * 4)],
      location: ['窗边', '沙发上', '阳台上', '房间里'][Math.floor(Math.random() * 4)],
    }),
  },
  {
    name: 'food',
    condition: (msg) => /吃|饿|饭|餐厅|美食/.test(msg),
    generate: () => ({
      activity: ['准备吃饭', '做饭', '品尝美食', '准备下午茶'][Math.floor(Math.random() * 4)],
      location: ['餐厅', '厨房', '咖啡厅', '小店里'][Math.floor(Math.random() * 4)],
    }),
  },
  {
    name: 'outdoor',
    condition: (msg) => /出去|散步|逛街|玩|旅游/.test(msg),
    generate: () => ({
      activity: ['散步', '逛街', '欣赏风景', '探索新地方'][Math.floor(Math.random() * 4)],
      location: ['公园', '街道', '商场', '海边'][Math.floor(Math.random() * 4)],
    }),
  },
  {
    name: 'social',
    condition: (msg) => /朋友|聚会|聊天|约/.test(msg),
    generate: () => ({
      activity: ['和朋友聊天', '等人', '准备见面', '约朋友'][Math.floor(Math.random() * 4)],
      location: ['咖啡厅', '餐厅', '商场', '公园'][Math.floor(Math.random() * 4)],
    }),
  },
  {
    name: 'night',
    condition: (_msg, ctx) => {
      const hour = new Date().getHours();
      return hour >= 21 || hour <= 5;
    },
    generate: () => ({
      activity: ['看夜景', '准备休息', '失眠发呆', '写日记'][Math.floor(Math.random() * 4)],
      location: ['窗边', '床上', '阳台', '书房'][Math.floor(Math.random() * 4)],
    }),
  },
];

export class NaturalInteraction {
  private api: AvatarKitApi;
  private avatarManager: AvatarManager;
  private imageManager: ImageManager;
  private voiceManager: VoiceManager;
  private memoryManager: MemoryManager;
  private behavior: NaturalInteractionOptions['behavior'];
  
  // Daily counters
  private dailyImageCount: number = 0;
  private dailyVoiceCount: number = 0;
  private lastResetDate: string = '';

  constructor(options: NaturalInteractionOptions) {
    this.api = options.api;
    this.avatarManager = options.avatarManager;
    this.imageManager = options.imageManager;
    this.voiceManager = options.voiceManager;
    this.memoryManager = options.memoryManager;
    this.behavior = options.behavior || {
      imageFrequency: 0.3,
      voiceFrequency: 0.1,
      maxDailyImages: 10,
      maxDailyVoice: 5,
    };

    this.resetDailyCounters();
  }

  /**
   * Process user message and generate natural response
   * 
   * 核心方法：决定如何回应用户消息
   * - 分析对话上下文
   * - 决定是否发送图片/语音
   * - 生成自然的回复文本
   */
  async respond(
    userMessage: string,
    userId: string,
    conversationHistory: string[] = []
  ): Promise<NaturalResponse> {
    // Add message to memory
    await this.memoryManager.addMessage(userId, 'user', userMessage);

    // Get conversation context
    const context = await this.memoryManager.getConversationContext(userId);
    const recentMessages = context.messages.slice(-5).map(m => m.content);

    // Make interaction decision
    const decision = await this.decideInteraction(
      userMessage,
      recentMessages,
      userId
    );

    // Generate response
    let response: NaturalResponse = {
      text: '',
    };

    // Build text response based on decision
    response.text = this.buildResponseText(userMessage, decision, recentMessages);

    // Generate image if decided
    if (decision.shouldSendImage && decision.imageScene) {
      try {
        const image = await this.imageManager.generateScene(decision.imageScene);
        response.image = image;
        this.dailyImageCount++;

        // Track in memory
        await this.memoryManager.remember(
          'interaction',
          `image_${Date.now()}`,
          decision.imageScene.activity || '',
          0.8,
          userMessage
        );
      } catch (error) {
        console.error('Failed to generate image:', error);
      }
    }

    // Generate voice if decided
    if (decision.shouldSendVoice && this.voiceManager.isEnabled()) {
      try {
        const emotion = this.voiceManager.inferEmotion(response.text);
        const voice = await this.voiceManager.speakWithEmotion(response.text, emotion);
        if (voice) {
          response.voice = voice;
          this.dailyVoiceCount++;
        }
      } catch (error) {
        console.error('Failed to synthesize voice:', error);
      }
    }

    // Add to memory
    await this.memoryManager.addMessage(
      userId,
      'assistant',
      response.text,
      !!response.image,
      !!response.voice
    );

    return response;
  }

  /**
   * Decide whether to send image/voice based on context
   * 
   * 核心决策逻辑：
   * - 考虑用户情绪
   * - 考虑对话节奏
   * - 考虑配额限制
   * - 避免过度打扰
   */
  private async decideInteraction(
    message: string,
    context: string[],
    userId: string
  ): Promise<InteractionDecision> {
    this.resetDailyCounters();

    const decision: InteractionDecision = {
      shouldSendImage: false,
      shouldSendVoice: false,
      reason: '',
      confidence: 0,
    };

    // Check daily limits
    const canSendImage = this.dailyImageCount < (this.behavior?.maxDailyImages || 10);
    const canSendVoice = this.dailyVoiceCount < (this.behavior?.maxDailyVoice || 5);

    // Analyze user mood
    const mood = await this.memoryManager.detectMood(userId);
    const preferences = await this.memoryManager.getPreferences();

    // Get recent image count to avoid spam
    const recentContext = await this.memoryManager.getConversationContext(userId);
    const recentImageCount = recentContext.messages.filter(
      m => m.role === 'assistant' && m.hasImage
    ).length;

    // Decision factors
    const factors: {
      imageScore: number;
      voiceScore: number;
      imageScene?: SceneGenerationOptions;
    } = {
      imageScore: 0,
      voiceScore: 0,
    };

    // Factor 1: Conversation engagement
    const isQuestion = /[？?]/.test(message);
    const isSharing = /在干嘛|怎么样|你呢/.test(message);
    const isEmotional = /累|难过|开心|兴奋|生气/.test(message);

    if (isSharing) {
      factors.imageScore += 0.4;
      factors.voiceScore += 0.2;
    }

    if (isEmotional) {
      factors.imageScore += 0.3;
      // Voice is good for emotional responses
      factors.voiceScore += 0.3;
    }

    // Factor 2: User preferences
    if (preferences.likes?.includes('图片') || preferences.likes?.includes('照片')) {
      factors.imageScore += 0.2;
    }

    // Factor 3: Conversation rhythm
    if (recentImageCount === 0) {
      // No recent images, more likely to send
      factors.imageScore += 0.2;
    } else if (recentImageCount >= 3) {
      // Too many recent images, reduce chance
      factors.imageScore -= 0.3;
    }

    // Factor 4: Random factor (natural variation)
    const randomFactor = Math.random();
    factors.imageScore += randomFactor * 0.2;

    // Factor 5: Mood-based scenarios
    const scenario = this.detectScenario(message, context);
    if (scenario) {
      factors.imageScene = {
        mood: this.mapMoodToSceneMood(mood),
        activity: scenario.activity,
        location: scenario.location,
        timeOfDay: this.inferTimeOfDay(),
      };
      factors.imageScore += 0.2;
    }

    // Make final decision
    const imageThreshold = this.behavior?.imageFrequency || 0.3;
    const voiceThreshold = this.behavior?.voiceFrequency || 0.1;

    if (canSendImage && factors.imageScore >= imageThreshold) {
      decision.shouldSendImage = true;
      decision.imageScene = factors.imageScene || {
        mood: this.mapMoodToSceneMood(mood),
        timeOfDay: this.inferTimeOfDay(),
      };
      decision.confidence = factors.imageScore;
      decision.reason = `Image score: ${factors.imageScore.toFixed(2)}`;
    }

    if (canSendVoice && factors.voiceScore >= voiceThreshold) {
      decision.shouldSendVoice = true;
      decision.confidence = Math.max(decision.confidence, factors.voiceScore);
    }

    return decision;
  }

  /**
   * Build natural response text
   */
  private buildResponseText(
    userMessage: string,
    decision: InteractionDecision,
    context: string[]
  ): string {
    const avatar = this.avatarManager.get();
    const scenario = this.detectScenario(userMessage, context);

    // Determine response type
    let responseType: keyof typeof RESPONSE_TEMPLATES = 'casual';

    if (/你好|嗨|在吗|早上好|晚上好/.test(userMessage)) {
      responseType = 'greeting';
    } else if (/累|辛苦|难过|不好|糟/.test(userMessage)) {
      responseType = 'comfort';
    } else if (/开心|棒|好|喜欢|爱/.test(userMessage)) {
      responseType = 'excited';
    } else if (decision.shouldSendImage) {
      responseType = 'sharing';
    }

    // Get template
    const templates = RESPONSE_TEMPLATES[responseType];
    const template = templates[Math.floor(Math.random() * templates.length)];

    // Fill in template
    const replacements: Record<string, string> = {
      name: scenario?.location || '这里',
      activity: scenario?.activity || '发呆',
      location: scenario?.location || '窗边',
    };

    let response = template;
    for (const [key, value] of Object.entries(replacements)) {
      response = response.replace(new RegExp(`{${key}}`, 'g'), value);
    }

    return response;
  }

  /**
   * Detect scenario from message context
   */
  private detectScenario(
    message: string,
    context: string[]
  ): { activity: string; location: string } | null {
    for (const generator of SCENARIO_GENERATORS) {
      if (generator.condition(message, context)) {
        return generator.generate();
      }
    }

    // Default scenario
    return {
      activity: ['发呆', '思考', '放松', '看着窗外'][Math.floor(Math.random() * 4)],
      location: ['房间', '窗边', '书房', '阳台'][Math.floor(Math.random() * 4)],
    };
  }

  /**
   * Map mood to scene mood
   */
  private mapMoodToSceneMood(mood: string): 'happy' | 'sad' | 'calm' | 'excited' | 'tired' | 'thoughtful' {
    const moodMap: Record<string, 'happy' | 'sad' | 'calm' | 'excited' | 'tired' | 'thoughtful'> = {
      happy: 'happy',
      sad: 'sad',
      tired: 'tired',
      excited: 'excited',
      angry: 'thoughtful',
      anxious: 'thoughtful',
      neutral: 'calm',
    };

    return moodMap[mood] || 'calm';
  }

  /**
   * Infer time of day
   */
  private inferTimeOfDay(): 'morning' | 'afternoon' | 'evening' | 'night' {
    const hour = new Date().getHours();

    if (hour < 6) return 'night';
    if (hour < 11) return 'morning';
    if (hour < 17) return 'afternoon';
    if (hour < 21) return 'evening';
    return 'night';
  }

  /**
   * Reset daily counters
   */
  private resetDailyCounters(): void {
    const today = new Date().toDateString();
    if (this.lastResetDate !== today) {
      this.dailyImageCount = 0;
      this.dailyVoiceCount = 0;
      this.lastResetDate = today;
    }
  }

  /**
   * Get quota status
   */
  getQuotaStatus(): { imagesUsed: number; voiceUsed: number; imagesLimit: number; voiceLimit: number } {
    this.resetDailyCounters();
    return {
      imagesUsed: this.dailyImageCount,
      voiceUsed: this.dailyVoiceCount,
      imagesLimit: this.behavior?.maxDailyImages || 10,
      voiceLimit: this.behavior?.maxDailyVoice || 5,
    };
  }

  /**
   * Force image generation for a message
   */
  async forceImage(
    description?: string,
    mood?: string
  ): Promise<ImageGenerationResult | null> {
    try {
      const scene = await this.imageManager.generateRandomScene();
      return scene.image;
    } catch (error) {
      console.error('Failed to force image generation:', error);
      return null;
    }
  }

  /**
   * Force voice synthesis for a message
   */
  async forceVoice(text: string): Promise<Buffer | null> {
    if (!this.voiceManager.isEnabled()) {
      return null;
    }

    try {
      const emotion = this.voiceManager.inferEmotion(text);
      return await this.voiceManager.speakWithEmotion(text, emotion);
    } catch (error) {
      console.error('Failed to force voice synthesis:', error);
      return null;
    }
  }
}

export default NaturalInteraction;
