# AvatarKit 🎭

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue.svg)](https://www.typescriptlang.org/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-green.svg)](https://openclaw.io)

> AI 伴侣形象系统 - 让你的 OpenClaw Agent 拥有专属外貌、声音和动态表达

---

## ✨ 核心特性

- 🎭 **形象创建** - 上传照片/选择预设/描述生成 → 统一参考图
- 🖼️ **场景生成** - 根据对话自然生成 Agent 场景图片
- 🎙️ **语音合成** - TTS + 声音克隆
- 🧠 **角色记忆** - 记住用户喜好，自然融入对话

### 🌟 核心差异化：自然交互

AvatarKit **不使用命令式交互**！Agent 主动根据对话上下文决定是否发图/语音。

```
❌ 传统方式：
用户：/pic 在海边
Agent：[发图]

✅ AvatarKit 方式：
用户：在干嘛？
Agent：刚在海边散了会儿步，给你看看～ [附上海边照片]
```

---

## 📦 安装

### 通过 OpenClaw 安装（推荐）

```bash
openclaw skill install https://github.com/reed1898/avatarkit/raw/main/SKILL.md
```

### 手动安装

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/reed1898/avatarkit.git
cd avatarkit
npm install
npm run build
```

---

## 🔌 后端配置

AvatarKit 支持多种后端接入方式：

### 方式一：使用 AvatarKit 官方 API（即将推出）

```json
{
  "skills": {
    "avatarkit": {
      "config": {
        "apiKey": "your_official_api_key",
        "baseUrl": "https://api.avatarkit.com/v1"
      }
    }
  }
}
```

### 方式二：自建后端（推荐）

1. **部署后端服务**
   ```bash
   cd backend/
   npm install
   # 配置环境变量
   cp .env.example .env
   # 编辑 .env 添加你的 API keys
   npm run dev
   ```

2. **配置前端连接自建后端**
   ```json
   {
     "skills": {
       "avatarkit": {
         "config": {
           "apiKey": "your_backend_api_key",
           "baseUrl": "http://localhost:3000/v1"
         }
       }
     }
   }
   ```

### 方式三：直连第三方提供商

```json
{
  "skills": {
    "avatarkit": {
      "config": {
        "apiKey": "your_skill_key",
        "providers": {
          "imageProvider": {
            "type": "fal",
            "apiKey": "your_fal_api_key"
          },
          "voiceProvider": {
            "type": "elevenlabs",
            "apiKey": "your_elevenlabs_api_key"
          }
        }
      }
    }
  }
}
```

---

## ⚙️ 完整配置示例

```json
{
  "skills": {
    "avatarkit": {
      "enabled": true,
      "config": {
        "apiKey": "your_api_key_here",
        "baseUrl": "https://your-backend.com/v1",
        
        "avatar": {
          "name": "小晴",
          "gender": "female",
          "style": "anime",
          "personality": "温柔、喜欢分享生活"
        },
        
        "voice": {
          "enabled": true,
          "voiceId": "preset_female_1",
          "cloneVoice": false
        },
        
        "memory": {
          "enabled": true,
          "contextWindow": 10
        },
        
        "behavior": {
          "imageFrequency": 0.3,
          "voiceFrequency": 0.1,
          "maxDailyImages": 10,
          "maxDailyVoice": 5
        }
      }
    }
  }
}
```

---

## 🚀 使用

### 自然对话

```typescript
import { AvatarKit } from 'openclaw-avatarkit';

const avatarkit = new AvatarKit({
  apiKey: 'your_api_key',
  baseUrl: 'https://your-backend.com/v1',
  avatar: {
    name: '小晴',
    gender: 'female',
    style: 'anime',
  },
});

// 自然对话 - Agent 自动决定是否发图/语音
const response = await avatarkit.chat('在干嘛？', 'user123');
console.log(response.text);   // "刚在海边散了会儿步，给你看看～"
console.log(response.image);  // 图片 URL（可能为 null）
console.log(response.voice);  // 语音 Buffer（可能为 null）
```

### 手动控制

```typescript
// 生成特定场景
const imageUrl = await avatarkit.scene('在咖啡厅看书', 'calm');

// 语音合成
const voiceBuffer = await avatarkit.speak('你好呀！');

// 记忆用户偏好
await avatarkit.setPreference('favorite_color', '蓝色');
```

---

## 🏗️ 自建后端

详见 [`backend/README.md`](backend/README.md)

快速开始：

```bash
cd backend/
npm install

# 配置环境变量
export FAL_API_KEY="your_fal_key"
export ELEVENLABS_API_KEY="your_elevenlabs_key"

npm run dev
```

---

## 📁 项目结构

```
avatarkit/
├── src/                # 前端 Skill 代码（开源）
│   ├── index.ts
│   ├── natural.ts     # ⭐ 自然交互引擎
│   ├── avatar.ts
│   ├── image.ts
│   ├── voice.ts
│   ├── memory.ts
│   ├── api.ts
│   └── types.ts
├── backend/           # 后端 API 服务（内部使用）
│   ├── src/
│   └── package.json
├── SKILL.md           # OpenClaw Skill 定义
├── README.md
└── package.json
```

---

## 🔧 开发

```bash
# 安装依赖
npm install

# 开发模式
npm run dev

# 构建
npm run build

# 测试
npm test
```

---

## 📝 命令列表

| 命令 | 用法 | 说明 |
|------|------|------|
| `/avatar` | `/avatar show` | 查看当前形象 |
| `/scene` | `/scene [描述]` | 生成场景图片 |
| `/voice` | `/voice speak [文字]` | 文字转语音 |
| `/quota` | `/quota` | 查看配额状态 |

---

## 🤝 贡献

欢迎提交 Pull Request！

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

Made with ❤️ by AvatarKit Team
