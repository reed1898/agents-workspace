# 交易记录应用 - 开发计划

## 项目概览

**项目名称**: Trading Notes（交易笔记）

**开发周期**: 10-15周（2.5-4个月）

**开发模式**: 敏捷迭代开发，每个 Phase 完成后进行测试和用户反馈

---

## 开发阶段规划

### Phase 1: 项目初始化与基础架构（1-2周）

#### 目标
搭建完整的项目框架，完成开发环境配置，实现用户认证系统。

#### 任务清单

##### 1.1 前端项目初始化
- [ ] 创建 Next.js 15 项目
  ```bash
  npx create-next-app@latest trading-notes-frontend --typescript --tailwind --app
  ```
- [ ] 配置 TypeScript 严格模式
- [ ] 安装和配置 shadcn/ui
- [ ] 设置 ESLint 和 Prettier
- [ ] 配置路径别名（@/components, @/lib, etc.）
- [ ] 创建基础目录结构
  ```
  src/
  ├── app/              # App Router 页面
  ├── components/       # React 组件
  │   ├── ui/          # shadcn/ui 组件
  │   ├── layout/      # 布局组件
  │   └── features/    # 功能组件
  ├── lib/             # 工具函数
  ├── hooks/           # 自定义 Hooks
  ├── store/           # 状态管理
  ├── types/           # TypeScript 类型
  └── styles/          # 全局样式
  ```

##### 1.2 后端项目初始化
- [ ] 创建 FastAPI 项目
  ```bash
  mkdir trading-notes-backend
  cd trading-notes-backend
  poetry init  # 或使用 pip + requirements.txt
  ```
- [ ] 安装核心依赖
  ```
  fastapi
  uvicorn[standard]
  sqlalchemy
  alembic
  psycopg2-binary
  pydantic
  python-jose[cryptography]
  passlib[bcrypt]
  python-multipart
  redis
  celery
  ```
- [ ] 创建项目结构
  ```
  backend/
  ├── app/
  │   ├── api/          # API 路由
  │   │   ├── v1/       # API v1
  │   │   └── deps.py   # 依赖注入
  │   ├── core/         # 核心配置
  │   │   ├── config.py
  │   │   ├── security.py
  │   │   └── database.py
  │   ├── models/       # SQLAlchemy 模型
  │   ├── schemas/      # Pydantic 模式
  │   ├── services/     # 业务逻辑
  │   ├── tasks/        # Celery 任务
  │   └── utils/        # 工具函数
  ├── alembic/          # 数据库迁移
  ├── tests/            # 测试
  └── main.py           # 入口文件
  ```

##### 1.3 Docker 和数据库配置
- [ ] 编写 `docker-compose.yml`
  ```yaml
  version: '3.8'
  services:
    mysql:
      image: mysql:8
      environment:
        MYSQL_DATABASE: trading_notes
        MYSQL_ROOT_PASSWORD: password
      ports:
        - "3306:3306"
      volumes:
        - mysql_data:/var/lib/mysql

    redis:
      image: redis:7-alpine
      ports:
        - "6379:6379"

    backend:
      build: ./backend
      ports:
        - "8000:8000"
      depends_on:
        - mysql
        - redis
      environment:
        DATABASE_URL: mysql+pymysql://root:password@mysql:3306/trading_notes
        REDIS_URL: redis://redis:6379

  volumes:
    mysql_data:
  ```
- [ ] 配置环境变量（.env 文件）
- [ ] 初始化数据库连接
- [ ] 测试数据库连接

##### 1.4 用户认证系统
- [ ] 创建 User 模型（SQLAlchemy）
- [ ] 创建用户 Schema（Pydantic）
- [ ] 实现密码哈希（Bcrypt）
- [ ] 实现 JWT Token 生成和验证
- [ ] 实现注册接口 `POST /api/v1/auth/register`
- [ ] 实现登录接口 `POST /api/v1/auth/login`
- [ ] 实现刷新 Token 接口 `POST /api/v1/auth/refresh`
- [ ] 实现获取当前用户接口 `GET /api/v1/auth/me`
- [ ] JWT 认证中间件

