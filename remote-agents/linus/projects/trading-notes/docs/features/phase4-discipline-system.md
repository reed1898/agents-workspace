# Phase 4: 交易纪律与复盘分析系统

## 文档信息

- **创建日期**: 2025-11-03
- **状态**: 设计完成,待实施
- **优先级**: 高
- **预计工期**: 7-9 天

## 1. 需求背景

### 1.1 核心场景

基于实际使用场景的设计:

```
真实流程: 执行交易(来不及记录) → 同步/导入交易记录 → 事后补录计划和理由
```

**关键特点**:
- ✅ **事后补录**:交易时来不及填写详细信息,需要在交易后补充
- ✅ **灵活时间**:支持当天晚上集中补录,也支持随时想起来就补
- ✅ **极简主义**:不引入复杂的计划系统,直接增强现有功能
- ✅ **分析优先**:重点是事后统计分析,而非实时监控

### 1.2 用户需求调研结果

通过需求调研,用户选择了以下方案:
- **核心价值**: 两者并重(实时纪律检查 + 事后复盘分析)
- **止损止盈**: 支持固定价格、追踪止损、多级止盈
- **补录方式**: 单笔交易补录(极简模式)
- **补录时间**: 当天晚上集中补录 + 随时想起来就补
- **情绪记录**: 非常重要,需要独立字段和分析

### 1.3 核心分析需求

用户最看重的纪律检查:
1. ✅ 止损执行检查
2. ✅ 情绪影响分析
3. ✅ 策略有效性分析(底部反转/形态突破/回调低吸)
4. ✅ 持仓时间分析

---

## 2. 架构设计

### 2.1 设计原则

**极简主义 - 不创建复杂的计划系统**:
- 不引入 TradingPlan 表(避免过度设计)
- 直接在 Trade 表上添加补录字段
- 新增轻量级的 PositionCycle 表用于周期分析

**事后补录友好**:
- 所有新增字段都是 nullable
- 支持单笔补录和批量补录
- 提供未复盘交易提醒

**分析驱动**:
- 重点是生成有价值的统计报告
- 提供可操作的 Insight 建议
- 支持多维度交叉分析

### 2.2 数据模型设计

#### 2.2.1 增强 Trade 表(在 Phase 3 基础上扩展)

```sql
-- Phase 4 新增字段
ALTER TABLE trades
ADD COLUMN emotion_state VARCHAR(50),           -- 情绪状态
ADD COLUMN emotion_intensity INTEGER,           -- 情绪强度(1-10)
ADD COLUMN planned_stop_loss DECIMAL(20,8),     -- 计划止损价
ADD COLUMN actual_stop_loss DECIMAL(20,8),      -- 实际止损价
ADD COLUMN stop_loss_executed BOOLEAN,          -- 是否执行了止损
ADD COLUMN planned_take_profit DECIMAL(20,8),   -- 计划止盈价
ADD COLUMN actual_take_profit DECIMAL(20,8),    -- 实际止盈价
ADD COLUMN entry_strategy VARCHAR(50),          -- 入场策略
ADD COLUMN reviewed BOOLEAN DEFAULT FALSE,      -- 是否已复盘
ADD COLUMN reviewed_at TIMESTAMP;               -- 复盘时间

-- 创建索引
CREATE INDEX idx_trades_reviewed ON trades(reviewed);
CREATE INDEX idx_trades_emotion_state ON trades(emotion_state);
CREATE INDEX idx_trades_entry_strategy ON trades(entry_strategy);
```

**字段说明**:

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `emotion_state` | VARCHAR(50) | 情绪状态枚举 | 'calm', 'fearful', 'greedy', 'fomo', 'panic', 'confident', 'regretful' |
| `emotion_intensity` | INTEGER | 情绪强度(1-10) | 7 |
| `planned_stop_loss` | DECIMAL(20,8) | 计划止损价(事后补充) | 48000.00 |
| `actual_stop_loss` | DECIMAL(20,8) | 实际止损价(如果触发) | 48500.00 |
| `stop_loss_executed` | BOOLEAN | 是否执行了止损 | True/False |
| `planned_take_profit` | DECIMAL(20,8) | 计划止盈价 | 55000.00 |
| `actual_take_profit` | DECIMAL(20,8) | 实际止盈价 | 54000.00 |
| `entry_strategy` | VARCHAR(50) | 入场策略标签 | '底部反转', '形态突破', '回调低吸', '其他' |
| `reviewed` | BOOLEAN | 是否已复盘 | False |
| `reviewed_at` | TIMESTAMP | 复盘时间 | 2025-11-03 22:30:00 |

**情绪状态枚举**:
```python
class EmotionState(str, Enum):
    CALM = "calm"           # 冷静
    CONFIDENT = "confident" # 自信
    FEARFUL = "fearful"     # 恐惧
    GREEDY = "greedy"       # 贪婪
    FOMO = "fomo"          # 害怕踏空
    PANIC = "panic"         # 恐慌
    EXCITED = "excited"     # 兴奋
    REGRETFUL = "regretful" # 后悔
```

#### 2.2.2 新建 PositionCycle 表(持仓周期分析)

