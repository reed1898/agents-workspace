# Trading Notes - 下一阶段开发计划

## 项目现状总结

根据 Git 提交记录，当前已完成：

### ✅ 已完成功能（Phase 1-4）

#### Phase 1: 基础架构
- 用户认证系统（注册/登录/JWT）
- 前后端项目框架搭建（Next.js 15 + FastAPI）
- MySQL 数据库基础设施
- Docker 开发环境配置

#### Phase 2: 交易数据管理
- 交易账户管理（CRUD）
- CSV 文件导入功能
- 交易记录展示和筛选
- 手动同步功能
- 数据导入历史记录

#### Phase 3: 持仓管理
- 持仓自动计算（基于交易记录）
- 合约交易支持（多空持仓、保证金）
- 持仓周期管理（position_cycles）
- 持仓详情页面
- 标的聚合视图

#### Phase 4: 交易纪律分析系统
- 持仓周期复盘功能
- 交易理由记录（action_reason）
- K线图截图上传和展示
- 操作类型自动判断（建仓/加仓/减仓/清仓）
- 纪律分析仪表盘（基础版）
- 交易复盘服务（TradeReviewService）
- 纪律分析服务（DisciplineAnalyticsService）

---

## 🚧 待开发功能优先级

### 第一阶段：核心功能完善（1周）

#### 1. 行情数据接入（1-2天）⭐⭐⭐

**目标**：让持仓页面显示实时市值和浮动盈亏

**背景**：
- 目前持仓页面只显示持仓数量和成本
- 用户无法看到当前市值和实时盈亏
- 这是交易应用最基础的功能

**技术方案**：

##### 后端实现

1. **创建行情数据服务**（`backend/app/services/market_data_service.py`）
   ```python
   class MarketDataService:
       async def fetch_crypto_price(symbol: str) -> float:
           # 使用 CoinGecko API
           # 支持币安交易对映射（如 BTCUSDT -> bitcoin）

       async def fetch_stock_price(symbol: str, market: str) -> float:
           # 使用 Yahoo Finance API
           # market: 'us_stock', 'a_stock', 'hk_stock'

       async def get_current_price(symbol: str, market_type: str) -> Optional[float]:
           # 统一接口，根据市场类型调用不同数据源
           # 先查 Redis 缓存，未命中则调用 API

       async def batch_fetch_prices(positions: List[Position]) -> Dict[str, float]:
           # 批量获取价格，减少 API 调用
   ```

2. **Redis 缓存配置**
   - 缓存键格式：`market_price:{market_type}:{symbol}`
   - TTL：5分钟
   - 缓存失效策略：被动失效 + 主动刷新

3. **更新 Position Schema**（`backend/app/schemas/position.py`）
   ```python
   class PositionResponse(PositionBase):
       current_price: Optional[float] = None
       market_value: Optional[float] = None  # quantity * current_price
       unrealized_pnl: Optional[float] = None  # market_value - cost
       unrealized_pnl_percent: Optional[float] = None
       last_updated: Optional[datetime] = None  # 价格更新时间
   ```

4. **修改持仓 API**（`backend/app/api/v1/endpoints/positions.py`）
   - `GET /api/v1/positions` - 返回持仓列表时附带实时价格
   - `GET /api/v1/positions/{id}` - 持仓详情附带价格
   - `POST /api/v1/positions/refresh-prices` - 手动刷新所有价格

5. **Celery 定时任务**（`backend/app/tasks/market_data_tasks.py`）
   ```python
   @celery_app.task
   def update_market_prices():
       # 每5分钟更新一次所有活跃持仓的价格
       # 只更新 Redis 缓存，不写入数据库
   ```

##### 前端实现

1. **更新持仓类型定义**（`frontend/types/position.ts`）
   ```typescript
   interface Position {
     // ... 现有字段
     current_price?: number;
     market_value?: number;
     unrealized_pnl?: number;
     unrealized_pnl_percent?: number;
     last_updated?: string;
   }
   ```

2. **修改持仓列表页**（`frontend/app/positions/page.tsx`）
   - 新增列：现价、市值、浮动盈亏（金额 + 百分比）
   - 盈亏用颜色标识（红色/绿色）
   - 添加"刷新价格"按钮
   - 显示最后更新时间

3. **修改持仓详情页**
   - 显示实时价格和市值
   - 盈亏趋势图（可选，后期优化）