##### 1.5 数据库设计与迁移
- [ ] 设计核心数据表结构（见架构文档）
- [ ] 创建 Alembic 迁移脚本
  ```bash
  alembic init alembic
  alembic revision --autogenerate -m "Initial migration"
  alembic upgrade head
  ```
- [ ] 创建数据库索引
- [ ] 编写种子数据（可选）

##### 1.6 前端基础 UI 框架
- [ ] 设置全局样式和主题
- [ ] 创建主布局组件（Layout）
  - 顶部导航栏（Logo、用户信息、退出）
  - 侧边栏（Dashboard、持仓、计划、分析、设置）
  - 主内容区
- [ ] 实现登录页面
- [ ] 实现注册页面
- [ ] 实现 Dashboard 基础框架（空页面）
- [ ] 前端路由保护（未登录跳转）
- [ ] 集成 Axios 和 API 客户端
- [ ] 实现全局错误处理

##### 1.7 开发工具配置
- [ ] 配置 Git 和 .gitignore
- [ ] 设置 GitHub 仓库
- [ ] 配置 pre-commit hooks（代码格式化）
- [ ] 编写 README.md

#### 交付物
- ✅ 完整的项目框架
- ✅ 用户可以注册、登录、查看个人信息
- ✅ Docker 一键启动开发环境
- ✅ 基础 UI 布局完成

---

### Phase 2: 交易数据同步（2-3周）

#### 目标
实现从币安交易所同步交易记录，支持手动导入 CSV 文件。

#### 任务清单

##### 2.1 账户管理模块
- [ ] 创建 Account 模型和 Schema
- [ ] 实现账户 CRUD API
  - `GET /api/v1/accounts` - 获取账户列表
  - `POST /api/v1/accounts` - 创建账户
  - `PUT /api/v1/accounts/{id}` - 更新账户
  - `DELETE /api/v1/accounts/{id}` - 删除账户
- [ ] 实现 API 密钥加密存储（Fernet）
- [ ] 前端：账户管理页面
  - 账户列表展示
  - 添加账户表单
  - 编辑和删除功能

##### 2.2 币安 API 集成
- [ ] 安装 CCXT 库
  ```bash
  pip install ccxt
  ```
- [ ] 实现币安 API 连接测试
- [ ] 实现获取交易历史
  ```python
  def fetch_binance_trades(api_key, api_secret, symbol=None, since=None):
      exchange = ccxt.binance({
          'apiKey': api_key,
          'secret': api_secret,
      })
      trades = exchange.fetch_my_trades(symbol, since)
      return trades
  ```
- [ ] 实现获取当前持仓
- [ ] 实现数据标准化（统一格式）
- [ ] 错误处理（API 限流、网络错误等）

##### 2.3 交易记录数据模型
- [ ] 创建 Trade 模型和 Schema
- [ ] 实现交易记录保存逻辑
- [ ] 防止重复导入（唯一索引）
- [ ] 交易记录数据清洗和验证

##### 2.4 数据同步服务
- [ ] 创建 Celery 任务
  ```python
  @celery_app.task
  def sync_account_trades(account_id: str):
      # 同步逻辑
      pass
  ```
- [ ] 配置 Celery Beat（定时任务）
  ```python
  # 每小时同步一次
  celery_app.conf.beat_schedule = {
      'sync-all-accounts': {
          'task': 'sync_all_accounts',
          'schedule': crontab(minute=0),
      },
  }
  ```
- [ ] 实现同步状态跟踪
  - 同步进度
  - 成功/失败状态
  - 错误日志
- [ ] API 端点
  - `POST /api/v1/accounts/{id}/sync` - 手动触发同步
  - `GET /api/v1/accounts/{id}/sync-status` - 查询同步状态

##### 2.5 文件导入功能
- [ ] 实现 CSV 文件解析
  ```python
  import pandas as pd

  def parse_csv(file):
      df = pd.read_csv(file)
      # 数据清洗和转换
      return trades
  ```
- [ ] 支持多种 CSV 格式
  - 币安导出格式
  - 盈透导出格式
  - 通用格式
