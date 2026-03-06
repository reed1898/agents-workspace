# 交易记录应用 - 技术架构文档

## 技术栈选择

### 前端技术栈

#### 核心框架
- **Next.js 15**: React 全栈框架，支持 SSR、SSG、API Routes
  - 使用 App Router（最新架构）
  - React 19 特性支持
  - 内置优化（图片、字体、打包）

#### UI 框架与样式
- **TailwindCSS 4.x**: 原子化 CSS 框架
- **shadcn/ui**: 高质量 React 组件库
  - 基于 Radix UI（无障碍性强）
  - 完全可定制
  - TypeScript 支持

#### 图表可视化
- **Recharts**: 基于 React 的图表库（简单图表）
- **Apache ECharts**: 功能强大的数据可视化库（复杂图表）
  - 支持大数据量渲染
  - 丰富的图表类型

#### 状态管理
- **Zustand**: 轻量级状态管理库
  - 比 Redux 更简单
  - TypeScript 友好
  - 支持中间件

#### 表单处理
- **React Hook Form**: 高性能表单库
- **Zod**: TypeScript-first 的验证库
  - 类型安全
  - 与 React Hook Form 完美集成

#### 其他工具
- **Axios**: HTTP 客户端
- **date-fns**: 日期处理库
- **React Query (TanStack Query)**: 服务端状态管理
- **NextAuth.js**: 认证解决方案（可选）

### 后端技术栈

#### Web 框架
- **FastAPI**: 现代、高性能的 Python Web 框架
  - 基于 Python 3.11+
  - 自动生成 OpenAPI 文档
  - 原生支持异步
  - Pydantic 数据验证

#### 数据库
- **MySQL 8+**: 主数据库
  - 成熟可靠的关系型数据库
  - 支持 JSON 类型（灵活性）
  - 强大的查询优化

- **Redis 7+**: 缓存和消息队列
  - 行情数据缓存
  - Session 存储
  - Celery 任务队列

#### ORM 与数据库迁移
- **SQLAlchemy 2.0**: Python ORM
  - 支持异步操作
  - 类型提示支持
- **Alembic**: 数据库迁移工具

#### 异步任务
- **Celery**: 分布式任务队列
  - 定时任务（交易数据同步）
  - 后台任务（数据分析）
- **Celery Beat**: 定时任务调度器

#### 认证与安全
- **PyJWT**: JWT Token 生成和验证
- **Passlib + Bcrypt**: 密码哈希
- **Cryptography (Fernet)**: API 密钥加密
- **Python-dotenv**: 环境变量管理

#### 外部 API 集成
- **CCXT**: 加密货币交易所统一 API
  - 支持 Binance 等主流交易所
  - 统一的接口标准
- **ib_insync**: Interactive Brokers Python API
- **yfinance**: Yahoo Finance 数据接口
- **requests** / **httpx**: HTTP 客户端

#### 数据处理
- **Pandas**: 数据分析和处理
  - 交易记录分析
  - 统计计算
- **NumPy**: 数值计算

#### API 文档
- **FastAPI 内置**: 自动生成 Swagger UI
- **ReDoc**: 备选文档界面

---

## 系统架构设计

### 整体架构图

