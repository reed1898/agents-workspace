/**
 * SKILL.md - OpenClaw Skill Definition
 * AvatarKit - AI 伴侣形象系统
 */

export interface SkillManifest {
  name: string;
  version: string;
  description: string;
  author: string;
  homepage: string;
  repository: string;
  license: string;
  
  // OpenClaw Integration
  openclaw: {
    version: string;
    hooks: {
      onMessage: boolean;
      onReaction: boolean;
      onCommand: boolean;
    };
    commands?: Array<{
      name: string;
      description: string;
      usage: string;
    }>;
  };
  
  // Configuration Schema
  config: {
    apiKey: {
      type: 'string';
      required: true;
      description: 'AvatarKit API Key';
    };
    avatar: {
      type: 'object';
      required: false;
      properties: {
        name: { type: 'string'; default: '小晴'; };
        gender: { type: 'string'; enum: ['male', 'female', 'neutral']; default: 'female'; };
        style: { type: 'string'; enum: ['anime', 'realistic', '3d', 'pixel']; default: 'anime'; };
        personality: { type: 'string'; default: '温柔、喜欢分享生活'; };
        referenceImage: { type: 'string'; description: 'Reference image URL or path'; };
      };
    };
    voice: {
      type: 'object';
      required: false;
      properties: {
        enabled: { type: 'boolean'; default: true; };
        voiceId: { type: 'string'; default: 'preset_female_1'; };
        cloneVoice: { type: 'boolean'; default: false; };
      };
    };
    memory: {
      type: 'object';
      required: false;
      properties: {
        enabled: { type: 'boolean'; default: true; };
        contextWindow: { type: 'number'; default: 10; description: 'Number of messages to remember'; };
      };
    };
    behavior: {
      type: 'object';
      required: false;
      properties: {
        imageFrequency: { type: 'number'; default: 0.3; description: 'Probability of sending image (0-1)'; };
        voiceFrequency: { type: 'number'; default: 0.1; description: 'Probability of sending voice (0-1)'; };
        maxDailyImages: { type: 'number'; default: 10; };
        maxDailyVoice: { type: 'number'; default: 5; };
      };
    };
  };
  
  // API Endpoints
  api: {
    baseUrl: string;
    version: string;
    endpoints: {
      avatar: {
        create: { method: 'POST'; path: '/avatar/create'; };
        get: { method: 'GET'; path: '/avatar/{id}'; };
        update: { method: 'PUT'; path: '/avatar/{id}'; };
        delete: { method: 'DELETE'; path: '/avatar/{id}'; };
      };
      image: {
        generate: { method: 'POST'; path: '/image/generate'; };
        scene: { method: 'POST'; path: '/image/scene'; };
        status: { method: 'GET'; path: '/image/{id}/status'; };
      };
      voice: {
        synthesize: { method: 'POST'; path: '/voice/synthesize'; };
        clone: { method: 'POST'; path: '/voice/clone'; };
        list: { method: 'GET'; path: '/voice/list'; };
      };
      quota: {
        get: { method: 'GET'; path: '/quota'; };
        usage: { method: 'GET'; path: '/quota/usage'; };
      };
    };
  };
}

// Default manifest
export const manifest: SkillManifest = {
  name: 'avatarkit',
  version: '0.1.0',
  description: 'AI 伴侣形象系统 - 让你的 Agent 拥有专属外貌、声音和动态表达',
  author: 'AvatarKit Team',
  homepage: 'https://avatarkit.com',
  repository: 'https://github.com/avatarkit/avatarkit-skill',
  license: 'MIT',
  
  openclaw: {
    version: '>=0.5.0',
    hooks: {
      onMessage: true,
      onReaction: false,
      onCommand: true,
    },
    commands: [
      {
        name: 'avatar',
        description: '管理你的 Agent 形象',
        usage: '/avatar [create|set|show]',
      },
      {
        name: 'scene',
        description: '生成特定场景图片',
        usage: '/scene [description]',
      },
      {
        name: 'voice',
        description: '语音相关设置',
        usage: '/voice [speak|clone|list]',
      },
    ],
  },
  
  config: {
    apiKey: {
      type: 'string',
      required: true,
      description: 'AvatarKit API Key',
    },
    avatar: {
      type: 'object',
      required: false,
      properties: {
        name: { type: 'string', default: '小晴' },
        gender: { type: 'string', enum: ['male', 'female', 'neutral'], default: 'female' },
        style: { type: 'string', enum: ['anime', 'realistic', '3d', 'pixel'], default: 'anime' },
        personality: { type: 'string', default: '温柔、喜欢分享生活' },
        referenceImage: { type: 'string', description: 'Reference image URL or path' },
      },
    },
    voice: {
      type: 'object',
      required: false,
      properties: {
        enabled: { type: 'boolean', default: true },
        voiceId: { type: 'string', default: 'preset_female_1' },
        cloneVoice: { type: 'boolean', default: false },
      },
    },
    memory: {
      type: 'object',
      required: false,
      properties: {
        enabled: { type: 'boolean', default: true },
        contextWindow: { type: 'number', default: 10, description: 'Number of messages to remember' },
      },
    },
    behavior: {
      type: 'object',
      required: false,
      properties: {
        imageFrequency: { type: 'number', default: 0.3, description: 'Probability of sending image (0-1)' },
        voiceFrequency: { type: 'number', default: 0.1, description: 'Probability of sending voice (0-1)' },
        maxDailyImages: { type: 'number', default: 10 },
        maxDailyVoice: { type: 'number', default: 5 },
      },
    },
  },
  
  api: {
    baseUrl: 'https://api.avatarkit.com',
    version: 'v1',
    endpoints: {
      avatar: {
        create: { method: 'POST', path: '/avatar/create' },
        get: { method: 'GET', path: '/avatar/{id}' },
        update: { method: 'PUT', path: '/avatar/{id}' },
        delete: { method: 'DELETE', path: '/avatar/{id}' },
      },
      image: {
        generate: { method: 'POST', path: '/image/generate' },
        scene: { method: 'POST', path: '/image/scene' },
        status: { method: 'GET', path: '/image/{id}/status' },
      },
      voice: {
        synthesize: { method: 'POST', path: '/voice/synthesize' },
        clone: { method: 'POST', path: '/voice/clone' },
        list: { method: 'GET', path: '/voice/list' },
      },
      quota: {
        get: { method: 'GET', path: '/quota' },
        usage: { method: 'GET', path: '/quota/usage' },
      },
    },
  },
};

export default manifest;