```sql
CREATE TABLE position_cycles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    account_id UUID NOT NULL REFERENCES trade_accounts(id) ON DELETE CASCADE,
    symbol VARCHAR(50) NOT NULL,

    -- 持仓周期时间
    open_time TIMESTAMP NOT NULL,               -- 首次建仓时间
    close_time TIMESTAMP,                       -- 完全清仓时间
    status VARCHAR(20) DEFAULT 'open',          -- 'open' / 'closed'

    -- 关联的所有交易
    trade_ids UUID[] NOT NULL,                  -- 按时间顺序排列

    -- 整体策略
    primary_strategy VARCHAR(50),               -- 主要策略

    -- 整体情绪评估
    dominant_emotion VARCHAR(50),               -- 主导情绪
    emotion_stability INTEGER,                  -- 情绪稳定性(1-10)

    -- 持仓统计
    total_quantity DECIMAL(20,8),               -- 总买入量
    average_entry_price DECIMAL(20,8),          -- 平均成本
    average_exit_price DECIMAL(20,8),           -- 平均卖出价
    total_profit_loss DECIMAL(20,2),            -- 总盈亏
    roi_percent DECIMAL(10,2),                  -- 收益率

    -- 持仓时长
    holding_hours INTEGER,                      -- 持仓小时数

    -- 纪律评估
    followed_stop_loss BOOLEAN,                 -- 是否执行止损
    followed_take_profit BOOLEAN,               -- 是否执行止盈
    discipline_score INTEGER,                   -- 纪律评分(0-100)

    -- 复盘总结
    what_went_well TEXT,                        -- 做得好的地方
    what_to_improve TEXT,                       -- 需要改进的地方
    lessons_learned TEXT,                       -- 经验教训

    -- 时间戳
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 创建索引
CREATE INDEX idx_position_cycles_user_id ON position_cycles(user_id);
CREATE INDEX idx_position_cycles_account_id ON position_cycles(account_id);
CREATE INDEX idx_position_cycles_symbol ON position_cycles(symbol);
CREATE INDEX idx_position_cycles_status ON position_cycles(status);
CREATE INDEX idx_position_cycles_open_time ON position_cycles(open_time);
```

---

## 3. 核心功能设计

### 3.1 交易补录(Trade Review)

#### 3.1.1 单笔补录

```python
# Service: TradeReviewService

def review_trade(
    db: Session,
    trade_id: UUID,
    user_id: UUID,
    review_data: TradeReviewData
) -> Trade:
    """单笔交易补录"""

    trade = db.query(Trade).filter(
        Trade.id == trade_id,
        Trade.user_id == user_id
    ).first()

    if not trade:
        raise HTTPException(404, "交易不存在")

    # 补充情绪
    if review_data.emotion_state:
        trade.emotion_state = review_data.emotion_state
    if review_data.emotion_intensity:
        trade.emotion_intensity = review_data.emotion_intensity

    # 补充止损止盈
    if review_data.planned_stop_loss:
        trade.planned_stop_loss = review_data.planned_stop_loss
    if review_data.planned_take_profit:
        trade.planned_take_profit = review_data.planned_take_profit

    # 补充策略标签
    if review_data.entry_strategy:
        trade.entry_strategy = review_data.entry_strategy

    # 标记为已复盘
    trade.reviewed = True
    trade.reviewed_at = datetime.utcnow()

    db.commit()
    db.refresh(trade)

    return trade
```

#### 3.1.2 批量补录

```python
def batch_review_trades(
    db: Session,
    user_id: UUID,
    trade_ids: List[UUID],
    common_data: dict
) -> List[Trade]:
    """批量补录交易(当晚集中补录)"""

    trades = db.query(Trade).filter(
        Trade.id.in_(trade_ids),
        Trade.user_id == user_id
    ).all()

    for trade in trades:
        # 应用通用数据(如相同的策略、相同的情绪)
        if common_data.get('entry_strategy'):
            trade.entry_strategy = common_data['entry_strategy']
        if common_data.get('emotion_state'):
            trade.emotion_state = common_data['emotion_state']

        trade.reviewed = True
        trade.reviewed_at = datetime.utcnow()

    db.commit()

    return trades
```

#### 3.1.3 获取未复盘交易

```python
def get_unreviewed_trades(
    db: Session,
    user_id: UUID,
    days: int = 7,
    account_id: Optional[UUID] = None
) -> List[Trade]:
    """获取未复盘的交易(用于提醒)"""

    cutoff_date = datetime.utcnow() - timedelta(days=days)

    query = db.query(Trade).filter(
        Trade.user_id == user_id,
        Trade.reviewed == False,
        Trade.trade_time >= cutoff_date
    )

    if account_id:
        query = query.filter(Trade.account_id == account_id)

    return query.order_by(Trade.trade_time.desc()).all()
```

### 3.2 持仓周期自动识别

#### 3.2.1 自动检测周期