- [ ] 文件验证（必填字段检查）
- [ ] 批量导入优化
- [ ] API 端点
  - `POST /api/v1/trades/import` - 上传文件导入

##### 2.6 交易记录展示
- [ ] 实现交易列表 API
  - 分页
  - 筛选（按账户、标的、日期）
  - 排序
- [ ] 前端：交易记录页面
  - 数据表格（shadcn/ui Table）
  - 筛选器
  - 分页控件
  - 同步按钮
  - 导入按钮
- [ ] 交易详情弹窗

##### 2.7 数据导出功能
- [ ] 实现 CSV 导出
- [ ] 实现 Excel 导出
- [ ] API 端点
  - `GET /api/v1/trades/export?format=csv`

#### 交付物
- ✅ 用户可以添加币安账户
- ✅ 自动同步币安交易历史
- ✅ 支持导入 CSV 文件
- ✅ 查看交易历史列表
- ✅ 导出交易数据

---

### Phase 3: 持仓管理（1-2周）

#### 目标
基于交易记录计算持仓，接入行情数据，展示持仓盈亏。

#### 任务清单

##### 3.1 持仓计算逻辑
- [ ] 实现持仓计算服务
  ```python
  def calculate_positions(account_id: str):
      # 1. 获取所有交易
      # 2. 按标的分组
      # 3. 计算持仓数量和平均成本
      # 4. 保存到 positions 表
      pass
  ```
- [ ] 处理买入/卖出逻辑
- [ ] 计算加权平均成本
- [ ] 计算首次买入时间和持仓周期

##### 3.2 行情数据接入
- [ ] 选择行情数据源
  - 加密货币：CoinGecko API / Binance API
  - 美股：Yahoo Finance / Alpha Vantage
- [ ] 实现行情数据获取
  ```python
  def fetch_current_price(symbol: str, market_type: str):
      if market_type == 'crypto':
          # 使用 CoinGecko
          pass
      elif market_type == 'us_stock':
          # 使用 Yahoo Finance
          pass
  ```
- [ ] 行情数据缓存（Redis，TTL 5分钟）
- [ ] 定时更新行情（Celery Beat）

##### 3.3 持仓盈亏计算
- [ ] 实时市值计算
  ```python
  market_value = quantity * current_price
  ```
- [ ] 浮动盈亏计算
  ```python
  unrealized_pnl = (current_price - average_cost) * quantity
  unrealized_pnl_percent = unrealized_pnl / (average_cost * quantity) * 100
  ```
- [ ] 更新 Position 表

##### 3.4 持仓管理 API
- [ ] `GET /api/v1/positions` - 获取持仓列表
- [ ] `GET /api/v1/positions/{id}` - 获取持仓详情
- [ ] `GET /api/v1/positions/summary` - 持仓汇总
  ```json
  {
    "total_market_value": 100000,
    "total_cost": 90000,
    "total_pnl": 10000,
    "total_pnl_percent": 11.11,
    "positions_count": 10,
    "by_market": {
      "crypto": {"value": 50000, "pnl": 5000},
      "us_stock": {"value": 50000, "pnl": 5000}
    }
  }
  ```
- [ ] `POST /api/v1/positions/refresh` - 刷新持仓价格

##### 3.5 前端持仓页面
- [ ] 持仓列表页
  - 表格展示（标的、数量、成本、现价、盈亏）
  - 盈亏用颜色标识（红/绿）
  - 实时刷新按钮
- [ ] 持仓详情页
  - 成本构成
  - 交易历史
  - 盈亏趋势图
- [ ] 持仓分布图表
  - 饼图（按标的分布）
  - 柱状图（按市场分布）

##### 3.6 账户分组功能
- [ ] 在 Account 表添加 `account_group` 字段
- [ ] 前端添加分组选择器
- [ ] 支持按分组筛选持仓
- [ ] 分组汇总视图

##### 3.7 历史持仓
- [ ] 创建 `position_history` 表（可选）
- [ ] 记录已清仓的持仓
- [ ] 历史持仓查询 API
- [ ] 前端历史持仓页面

