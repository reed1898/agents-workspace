# AvatarKit Skill 开发日志

## Phase 1: 项目框架搭建 (2026-02-11) ✅

### 已完成工作

#### 1. 项目结构（前后端分离）

```
avatarkit/                      ← GitHub 公开仓库（开源）
├── src/                        ← 前端 Skill 代码
│   ├── index.ts               # 主入口，支持灵活后端配置
│   ├── api.ts                 # API 客户端（支持自定义提供商）
│   ├── natural.ts             # ⭐ 自然交互引擎
│   ├── avatar.ts              # 形象管理
│   ├── image.ts               # 图片生成
│   ├── voice.ts               # 语音合成
│   ├── memory.ts              # 角色记忆
│   ├── types.ts               # 类型定义
│   └── SKILL.ts               # Skill manifest
├── backend/                    ← 后端服务（内部使用）
│   ├── README.md              # 后端部署文档
│   └── package.json           # 后端依赖
├── SKILL.md                    # OpenClaw Skill 定义（公开访问）
├── README.md                   # 完整文档（中英双语）
├── LICENSE                     # MIT 许可证
├── DEVELOPMENT.md              # 本开发日志
├── example.ts                  # 使用示例
├── package.json                # 前端依赖
└── tsconfig.json               # TypeScript 配置
```

#### 2. 后端接入方式（3种）

| 方式 | 说明 | 配置 |
|------|------|------|
| **自建后端** | 部署自己的 API 服务 | `baseUrl: "https://your-api.com/v1"` |
| **直连提供商** | 直连 FAL/ElevenLabs | `providers: { imageProvider, voiceProvider }` |
| **官方云服务** | 即将推出 | `baseUrl: "https://api.avatarkit.com/v1"` |

#### 3. 核心差异化功能 - 自然交互

**实现要点：**
- ✅ 场景检测引擎（工作/休息/吃饭/户外/社交）
- ✅ 情绪感知系统（6种情绪映射）
- ✅ 多因素决策评分（参与度+偏好+节奏+配额）
- ✅ 自然响应模板（6类场景回复）

**关键设计：**
```typescript
// 不使用命令式交互
const response = await avatarkit.chat('在干嘛？');
// response.text: "刚在海边散了会儿步，给你看看～"
// response.image: [自动生成的场景图片]
```

#### 4. GitHub 提交状态

| 项目 | 状态 |
|------|------|
| 仓库初始化 | ✅ 完成 |
| 分支名称 | ✅ `main` |
| 提交数量 | ✅ 2 个提交 |
| 文件数量 | ✅ 19 个文件 |
| 敏感信息检查 | ✅ 已清理 |
| LICENSE | ✅ MIT |
| README.md | ✅ 完整（含后端配置说明） |
| SKILL.md | ✅ 可公开访问 |

### 提交记录

```
51fcc7b feat: Add flexible backend configuration and provider support
         - Support custom backend API URL
         - Support direct third-party providers
         - Add backend/ directory
         - Update documentation

e85e38b feat: Initial AvatarKit Skill implementation
         - Complete TypeScript project structure
         - Natural interaction engine
         - Avatar, image, voice, memory modules
         - OpenClaw skill integration
```

---

## 代码统计

| 模块 | 行数 | 功能 |
|------|------|------|
| types.ts | 170 | 16种核心类型定义 |
| api.ts | 280 | API 客户端 + 自定义提供商支持 |
| avatar.ts | 165 | 形象 CRUD |
| image.ts | 320 | 场景生成 + 智能推断 |
| voice.ts | 230 | TTS + 声音克隆 |
| memory.ts | 365 | 记忆管理 + 偏好提取 |
| natural.ts | 520 | ⭐ 自然交互核心引擎 |
| index.ts | 400 | 主入口 + OpenClaw 集成 |

**总计：~2,400 行 TypeScript 代码**

---

## 后端部署说明

### 环境变量

```env
PORT=3000
API_KEY=your_secure_key
FAL_API_KEY=your_fal_key
ELEVENLABS_API_KEY=your_elevenlabs_key
```

### Docker 部署

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY backend/package*.json ./
RUN npm ci --only=production
COPY backend/ .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

---

## 下一步计划

### Phase 2（第2周）

- [ ] 完成后端核心 API 实现
- [ ] 集成 FAL.ai 图片生成
- [ ] 集成 ElevenLabs 语音
- [ ] 添加配额管理
- [ ] Docker 部署配置

### Phase 3（第3周）

- [ ] 实现形象参考图生成
- [ ] 完善场景模板库
- [ ] 优化自然交互算法
- [ ] 添加更多预设声音

### Phase 4（第4周）

- [ ] 端到端测试
- [ ] 性能优化
- [ ] 完善文档
- [ ] 演示准备

---

## 技术决策

### 1. 前后端分离
- **原因**：后端涉及 API keys 和计费，不适合开源
- **方案**：前端 Skill 开源，后端内部部署

### 2. 提供商抽象
- **原因**：用户可能有不同提供商的 API keys
- **方案**：支持 FAL、ElevenLabs、自定义提供商

### 3. 存储方案
- **当前**：内存存储（开发阶段）
- **生产**：Redis 或 SQLite

### 4. 配额管理
- **当前**：简单每日计数
- **生产**：配合后端配额验证

---

## 开发规范

- TypeScript 严格模式
- 所有模块使用 ES Module
- 异步 API 使用 async/await
- 错误处理使用 try-catch
- JSDoc 文档注释

---

## 注意事项

1. **API Keys**：永远不要提交到 GitHub
2. **后端部署**：生产环境使用 HTTPS
3. **配额监控**：定期检查使用情况
4. **错误处理**：完善日志记录