```python
# Service: PositionCycleService

def auto_detect_position_cycles(
    db: Session,
    account_id: UUID,
    symbol: str
) -> List[PositionCycle]:
    """自动识别该标的的完整持仓周期"""

    # 获取所有交易,按时间排序
    trades = db.query(Trade).filter(
        Trade.account_id == account_id,
        Trade.symbol == symbol
    ).order_by(Trade.trade_time).all()

    cycles = []
    current_cycle_trades = []
    position_quantity = Decimal(0)

    for trade in trades:
        current_cycle_trades.append(trade.id)

        # 计算持仓变化
        if trade.side == 'buy':
            position_quantity += trade.quantity
        elif trade.side == 'sell':
            position_quantity -= trade.quantity

        # 持仓归零 = 一个周期结束
        if position_quantity == 0 and current_cycle_trades:
            cycle = _create_position_cycle(
                db=db,
                account_id=account_id,
                symbol=symbol,
                trade_ids=current_cycle_trades,
                status='closed'
            )
            cycles.append(cycle)
            current_cycle_trades = []

    # 如果还有未平仓的,创建一个 open 状态的周期
    if current_cycle_trades and position_quantity != 0:
        cycle = _create_position_cycle(
            db=db,
            account_id=account_id,
            symbol=symbol,
            trade_ids=current_cycle_trades,
            status='open'
        )
        cycles.append(cycle)

    return cycles

def _create_position_cycle(
    db: Session,
    account_id: UUID,
    symbol: str,
    trade_ids: List[UUID],
    status: str
) -> PositionCycle:
    """创建持仓周期记录"""

    trades = db.query(Trade).filter(Trade.id.in_(trade_ids)).all()

    cycle = PositionCycle(
        user_id=trades[0].user_id,
        account_id=account_id,
        symbol=symbol,
        trade_ids=trade_ids,
        open_time=trades[0].trade_time,
        close_time=trades[-1].trade_time if status == 'closed' else None,
        status=status
    )

    db.add(cycle)
    db.commit()
    db.refresh(cycle)

    # 计算指标
    calculate_cycle_metrics(db, cycle.id)

    return cycle
```

#### 3.2.2 计算周期指标

```python
def calculate_cycle_metrics(
    db: Session,
    cycle_id: UUID
) -> PositionCycle:
    """计算持仓周期的各项指标"""

    cycle = db.query(PositionCycle).filter(PositionCycle.id == cycle_id).first()
    trades = db.query(Trade).filter(Trade.id.in_(cycle.trade_ids)).all()

    # 分离买入和卖出交易
    buy_trades = [t for t in trades if t.side == 'buy']
    sell_trades = [t for t in trades if t.side == 'sell']

    # 计算平均成本
    total_buy_cost = sum(t.quantity * t.price for t in buy_trades)
    total_buy_quantity = sum(t.quantity for t in buy_trades)
    cycle.average_entry_price = total_buy_cost / total_buy_quantity if total_buy_quantity > 0 else 0

    # 计算平均卖出价
    if sell_trades:
        total_sell_revenue = sum(t.quantity * t.price for t in sell_trades)
        total_sell_quantity = sum(t.quantity for t in sell_trades)
        cycle.average_exit_price = total_sell_revenue / total_sell_quantity if total_sell_quantity > 0 else 0

    # 计算盈亏
    if cycle.status == 'closed':
        total_cost = sum(t.quantity * t.price for t in buy_trades)
        total_revenue = sum(t.quantity * t.price for t in sell_trades)
        cycle.total_profit_loss = total_revenue - total_cost
        cycle.roi_percent = (cycle.total_profit_loss / total_cost) * 100 if total_cost > 0 else 0

    # 计算持仓时长
    if cycle.close_time:
        cycle.holding_hours = int((cycle.close_time - cycle.open_time).total_seconds() / 3600)

    # 判断止损执行
    cycle.followed_stop_loss = _check_stop_loss_execution(trades)
    cycle.followed_take_profit = _check_take_profit_execution(trades)

    # 计算纪律评分
    cycle.discipline_score = _calculate_discipline_score(cycle)

    # 分析主导情绪
    emotions = [t.emotion_state for t in trades if t.emotion_state]
    if emotions:
        cycle.dominant_emotion = max(set(emotions), key=emotions.count)

        # 计算情绪稳定性(情绪种类越少,稳定性越高)
        unique_emotions = len(set(emotions))
        cycle.emotion_stability = max(1, 10 - unique_emotions)

    # 推断主要策略
    strategies = [t.entry_strategy for t in trades if t.entry_strategy]
    if strategies:
        cycle.primary_strategy = max(set(strategies), key=strategies.count)

    db.commit()
    db.refresh(cycle)

    return cycle

def _check_stop_loss_execution(trades: List[Trade]) -> Optional[bool]:
    """检查是否执行了止损"""

    # 如果有任何交易设置了止损价
    trades_with_stop_loss = [t for t in trades if t.planned_stop_loss]

    if not trades_with_stop_loss:
        return None  # 没有设置止损,无法判断

    # 检查是否有止损执行记录
    executed = any(t.stop_loss_executed for t in trades_with_stop_loss)

    return executed

def _check_take_profit_execution(trades: List[Trade]) -> Optional[bool]:
    """检查是否执行了止盈"""

    trades_with_take_profit = [t for t in trades if t.planned_take_profit]

    if not trades_with_take_profit:
        return None

    # 检查是否达到止盈价
    for trade in trades_with_take_profit:
        if trade.actual_take_profit and trade.actual_take_profit >= trade.planned_take_profit:
            return True

    return False

def _calculate_discipline_score(cycle: PositionCycle) -> int:
    """计算纪律评分(0-100)"""

    score = 50  # 基础分

    # 止损执行(+20分)
    if cycle.followed_stop_loss == True:
        score += 20
    elif cycle.followed_stop_loss == False:
        score -= 20

    # 止盈执行(+15分)
    if cycle.followed_take_profit == True:
        score += 15

    # 情绪稳定性(+15分)
    if cycle.emotion_stability:
        score += int(cycle.emotion_stability * 1.5)

    # 限制在 0-100 范围内
    return max(0, min(100, score))
```

### 3.3 纪律分析

#### 3.3.1 止损纪律分析