#### 交付物
- ✅ 自动计算当前持仓
- ✅ 显示实时市值和盈亏
- ✅ 持仓可视化图表
- ✅ 账户分组功能

---

### Phase 4: 交易计划与记录（2-3周）

#### 目标
核心功能 - 支持创建交易计划，记录每次操作，关联实际交易。

#### 任务清单

##### 4.1 交易计划数据模型
- [ ] 创建 TradingPlan 模型和 Schema
- [ ] 创建 TradingAction 模型和 Schema
- [ ] 数据库迁移

##### 4.2 交易计划创建
- [ ] 实现计划 CRUD API
  - `POST /api/v1/plans` - 创建计划
  - `GET /api/v1/plans` - 获取计划列表
  - `GET /api/v1/plans/{id}` - 获取计划详情
  - `PUT /api/v1/plans/{id}` - 更新计划
  - `DELETE /api/v1/plans/{id}` - 删除计划
- [ ] 前端：创建计划表单
  - **建仓理由**
    - 富文本编辑器（或 Markdown）
    - 技术分析要点
    - 基本面分析
    - 入场信号
  - **止损止盈设置**
    - 止损价格/百分比
    - 多级止盈设置（动态添加）
  - **仓位管理**
    - 计划仓位大小
    - 分批建仓计划
  - **风险评估**
    - 风险等级选择
    - 盈亏比计算
    - 最大亏损金额
- [ ] 表单验证（Zod）
- [ ] 提交和保存

##### 4.3 计划模板功能
- [ ] 创建计划模板表（可选）
- [ ] 支持保存常用计划模板
- [ ] 从模板创建计划

##### 4.4 操作记录功能
- [ ] 实现操作记录 API
  - `POST /api/v1/actions` - 创建操作记录
  - `GET /api/v1/actions` - 获取操作列表
- [ ] 前端：记录操作弹窗
  - 操作类型选择（建仓/加仓/减仓/清仓）
  - 操作理由（文本框）
  - 情绪标签（多选：冷静、恐惧、贪婪、FOMO）
  - 是否按计划执行（复选框）
  - 偏离说明（条件显示）

##### 4.5 自动关联交易
- [ ] 实现交易和计划的自动关联
  ```python
  # 根据账户、标的、时间自动匹配
  def link_trade_to_plan(trade_id: str):
      trade = get_trade(trade_id)
      plan = find_active_plan(trade.account_id, trade.symbol)
      if plan:
          create_trading_action(trade_id, plan.id)
  ```
- [ ] 手动关联功能（如果自动匹配失败）

##### 4.6 计划执行对比
- [ ] 前端：计划详情页
  - **计划 vs 实际对比**
    - 计划止损 vs 实际止损
    - 计划仓位 vs 实际仓位
    - 计划时间 vs 实际时间
  - **偏离提醒**（高亮显示）
  - **执行进度**
    - 已开仓比例
    - 止损是否触发
    - 止盈是否达成
- [ ] 偏离统计
  ```python
  deviation_percent = (actual - planned) / planned * 100
  ```

##### 4.7 计划状态管理
- [ ] 计划状态流转
  - `active` - 活跃（未开仓）
  - `executing` - 执行中
  - `closed` - 已关闭（盈利/止损）
  - `cancelled` - 已取消
- [ ] 自动更新状态
- [ ] 手动关闭计划 API
  - `POST /api/v1/plans/{id}/close`

##### 4.8 计划列表和筛选
- [ ] 前端：计划列表页
  - 表格展示
  - 状态筛选
  - 按标的、账户筛选
  - 排序（按创建时间、状态）
- [ ] 快速创建入口

#### 交付物
- ✅ 用户可以创建完整的交易计划
- ✅ 记录每次操作和情绪
- ✅ 交易自动关联到计划
- ✅ 显示计划执行情况

---

### Phase 5: 交易纪律检查（1-2周）

#### 目标
自动和手动检查交易纪律，生成纪律报告。

#### 任务清单

##### 5.1 纪律检查数据模型
- [ ] 创建 DisciplineCheck 模型和 Schema
- [ ] 数据库迁移

