/**
 * types.ts - Shared Type Definitions
 */

// Avatar Types
export interface AvatarConfig {
  id?: string;
  name: string;
  gender: 'male' | 'female' | 'neutral';
  style: 'anime' | 'realistic' | '3d' | 'pixel';
  personality: string;
  referenceImage?: string;
  createdAt?: Date;
  updatedAt?: Date;
}

export interface AvatarCreateOptions {
  name?: string;
  gender?: 'male' | 'female' | 'neutral';
  style?: 'anime' | 'realistic' | '3d' | 'pixel';
  personality?: string;
  referenceImage?: string; // URL or base64
  referenceDescription?: string;
}

// Image Types
export interface ImageGenerationOptions {
  prompt: string;
  negativePrompt?: string;
  width?: number;
  height?: number;
  style?: string;
  seed?: number;
}

export interface SceneGenerationOptions extends ImageGenerationOptions {
  mood?: 'happy' | 'sad' | 'calm' | 'excited' | 'tired' | 'thoughtful';
  activity?: string;
  location?: string;
  timeOfDay?: 'morning' | 'afternoon' | 'evening' | 'night';
}

export interface ImageGenerationResult {
  id: string;
  url: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress?: number;
  error?: string;
}

// Voice Types
export interface VoiceConfig {
  enabled: boolean;
  voiceId: string;
  cloneVoice: boolean;
  clonedVoiceId?: string;
}

export interface VoiceSynthesisOptions {
  text: string;
  voiceId?: string;
  speed?: number;
  emotion?: 'neutral' | 'happy' | 'sad' | 'excited' | 'calm';
}

export interface VoiceCloneOptions {
  audioData: Buffer | string; // Buffer or base64
  name: string;
  description?: string;
}

export interface Voice {
  id: string;
  name: string;
  description: string;
  previewUrl?: string;
  gender: 'male' | 'female' | 'neutral';
}

// Memory Types
export interface MemoryEntry {
  id: string;
  type: 'preference' | 'interaction' | 'fact' | 'emotion';
  key: string;
  value: string;
  confidence: number;
  timestamp: Date;
  context?: string;
}

export interface ConversationContext {
  userId: string;
  messages: Array<{
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
    hasImage?: boolean;
    hasVoice?: boolean;
  }>;
  currentMood?: string;
  lastInteractionAt?: Date;
}

// Natural Interaction Types
export interface InteractionDecision {
  shouldSendImage: boolean;
  shouldSendVoice: boolean;
  imagePrompt?: string;
  voiceText?: string;
  imageScene?: SceneGenerationOptions;
  reason: string;
  confidence: number;
}

export interface NaturalResponse {
  text: string;
  image?: ImageGenerationResult;
  voice?: Buffer;
  actions?: Array<{
    type: 'image' | 'voice' | 'reaction';
    data?: unknown;
  }>;
}

// API Types
export interface ApiConfig {
  apiKey: string;
  baseUrl: string;
  timeout?: number;
}

export interface QuotaInfo {
  total: number;
  used: number;
  remaining: number;
  resetDate: Date;
  tier: 'free' | 'pro' | 'enterprise';
}

export interface QuotaUsage {
  imagesGenerated: number;
  voicesSynthesized: number;
  voicesCloned: number;
  apiCalls: number;
}

// Event Types
export interface SkillEvents {
  'avatar:created': { avatar: AvatarConfig };
  'avatar:updated': { avatar: AvatarConfig };
  'image:generated': { image: ImageGenerationResult };
  'voice:synthesized': { voiceId: string; duration: number };
  'memory:updated': { entry: MemoryEntry };
  'quota:exceeded': { resource: string };
}

// Configuration Types
export interface AvatarKitConfig {
  apiKey: string;
  avatar?: Partial<AvatarConfig>;
  voice?: Partial<VoiceConfig>;
  memory?: {
    enabled: boolean;
    contextWindow: number;
  };
  behavior?: {
    imageFrequency: number;
    voiceFrequency: number;
    maxDailyImages: number;
    maxDailyVoice: number;
  };
}