```
┌─────────────────────────────────────────────────────────────┐
│                       用户界面层                              │
│                    (Next.js Frontend)                        │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Dashboard │  │Positions │  │  Plans   │  │Analytics │   │
│  │  仪表盘   │  │  持仓    │  │ 交易计划  │  │  分析    │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                              │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTPS / REST API
                     │ (JSON)
┌────────────────────┴────────────────────────────────────────┐
│                      API Gateway                             │
│                   (FastAPI + Nginx)                          │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              JWT Authentication                     │    │
│  │          Middleware (CORS, Rate Limit)              │    │
│  └────────────────────────────────────────────────────┘    │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────┴─────┐ ┌───┴──────┐ ┌──┴──────────┐
│Trade Sync   │ │Position  │ │Analytics    │
│Service      │ │Service   │ │Service      │
│             │ │          │ │             │
│- API同步    │ │- 持仓计算 │ │- 收益分析   │
│- 文件导入   │ │- 市值更新 │ │- 纪律检查   │
│- 数据清洗   │ │- 盈亏计算 │ │- 报表生成   │
└───────┬─────┘ └───┬──────┘ └──┬──────────┘
        │           │            │
        └───────────┼────────────┘
                    │
        ┌───────────┴────────────┐
        │                        │
┌───────┴────────┐      ┌────────┴─────────┐
│    MySQL       │      │      Redis       │
│                │      │                  │
│- Users         │      │- Session Store   │
│- Accounts      │      │- Market Data     │
│- Trades        │      │- Task Queue      │
│- Positions     │      │- Rate Limit      │
│- Plans         │      └──────────────────┘
│- Checks        │
└───────┬────────┘
        │
┌───────┴──────────────────────────────────┐
│        Celery Worker Cluster              │
│                                           │
│  ┌──────────────┐  ┌──────────────┐     │
│  │ Sync Worker  │  │ Price Worker │     │
│  │ (定时同步)    │  │ (行情更新)    │     │
│  └──────────────┘  └──────────────┘     │
└───────┬───────────────────────────────────┘
        │
┌───────┴───────────────────────────────────┐
│         External APIs                     │
│                                           │
│  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │ Binance  │  │    IB    │  │ Yahoo  │ │
│  │   API    │  │   API    │  │Finance │ │
│  └──────────┘  └──────────┘  └────────┘ │
└───────────────────────────────────────────┘
```

---

## 数据库设计

### 数据库选型：MySQL

**选择原因**:
- 成熟稳定的关系型数据库
- 支持 JSON 类型（灵活存储扩展字段）
- 强大的查询性能和索引能力
- 支持事务和外键约束
- 丰富的分析函数

### 核心表结构

> 说明：示例中用 UUID 表达主键概念；在 MySQL 中本项目实际以 `CHAR(32)` 存储 UUID（无短横线），JSON 字段使用 `JSON` 类型。

#### 1. users - 用户表
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    username VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_users_email ON users(email);
```

#### 2. accounts - 交易账户表
```sql
CREATE TABLE accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    account_name VARCHAR(100) NOT NULL,
    account_type VARCHAR(50) NOT NULL, -- binance, ib, a_stock, hk_stock
    account_group VARCHAR(50), -- 长期, 短线, etc.
    api_key_encrypted TEXT,
    api_secret_encrypted TEXT,
    extra_config JSON, -- 额外配置（灵活扩展）
    is_active BOOLEAN DEFAULT TRUE,
    last_sync_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_accounts_user_id ON accounts(user_id);
CREATE INDEX idx_accounts_type ON accounts(account_type);
```

#### 3. trades - 交易记录表
```sql
CREATE TABLE trades (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    symbol VARCHAR(50) NOT NULL, -- BTC/USDT, AAPL, 000001.SZ
    side VARCHAR(10) NOT NULL, -- buy, sell
    quantity DECIMAL(20, 8) NOT NULL,
    price DECIMAL(20, 8) NOT NULL,
    fee DECIMAL(20, 8) DEFAULT 0,
    fee_currency VARCHAR(10),
    trade_time TIMESTAMP NOT NULL,
    trade_id_external VARCHAR(100), -- 交易所原始 ID
    sync_source VARCHAR(20) NOT NULL, -- api, manual, import
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(account_id, trade_id_external) -- 防止重复导入
);

CREATE INDEX idx_trades_account_id ON trades(account_id);
CREATE INDEX idx_trades_symbol ON trades(symbol);
CREATE INDEX idx_trades_trade_time ON trades(trade_time);
CREATE INDEX idx_trades_sync_source ON trades(sync_source);
```

#### 4. positions - 持仓表
```sql
CREATE TABLE positions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    symbol VARCHAR(50) NOT NULL,
    quantity DECIMAL(20, 8) NOT NULL,
    average_cost DECIMAL(20, 8) NOT NULL,
    current_price DECIMAL(20, 8),
    unrealized_pnl DECIMAL(20, 8),
    unrealized_pnl_percent DECIMAL(10, 4),
    first_buy_time TIMESTAMP,
    holding_days INTEGER,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(account_id, symbol)
);

