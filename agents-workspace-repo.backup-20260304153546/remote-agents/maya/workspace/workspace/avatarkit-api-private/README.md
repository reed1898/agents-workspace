# AvatarKit API - SaaS 版本

多用户 Avatar 生成 SaaS 服务，支持 API Key 认证和按量计费。

## 功能特性

- 🔐 **API Key 认证**：安全的 API 访问控制
- 💰 **按量计费**：图片 ¥0.2/张，语音 ¥0.1/次
- 🎁 **免费额度**：新用户每月 10 张图片免费
- 🎨 **图片生成**：基于 FAL AI (Flux) 模型
- 🎤 **语音合成**：基于 ElevenLabs API
- 📊 **使用统计**：详细的使用记录和报表
- 💳 **在线充值**：支持支付宝/微信支付

## 快速开始

### 1. 环境要求

- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### 2. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填入你的配置
```

必需配置：
- `DATABASE_URL`: PostgreSQL 连接字符串
- `REDIS_URL`: Redis 连接字符串
- `JWT_SECRET`: JWT 密钥（至少 32 字符）
- `API_KEY_SALT`: API Key 加密盐
- `FAL_KEY`: FAL AI API 密钥
- `ELEVENLABS_API_KEY`: ElevenLabs API 密钥

### 4. 数据库迁移

```bash
# 创建迁移
alembic revision --autogenerate -m "initial migration"

# 执行迁移
alembic upgrade head
```

### 5. 启动服务

```bash
# 开发模式
uvicorn app.main:app --reload

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Docker 部署

### 使用 Docker Compose（推荐）

```bash
# 设置环境变量
export JWT_SECRET="your-super-secret-key"
export DB_PASSWORD="your-db-password"

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f api

# 停止服务
docker-compose down
```

### 生产环境部署

1. 修改 `docker-compose.yml` 中的环境变量
2. 配置 Nginx 反向代理 + HTTPS
3. 配置监控和日志收集

详细部署指南请参考 [DEPLOYMENT.md](./DEPLOYMENT.md)

## API 使用指南

### 1. 注册用户

```bash
curl -X POST "http://localhost:8000/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "your-password"
  }'
```

响应：
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 86400,
  "api_key": "ak_xxxxxxxxxxxxxxxx",
  "api_secret": "yyyyyyyyyyyyyyyy"
}
```

⚠️ **重要**：`api_secret` 仅在注册时返回一次，请妥善保存！

### 2. 创建形象

```bash
curl -X POST "http://localhost:8000/v1/avatars" \
  -H "X-API-Key: ak_xxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Avatar",
    "style": "realistic",
    "voice_id": "voice-id-from-elevenlabs"
  }'
```

### 3. 生成图片

```bash
curl -X POST "http://localhost:8000/v1/avatars/{avatar_id}/generate" \
  -H "X-API-Key: ak_xxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A professional photo portrait in office setting"
  }'
```

### 4. 查询余额

```bash
curl "http://localhost:8000/v1/user/balance" \
  -H "X-API-Key: ak_xxxxxxxxxxxxxxxx"
```

## API 文档

启动服务后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 项目结构

```
avatarkit-api-private/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接
│   ├── schemas.py           # Pydantic 模型
│   ├── redis_cache.py       # Redis 缓存
│   ├── models/              # SQLAlchemy 模型
│   │   ├── user.py          # 用户模型
│   │   ├── avatar.py        # 形象模型
│   │   ├── usage.py         # 使用记录
│   │   └── order.py         # 订单模型
│   ├── routers/             # API 路由
│   │   ├── auth.py          # 认证
│   │   ├── user.py          # 用户
│   │   ├── avatar.py        # 形象
│   │   ├── generate.py      # 生成
│   │   └── billing.py       # 计费
│   ├── middleware/          # 中间件
│   │   ├── auth.py          # API Key 认证
│   │   └── billing.py       # 计费中间件
│   └── services/            # 外部服务
│       ├── fal.py           # FAL AI
│       ├── elevenlabs.py    # ElevenLabs
│       ├── storage.py       # 文件存储
│       ├── alipay.py        # 支付宝
│       └── wechat_pay.py    # 微信支付
├── migrations/              # Alembic 迁移
├── docker-compose.yml       # Docker Compose 配置
├── Dockerfile               # Docker 构建文件
├── requirements.txt         # Python 依赖
├── alembic.ini              # Alembic 配置
├── .env.example             # 环境变量示例
├── DEPLOYMENT.md            # 部署文档
└── README.md                # 本文档
```

## 技术栈

- **框架**: FastAPI + Uvicorn
- **数据库**: PostgreSQL 15 + SQLAlchemy 2.0 + Alembic
- **缓存**: Redis 7
- **认证**: JWT + API Key
- **部署**: Docker + Docker Compose

## 定价

| 服务 | 价格 | 说明 |
|------|------|------|
| 图片生成 | ¥0.2/张 | 基于 FAL Flux 模型 |
| 语音合成 | ¥0.1/次 | 基于 ElevenLabs |
| 视频生成 | ¥2/个 | 即将上线 |
| 免费额度 | 10张/月 | 新用户注册赠送 |

## 许可证

私有软件，未经授权不得使用或分发。

## 支持

如有问题，请联系技术支持。