##### 第三方 API 配置

1. **CoinGecko API**
   - 免费版：50 calls/min
   - 无需 API key（Demo 模式）
   - 付费版：500 calls/min（可选）
   - 文档：https://docs.coingecko.com/

2. **Yahoo Finance（通过 yfinance 库）**
   - 免费，无限制
   - 安装：`pip install yfinance`
   - 支持美股、A股、港股

##### 环境变量配置

```bash
# .env
COINGECKO_API_KEY=  # 可选，付费版
REDIS_CACHE_TTL=300  # 5分钟
```

##### 依赖安装

```bash
# backend/requirements.txt
httpx==0.27.0  # HTTP 客户端
yfinance==0.2.36  # Yahoo Finance
```

##### 测试要点

- [ ] 测试币安加密货币价格获取（BTCUSDT, ETHUSDT）
- [ ] 测试美股价格获取（AAPL, TSLA）
- [ ] 测试 Redis 缓存命中
- [ ] 测试批量获取性能
- [ ] 测试前端价格刷新

##### 交付标准

- ✅ 持仓列表显示实时价格和盈亏
- ✅ 价格数据缓存在 Redis，5分钟刷新
- ✅ 支持手动刷新按钮
- ✅ 前端显示最后更新时间
- ✅ 盈亏用颜色标识

---

#### 2. Dashboard 仪表盘完善（1-2天）⭐⭐⭐

**目标**：用户登录后一眼看到核心数据概览

**背景**：
- 目前 Dashboard 页面过于简单
- 缺少关键数据汇总
- 用户体验不够直观

**技术方案**：

##### 后端实现

1. **创建 Dashboard 聚合 API**（`backend/app/api/v1/endpoints/dashboard.py`）
   ```python
   @router.get("/summary")
   async def get_dashboard_summary(
       db: Session = Depends(get_db),
       current_user: User = Depends(get_current_user)
   ) -> DashboardSummary:
       """
       返回 Dashboard 所需的所有数据
       """
       return {
           "overview": {
               "total_market_value": 100000.0,  # 总市值
               "total_cost": 90000.0,  # 总成本
               "total_pnl": 10000.0,  # 总盈亏
               "total_pnl_percent": 11.11,  # 总收益率
               "today_pnl": 500.0,  # 今日盈亏（需要历史价格）
               "today_pnl_percent": 0.5
           },
           "positions_summary": {
               "total_positions": 10,
               "profitable_count": 7,
               "losing_count": 3,
               "by_market": {
                   "crypto": {"value": 50000, "pnl": 5000, "count": 5},
                   "us_stock": {"value": 50000, "pnl": 5000, "count": 5}
               }
           },
           "recent_trades": [
               # 最近10笔交易
           ],
           "pending_reviews": [
               # 待复盘的持仓周期（已清仓但未复盘）
           ],
           "discipline_score": 85.0,  # 纪律评分
           "quick_stats": {
               "open_position_cycles": 5,  # 持仓中的周期数
               "trades_this_month": 20,  # 本月交易次数
               "win_rate_this_month": 65.0  # 本月胜率
           }
       }
   ```

2. **优化查询性能**
   - 使用 SQL 聚合查询减少数据库往返
   - 添加 Redis 缓存（1分钟 TTL）
   - 避免 N+1 查询

##### 前端实现

1. **重构 Dashboard 页面**（`frontend/app/dashboard/page.tsx`）

   **布局结构**：
   ```
   ┌─────────────────────────────────────────────┐
   │  概览卡片（4个并排）                          │
   │  总市值 | 今日盈亏 | 总收益 | 纪律评分         │
   └─────────────────────────────────────────────┘

   ┌──────────────────────┐  ┌──────────────────┐
   │  持仓分布图          │  │  最近交易        │
   │  (饼图/柱状图)       │  │  (列表)          │
   └──────────────────────┘  └──────────────────┘

   ┌──────────────────────┐  ┌──────────────────┐
   │  待复盘提醒          │  │  快速统计        │
   │  (卡片列表)          │  │  (指标卡片)      │
   └──────────────────────┘  └──────────────────┘
   ```

2. **使用 shadcn/ui 组件**
   - Card（卡片容器）
   - Badge（标签）
   - Progress（进度条）
   - Table（表格）