CREATE INDEX idx_positions_account_id ON positions(account_id);
CREATE INDEX idx_positions_symbol ON positions(symbol);
```

#### 5. trading_plans - 交易计划表
```sql
CREATE TABLE trading_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    symbol VARCHAR(50) NOT NULL,
    plan_type VARCHAR(20) DEFAULT 'long', -- long, short

    -- 建仓理由
    entry_reason TEXT NOT NULL,
    technical_analysis TEXT,
    fundamental_analysis TEXT,
    entry_signals JSON, -- 入场信号数组

    -- 止损止盈
    stop_loss_price DECIMAL(20, 8),
    stop_loss_percent DECIMAL(10, 4),
    take_profit_levels JSON, -- 多级止盈 [{price, percent, quantity_percent}]

    -- 仓位管理
    planned_position_size DECIMAL(20, 8),
    max_position_size DECIMAL(20, 8),
    entry_strategy JSON, -- 分批建仓计划

    -- 风险评估
    risk_level VARCHAR(20), -- low, medium, high
    risk_reward_ratio DECIMAL(10, 4),
    max_loss_amount DECIMAL(20, 8),

    -- 状态
    plan_status VARCHAR(20) DEFAULT 'active', -- active, executing, closed, cancelled
    actual_entry_price DECIMAL(20, 8),
    actual_entry_time TIMESTAMP,
    close_price DECIMAL(20, 8),
    close_time TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_trading_plans_account_id ON trading_plans(account_id);
CREATE INDEX idx_trading_plans_symbol ON trading_plans(symbol);
CREATE INDEX idx_trading_plans_status ON trading_plans(plan_status);
```

#### 6. trading_actions - 交易操作记录表
```sql
CREATE TABLE trading_actions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trade_id UUID REFERENCES trades(id) ON DELETE CASCADE,
    trading_plan_id UUID REFERENCES trading_plans(id) ON DELETE CASCADE,

    action_type VARCHAR(20) NOT NULL, -- open, add, reduce, close
    action_reason TEXT NOT NULL,

    -- 情绪记录
    emotion_tags VARCHAR(100)[], -- ['calm', 'fear', 'greed', 'fomo']
    emotion_note TEXT,

    -- 纪律检查
    is_planned BOOLEAN DEFAULT TRUE,
    deviation_note TEXT, -- 偏离计划的说明

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_trading_actions_trade_id ON trading_actions(trade_id);
CREATE INDEX idx_trading_actions_plan_id ON trading_actions(trading_plan_id);
CREATE INDEX idx_trading_actions_type ON trading_actions(action_type);
```

#### 7. discipline_checks - 纪律检查表
```sql
CREATE TABLE discipline_checks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trading_plan_id UUID NOT NULL REFERENCES trading_plans(id) ON DELETE CASCADE,

    check_type VARCHAR(50) NOT NULL, -- stop_loss, position_size, emotion, timing, etc.
    check_result VARCHAR(20) NOT NULL, -- compliant, violated, warning

    expected_value VARCHAR(100), -- 预期值（如预期止损价）
    actual_value VARCHAR(100), -- 实际值
    deviation_percent DECIMAL(10, 4), -- 偏离百分比

    impact_analysis TEXT, -- 影响分析
    lesson_learned TEXT, -- 经验教训

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_discipline_checks_plan_id ON discipline_checks(trading_plan_id);
CREATE INDEX idx_discipline_checks_type ON discipline_checks(check_type);
CREATE INDEX idx_discipline_checks_result ON discipline_checks(check_result);
```

#### 8. market_prices - 市场价格缓存表
```sql
CREATE TABLE market_prices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    symbol VARCHAR(50) NOT NULL,
    market_type VARCHAR(20) NOT NULL, -- crypto, us_stock, a_stock, hk_stock
    price DECIMAL(20, 8) NOT NULL,
    price_time TIMESTAMP NOT NULL,
    source VARCHAR(50), -- binance, yahoo, etc.

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(symbol, market_type, price_time)
);