```python
# Service: DisciplineAnalyticsService

def analyze_stop_loss_discipline(
    db: Session,
    user_id: UUID,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> dict:
    """分析止损执行纪律"""

    # 获取已关闭的持仓周期
    query = db.query(PositionCycle).filter(
        PositionCycle.user_id == user_id,
        PositionCycle.status == 'closed',
        PositionCycle.followed_stop_loss.isnot(None)
    )

    if start_date:
        query = query.filter(PositionCycle.open_time >= start_date)
    if end_date:
        query = query.filter(PositionCycle.close_time <= end_date)

    cycles = query.all()

    if not cycles:
        return {"message": "暂无数据"}

    total = len(cycles)
    executed = len([c for c in cycles if c.followed_stop_loss == True])
    violated = len([c for c in cycles if c.followed_stop_loss == False])

    # 分析违规案例
    violations = []
    for cycle in cycles:
        if not cycle.followed_stop_loss and cycle.total_profit_loss < 0:
            violations.append({
                "symbol": cycle.symbol,
                "loss": float(cycle.total_profit_loss),
                "holding_hours": cycle.holding_hours,
                "emotion": cycle.dominant_emotion,
                "open_time": cycle.open_time.isoformat()
            })

    # 按亏损额排序
    violations.sort(key=lambda x: x['loss'])

    return {
        "total_cycles": total,
        "executed_count": executed,
        "violated_count": violated,
        "execution_rate": round(executed / total * 100, 2) if total > 0 else 0,
        "violations": violations[:10],  # 返回最严重的 10 个案例
        "insight": _generate_stop_loss_insight(executed, violated, violations)
    }

def _generate_stop_loss_insight(executed: int, violated: int, violations: list) -> str:
    """生成止损纪律的 Insight"""

    if violated == 0:
        return "✅ 优秀!你严格执行了所有止损计划。"

    rate = executed / (executed + violated) * 100 if (executed + violated) > 0 else 0

    if rate >= 80:
        return f"✅ 良好!止损执行率 {rate:.1f}%,继续保持。"
    elif rate >= 60:
        return f"⚠️ 一般。止损执行率 {rate:.1f}%,建议加强纪律。"
    else:
        # 分析违规时的情绪
        emotions = [v['emotion'] for v in violations if v.get('emotion')]
        if emotions:
            dominant_emotion = max(set(emotions), key=emotions.count)
            return f"❌ 需改进!止损执行率仅 {rate:.1f}%,违规时常伴随'{dominant_emotion}'情绪。"
        else:
            return f"❌ 需改进!止损执行率仅 {rate:.1f}%,请严格遵守止损纪律。"
```

#### 3.3.2 情绪影响分析

```python
def analyze_emotion_impact(
    db: Session,
    user_id: UUID
) -> dict:
    """分析情绪对交易结果的影响"""

    cycles = db.query(PositionCycle).filter(
        PositionCycle.user_id == user_id,
        PositionCycle.status == 'closed',
        PositionCycle.dominant_emotion.isnot(None)
    ).all()

    if not cycles:
        return {"message": "暂无情绪数据"}

    emotion_stats = {}
    emotions = ['calm', 'fearful', 'greedy', 'fomo', 'panic', 'confident', 'regretful']

    for emotion in emotions:
        emotion_cycles = [c for c in cycles if c.dominant_emotion == emotion]

        if not emotion_cycles:
            continue

        win_count = len([c for c in emotion_cycles if c.total_profit_loss > 0])
        total_count = len(emotion_cycles)

        emotion_stats[emotion] = {
            "cycle_count": total_count,
            "win_rate": round(win_count / total_count * 100, 2) if total_count > 0 else 0,
            "avg_roi": round(sum(c.roi_percent for c in emotion_cycles) / total_count, 2) if total_count > 0 else 0,
            "avg_holding_hours": round(sum(c.holding_hours for c in emotion_cycles if c.holding_hours) / total_count, 1) if total_count > 0 else 0,
            "total_pnl": round(sum(c.total_profit_loss for c in emotion_cycles), 2)
        }

    # 生成 Insight
    insight = _generate_emotion_insight(emotion_stats)

    return {
        "emotion_stats": emotion_stats,
        "insight": insight
    }

def _generate_emotion_insight(emotion_stats: dict) -> str:
    """生成情绪分析的 Insight"""

    if not emotion_stats:
        return "暂无足够数据生成建议"

    # 找到表现最好和最差的情绪
    best_emotion = max(emotion_stats.items(), key=lambda x: x[1]['avg_roi'])
    worst_emotion = min(emotion_stats.items(), key=lambda x: x[1]['avg_roi'])

    emotion_names = {
        'calm': '冷静',
        'fearful': '恐惧',
        'greedy': '贪婪',
        'fomo': '害怕踏空',
        'panic': '恐慌',
        'confident': '自信',
        'regretful': '后悔'
    }

    best_name = emotion_names.get(best_emotion[0], best_emotion[0])
    worst_name = emotion_names.get(worst_emotion[0], worst_emotion[0])

    return f"在'{best_name}'状态下,平均收益率为 {best_emotion[1]['avg_roi']:.2f}%;而在'{worst_name}'状态下仅为 {worst_emotion[1]['avg_roi']:.2f}%。建议交易时保持{best_name}心态。"
```

#### 3.3.3 策略有效性分析