3. **数据可视化**
   - 安装 Recharts：`npm install recharts`
   - 持仓分布饼图（按标的）
   - 持仓分布柱状图（按市场）

4. **交互功能**
   - 点击持仓分布跳转到持仓页面
   - 点击最近交易查看详情
   - 待复盘卡片快速跳转到复盘页面
   - 实时刷新按钮

##### UI 组件设计

```tsx
// 概览卡片
<OverviewCard
  title="总市值"
  value="¥100,000"
  change="+10.5%"
  trend="up"
  icon={<TrendingUp />}
/>

// 待复盘提醒
<PendingReviewCard
  symbol="BTCUSDT"
  closedAt="2024-11-01"
  pnl="+1500.0"
  pnlPercent="+15.5%"
  daysAgo={3}
  onReview={() => router.push(`/position-cycles/${id}`)}
/>
```

##### 依赖安装

```bash
# frontend
npm install recharts lucide-react
```

##### 测试要点

- [ ] 测试数据加载速度（< 1秒）
- [ ] 测试图表渲染
- [ ] 测试响应式布局（桌面/平板）
- [ ] 测试空数据状态

##### 交付标准

- ✅ 显示总市值、今日盈亏、总收益率
- ✅ 持仓分布可视化（饼图/柱状图）
- ✅ 最近10笔交易列表
- ✅ 待复盘持仓周期提醒
- ✅ 纪律评分展示
- ✅ 页面加载时间 < 2秒

---

### 第二阶段：自动化与体验优化（1周）

#### 3. 币安 API 自动同步（2-3天）⭐⭐

**目标**：自动从币安同步交易记录，减少手动导入

**背景**：
- 目前只支持 CSV 手动导入
- 用户体验不佳，容易遗漏交易
- 自动同步是交易日志应用的核心功能

**技术方案**：

##### 后端实现

1. **安装 CCXT 库**
   ```bash
   pip install ccxt==4.2.0
   ```

2. **API 密钥加密存储**
   - 使用 Fernet 对称加密
   - 密钥存储在 `trade_accounts` 表的 `api_config` 字段（JSONB 加密后）
   - 加密密钥存储在环境变量 `ENCRYPTION_KEY`

   ```python
   # backend/app/core/security.py
   from cryptography.fernet import Fernet

   def encrypt_api_credentials(api_key: str, api_secret: str) -> str:
       fernet = Fernet(settings.ENCRYPTION_KEY)
       data = json.dumps({"api_key": api_key, "api_secret": api_secret})
       return fernet.encrypt(data.encode()).decode()

   def decrypt_api_credentials(encrypted: str) -> dict:
       fernet = Fernet(settings.ENCRYPTION_KEY)
       data = fernet.decrypt(encrypted.encode()).decode()
       return json.loads(data)
   ```

3. **创建币安同步服务**（`backend/app/services/binance_sync_service.py`）
   ```python
   class BinanceSyncService:
       def __init__(self, api_key: str, api_secret: str):
           self.exchange = ccxt.binance({
               'apiKey': api_key,
               'secret': api_secret,
               'enableRateLimit': True,
               'options': {'defaultType': 'future'}  # 支持合约
           })

       async def fetch_trades(
           self,
           symbol: Optional[str] = None,
           since: Optional[int] = None,
           limit: int = 1000
       ) -> List[dict]:
           """获取交易历史"""

       async def fetch_all_trades(
           self,
           account_id: str,
           start_date: datetime
       ) -> List[Trade]:
           """获取所有交易（分批处理）"""

       def normalize_trade(self, raw_trade: dict) -> dict:
           """标准化交易数据"""
   ```

4. **防止重复导入**
   - 使用 `external_trade_id` 唯一索引
   - 导入前检查是否已存在
   - 使用事务保证原子性

5. **同步状态管理**
   - 在 `trade_accounts` 表添加字段：
     ```python
     last_sync_at: datetime  # 最后同步时间
     sync_status: str  # 'idle', 'syncing', 'success', 'error'
     sync_error: str  # 错误信息
     ```