CREATE INDEX idx_market_prices_symbol ON market_prices(symbol, market_type);
CREATE INDEX idx_market_prices_time ON market_prices(price_time DESC);
```

#### 9. review_notes - 复盘笔记表
```sql
CREATE TABLE review_notes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trading_plan_id UUID NOT NULL REFERENCES trading_plans(id) ON DELETE CASCADE,

    review_type VARCHAR(20), -- daily, weekly, trade_specific
    summary TEXT NOT NULL,
    what_went_well TEXT,
    what_went_wrong TEXT,
    lessons_learned TEXT,
    action_items JSON, -- 行动项数组

    tags VARCHAR(50)[],

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_review_notes_plan_id ON review_notes(trading_plan_id);
CREATE INDEX idx_review_notes_type ON review_notes(review_type);
```

---

## API 设计

### RESTful API 规范

#### 基础路径
```
Base URL: https://api.tradingnotes.com/api/v1
```

#### 认证
```
Authorization: Bearer <JWT_TOKEN>
```

### 核心 API 端点

#### 1. 认证相关
```
POST   /auth/register          # 用户注册
POST   /auth/login             # 用户登录
POST   /auth/refresh           # 刷新 Token
POST   /auth/logout            # 登出
GET    /auth/me                # 获取当前用户信息
```

#### 2. 账户管理
```
GET    /accounts               # 获取账户列表
POST   /accounts               # 创建新账户
GET    /accounts/{id}          # 获取账户详情
PUT    /accounts/{id}          # 更新账户
DELETE /accounts/{id}          # 删除账户
POST   /accounts/{id}/sync     # 触发同步
GET    /accounts/{id}/status   # 获取同步状态
```

#### 3. 交易记录
```
GET    /trades                 # 获取交易列表（支持分页、筛选）
POST   /trades                 # 手动添加交易
GET    /trades/{id}            # 获取交易详情
PUT    /trades/{id}            # 更新交易
DELETE /trades/{id}            # 删除交易
POST   /trades/import          # 批量导入交易
GET    /trades/export          # 导出交易记录
```

#### 4. 持仓管理
```
GET    /positions              # 获取持仓列表
GET    /positions/{id}         # 获取持仓详情
GET    /positions/summary      # 持仓汇总
POST   /positions/refresh      # 刷新持仓价格
```

#### 5. 交易计划
```
GET    /plans                  # 获取计划列表
POST   /plans                  # 创建交易计划
GET    /plans/{id}             # 获取计划详情
PUT    /plans/{id}             # 更新计划
DELETE /plans/{id}             # 删除计划
POST   /plans/{id}/close       # 关闭计划
GET    /plans/{id}/actions     # 获取计划的操作记录
```

#### 6. 交易操作
```
POST   /actions                # 记录交易操作
GET    /actions/{id}           # 获取操作详情
PUT    /actions/{id}           # 更新操作记录
```

#### 7. 纪律检查
```
GET    /discipline/checks      # 获取纪律检查列表
POST   /discipline/checks      # 创建纪律检查
GET    /discipline/statistics  # 纪律统计
GET    /discipline/violations  # 违规列表
```

#### 8. 数据分析
```
GET    /analytics/returns      # 收益率分析
GET    /analytics/performance  # 绩效分析
GET    /analytics/discipline   # 纪律分析
GET    /analytics/dashboard    # 仪表盘数据
```

#### 9. 复盘笔记
```
GET    /reviews                # 获取复盘列表
POST   /reviews                # 创建复盘
GET    /reviews/{id}           # 获取复盘详情
PUT    /reviews/{id}           # 更新复盘
DELETE /reviews/{id}           # 删除复盘
```

---

## 部署架构

### 开发环境
```
Frontend: localhost:3000 (Next.js Dev Server)
Backend:  localhost:8000 (FastAPI + Uvicorn)
Database: localhost:3306 (MySQL)
Redis:    localhost:6379
```

### 生产环境（推荐架构）

```
┌─────────────────────────────────────────┐
│           Cloudflare / CDN              │
│         (SSL, DDoS Protection)          │
└────────────────┬────────────────────────┘
                 │