##### 5.2 自动纪律检查
- [ ] **止损执行检查**
  ```python
  def check_stop_loss_execution(plan_id):
      plan = get_plan(plan_id)
      actions = get_actions(plan_id)

      # 检查是否触发止损
      # 检查执行时机（延迟/提前）
      # 记录检查结果
  ```
- [ ] **持仓时间检查**（可选）
- [ ] **仓位大小检查**
  ```python
  def check_position_size(plan_id):
      plan = get_plan(plan_id)
      actual_position = calculate_position_size(plan_id)

      deviation = (actual_position - plan.planned_position_size) / plan.planned_position_size

      if abs(deviation) > 0.1:  # 超过 10%
          create_discipline_check(
              plan_id=plan_id,
              check_type='position_size',
              check_result='violated',
              deviation_percent=deviation * 100
          )
  ```
- [ ] 自动触发检查（计划关闭时）

##### 5.3 手动纪律记录
- [ ] 前端：添加纪律记录表单
  - 检查类型
  - 是否合规
  - 偏离说明
  - 影响分析
  - 经验教训
- [ ] API 端点
  - `POST /api/v1/discipline/checks`

##### 5.4 纪律统计
- [ ] 实现统计 API
  - `GET /api/v1/discipline/statistics`
  ```json
  {
    "total_checks": 100,
    "compliant_count": 80,
    "violated_count": 20,
    "compliance_rate": 80.0,
    "by_type": {
      "stop_loss": {"compliant": 30, "violated": 5},
      "position_size": {"compliant": 25, "violated": 8}
    }
  }
  ```
- [ ] 违规列表 API
  - `GET /api/v1/discipline/violations`

##### 5.5 纪律报告页面
- [ ] 前端：纪律检查页面
  - **纪律评分卡片**
    - 整体评分（0-100）
    - 遵守率
    - 违规次数
  - **检查列表**
    - 表格展示
    - 按类型筛选
    - 按结果筛选（合规/违规）
  - **违规交易列表**
    - 高亮显示
    - 快速跳转到计划详情
  - **趋势图表**
    - 纪律遵守率趋势

##### 5.6 偏离分析
- [ ] 计算偏离交易的盈亏
  ```python
  def analyze_deviation_impact():
      # 对比按计划执行 vs 偏离计划的交易
      compliant_trades = get_compliant_trades()
      violated_trades = get_violated_trades()

      compliant_avg_pnl = calculate_avg_pnl(compliant_trades)
      violated_avg_pnl = calculate_avg_pnl(violated_trades)

      return {
          'compliant_avg_pnl': compliant_avg_pnl,
          'violated_avg_pnl': violated_avg_pnl,
          'impact': violated_avg_pnl - compliant_avg_pnl
      }
  ```
- [ ] 前端展示偏离影响分析

##### 5.7 情绪分析
- [ ] 统计情绪标签分布
- [ ] 分析不同情绪下的交易结果
- [ ] 前端：情绪分析图表
  - 情绪标签云
  - 情绪与盈亏关系图

#### 交付物
- ✅ 自动检查止损执行
- ✅ 统计纪律遵守情况
- ✅ 生成纪律报告
- ✅ 分析偏离对盈亏的影响

---

### Phase 6: 数据分析与可视化（2周）

#### 目标
提供多维度的数据分析和可视化，帮助用户复盘和改进。

#### 任务清单

##### 6.1 收益率分析
- [ ] 实现收益率计算
  ```python
  def calculate_returns(account_id, start_date, end_date):
      # 计算总收益、收益率
      # 按天/周/月分组
      # 返回时间序列数据
  ```
- [ ] API 端点
  - `GET /api/v1/analytics/returns`
  - 支持时间范围参数
  - 支持按账户、标的筛选
- [ ] 前端：收益率图表
  - 资产净值曲线（折线图）
  - 累计收益率
  - 年化收益率
  - 最大回撤