```python
def analyze_strategy_effectiveness(
    db: Session,
    user_id: UUID
) -> dict:
    """分析策略有效性(底部反转 vs 突破 vs 回调)"""

    cycles = db.query(PositionCycle).filter(
        PositionCycle.user_id == user_id,
        PositionCycle.status == 'closed',
        PositionCycle.primary_strategy.isnot(None)
    ).all()

    if not cycles:
        return {"message": "暂无策略数据"}

    strategy_stats = {}
    strategies = ['底部反转', '形态突破', '回调低吸', '其他']

    for strategy in strategies:
        strategy_cycles = [c for c in cycles if c.primary_strategy == strategy]

        if not strategy_cycles:
            continue

        win_count = len([c for c in strategy_cycles if c.total_profit_loss > 0])
        total_count = len(strategy_cycles)

        strategy_stats[strategy] = {
            "cycle_count": total_count,
            "win_rate": round(win_count / total_count * 100, 2) if total_count > 0 else 0,
            "avg_roi": round(sum(c.roi_percent for c in strategy_cycles) / total_count, 2) if total_count > 0 else 0,
            "avg_holding_hours": round(sum(c.holding_hours for c in strategy_cycles if c.holding_hours) / total_count, 1) if total_count > 0 else 0,
            "best_case": {
                "symbol": max(strategy_cycles, key=lambda c: c.roi_percent).symbol,
                "roi": round(max(strategy_cycles, key=lambda c: c.roi_percent).roi_percent, 2)
            } if strategy_cycles else None,
            "worst_case": {
                "symbol": min(strategy_cycles, key=lambda c: c.roi_percent).symbol,
                "roi": round(min(strategy_cycles, key=lambda c: c.roi_percent).roi_percent, 2)
            } if strategy_cycles else None
        }

    # 生成 Insight
    insight = _generate_strategy_insight(strategy_stats)

    return {
        "strategy_stats": strategy_stats,
        "insight": insight
    }

def _generate_strategy_insight(strategy_stats: dict) -> str:
    """生成策略分析的 Insight"""

    if not strategy_stats:
        return "暂无足够数据生成建议"

    # 找到胜率最高的策略
    best_strategy = max(strategy_stats.items(), key=lambda x: x[1]['win_rate'])

    # 找到平均收益最高的策略
    most_profitable = max(strategy_stats.items(), key=lambda x: x[1]['avg_roi'])

    if best_strategy[0] == most_profitable[0]:
        return f"'{best_strategy[0]}'策略表现最佳,胜率 {best_strategy[1]['win_rate']:.2f}%,平均收益 {best_strategy[1]['avg_roi']:.2f}%。建议重点使用此策略。"
    else:
        return f"'{best_strategy[0]}'胜率最高({best_strategy[1]['win_rate']:.2f}%),但'{most_profitable[0]}'平均收益最高({most_profitable[1]['avg_roi']:.2f}%)。建议根据风险偏好选择。"
```

#### 3.3.4 持仓时间分析

```python
def analyze_holding_time_pattern(
    db: Session,
    user_id: UUID
) -> dict:
    """分析持仓时间模式"""

    cycles = db.query(PositionCycle).filter(
        PositionCycle.user_id == user_id,
        PositionCycle.status == 'closed',
        PositionCycle.holding_hours.isnot(None)
    ).all()

    if not cycles:
        return {"message": "暂无数据"}

    # 按盈亏分组
    profit_cycles = [c for c in cycles if c.total_profit_loss > 0]
    loss_cycles = [c for c in cycles if c.total_profit_loss < 0]

    def calculate_avg(cycles_list):
        if not cycles_list:
            return 0
        return sum(c.holding_hours for c in cycles_list) / len(cycles_list)

    def calculate_median(cycles_list):
        if not cycles_list:
            return 0
        sorted_hours = sorted(c.holding_hours for c in cycles_list)
        n = len(sorted_hours)
        if n % 2 == 0:
            return (sorted_hours[n//2 - 1] + sorted_hours[n//2]) / 2
        else:
            return sorted_hours[n//2]

    profit_avg = calculate_avg(profit_cycles)
    loss_avg = calculate_avg(loss_cycles)

    result = {
        "profitable_trades": {
            "count": len(profit_cycles),
            "avg_holding_hours": round(profit_avg, 1),
            "median_holding_hours": round(calculate_median(profit_cycles), 1)
        },
        "loss_trades": {
            "count": len(loss_cycles),
            "avg_holding_hours": round(loss_avg, 1),
            "median_holding_hours": round(calculate_median(loss_cycles), 1)
        },
        "insight": _generate_holding_time_insight(profit_avg, loss_avg)
    }

    return result

def _generate_holding_time_insight(profit_avg: float, loss_avg: float) -> str:
    """生成持仓时间的 Insight"""

    if profit_avg == 0 or loss_avg == 0:
        return "暂无足够数据生成建议"

    ratio = profit_avg / loss_avg

    if ratio < 0.5:
        return f"⚠️ 你倾向于拿不住盈利(平均 {profit_avg:.1f}h),但拿得住亏损(平均 {loss_avg:.1f}h)。建议:让利润奔跑,及时止损。"
    elif ratio > 2:
        return f"✅ 优秀!你能够持有盈利仓位(平均 {profit_avg:.1f}h),并及时止损(平均 {loss_avg:.1f}h)。"
    else:
        return f"持仓时间较为均衡,盈利平均 {profit_avg:.1f}h,亏损平均 {loss_avg:.1f}h。"
```

---

## 4. API 端点设计

### 4.1 交易补录 API