6. **同步 API 端点**（`backend/app/api/v1/endpoints/trade_accounts.py`）
   ```python
   @router.post("/{account_id}/sync")
   async def sync_account(
       account_id: str,
       sync_request: SyncRequest,  # start_date, symbol
       background_tasks: BackgroundTasks,
       db: Session = Depends(get_db),
       current_user: User = Depends(get_current_user)
   ):
       """触发同步任务"""
       background_tasks.add_task(
           sync_binance_account,
           account_id,
           sync_request.start_date
       )
       return {"message": "同步任务已启动"}

   @router.get("/{account_id}/sync-status")
   async def get_sync_status(account_id: str):
       """查询同步状态"""
   ```

7. **Celery 定时任务**（`backend/app/tasks/sync_tasks.py`）
   ```python
   @celery_app.task
   def sync_all_accounts():
       """每小时同步所有账户"""
       accounts = get_active_accounts()
       for account in accounts:
           if account.sync_enabled:
               sync_binance_account.delay(account.id)

   # Celery Beat 配置
   celery_app.conf.beat_schedule = {
       'sync-all-accounts': {
           'task': 'sync_all_accounts',
           'schedule': crontab(minute=0),  # 每小时
       },
   }
   ```

##### 前端实现

1. **修改账户表单**（`frontend/app/accounts/page.tsx`）
   - 添加 API Key 和 Secret 输入框（类型：password）
   - 添加"启用自动同步"开关
   - 表单验证

2. **添加同步功能**
   - 同步按钮（手动触发）
   - 同步状态显示（syncing/success/error）
   - 同步进度条（可选）
   - 最后同步时间显示

3. **同步历史记录**（可选）
   - 显示同步历史（时间、结果、导入数量）

##### 安全考虑

1. **API 权限最小化**
   - 只需要"只读"权限
   - 不需要"提现"和"交易"权限
   - 在 UI 上明确说明

2. **加密密钥管理**
   - `ENCRYPTION_KEY` 存储在 `.env` 文件
   - 生产环境使用环境变量
   - 定期轮换密钥（手动）

3. **错误处理**
   - API 限流：使用 CCXT 的 `enableRateLimit`
   - 网络错误：重试机制（最多3次）
   - 认证失败：提示用户检查密钥

##### 环境变量

```bash
# .env
ENCRYPTION_KEY=  # 使用 Fernet.generate_key() 生成
```

##### 测试要点

- [ ] 测试币安 API 连接
- [ ] 测试现货交易同步
- [ ] 测试合约交易同步
- [ ] 测试重复导入防护
- [ ] 测试 API 限流处理
- [ ] 测试加密存储

##### 交付标准

- ✅ 用户可以添加币安 API 密钥
- ✅ 支持手动触发同步
- ✅ 支持自动定时同步（每小时）
- ✅ 显示同步状态和最后同步时间
- ✅ API 密钥加密存储
- ✅ 防止重复导入

---

#### 4. 数据分析功能增强（3-4天）⭐⭐

**目标**：提供更深入的交易分析，帮助用户改进策略

**背景**：
- 目前 analytics 页面功能较单薄
- 缺少收益率曲线、绩效指标
- 用户需要更全面的交易分析

**技术方案**：

##### 后端实现

1. **创建分析服务**（`backend/app/services/analytics_service.py`）

   **收益率分析**：
   ```python
   class AnalyticsService:
       def calculate_equity_curve(
           self,
           user_id: str,
           start_date: datetime,
           end_date: datetime,
           interval: str = 'day'  # day, week, month
       ) -> List[EquityPoint]:
           """计算资产净值曲线"""
           # 1. 获取所有交易
           # 2. 按时间排序
           # 3. 计算每个时间点的资产净值
           # 4. 按 interval 分组

       def calculate_returns(self, user_id: str) -> ReturnsMetrics:
           """计算收益率指标"""
           return {
               "total_return": 10.5,  # 总收益率 %
               "annualized_return": 15.2,  # 年化收益率
               "max_drawdown": -8.5,  # 最大回撤 %
               "sharpe_ratio": 1.5,  # 夏普比率（可选）
               "cumulative_pnl": 10000.0  # 累计盈亏
           }

       def calculate_performance_metrics(self, user_id: str) -> PerformanceMetrics:
           """计算绩效指标"""
           trades = get_closed_position_cycles(user_id)
           winning_trades = [t for t in trades if t.realized_pnl > 0]
           losing_trades = [t for t in trades if t.realized_pnl < 0]

           return {
               "total_trades": len(trades),
               "winning_trades": len(winning_trades),
               "losing_trades": len(losing_trades),
               "win_rate": len(winning_trades) / len(trades) * 100,
               "avg_win": sum([t.realized_pnl for t in winning_trades]) / len(winning_trades),
               "avg_loss": sum([t.realized_pnl for t in losing_trades]) / len(losing_trades),
               "profit_factor": abs(avg_win / avg_loss),
               "max_win": max([t.realized_pnl for t in winning_trades]),
               "max_loss": min([t.realized_pnl for t in losing_trades]),
               "avg_holding_days": sum([t.holding_days for t in trades]) / len(trades)
           }

       def analyze_by_market(self, user_id: str) -> Dict[str, MarketAnalysis]:
           """按市场维度分析"""

       def analyze_by_symbol(self, user_id: str) -> List[SymbolAnalysis]:
           """按标的分析（排行榜）"""

       def calculate_monthly_heatmap(self, user_id: str) -> List[MonthlyReturn]:
           """月度收益热力图数据"""
   ```

