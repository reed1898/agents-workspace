# AvatarKit - AI 伴侣形象系统

**Version:** 0.1.0  
**Author:** AvatarKit Team  
**License:** MIT  
**Homepage:** https://github.com/rain1898/avatarkit

---

## 简介

AvatarKit 是 OpenClaw 生态内的 AI 伴侣形象系统，让你的 Agent 拥有统一的外貌、声音和动态表达。

### 核心特性

- 🎭 **形象创建** - 上传照片/选择预设/描述生成 → 生成统一参考图
- 🖼️ **场景生成** - 根据自然语言描述生成 Agent 场景图片
- 🎙️ **语音合成** - TTS + 声音克隆
- 🧠 **角色记忆** - 记住用户喜好，自然融入对话

### 自然交互设计

AvatarKit 采用自然交互设计，Agent 会根据对话上下文主动决定是否发送图片或语音。

```
❌ 错误示例：
用户：/pic 在海边
Agent：[发图]

✅ 正确示例：
用户：在干嘛？
Agent：刚在海边散了会儿步，给你看看～ [附上海边照片]

用户：今天好累
Agent：辛苦啦，我在窗边泡了杯茶，要不要聊聊天？ [附上窗边照片]
```

---

## 安装

### 通过 OpenClaw 安装

```bash
openclaw skill install https://github.com/rain1898/avatarkit/raw/main/SKILL.md
```

### 手动安装

1. 克隆仓库
```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/rain1898/avatarkit.git avatarkit
```

2. 安装依赖
```bash
cd avatarkit
npm install
```

3. 编译
```bash
npm run build
```

---

## ⚠️ 重要：后端配置

**AvatarKit 需要后端 API 支持**，你可以选择以下方式之一：

### 方式一：自建后端（推荐）

1. 克隆仓库后，进入 backend 目录
2. 配置 FAL.ai 和 ElevenLabs API keys
3. 部署到你的服务器
4. 配置前端连接你的后端

详见 [backend/README.md](https://github.com/rain1898/avatarkit/blob/main/backend/README.md)

### 方式二：直连第三方服务

配置 providers 直接连接 FAL、ElevenLabs 等：

```json
{
  "providers": {
    "imageProvider": {
      "type": "fal",
      "apiKey": "your_fal_key"
    },
    "voiceProvider": {
      "type": "elevenlabs",
      "apiKey": "your_elevenlabs_key"
    }
  }
}
```

### 方式三：等待官方云服务

AvatarKit 官方云服务即将推出，届时可直接使用托管服务。

---

## 配置

在 OpenClaw 配置文件中添加：

```json
{
  "skills": {
    "avatarkit": {
      "enabled": true,
      "config": {
        "apiKey": "your_backend_api_key",
        "baseUrl": "https://your-backend.com/v1",
        "avatar": {
          "name": "小晴",
          "gender": "female",
          "style": "anime",
          "personality": "温柔、喜欢分享生活"
        },
        "voice": {
          "enabled": true,
          "voiceId": "preset_female_1"
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

### 配置项说明

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `apiKey` | string | - | **必需** 后端 API Key |
| `baseUrl` | string | - | **必需** 后端 API 地址 |
| `avatar.name` | string | "小晴" | Agent 名字 |
| `avatar.gender` | string | "female" | 性别: male/female/neutral |
| `avatar.style` | string | "anime" | 风格: anime/realistic/3d/pixel |
| `avatar.personality` | string | "温柔、喜欢分享生活" | 性格描述 |
| `voice.enabled` | boolean | true | 是否启用语音 |
| `voice.voiceId` | string | "preset_female_1" | 声音ID |
| `behavior.imageFrequency` | number | 0.3 | 发图概率 (0-1) |
| `behavior.voiceFrequency` | number | 0.1 | 发语音概率 (0-1) |

---

## 使用

### 自然对话

AvatarKit 会自动处理消息，无需命令：

```typescript
const avatarkit = new AvatarKit(config);

// 自然对话 - Agent 可能回复文字、图片或语音
const response = await avatarkit.chat('在干嘛？', 'user123');
console.log(response.text);  // "刚在海边散了会儿步，给你看看～"
console.log(response.image); // 图片URL
console.log(response.voice); // 语音Buffer
```

### 命令

AvatarKit 注册以下命令：

| 命令 | 用法 | 说明 |
|------|------|------|
| `/avatar` | `/avatar [create\|show]` | 管理形象 |
| `/scene` | `/scene [description]` | 生成场景图片 |
| `/voice` | `/voice [speak\|list]` | 语音相关 |
| `/quota` | `/quota` | 查看配额 |

### SDK API

```typescript
import { AvatarKit } from 'openclaw-avatarkit';

const avatarkit = new AvatarKit({
  apiKey: 'your_api_key',
  baseUrl: 'https://your-backend.com/v1',
});

// 创建形象
await avatarkit.createAvatar({
  name: '小晴',
  gender: 'female',
  style: 'anime',
});

// 自然对话
const response = await avatarkit.chat('你好！');

// 生成场景
const imageUrl = await avatarkit.scene('在咖啡厅看书');

// 语音合成
const voiceBuffer = await avatarkit.speak('你好呀！');

// 记忆用户偏好
await avatarkit.setPreference('favorite_color', '蓝色');
const prefs = await avatarkit.getPreferences();
```

---

## 技术架构

```
用户(OpenClaw)
    ↓
AvatarKit Skill (TypeScript)  ← 开源
    ↓
AvatarKit API (REST)          ← 需自建或使用官方服务
    ↓
模型供应商 (FAL/ElevenLabs等)
```

### 模块结构

```
avatarkit/
├── src/              # Skill 代码（开源）
│   ├── api.ts
│   ├── avatar.ts
│   ├── image.ts
│   ├── voice.ts
│   ├── memory.ts
│   ├── natural.ts    # ⭐ 自然交互核心
│   └── index.ts
├── backend/          # 后端服务（自建）
├── SKILL.md
└── README.md
```

---

## 开发

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

## 支持与反馈

- GitHub: https://github.com/rain1898/avatarkit
- Issues: https://github.com/rain1898/avatarkit/issues
- 文档: https://github.com/rain1898/avatarkit/blob/main/README.md

---

## 开源协议

MIT License