```python
# backend/app/api/v1/endpoints/trades.py

@router.put("/{trade_id}/review")
async def review_trade(
    trade_id: UUID,
    review_data: TradeReviewRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """单笔交易补录"""
    return trade_review_service.review_trade(db, trade_id, current_user.id, review_data)

@router.post("/batch-review")
async def batch_review_trades(
    request: BatchReviewRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """批量补录交易"""
    return trade_review_service.batch_review_trades(
        db, current_user.id, request.trade_ids, request.common_data
    )

@router.get("/unreviewed")
async def get_unreviewed_trades(
    days: int = 7,
    account_id: Optional[UUID] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取未复盘的交易"""
    return trade_review_service.get_unreviewed_trades(db, current_user.id, days, account_id)
```

### 4.2 持仓周期 API

```python
# backend/app/api/v1/endpoints/position_cycles.py

@router.get("")
async def list_position_cycles(
    account_id: Optional[UUID] = None,
    symbol: Optional[str] = None,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """列出所有持仓周期"""
    return position_cycle_service.list_cycles(db, current_user.id, account_id, symbol, status)

@router.get("/{cycle_id}")
async def get_position_cycle(
    cycle_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取持仓周期详情"""
    return position_cycle_service.get_cycle(db, cycle_id, current_user.id)

@router.post("/auto-detect")
async def auto_detect_cycles(
    request: AutoDetectRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """自动识别持仓周期"""
    return position_cycle_service.auto_detect_position_cycles(
        db, request.account_id, request.symbol
    )

@router.post("/{cycle_id}/review")
async def review_position_cycle(
    cycle_id: UUID,
    review_data: CycleReviewRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """补充持仓周期的复盘总结"""
    return position_cycle_service.review_cycle(db, cycle_id, current_user.id, review_data)
```

### 4.3 纪律分析 API

```python
# backend/app/api/v1/endpoints/analytics.py

@router.get("/stop-loss-discipline")
async def get_stop_loss_discipline(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """止损纪律分析"""
    return discipline_analytics_service.analyze_stop_loss_discipline(
        db, current_user.id, start_date, end_date
    )

@router.get("/emotion-impact")
async def get_emotion_impact(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """情绪影响分析"""
    return discipline_analytics_service.analyze_emotion_impact(db, current_user.id)

@router.get("/strategy-effectiveness")
async def get_strategy_effectiveness(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """策略有效性分析"""
    return discipline_analytics_service.analyze_strategy_effectiveness(db, current_user.id)

@router.get("/holding-time-pattern")
async def get_holding_time_pattern(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """持仓时间模式分析"""
    return discipline_analytics_service.analyze_holding_time_pattern(db, current_user.id)

@router.get("/discipline-dashboard")
async def get_discipline_dashboard(
    time_range: str = "30d",  # 7d, 30d, 90d, all
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """综合纪律分析仪表盘"""
    return discipline_analytics_service.get_dashboard(db, current_user.id, time_range)
```

---

## 5. 前端页面设计

### 5.1 交易列表页增强

**新增功能**:
- 筛选未复盘的交易(显示红色标记)
- 点击交易卡片,弹出补录表单
- 批量选择,统一补充策略和情绪

**补录表单组件** (`ReviewTradeModal.tsx`):
```tsx
<Dialog>
  <DialogContent>
    <DialogHeader>补录交易信息</DialogHeader>

    <Form>
      {/* 情绪选择 */}
      <Select label="情绪状态">
        <option value="calm">😌 冷静</option>
        <option value="fearful">😰 恐惧</option>
        <option value="greedy">🤑 贪婪</option>
        <option value="fomo">😱 害怕踏空</option>
        <option value="panic">😨 恐慌</option>
        <option value="confident">😎 自信</option>
      </Select>

      {/* 情绪强度滑块 */}
      <Slider
        label="情绪强度"
        min={1}
        max={10}
        step={1}
      />

      {/* 止损止盈 */}
      <Input label="计划止损价" type="number" />
      <Input label="计划止盈价" type="number" />

      {/* 策略类型 */}
      <Select label="入场策略">
        <option value="底部反转">底部反转</option>
        <option value="形态突破">形态突破</option>
        <option value="回调低吸">回调低吸</option>
        <option value="其他">其他</option>
      </Select>

      {/* 补充备注 */}
      <Textarea label="补充备注" placeholder="可选..." />

      <Button type="submit">保存</Button>
    </Form>
  </DialogContent>
</Dialog>
```

### 5.2 持仓周期页面

**新建页面** `/position-cycles`:
- 展示所有持仓周期(已完成 + 进行中)
- 时间线展示每个周期的操作历史
- 盈亏和纪律评分可视化
- 补充复盘总结

**时间线组件** (`CycleTimeline.tsx`):
```tsx
<Timeline>
  {cycle.trades.map(trade => (
    <TimelineItem key={trade.id}>
      <TimelineDot color={getActionColor(trade.action_type)} />

      <TimelineContent>
        <div className="flex items-center gap-2">
          <ActionTypeBadge type={trade.action_type} />
          <span>{trade.quantity} @ {trade.price}</span>

          {trade.emotion_state && (
            <Badge variant="outline">
              {getEmotionIcon(trade.emotion_state)} {trade.emotion_state}
            </Badge>
          )}
        </div>

        <time className="text-sm text-gray-500">
          {formatDateTime(trade.trade_time)}
        </time>
      </TimelineContent>
    </TimelineItem>
  ))}
</Timeline>
```

