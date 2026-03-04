/**
 * api.ts - API Client for AvatarKit Service
 * 
 * 支持自定义后端 API，可配置 baseUrl 和 model providers
 */
import axios, { AxiosInstance, AxiosResponse } from 'axios';
import FormData from 'form-data';
import {
  ApiConfig,
  AvatarConfig,
  AvatarCreateOptions,
  ImageGenerationOptions,
  ImageGenerationResult,
  SceneGenerationOptions,
  VoiceSynthesisOptions,
  VoiceCloneOptions,
  Voice,
  QuotaInfo,
  QuotaUsage,
} from './types';

export interface ProviderConfig {
  // 图片生成提供商配置
  imageProvider?: {
    type: 'fal' | 'replicate' | 'custom';
    apiKey: string;
    endpoint?: string;
  };
  // 语音合成提供商配置
  voiceProvider?: {
    type: 'elevenlabs' | 'azure' | 'custom';
    apiKey: string;
    endpoint?: string;
  };
}

export class AvatarKitApi {
  private client: AxiosInstance;
  private config: ApiConfig;
  private providers?: ProviderConfig;

  constructor(config: ApiConfig, providers?: ProviderConfig) {
    this.config = {
      baseUrl: 'https://api.avatarkit.com/v1',
      timeout: 30000,
      ...config,
    };
    this.providers = providers;

    this.client = axios.create({
      baseURL: this.config.baseUrl,
      timeout: this.config.timeout,
      headers: {
        'Authorization': `Bearer ${this.config.apiKey}`,
        'Content-Type': 'application/json',
      },
    });

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 429) {
          throw new Error('QUOTA_EXCEEDED: API quota exceeded. Please upgrade your plan.');
        }
        if (error.response?.status === 401) {
          throw new Error('UNAUTHORIZED: Invalid API key.');
        }
        throw error;
      }
    );
  }

  // ==================== Avatar API ====================

  async createAvatar(options: AvatarCreateOptions): Promise<AvatarConfig> {
    const response: AxiosResponse<AvatarConfig> = await this.client.post('/avatar/create', options);
    return response.data;
  }

  async getAvatar(id: string): Promise<AvatarConfig> {
    const response: AxiosResponse<AvatarConfig> = await this.client.get(`/avatar/${id}`);
    return response.data;
  }

  async updateAvatar(id: string, options: Partial<AvatarConfig>): Promise<AvatarConfig> {
    const response: AxiosResponse<AvatarConfig> = await this.client.put(`/avatar/${id}`, options);
    return response.data;
  }

  async deleteAvatar(id: string): Promise<void> {
    await this.client.delete(`/avatar/${id}`);
  }

  // ==================== Image API ====================

  async generateImage(options: ImageGenerationOptions): Promise<ImageGenerationResult> {
    // 如果使用自定义图片提供商
    if (this.providers?.imageProvider?.type === 'custom') {
      return this.generateImageWithCustomProvider(options);
    }

    const response: AxiosResponse<ImageGenerationResult> = await this.client.post('/image/generate', options);
    return response.data;
  }

  async generateScene(options: SceneGenerationOptions): Promise<ImageGenerationResult> {
    const response: AxiosResponse<ImageGenerationResult> = await this.client.post('/image/scene', options);
    return response.data;
  }

  async getImageStatus(id: string): Promise<ImageGenerationResult> {
    const response: AxiosResponse<ImageGenerationResult> = await this.client.get(`/image/${id}/status`);
    return response.data;
  }

  async waitForImage(id: string, maxAttempts = 60, intervalMs = 2000): Promise<ImageGenerationResult> {
    for (let attempt = 0; attempt < maxAttempts; attempt++) {
      const result = await this.getImageStatus(id);
      
      if (result.status === 'completed') {
        return result;
      }
      
      if (result.status === 'failed') {
        throw new Error(`Image generation failed: ${result.error || 'Unknown error'}`);
      }

      await this.sleep(intervalMs);
    }

    throw new Error('Image generation timeout');
  }

  // ==================== Voice API ====================

  async synthesizeVoice(options: VoiceSynthesisOptions): Promise<Buffer> {
    // 如果使用自定义语音提供商
    if (this.providers?.voiceProvider?.type === 'custom') {
      return this.synthesizeVoiceWithCustomProvider(options);
    }

    const response = await this.client.post('/voice/synthesize', options, {
      responseType: 'arraybuffer',
    });
    return Buffer.from(response.data);
  }

  async cloneVoice(options: VoiceCloneOptions): Promise<Voice> {
    const formData = new FormData();
    
    if (typeof options.audioData === 'string') {
      // Base64 string
      formData.append('audio', Buffer.from(options.audioData, 'base64'), {
        filename: 'voice.mp3',
        contentType: 'audio/mpeg',
      });
    } else {
      // Buffer
      formData.append('audio', options.audioData, {
        filename: 'voice.mp3',
        contentType: 'audio/mpeg',
      });
    }
    
    formData.append('name', options.name);
    if (options.description) {
      formData.append('description', options.description);
    }

    const response: AxiosResponse<Voice> = await this.client.post('/voice/clone', formData, {
      headers: formData.getHeaders(),
    });

    return response.data;
  }

  async listVoices(): Promise<Voice[]> {
    const response: AxiosResponse<Voice[]> = await this.client.get('/voice/list');
    return response.data;
  }

  // ==================== Quota API ====================

  async getQuota(): Promise<QuotaInfo> {
    const response: AxiosResponse<QuotaInfo> = await this.client.get('/quota');
    return response.data;
  }

  async getQuotaUsage(): Promise<QuotaUsage> {
    const response: AxiosResponse<QuotaUsage> = await this.client.get('/quota/usage');
    return response.data;
  }

  // ==================== Custom Provider Handlers ====================

  private async generateImageWithCustomProvider(
    options: ImageGenerationOptions
  ): Promise<ImageGenerationResult> {
    const endpoint = this.providers?.imageProvider?.endpoint;
    if (!endpoint) {
      throw new Error('Custom image provider endpoint not configured');
    }

    const response = await axios.post(endpoint, {
      prompt: options.prompt,
      width: options.width,
      height: options.height,
      seed: options.seed,
    }, {
      headers: {
        'Authorization': `Bearer ${this.providers?.imageProvider?.apiKey}`,
        'Content-Type': 'application/json',
      },
    });

    return {
      id: response.data.id || `custom_${Date.now()}`,
      url: response.data.url || response.data.image_url,
      status: 'completed',
    };
  }

  private async synthesizeVoiceWithCustomProvider(
    options: VoiceSynthesisOptions
  ): Promise<Buffer> {
    const endpoint = this.providers?.voiceProvider?.endpoint;
    if (!endpoint) {
      throw new Error('Custom voice provider endpoint not configured');
    }

    const response = await axios.post(endpoint, {
      text: options.text,
      voice_id: options.voiceId,
      speed: options.speed,
    }, {
      headers: {
        'Authorization': `Bearer ${this.providers?.voiceProvider?.apiKey}`,
        'Content-Type': 'application/json',
      },
      responseType: 'arraybuffer',
    });

    return Buffer.from(response.data);
  }

  // ==================== Utility ====================

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

export default AvatarKitApi;