##### 6.2 绩效分析
- [ ] 实现绩效指标计算
  ```python
  def calculate_performance_metrics(trades):
      total_trades = len(trades)
      winning_trades = [t for t in trades if t.pnl > 0]
      losing_trades = [t for t in trades if t.pnl < 0]

      win_rate = len(winning_trades) / total_trades * 100
      avg_win = sum([t.pnl for t in winning_trades]) / len(winning_trades)
      avg_loss = sum([t.pnl for t in losing_trades]) / len(losing_trades)
      profit_factor = abs(avg_win / avg_loss)

      return {
          'win_rate': win_rate,
          'avg_win': avg_win,
          'avg_loss': avg_loss,
          'profit_factor': profit_factor
      }
  ```
- [ ] API 端点
  - `GET /api/v1/analytics/performance`
- [ ] 前端：绩效指标卡片
  - 胜率
  - 平均盈利
  - 平均亏损
  - 盈亏比
  - 最大单笔盈利/亏损

##### 6.3 按维度统计
- [ ] 按市场统计
  - 各市场收益对比
  - 条形图展示
- [ ] 按标的统计
  - 收益排行榜
  - 交易次数排行
- [ ] 按时间统计
  - 月度收益热力图
  - 周度收益分布

##### 6.4 纪律分析仪表盘
- [ ] 纪律评分系统
  ```python
  def calculate_discipline_score(user_id):
      checks = get_all_discipline_checks(user_id)

      # 权重分配
      weights = {
          'stop_loss': 0.4,
          'position_size': 0.3,
          'emotion': 0.3
      }

      score = 0
      for check_type, weight in weights.items():
          compliance_rate = calculate_compliance_rate(checks, check_type)
          score += compliance_rate * weight

      return score * 100  # 0-100
  ```
- [ ] API 端点
  - `GET /api/v1/analytics/discipline`
- [ ] 前端：纪律分析页
  - 纪律评分（进度环）
  - 各维度雷达图
  - 改进建议

##### 6.5 Dashboard 仪表盘
- [ ] 实现 Dashboard 数据聚合 API
  - `GET /api/v1/analytics/dashboard`
  ```json
  {
    "overview": {
      "total_assets": 100000,
      "today_pnl": 1000,
      "today_pnl_percent": 1.0,
      "total_pnl": 10000,
      "total_return": 10.0
    },
    "positions_summary": {...},
    "recent_trades": [...],
    "active_plans": [...],
    "discipline_score": 85,
    "alerts": [...]
  }
  ```
- [ ] 前端：Dashboard 页面
  - **概览卡片**（总资产、今日盈亏、总收益）
  - **持仓分布图**（饼图）
  - **收益曲线**（迷你图）
  - **最近交易**（列表）
  - **活跃计划**（列表）
  - **纪律评分**（进度环）

##### 6.6 数据导出
- [ ] 实现完整数据导出
  - CSV 格式
  - Excel 格式（多个 Sheet）
  - JSON 格式
- [ ] API 端点
  - `GET /api/v1/export?format=excel`
- [ ] 前端：导出按钮

##### 6.7 图表优化
- [ ] 集成 Recharts / ECharts
- [ ] 响应式图表（适配移动端）
- [ ] 图表交互（tooltip、zoom、drill-down）
- [ ] 图表主题切换（可选）

#### 交付物
- ✅ 完整的数据分析仪表盘
- ✅ 收益率和绩效分析
- ✅ 纪律分析和评分
- ✅ 多维度可视化图表
- ✅ 数据导出功能

---

### Phase 7: 测试、优化与文档（1周）

#### 目标
完善系统，进行全面测试，编写文档。

#### 任务清单

##### 7.1 后端测试
- [ ] 编写单元测试（Pytest）
  - 核心业务逻辑测试
  - API 端点测试
  - 覆盖率目标：> 80%
- [ ] 集成测试
  - 数据库操作测试
  - 外部 API 集成测试
- [ ] 性能测试
  - 大数据量测试（10万+交易记录）
  - API 响应时间测试
  - 数据库查询优化

##### 7.2 前端测试
- [ ] 组件测试（React Testing Library）
- [ ] E2E 测试（Playwright / Cypress）
  - 关键用户流程测试
  - 登录 → 同步 → 查看持仓 → 创建计划
- [ ] 浏览器兼容性测试