┌────────────────┴────────────────────────┐
│            Nginx (Reverse Proxy)        │
│         (Load Balancer, SSL)            │
└────────────────┬────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
┌───────┴─────────┐  ┌────┴──────────┐
│   Next.js App   │  │  FastAPI App  │
│  (Vercel / VPS) │  │  (Gunicorn +  │
│                 │  │   Uvicorn)    │
└─────────────────┘  └────┬──────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
┌───────┴────────┐  ┌─────┴──────┐  ┌──────┴───────┐
│    MySQL       │  │   Redis    │  │Celery Workers│
│  (Managed DB)  │  │  (Managed) │  │ (Background) │
└────────────────┘  └────────────┘  └──────────────┘
```

### 部署选项

#### 选项 1: 全云部署（推荐）
- **前端**: Vercel (自动部署、全球 CDN)
- **后端**: 阿里云 ECS / 腾讯云 CVM
- **数据库**: 阿里云 RDS MySQL
- **Redis**: 阿里云 Redis
- **文件存储**: 阿里云 OSS

#### 选项 2: 混合部署
- **前端**: Vercel
- **后端**: 本地服务器 + Nginx
- **数据库**: Docker 部署

#### 选项 3: 全容器化部署
- 使用 Docker Compose 一键部署
- 适合开发和小规模生产

---

## 安全架构

### 1. 认证与授权
- JWT Token 认证
- Token 过期时间：访问 Token 1小时，刷新 Token 30天
- 密码使用 Bcrypt 哈希（成本因子 12）

### 2. API 密钥保护
```python
from cryptography.fernet import Fernet

# 使用 Fernet 对称加密
# 主密钥存储在环境变量中
# 每个用户的 API 密钥单独加密
```

### 3. HTTPS 强制
- 生产环境强制 HTTPS
- HSTS 头部设置

### 4. 速率限制
- 基于 Redis 的速率限制
- API 限制：100 请求/分钟/用户
- 登录限制：5 次失败后锁定 15 分钟

### 5. CORS 配置
```python
CORS_ORIGINS = [
    "https://tradingnotes.com",
    "http://localhost:3000"  # 开发环境
]
```

### 6. SQL 注入防护
- 使用 SQLAlchemy ORM（参数化查询）
- 不直接拼接 SQL

### 7. XSS 防护
- 前端输入验证
- 后端输出转义
- CSP 头部设置

---

## 性能优化策略

### 1. 数据库优化
- 合理的索引设计
- 查询分页（Limit + Offset）
- 数据库连接池

### 2. 缓存策略
- Redis 缓存热点数据
  - 市场价格（TTL: 5分钟）
  - 用户持仓（TTL: 1分钟）
  - 统计数据（TTL: 30分钟）

### 3. 前端优化
- Next.js 静态生成（SSG）
- 图片懒加载和优化
- 代码分割（Code Splitting）
- 使用 React Server Components

### 4. API 优化
- 响应压缩（Gzip）
- 批量查询接口
- GraphQL（可选，后期优化）

---

## 监控与日志

### 日志系统
```python
# 使用 structlog
- 应用日志: app.log
- 错误日志: error.log
- 访问日志: access.log
- 任务日志: celery.log
```

### 监控指标
- API 响应时间
- 数据库查询时间
- 缓存命中率
- 错误率
- 同步任务成功率

---

## 文档版本
- **版本**: v1.0
- **创建日期**: 2025-11-02
- **最后更新**: 2025-11-02
- **维护者**: Trading Notes Team