### 5.3 纪律分析仪表盘

**新建页面** `/analytics/discipline`:

**布局结构**:
```tsx
<DisciplineDashboard>
  {/* 时间范围选择器 */}
  <Tabs value={timeRange} onValueChange={setTimeRange}>
    <TabsList>
      <TabsTrigger value="7d">近7天</TabsTrigger>
      <TabsTrigger value="30d">近30天</TabsTrigger>
      <TabsTrigger value="90d">近90天</TabsTrigger>
      <TabsTrigger value="all">全部</TabsTrigger>
    </TabsList>
  </Tabs>

  {/* 区域 1: 止损纪律 */}
  <Section title="止损执行纪律">
    <div className="grid md:grid-cols-2 gap-4">
      {/* 饼图 */}
      <Card>
        <PieChart
          data={[
            { name: '执行', value: stopLossData.executed_count },
            { name: '违背', value: stopLossData.violated_count }
          ]}
        />
        <div className="text-center mt-4">
          <div className="text-3xl font-bold">{stopLossData.execution_rate}%</div>
          <div className="text-sm text-gray-500">止损执行率</div>
        </div>
      </Card>

      {/* 违规列表 */}
      <Card>
        <CardHeader>违规案例(最严重的10个)</CardHeader>
        <CardContent>
          {stopLossData.violations.map(v => (
            <div key={v.symbol} className="flex justify-between py-2 border-b">
              <div>
                <div className="font-medium">{v.symbol}</div>
                <div className="text-sm text-gray-500">{v.emotion}</div>
              </div>
              <div className="text-right">
                <div className="text-red-600">{v.loss}</div>
                <div className="text-xs text-gray-500">{v.holding_hours}h</div>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>

    {/* Insight */}
    <Alert className="mt-4">
      <AlertDescription>{stopLossData.insight}</AlertDescription>
    </Alert>
  </Section>

  {/* 区域 2: 情绪影响 */}
  <Section title="情绪与收益关系">
    <Card>
      <BarChart
        data={Object.entries(emotionData.emotion_stats).map(([emotion, stats]) => ({
          emotion: getEmotionLabel(emotion),
          avg_roi: stats.avg_roi,
          cycle_count: stats.cycle_count
        }))}
        xKey="emotion"
        yKey="avg_roi"
      />
    </Card>

    <Alert className="mt-4">
      <AlertDescription>{emotionData.insight}</AlertDescription>
    </Alert>
  </Section>

  {/* 区域 3: 策略有效性 */}
  <Section title="策略胜率对比">
    <div className="grid md:grid-cols-2 gap-4">
      {/* 雷达图 */}
      <Card>
        <RadarChart
          data={Object.entries(strategyData.strategy_stats).map(([strategy, stats]) => ({
            strategy,
            win_rate: stats.win_rate,
            avg_roi: stats.avg_roi
          }))}
        />
      </Card>

      {/* 策略详情 */}
      <Card>
        {Object.entries(strategyData.strategy_stats).map(([strategy, stats]) => (
          <div key={strategy} className="mb-4 p-4 border rounded">
            <h4 className="font-medium mb-2">{strategy}</h4>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div>胜率: {stats.win_rate}%</div>
              <div>平均收益: {stats.avg_roi}%</div>
              <div>交易次数: {stats.cycle_count}</div>
              <div>平均持仓: {stats.avg_holding_hours}h</div>
            </div>
          </div>
        ))}
      </Card>
    </div>

    <Alert className="mt-4">
      <AlertDescription>{strategyData.insight}</AlertDescription>
    </Alert>
  </Section>

  {/* 区域 4: 持仓时间 */}
  <Section title="持仓时间模式">
    <Card>
      <div className="grid md:grid-cols-2 gap-8">
        <div className="text-center">
          <div className="text-green-600 text-4xl font-bold">
            {holdingTimeData.profitable_trades.avg_holding_hours}h
          </div>
          <div className="text-sm text-gray-500 mt-2">盈利交易平均持仓</div>
          <div className="text-xs text-gray-400">
            ({holdingTimeData.profitable_trades.count} 笔)
          </div>
        </div>

        <div className="text-center">
          <div className="text-red-600 text-4xl font-bold">
            {holdingTimeData.loss_trades.avg_holding_hours}h
          </div>
          <div className="text-sm text-gray-500 mt-2">亏损交易平均持仓</div>
          <div className="text-xs text-gray-400">
            ({holdingTimeData.loss_trades.count} 笔)
          </div>
        </div>
      </div>
    </Card>

    <Alert className="mt-4" variant={getInsightVariant(holdingTimeData.insight)}>
      <AlertDescription>{holdingTimeData.insight}</AlertDescription>
    </Alert>
  </Section>
</DisciplineDashboard>
```

---

## 6. 实现计划

### Phase 4.1: 数据模型和基础补录 (2-3天)

**后端任务**:
- [x] 创建数据库迁移:给 `trades` 表添加 9 个新字段
- [ ] 创建 `position_cycles` 表的迁移脚本
- [ ] 更新 Trade Model 添加新字段
- [ ] 创建 PositionCycle Model
- [ ] 更新 Trade Schema 支持补录字段
- [ ] 创建 PositionCycle Schema
- [ ] 实现 TradeReviewService 服务层
- [ ] 创建交易补录相关 API 端点
- [ ] 运行数据库迁移并测试