##### 7.3 安全测试
- [ ] SQL 注入测试
- [ ] XSS 测试
- [ ] CSRF 保护验证
- [ ] API 速率限制测试
- [ ] 密码强度检查
- [ ] API 密钥加密验证

##### 7.4 性能优化
- [ ] 前端性能优化
  - 代码分割
  - 图片懒加载
  - 减少打包体积
- [ ] 后端性能优化
  - 数据库查询优化
  - 增加索引
  - N+1 查询优化
  - 实现缓存策略
- [ ] 加载速度优化
  - 目标：首屏加载 < 3秒

##### 7.5 用户体验优化
- [ ] 加载状态优化
  - Skeleton 加载
  - 进度条
- [ ] 错误提示优化
  - 友好的错误信息
  - 操作失败的重试机制
- [ ] 操作反馈优化
  - Toast 提示
  - 成功/失败动画
- [ ] 响应式设计优化
  - 移动端布局调整
  - 触摸友好

##### 7.6 文档编写
- [ ] **用户文档**
  - 快速开始指南
  - 功能使用说明
  - FAQ
- [ ] **开发文档**
  - 项目结构说明
  - API 文档（Swagger）
  - 数据库设计文档
  - 部署文档
- [ ] **代码注释**
  - 核心函数注释
  - 复杂逻辑说明

##### 7.7 部署准备
- [ ] 生产环境配置
  - 环境变量管理
  - 数据库备份策略
  - 日志配置
- [ ] 前端部署
  - Vercel 配置
  - 环境变量设置
- [ ] 后端部署
  - Docker 镜像构建
  - Nginx 配置
  - SSL 证书配置
- [ ] CI/CD 配置
  - GitHub Actions
  - 自动测试
  - 自动部署

##### 7.8 Bug 修复和优化
- [ ] 修复已知 Bug
- [ ] 代码重构
- [ ] 性能调优

#### 交付物
- ✅ 测试覆盖率 > 80%
- ✅ 完整的项目文档
- ✅ 生产环境部署就绪
- ✅ 用户可以稳定使用

---

## MVP 功能优先级

### P0 - 第一版本必须实现（Phase 1-4）
1. ✅ 用户注册和登录
2. ✅ 币安交易记录同步
3. ✅ 基础持仓展示
4. ✅ 交易计划创建和记录
5. ✅ 交易操作记录

### P1 - 第二版本（Phase 5-6）
1. ✅ 完整的纪律检查系统
2. ✅ 收益率分析图表
3. ✅ 数据分析仪表盘

### P2 - 后续版本（Phase 8+）
1. **交易理由和K线图功能** (详见 `docs/features/trading-rationale-and-charts.md`)
2. Interactive Brokers 集成
3. A股、港股支持
4. 复盘笔记功能
5. 交易系统模板
6. 移动端优化

---

## 技术债务管理

### 已知技术债务
1. 暂不实现 GraphQL（使用 RESTful API）
2. 暂不实现实时 WebSocket 推送（使用轮询）
3. 前端状态管理使用 Zustand（后期可考虑迁移 Redux）
4. 暂不支持多语言

### 后续优化方向
1. 引入 GraphQL（减少 API 请求）
2. 实现 WebSocket 实时推送
3. 微服务拆分（如果业务复杂度增加）
4. 引入消息队列（Kafka / RabbitMQ）

---

## 里程碑

| 里程碑 | 目标日期 | 交付内容 |
|--------|---------|---------|
| M1 - 项目初始化 | Week 2 | 用户可以注册登录，查看空白 Dashboard |
| M2 - 数据同步 | Week 5 | 可以同步币安交易，查看交易历史 |
| M3 - 持仓管理 | Week 7 | 可以查看持仓和盈亏 |
| M4 - 交易计划 | Week 10 | 可以创建和管理交易计划 |
| M5 - 纪律检查 | Week 12 | 可以查看纪律报告 |
| M6 - 数据分析 | Week 14 | 完整的数据分析仪表盘 |
| M7 - 上线准备 | Week 15 | 测试完成，部署上线 |

---

## 风险管理

### 潜在风险
1. **外部 API 变更**
   - 风险：交易所 API 接口变更导致同步失败
   - 缓解：使用 CCXT 库（统一接口），定期关注 API 更新

