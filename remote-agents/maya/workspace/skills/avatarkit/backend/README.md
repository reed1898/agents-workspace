# AvatarKit 后端 API

> ⚠️ **内部使用** - 此后端服务仅供自建部署，不对外公开

## 快速开始

### 1. 安装依赖

```bash
cd backend/
npm install
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env`：

```env
# 服务配置
PORT=3000
NODE_ENV=development

# 认证
API_KEY=your_secure_random_key

# 图片生成 - FAL.ai
FAL_API_KEY=your_fal_api_key

# 语音合成 - ElevenLabs
ELEVENLABS_API_KEY=your_elevenlabs_api_key

# 可选：其他提供商
# REPLICATE_API_KEY=...
# AZURE_SPEECH_KEY=...
```

### 3. 运行

```bash
# 开发模式
npm run dev

# 生产模式
npm run build
npm start
```

## API 端点

### 健康检查
- `GET /health` - 服务状态

### 形象管理
- `POST /v1/avatar/create` - 创建形象
- `GET /v1/avatar/:id` - 获取形象
- `PUT /v1/avatar/:id` - 更新形象
- `DELETE /v1/avatar/:id` - 删除形象

### 图片生成
- `POST /v1/image/generate` - 生成图片
- `POST /v1/image/scene` - 生成场景
- `GET /v1/image/:id/status` - 查询状态

### 语音合成
- `POST /v1/voice/synthesize` - 语音合成
- `POST /v1/voice/clone` - 声音克隆
- `GET /v1/voice/list` - 列出声音

### 配额管理
- `GET /v1/quota` - 获取配额
- `GET /v1/quota/usage` - 使用情况

## 架构

```
请求 → Express Router → Controller → Service → Provider
                          ↓
                    配额检查/认证
                          ↓
                    响应格式化
```

## 提供商支持

### 图片生成
- [x] FAL.ai (fal-ai/fast-sdxl)
- [ ] Replicate
- [ ] Stability AI
- [ ] 自定义

### 语音合成
- [x] ElevenLabs
- [ ] Azure Speech
- [ ] 自定义

## 部署

### Docker

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

### 环境要求

- Node.js 18+
- 内存：至少 512MB
- 无需数据库（可配置 Redis 缓存）

## 注意事项

- 妥善保管 API keys
- 建议添加速率限制
- 生产环境使用 HTTPS
- 定期监控配额使用