**前端任务**:
- [ ] 更新 Trade 类型定义
- [ ] 创建补录表单组件 `ReviewTradeModal`
- [ ] 交易列表页增强:未复盘标记、批量选择、快捷补录
- [ ] 测试补录流程

---

### Phase 4.2: 持仓周期自动识别 (2天)

**后端任务**:
- [ ] 实现 PositionCycleService
  - [ ] `auto_detect_position_cycles()` - 自动识别周期
  - [ ] `calculate_cycle_metrics()` - 计算指标
  - [ ] `check_stop_loss_execution()` - 判断止损执行
- [ ] 创建 API 端点:
  - [ ] `GET /api/v1/position-cycles`
  - [ ] `GET /api/v1/position-cycles/{id}`
  - [ ] `POST /api/v1/position-cycles/auto-detect`
  - [ ] `POST /api/v1/position-cycles/{id}/review`

**前端任务**:
- [ ] 创建持仓周期列表页 `/position-cycles`
- [ ] 设计时间线组件展示操作历史
- [ ] 创建周期复盘表单

---

### Phase 4.3: 纪律分析仪表盘 (3-4天)

**后端任务**:
- [ ] 实现 DisciplineAnalyticsService:
  - [ ] `analyze_stop_loss_discipline()` - 止损纪律报告
  - [ ] `analyze_emotion_impact()` - 情绪影响分析
  - [ ] `analyze_strategy_effectiveness()` - 策略有效性
  - [ ] `analyze_holding_time_pattern()` - 持仓时间模式
- [ ] 创建 API 端点(5个分析接口)

**前端任务**:
- [ ] 创建纪律分析仪表盘页 `/analytics/discipline`
- [ ] 集成图表库(Recharts)
- [ ] 实现 4 个分析区域
- [ ] 添加时间范围筛选器

---

## 7. 技术风险和注意事项

### 7.1 持仓周期识别准确性

**风险**: 需要处理合约双向持仓、部分平仓等复杂情况

**解决方案**:
- Phase 4.1 先支持现货简单场景
- 合约场景逐步完善,考虑 position_side 字段

### 7.2 情绪数据稀疏性

**风险**: 用户可能不会每笔都填写情绪

**解决方案**:
- 分析时标注样本数量
- 小样本(< 10)给出提示:"数据较少,仅供参考"

### 7.3 前端图表性能

**风险**: 大量数据时图表渲染可能较慢

**解决方案**:
- API 端返回聚合数据,前端只负责展示
- 图表组件使用虚拟化技术
- 添加加载状态

### 7.4 数据迁移

**风险**: 现有交易记录没有补录字段

**解决方案**:
- 所有新增字段都是 nullable
- 前端处理空值情况
- 提供批量补录工具

---

## 8. 成功标准

### 8.1 功能完整性
- ✅ 用户能在 2 分钟内完成一天交易的批量补录
- ✅ 持仓周期自动识别准确率 > 95%
- ✅ 支持至少 100 个持仓周期的分析计算

### 8.2 用户体验
- ✅ 补录表单简洁易用,不超过 5 个必填字段
- ✅ 纪律分析页面至少展示 4 个有价值的 Insight
- ✅ 页面加载时间 < 2 秒

### 8.3 数据准确性
- ✅ 止损执行判断准确率 > 90%
- ✅ 情绪分析样本数充足时,Insight 有参考价值
- ✅ 策略有效性统计无明显错误

---

## 9. 未来优化方向

### 9.1 AI 辅助功能
- 根据历史数据,自动推荐止损止盈价位
- 分析情绪文本,自动识别情绪状态
- 生成个性化的交易改进建议

### 9.2 移动端支持
- 移动端快速补录(语音转文字)
- 推送通知提醒补录
- 移动端查看纪律报告

### 9.3 社交功能
- 分享优秀的持仓周期案例
- 学习他人的交易纪律
- 纪律排行榜

### 9.4 高级分析
- 市场环境与策略的关系分析
- 时间段分析(早盘 vs 午盘 vs 尾盘)
- 宏观事件对交易纪律的影响

---

## 10. 文档维护

- **下次更新时间**: 完成 Phase 4.1 后
- **负责人**: [待填写]
- **关联文档**:
  - `docs/features/trading-rationale-and-charts.md` - Phase 3 功能文档
  - `docs/architecture.md` - 系统架构
  - `docs/development-plan.md` - 开发计划
  - `docs/api-reference.md` - API 文档(待创建)

---

## 附录

### A. 相关资源

- Recharts 文档: https://recharts.org/
- React Hook Form: https://react-hook-form.com/
- shadcn/ui Charts: https://ui.shadcn.com/docs/components/chart

### B. FAQ

**Q: 为什么不创建完整的计划系统?**
A: 基于实际使用场景,用户在交易时来不及填写计划,事后补录更符合实际。遵循 KISS 原则,先实现简单方案快速验证需求。

**Q: 情绪数据如何保证准确性?**
A: 情绪记录是主观的,系统只提供工具和分析,不保证绝对准确。重点是帮助用户识别模式,而非精确测量。

**Q: 持仓周期如何处理合约双向持仓?**
A: Phase 4.1 先支持现货和单向持仓合约。双向持仓需要根据 position_side 分别识别,将在后续版本支持。

**Q: 纪律评分的算法是否科学?**
A: 当前算法是简化版本,主要考虑止损执行、止盈执行和情绪稳定性。未来可以引入更多因素(如风险收益比、仓位管理等)并支持用户自定义权重。