2. **数据安全**
   - 风险：API 密钥泄露
   - 缓解：严格加密，定期审计，最小权限原则

3. **性能问题**
   - 风险：大数据量导致查询缓慢
   - 缓解：合理索引，缓存，分页，异步处理

4. **开发周期延期**
   - 风险：某些功能比预期复杂
   - 缓解：MVP 优先，迭代开发，及时调整计划

---

## 资源需求

### 开发环境
- 开发机：Mac / Linux / Windows
- IDE：VS Code / PyCharm / WebStorm
- 浏览器：Chrome（开发者工具）

### 服务器（生产环境）
- **前端**：Vercel（免费）或 Netlify
- **后端**：
  - 云服务器：2核4G（初期）
  - 数据库：MySQL（1核2G）
  - Redis：512MB
- **估算成本**：约 ¥200-300/月（阿里云/腾讯云）

### 第三方服务
- 行情数据：CoinGecko（免费）、Yahoo Finance（免费）
- 监控：Sentry（免费额度）
- 日志：ELK 或云日志服务

---

## 后续扩展计划（Phase 8+）

### Phase 8: 交易理由和K线图功能（1-2周）

**详细设计文档**: 参见 `docs/features/trading-rationale-and-charts.md`

#### 8.1 Phase 1: 核心功能（2-3天）
- [ ] 数据库迁移：给 trades 表添加 4 个新字段
  - `action_type` - 操作类型（建仓/加仓/减仓/清仓）
  - `action_reason` - 操作理由
  - `chart_image_url` - K线图截图
  - `chart_data` - K线数据快照(可选)
- [ ] 更新 Trade 模型和 Schema
- [ ] 实现自动判断操作类型逻辑
- [ ] 图片上传接口和文件存储
- [ ] 前端 UI 组件（操作类型标签、理由输入框、图片上传）
- [ ] 改造交易列表页和标的详情页

#### 8.2 Phase 2: 体验优化（1-2天）
- [ ] 批量导入支持理由字段
- [ ] 理由编辑专门页面
- [ ] 操作历史时间线视图
- [ ] 数据统计（各类操作次数分析）

#### 8.3 Phase 3: 自动K线图（可选，2-3天）
- [ ] 集成 Lightweight Charts 库
- [ ] 实现 K线数据获取服务（币安、TradingView等）
- [ ] 在详情页展示交互式K线图
- [ ] 自动标注买卖点

**交付物**:
- ✅ 用户可以记录每次操作的理由
- ✅ 支持手动上传K线图截图
- ✅ 在交易列表和详情页展示理由和图表
- ✅ 操作类型自动判断和标记

---

### Phase 9: Interactive Brokers 集成（2周）
- 集成 IB API
- 支持美股交易同步
- 测试和优化

### Phase 10: A股/港股支持（2-3周）
- 确定券商 API 或数据源
- 实现数据同步
- 行情数据接入

### Phase 11: 高级功能（3-4周）
- 交易系统编辑器
- 回测功能
- AI 辅助分析（ChatGPT 集成）
- 移动端优化

---

## 文档版本
- **版本**: v1.0
- **创建日期**: 2025-11-02
- **最后更新**: 2025-11-02
- **维护者**: Trading Notes Team

---

## 附录

### 开发规范
- **代码规范**：遵循 PEP 8（Python）和 Airbnb Style Guide（JavaScript）
- **Git 提交规范**：使用 Conventional Commits
  ```
  feat: 添加新功能
  fix: 修复 Bug
  docs: 文档更新
  style: 代码格式调整
  refactor: 重构
  test: 测试相关
  chore: 构建工具或辅助工具更新
  ```
- **分支管理**：Git Flow
  - `main` - 生产环境
  - `develop` - 开发环境
  - `feature/*` - 功能分支
  - `hotfix/*` - 紧急修复

### 工具推荐
- **项目管理**：GitHub Projects / Notion / Trello
- **设计工具**：Figma（可选）
- **API 测试**：Postman / Insomnia
- **数据库管理**：DBeaver / pgAdmin