2. **API 端点**（`backend/app/api/v1/endpoints/analytics.py`）
   ```python
   @router.get("/returns")
   async def get_returns_analysis():
       """收益率分析"""

   @router.get("/equity-curve")
   async def get_equity_curve(
       start_date: Optional[date],
       end_date: Optional[date],
       interval: str = 'day'
   ):
       """资产净值曲线"""

   @router.get("/performance")
   async def get_performance_metrics():
       """绩效指标"""

   @router.get("/by-market")
   async def analyze_by_market():
       """按市场分析"""

   @router.get("/by-symbol")
   async def analyze_by_symbol(limit: int = 20):
       """按标的分析（Top 20）"""

   @router.get("/monthly-heatmap")
   async def get_monthly_heatmap():
       """月度收益热力图"""
   ```

##### 前端实现

1. **完善 Analytics 页面**（`frontend/app/analytics/page.tsx`）

   **页面布局**：
   ```
   ┌─────────────────────────────────────────────┐
   │  关键指标卡片（并排）                        │
   │  总收益 | 年化收益 | 最大回撤 | 夏普比率      │
   └─────────────────────────────────────────────┘

   ┌─────────────────────────────────────────────┐
   │  资产净值曲线（折线图）                      │
   │  [切换：日/周/月]  [日期范围选择器]          │
   └─────────────────────────────────────────────┘

   ┌──────────────────────┐  ┌──────────────────┐
   │  绩效指标            │  │  按市场分析      │
   │  - 总交易次数        │  │  (柱状图对比)    │
   │  - 胜率              │  │                  │
   │  - 平均盈利/亏损     │  │                  │
   │  - 盈亏比            │  │                  │
   └──────────────────────┘  └──────────────────┘

   ┌─────────────────────────────────────────────┐
   │  标的收益排行榜（表格）                      │
   │  Top 20 盈利/亏损标的                       │
   └─────────────────────────────────────────────┘

   ┌─────────────────────────────────────────────┐
   │  月度收益热力图                             │
   │  (可选，后期优化)                           │
   └─────────────────────────────────────────────┘
   ```

2. **图表实现**
   - 使用 Recharts
   - 资产净值曲线：LineChart
   - 按市场对比：BarChart
   - 月度热力图：自定义 Heatmap 组件（可选）

3. **交互功能**
   - 日期范围选择器
   - 时间间隔切换（日/周/月）
   - 图表 Tooltip 显示详细数据
   - 导出报表按钮（可选）

##### 数据可视化组件

```tsx
// 资产净值曲线
<LineChart data={equityCurve}>
  <XAxis dataKey="date" />
  <YAxis />
  <Tooltip />
  <Legend />
  <Line type="monotone" dataKey="equity" stroke="#8884d8" />
</LineChart>

// 绩效指标卡片
<MetricCard
  label="胜率"
  value="65.5%"
  comparison="+5.2%"
  trend="up"
/>
```

##### 测试要点

- [ ] 测试收益率计算准确性
- [ ] 测试图表渲染性能（大数据量）
- [ ] 测试日期范围筛选
- [ ] 测试按市场/标的分析

##### 交付标准

- ✅ 显示资产净值曲线（可切换时间间隔）
- ✅ 显示总收益率、年化收益、最大回撤
- ✅ 显示绩效指标（胜率、盈亏比等）
- ✅ 按市场维度对比分析
- ✅ 标的收益排行榜（Top 20）
- ✅ 图表交互流畅

