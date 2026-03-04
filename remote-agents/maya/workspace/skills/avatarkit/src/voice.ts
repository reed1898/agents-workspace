/**
 * voice.ts - Voice Synthesis Module
 */
import { AvatarKitApi } from './api';
import { AvatarManager } from './avatar';
import {
  VoiceConfig,
  VoiceSynthesisOptions,
  VoiceCloneOptions,
  Voice,
} from './types';

export interface VoiceManagerOptions {
  api: AvatarKitApi;
  avatarManager: AvatarManager;
  config?: Partial<VoiceConfig>;
}

// Emotion to voice characteristics mapping
const EMOTION_VOICE_SETTINGS: Record<string, { speed: number; emotion: VoiceSynthesisOptions['emotion'] }> = {
  happy: { speed: 1.1, emotion: 'happy' },
  sad: { speed: 0.9, emotion: 'sad' },
  calm: { speed: 1.0, emotion: 'calm' },
  excited: { speed: 1.2, emotion: 'excited' },
  tired: { speed: 0.85, emotion: 'neutral' },
  thoughtful: { speed: 0.95, emotion: 'neutral' },
  neutral: { speed: 1.0, emotion: 'neutral' },
};

// Preset voices
const PRESET_VOICES: Voice[] = [
  { id: 'preset_female_1', name: '小雨', description: '温柔甜美的女声', gender: 'female' },
  { id: 'preset_female_2', name: '小晴', description: '活泼清新的女声', gender: 'female' },
  { id: 'preset_female_3', name: '小雅', description: '成熟知性的女声', gender: 'female' },
  { id: 'preset_male_1', name: '小明', description: '阳光开朗的男声', gender: 'male' },
  { id: 'preset_male_2', name: '小宇', description: '沉稳磁性的男声', gender: 'male' },
  { id: 'preset_male_3', name: '小杰', description: '年轻活力的男声', gender: 'male' },
  { id: 'preset_neutral_1', name: '小星', description: '中性柔和的声音', gender: 'neutral' },
];

export class VoiceManager {
  private api: AvatarKitApi;
  private avatarManager: AvatarManager;
  private config: VoiceConfig;
  private cachedVoices: Voice[] | null = null;

  constructor(options: VoiceManagerOptions) {
    this.api = options.api;
    this.avatarManager = options.avatarManager;
    this.config = {
      enabled: true,
      voiceId: 'preset_female_1',
      cloneVoice: false,
      ...options.config,
    };
  }

  /**
   * Check if voice is enabled
   */
  isEnabled(): boolean {
    return this.config.enabled;
  }

  /**
   * Enable voice
   */
  enable(): void {
    this.config.enabled = true;
  }

  /**
   * Disable voice
   */
  disable(): void {
    this.config.enabled = false;
  }

  /**
   * Get current voice config
   */
  getConfig(): VoiceConfig {
    return { ...this.config };
  }

  /**
   * Update voice config
   */
  updateConfig(updates: Partial<VoiceConfig>): void {
    this.config = { ...this.config, ...updates };
  }

  /**
   * Set voice ID
   */
  setVoice(voiceId: string): void {
    this.config.voiceId = voiceId;
  }

  /**
   * Synthesize text to speech
   */
  async speak(text: string, options?: Partial<VoiceSynthesisOptions>): Promise<Buffer | null> {
    if (!this.config.enabled) {
      return null;
    }

    // Truncate text if too long (API limit)
    const maxLength = 500;
    const truncatedText = text.length > maxLength 
      ? text.slice(0, maxLength) + '...'
      : text;

    const synthesisOptions: VoiceSynthesisOptions = {
      text: truncatedText,
      voiceId: this.config.clonedVoiceId || this.config.voiceId,
      speed: 1.0,
      emotion: 'neutral',
      ...options,
    };

    try {
      return await this.api.synthesizeVoice(synthesisOptions);
    } catch (error) {
      console.error('Voice synthesis failed:', error);
      return null;
    }
  }

  /**
   * Synthesize text with emotion
   */
  async speakWithEmotion(
    text: string,
    emotion: string,
    options?: Partial<VoiceSynthesisOptions>
  ): Promise<Buffer | null> {
    const settings = EMOTION_VOICE_SETTINGS[emotion] || EMOTION_VOICE_SETTINGS.neutral;

    return this.speak(text, {
      ...settings,
      ...options,
    });
  }

  /**
   * Clone a voice from audio
   */
  async cloneVoice(options: VoiceCloneOptions): Promise<Voice> {
    const voice = await this.api.cloneVoice(options);
    
    this.config.clonedVoiceId = voice.id;
    this.config.cloneVoice = true;

    // Clear cache
    this.cachedVoices = null;

    return voice;
  }

  /**
   * List available voices
   */
  async listVoices(): Promise<Voice[]> {
    if (this.cachedVoices) {
      return this.cachedVoices;
    }

    try {
      // Get API voices
      const apiVoices = await this.api.listVoices();
      
      // Merge with presets
      this.cachedVoices = [...PRESET_VOICES, ...apiVoices];
      return this.cachedVoices;
    } catch (error) {
      // Return presets if API fails
      return PRESET_VOICES;
    }
  }

  /**
   * Get voice by ID
   */
  async getVoice(voiceId: string): Promise<Voice | undefined> {
    const voices = await this.listVoices();
    return voices.find(v => v.id === voiceId);
  }

  /**
   * Get recommended voices for current avatar
   */
  async getRecommendedVoices(): Promise<Voice[]> {
    const avatar = await this.avatarManager.get();
    if (!avatar) {
      return PRESET_VOICES.slice(0, 3);
    }

    const voices = await this.listVoices();
    
    // Filter by gender preference
    return voices.filter(v => v.gender === avatar.gender).slice(0, 5);
  }

  /**
   * Clear voice cache
   */
  clearCache(): void {
    this.cachedVoices = null;
  }

  /**
   * Get emotion from text
   */
  inferEmotion(text: string): VoiceSynthesisOptions['emotion'] {
    const emotionMap: Record<string, string[]> = {
      happy: ['开心', '高兴', '快乐', '哈哈', '嘻嘻', '喜欢', '棒', '好'],
      sad: ['难过', '伤心', '哭', '痛苦', '糟', '不好'],
      excited: ['兴奋', '激动', '太棒了', ' amazing', '哇', '天哪'],
      calm: ['平静', '放松', '舒服', '安静'],
    };

    for (const [emotion, keywords] of Object.entries(emotionMap)) {
      if (keywords.some(kw => text.toLowerCase().includes(kw))) {
        return emotion as VoiceSynthesisOptions['emotion'];
      }
    }

    return 'neutral';
  }
}

export default VoiceManager;