---

### 第三阶段：质量保证与扩展（后续）

#### 5. 测试和优化（1周）

**单元测试**：
- 后端核心服务单元测试（Pytest）
- 目标覆盖率 > 80%
- Mock 外部 API 调用

**集成测试**：
- API 端点集成测试
- 数据库操作测试

**E2E 测试**：
- 前端关键流程测试（Playwright/Cypress）
- 登录 → 导入交易 → 查看持仓 → 复盘

**性能优化**：
- 数据库查询优化（索引、N+1 查询）
- 前端代码分割和懒加载
- 图片优化和懒加载
- API 响应时间优化

**安全加固**：
- SQL 注入测试
- XSS 测试
- CSRF 保护验证
- API 速率限制
- 密码强度检查

---

#### 6. Interactive Brokers 集成（2周）

**技术方案**：
- 使用 `ib_insync` 库
- 支持美股交易同步
- TWS/IB Gateway 连接

**实现内容**：
- IB API 集成
- 账户认证
- 交易记录同步
- 持仓同步
- 行情数据接入

---

#### 7. A股/港股支持（2-3周）

**技术方案**：
- 确定券商 API 或第三方数据源
- 行情数据接入（TuShare / AKShare）
- 交易记录导入

**实现内容**：
- A股券商 API 集成（待定）
- 港股券商 API 集成（待定）
- 行情数据接入
- 市场特性支持（涨跌停、T+1）

---

## 📊 开发时间估算

| 阶段 | 功能 | 预计时间 | 优先级 |
|------|------|----------|--------|
| 第一阶段 | 行情数据接入 | 1-2天 | ⭐⭐⭐ |
| 第一阶段 | Dashboard 完善 | 1-2天 | ⭐⭐⭐ |
| 第二阶段 | 币安 API 同步 | 2-3天 | ⭐⭐ |
| 第二阶段 | 数据分析增强 | 3-4天 | ⭐⭐ |
| 第三阶段 | 测试和优化 | 1周 | ⭐⭐ |
| 第三阶段 | IB 集成 | 2周 | ⭐ |
| 第三阶段 | A股/港股支持 | 2-3周 | ⭐ |

**总计**：第一阶段（1周） + 第二阶段（1周） = 2周核心功能完善

---

## 🎯 里程碑

### Milestone 1：核心功能完善（Week 1）
- ✅ 持仓页面显示实时盈亏
- ✅ Dashboard 完整数据展示
- ✅ 用户体验大幅提升

### Milestone 2：自动化与分析（Week 2）
- ✅ 币安自动同步上线
- ✅ 数据分析功能完整
- ✅ MVP 功能基本完善

### Milestone 3：质量保证（Week 3-4）
- ✅ 测试覆盖率 > 80%
- ✅ 性能优化完成
- ✅ 安全加固完成

### Milestone 4：市场扩展（后续）
- ✅ IB 美股支持
- ✅ A股/港股支持
- ✅ 产品功能全面

---

## 📝 开发建议

1. **遵循开发原则**：
   - 保持 KISS（Keep It Simple, Stupid）
   - 前后端功能一起开发
   - 每个功能完成后立即测试

2. **Git 提交规范**：
   - 使用 Conventional Commits
   - 每个功能独立分支
   - 完成后合并到 `develop`

3. **代码质量**：
   - 后端使用 Black 格式化
   - 前端使用 Prettier
   - 提交前运行 Lint

4. **文档更新**：
   - 每个阶段完成后更新文档
   - 记录遇到的问题和解决方案
   - 更新 API 文档（Swagger）

---

## 🚀 开始开发

选择一个功能开始实现：

```bash
# 创建功能分支
git checkout -b feature/market-data-integration

# 开发完成后
git add .
git commit -m "feat: 实现行情数据接入功能"
git push origin feature/market-data-integration

# 合并到 develop
git checkout develop
git merge feature/market-data-integration
```

---

## 📚 参考文档

- 产品需求：`docs/requirements.md`
- 系统架构：`docs/architecture.md`
- 原开发计划：`docs/development-plan.md`
- Phase 4 详细设计：`docs/features/phase4-discipline-system.md`

---

**版本**: v1.0
**创建日期**: 2025-11-04
**维护者**: Trading Notes Team
