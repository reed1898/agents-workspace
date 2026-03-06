# 交易理由和K线图功能设计文档

## 文档信息

- **创建日期**: 2025-11-03
- **状态**: 设计阶段
- **优先级**: 高
- **预计工期**: Phase 1 (2-3天), 完整实现 (7-10天)

## 1. 需求背景

### 业务需求

为交易记录系统添加操作理由记录和K线图关联功能,帮助用户:
1. 记录每次建仓/加仓/减仓/清仓的理由
2. 关联操作时的K线图(手动上传或自动获取)
3. 方便后续复盘和分析交易决策质量

### 用户调研结果

通过需求调研,用户选择了以下方案:
- **实现方式**: 混合方案(先简单后完整)
- **K线图来源**: 两者都要(优先手动上传,后续支持自动获取)
- **主要场景**: 记录历史(补录已有交易的理由)
- **操作类型**: 需要区分(建仓/加仓/减仓/清仓)

---

## 2. 架构设计

### 2.1 整体架构

采用**渐进式混合方案**,分为4个阶段实现:

```
Phase 1: 简单增强版 (MVP)
  ├── 在 Trade 表添加操作类型和理由字段
  ├── 支持手动上传K线图截图
  └── 基础UI展示和编辑

Phase 2: 体验优化
  ├── 批量导入支持理由
  ├── 操作历史时间线视图
  └── 理由编辑专门页面

Phase 3: 自动K线图
  ├── 集成K线数据API
  ├── 使用 Lightweight Charts 展示
  └── 自动标注买卖点

Phase 4: 完整计划系统 (可选)
  ├── 实现 trading_plans 表
  ├── 实现 trading_actions 表
  └── 纪律检查和偏差分析
```

### 2.2 数据模型设计

#### Phase 1: 扩展 Trade 表

在现有 `trades` 表上新增以下字段:

```sql
-- 数据库迁移 SQL
ALTER TABLE trades
ADD COLUMN action_type VARCHAR(20),     -- 操作类型
ADD COLUMN action_reason TEXT,          -- 操作理由
ADD COLUMN chart_image_url VARCHAR(500), -- K线图截图URL
ADD COLUMN chart_data JSONB;            -- K线数据快照(可选)

-- 创建索引
CREATE INDEX idx_trades_action_type ON trades(action_type);
CREATE INDEX idx_trades_symbol_action ON trades(symbol, action_type);
```

**字段说明**:

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `action_type` | VARCHAR(20) | 操作类型枚举 | 'open', 'add', 'reduce', 'close' |
| `action_reason` | TEXT | 操作理由(支持Markdown) | "突破前高阻力位,MACD金叉..." |
| `chart_image_url` | VARCHAR(500) | K线图截图存储路径 | "/uploads/charts/xxx.png" |
| `chart_data` | JSONB | 关键K线数据快照(可选) | `{"high": 50000, "low": 48000, ...}` |

**操作类型枚举**:

```python
from enum import Enum

class ActionType(str, Enum):
    OPEN = "open"       # 建仓(首次买入)
    ADD = "add"         # 加仓(持仓中增加)
    REDUCE = "reduce"   # 减仓(部分卖出)
    CLOSE = "close"     # 清仓(全部卖出/平仓)
```

#### 操作类型自动判断逻辑

系统可以根据交易方向和持仓状态自动推断 `action_type`:

**现货逻辑**:
```python
def infer_spot_action_type(symbol, side, account_id):
    existing_position = get_position(symbol, account_id)

    if side == 'buy':
        if not existing_position or existing_position.quantity == 0:
            return ActionType.OPEN  # 建仓
        else:
            return ActionType.ADD   # 加仓

    elif side == 'sell':
        if not existing_position:
            return None  # 异常情况

        remaining = existing_position.quantity - trade_quantity
        if remaining <= 0:
            return ActionType.CLOSE  # 清仓
        else:
            return ActionType.REDUCE # 减仓
```

**合约逻辑**:
```python
def infer_futures_action_type(symbol, position_side, account_id):
    # position_side: LONG/SHORT (开多/开空)
    existing_position = get_futures_position(symbol, position_side, account_id)

    if is_opening_order:  # 开仓订单
        if not existing_position or existing_position.quantity == 0:
            return ActionType.OPEN  # 建仓
        else:
            return ActionType.ADD   # 加仓

    elif is_closing_order:  # 平仓订单
        if remaining_quantity <= 0:
            return ActionType.CLOSE  # 平仓
        else:
            return ActionType.REDUCE # 减仓
```

**UI 行为**:
- 创建交易时,系统自动判断并预填充 `action_type`
- 用户可以手动修改(处理特殊情况)
- 导入历史数据时,可批量推断或手动指定

#### Phase 4: 完整计划系统(未来扩展)

当简单方案不够用时,可以升级到完整的计划系统:

```sql
-- 交易计划表
CREATE TABLE trading_plans (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    account_id UUID NOT NULL,
    symbol VARCHAR(50) NOT NULL,
    plan_type VARCHAR(20) NOT NULL, -- 'spot' | 'futures'

    -- 计划内容
    entry_reason TEXT NOT NULL,           -- 入场理由
    technical_analysis TEXT,              -- 技术面分析
    fundamental_analysis TEXT,            -- 基本面分析
    entry_signals JSONB,                  -- 入场信号

    -- 风险管理
    risk_reward_ratio DECIMAL(10,2),      -- 风险收益比
    position_size_percent DECIMAL(5,2),   -- 仓位占比
    stop_loss_price DECIMAL(20,8),        -- 止损价
    take_profit_prices JSONB,             -- 多个止盈位

    -- 状态
    status VARCHAR(20) DEFAULT 'active',  -- 'active' | 'completed' | 'cancelled'
    created_at TIMESTAMP DEFAULT NOW(),
    closed_at TIMESTAMP
);

-- 交易动作表(关联计划和实际交易)
CREATE TABLE trading_actions (
    id UUID PRIMARY KEY,
    plan_id UUID REFERENCES trading_plans(id),
    user_id UUID NOT NULL,
    account_id UUID NOT NULL,

    -- 动作类型
    action_type VARCHAR(20) NOT NULL,     -- 'open' | 'add' | 'reduce' | 'close'
    action_reason TEXT,                   -- 动作理由

    -- 关联的实际交易
    trade_ids UUID[],                     -- 关联的多笔交易

    -- 情绪跟踪
    emotion_tags VARCHAR(50)[],           -- 情绪标签
    emotion_note TEXT,                    -- 情绪备注

    -- K线图
    chart_image_url VARCHAR(500),
    chart_data JSONB,

    created_at TIMESTAMP DEFAULT NOW()
);
```

**升级路径**:
- Phase 1 的 `action_type` 和 `action_reason` 可以平滑迁移到 `trading_actions`
- 老数据作为"未关联计划的独立交易"继续存在
- 新数据可以选择性地创建计划或直接记录

---

## 3. 技术实现

### 3.1 后端实现

#### 3.1.1 数据库迁移

创建 Alembic 迁移脚本:

```python
# backend/alembic/versions/xxxx_add_trade_rationale.py
"""add trade rationale and chart fields

Revision ID: xxxx
Revises: yyyy
Create Date: 2025-11-03
"""

def upgrade():
    op.add_column('trades', sa.Column('action_type', sa.String(20), nullable=True))
    op.add_column('trades', sa.Column('action_reason', sa.Text(), nullable=True))
    op.add_column('trades', sa.Column('chart_image_url', sa.String(500), nullable=True))
    op.add_column('trades', sa.Column('chart_data', sa.JSON(), nullable=True))

    op.create_index('idx_trades_action_type', 'trades', ['action_type'])
    op.create_index('idx_trades_symbol_action', 'trades', ['symbol', 'action_type'])

def downgrade():
    op.drop_index('idx_trades_symbol_action')
    op.drop_index('idx_trades_action_type')
    op.drop_column('trades', 'chart_data')
    op.drop_column('trades', 'chart_image_url')
    op.drop_column('trades', 'action_reason')
    op.drop_column('trades', 'action_type')
```

#### 3.1.2 Model 更新

```python
# backend/app/models/trade.py
from sqlalchemy import Column, String, Text
from sqlalchemy import JSON

class Trade(Base):
    __tablename__ = "trades"

    # ... 现有字段 ...

    # 新增字段
    action_type = Column(String(20), nullable=True, index=True)
    action_reason = Column(Text, nullable=True)
    chart_image_url = Column(String(500), nullable=True)
    chart_data = Column(JSON, nullable=True)
```

#### 3.1.3 Schema 更新

```python
# backend/app/schemas/trade.py
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class ActionType(str, Enum):
    OPEN = "open"
    ADD = "add"
    REDUCE = "reduce"
    CLOSE = "close"

class TradeCreate(BaseModel):
    # ... 现有字段 ...

    # 新增字段(可选)
    action_type: Optional[ActionType] = None
    action_reason: Optional[str] = None
    chart_image_url: Optional[str] = None

class TradeUpdate(BaseModel):
    # ... 现有字段 ...

    action_type: Optional[ActionType] = None
    action_reason: Optional[str] = None
    chart_image_url: Optional[str] = None

class TradeResponse(BaseModel):
    # ... 现有字段 ...

    action_type: Optional[ActionType] = None
    action_reason: Optional[str] = None
    chart_image_url: Optional[str] = None
```

#### 3.1.4 Service 层业务逻辑

```python
# backend/app/services/trade_service.py

class TradeService:

    @staticmethod
    def infer_action_type(
        symbol: str,
        side: str,
        quantity: Decimal,
        account_id: UUID,
        position_side: Optional[str] = None  # 合约专用
    ) -> Optional[ActionType]:
        """自动推断操作类型"""

        # 获取当前持仓
        position = position_service.get_position_by_symbol(
            account_id=account_id,
            symbol=symbol,
            position_side=position_side
        )

        # 现货逻辑
        if position_side is None:
            if side == 'buy':
                if not position or position.quantity == 0:
                    return ActionType.OPEN
                else:
                    return ActionType.ADD
            elif side == 'sell':
                if not position:
                    return None
                remaining = position.quantity - quantity
                return ActionType.CLOSE if remaining <= 0 else ActionType.REDUCE

        # 合约逻辑(TODO: 实现合约判断)
        else:
            pass

        return None

    async def create_trade(
        self,
        db: Session,
        trade_data: TradeCreate,
        user_id: UUID
    ) -> Trade:
        """创建交易,自动推断 action_type"""

        # 如果没有指定 action_type,自动推断
        if not trade_data.action_type:
            trade_data.action_type = self.infer_action_type(
                symbol=trade_data.symbol,
                side=trade_data.side,
                quantity=trade_data.quantity,
                account_id=trade_data.account_id,
                position_side=getattr(trade_data, 'position_side', None)
            )

        # 创建交易记录
        trade = Trade(**trade_data.dict())
        db.add(trade)
        db.commit()

        return trade
```

#### 3.1.5 API 端点

```python
# backend/app/api/v1/endpoints/trades.py

@router.put("/{trade_id}/rationale")
async def update_trade_rationale(
    trade_id: UUID,
    action_type: Optional[ActionType] = None,
    action_reason: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """单独更新交易理由"""
    trade = trade_service.get_trade(db, trade_id, current_user.id)

    if action_type:
        trade.action_type = action_type
    if action_reason:
        trade.action_reason = action_reason

    db.commit()
    return trade

@router.post("/{trade_id}/upload-chart")
async def upload_chart_image(
    trade_id: UUID,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """上传K线图截图"""

    # 验证文件类型
    if not file.content_type.startswith('image/'):
        raise HTTPException(400, "Only image files are allowed")

    # 保存文件
    file_path = await save_upload_file(file, "charts")

    # 更新交易记录
    trade = trade_service.get_trade(db, trade_id, current_user.id)
    trade.chart_image_url = file_path
    db.commit()

    return {"chart_url": file_path}

@router.get("/by-symbol/{symbol}")
async def get_trades_by_symbol(
    symbol: str,
    account_id: Optional[UUID] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """按标的查询所有交易(用于展示操作历史)"""
    trades = trade_service.get_trades_by_symbol(
        db,
        symbol=symbol,
        account_id=account_id,
        user_id=current_user.id
    )
    return trades
```

#### 3.1.6 文件上传处理

```python
# backend/app/utils/file_upload.py
import os
import uuid
from pathlib import Path
from fastapi import UploadFile

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

async def save_upload_file(file: UploadFile, subdir: str) -> str:
    """保存上传的文件"""

    # 创建子目录
    target_dir = UPLOAD_DIR / subdir
    target_dir.mkdir(exist_ok=True)

    # 生成唯一文件名
    ext = Path(file.filename).suffix
    filename = f"{uuid.uuid4()}{ext}"
    file_path = target_dir / filename

    # 保存文件
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # 返回相对路径
    return f"/uploads/{subdir}/{filename}"
```

### 3.2 前端实现

#### 3.2.1 类型定义

```typescript
// frontend/src/types/trade.ts

export type ActionType = 'open' | 'add' | 'reduce' | 'close';

export interface Trade {
  // ... 现有字段 ...

  // 新增字段
  action_type?: ActionType;
  action_reason?: string;
  chart_image_url?: string;
}

// 操作类型显示配置
export const ACTION_TYPE_CONFIG: Record<ActionType, {
  label: string;
  color: string;
  icon: string;
}> = {
  open: {
    label: '建仓',
    color: 'bg-green-500',
    icon: '🟢'
  },
  add: {
    label: '加仓',
    color: 'bg-blue-500',
    icon: '🔵'
  },
  reduce: {
    label: '减仓',
    color: 'bg-orange-500',
    icon: '🟠'
  },
  close: {
    label: '清仓',
    color: 'bg-red-500',
    icon: '🔴'
  }
};
```

#### 3.2.2 UI 组件

```tsx
// frontend/src/components/features/trades/ActionTypeBadge.tsx
import { ActionType, ACTION_TYPE_CONFIG } from '@/types/trade';

interface Props {
  type?: ActionType;
}

export function ActionTypeBadge({ type }: Props) {
  if (!type) return null;

  const config = ACTION_TYPE_CONFIG[type];

  return (
    <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium text-white ${config.color}`}>
      <span className="mr-1">{config.icon}</span>
      {config.label}
    </span>
  );
}
```

```tsx
// frontend/src/components/features/trades/RationaleInput.tsx
import { Textarea } from '@/components/ui/textarea';

interface Props {
  value?: string;
  onChange: (value: string) => void;
  placeholder?: string;
}

export function RationaleInput({ value, onChange, placeholder }: Props) {
  return (
    <div className="space-y-2">
      <label className="text-sm font-medium">操作理由</label>
      <Textarea
        value={value || ''}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder || '请输入操作理由(支持 Markdown)'}
        rows={4}
        className="font-mono text-sm"
      />
      <p className="text-xs text-gray-500">
        提示:记录你的交易决策依据,比如技术指标、基本面因素等
      </p>
    </div>
  );
}
```

```tsx
// frontend/src/components/features/trades/ChartImageUpload.tsx
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Upload } from 'lucide-react';

interface Props {
  tradeId: string;
  currentUrl?: string;
  onUploadSuccess: (url: string) => void;
}

export function ChartImageUpload({ tradeId, currentUrl, onUploadSuccess }: Props) {
  const [uploading, setUploading] = useState(false);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`/api/v1/trades/${tradeId}/upload-chart`, {
        method: 'POST',
        body: formData,
        headers: {
          'Authorization': `Bearer ${getToken()}`
        }
      });

      const data = await response.json();
      onUploadSuccess(data.chart_url);
    } catch (error) {
      console.error('Upload failed:', error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-2">
      <label className="text-sm font-medium">K线图</label>

      {currentUrl && (
        <div className="border rounded-lg p-2">
          <img src={currentUrl} alt="K线图" className="max-w-full h-auto" />
        </div>
      )}

      <div>
        <input
          type="file"
          accept="image/*"
          onChange={handleUpload}
          className="hidden"
          id="chart-upload"
        />
        <label htmlFor="chart-upload">
          <Button variant="outline" size="sm" asChild disabled={uploading}>
            <span>
              <Upload className="w-4 h-4 mr-2" />
              {uploading ? '上传中...' : currentUrl ? '更换图片' : '上传K线图'}
            </span>
          </Button>
        </label>
      </div>
    </div>
  );
}
```

#### 3.2.3 页面改造

**交易列表页**:
```tsx
// frontend/src/app/trades/page.tsx

// 在表格中添加"操作类型"列
<TableHead>操作类型</TableHead>

// 表格行中显示
<TableCell>
  <ActionTypeBadge type={trade.action_type} />
</TableCell>

// 添加理由显示(hover tooltip)
<TableCell className="max-w-md">
  <TooltipProvider>
    <Tooltip>
      <TooltipTrigger asChild>
        <span className="cursor-help truncate">
          {trade.action_reason ? trade.action_reason.slice(0, 30) + '...' : '-'}
        </span>
      </TooltipTrigger>
      <TooltipContent className="max-w-sm">
        <p className="whitespace-pre-wrap">{trade.action_reason}</p>
      </TooltipContent>
    </Tooltip>
  </TooltipProvider>
</TableCell>
```

**标的详情页**:
```tsx
// frontend/src/app/symbols/[symbol]/page.tsx

// 添加操作历史时间线
<div className="mt-8">
  <h2 className="text-xl font-bold mb-4">操作历史</h2>

  <div className="space-y-4">
    {trades.map(trade => (
      <div key={trade.id} className="border-l-4 pl-4"
           style={{ borderColor: ACTION_TYPE_CONFIG[trade.action_type]?.color }}>
        <div className="flex items-center gap-2 mb-2">
          <ActionTypeBadge type={trade.action_type} />
          <span className="text-sm text-gray-500">
            {formatDate(trade.trade_time)}
          </span>
        </div>

        <div className="text-sm mb-2">
          <span className="font-medium">{trade.side === 'buy' ? '买入' : '卖出'}</span>
          {' '}
          {trade.quantity} @ {trade.price}
        </div>

        {trade.action_reason && (
          <div className="text-sm text-gray-700 bg-gray-50 p-2 rounded">
            {trade.action_reason}
          </div>
        )}

        {trade.chart_image_url && (
          <div className="mt-2">
            <img src={trade.chart_image_url} alt="K线图"
                 className="max-w-md rounded border cursor-pointer"
                 onClick={() => openImageModal(trade.chart_image_url)} />
          </div>
        )}
      </div>
    ))}
  </div>
</div>
```

---

## 4. K线图技术选型

### 4.1 方案对比

| 方案 | 优点 | 缺点 | 适用阶段 |
|------|------|------|----------|
| **手动上传截图** | 简单快速,无API依赖,适合补录历史 | 需要手动操作,不能交互 | Phase 1 ⭐⭐⭐⭐⭐ |
| **Lightweight Charts** | 轻量级,来自TradingView,专业K线图 | 需要K线数据API | Phase 3 ⭐⭐⭐⭐ |
| **ECharts** | 功能强大,中文文档好,支持多种图表 | 体积较大(~300KB) | Phase 3 ⭐⭐⭐ |
| **Recharts** | React原生,简单易用 | K线图支持较弱 | ⭐⭐ |

### 4.2 推荐方案

**Phase 1: 手动上传截图**
- 实现图片上传接口
- 存储在本地 `/uploads/charts/` 或对象存储(阿里云OSS/AWS S3)
- 前端展示图片,支持点击放大

**Phase 3: Lightweight Charts**
- 安装库: `npm install lightweight-charts`
- 集成K线数据API
- 自动标注买卖点

### 4.3 K线数据源

| 市场 | 推荐数据源 | API 地址 | 费用 |
|------|------------|----------|------|
| **加密货币** | 币安API | `GET /api/v3/klines` | 免费 |
| **加密货币** | CCXT | 已有依赖 | 免费 |
| **美股** | Yahoo Finance | 非官方API | 免费(有限制) |
| **美股** | Alpha Vantage | alphaantage.co/documentation | 免费500次/天 |
| **A股/港股** | Tushare | tushare.pro | 需要积分 |

---

## 5. 实现计划

### Phase 1: 核心功能 (预计 2-3 天)

#### Day 1: 后端基础
- [x] 创建数据库迁移:添加 4 个新字段
- [x] 更新 Trade 模型和 Schema
- [x] 实现 `infer_action_type()` 自动判断逻辑
- [x] 更新现有 API 支持新字段

#### Day 2: 图片上传
- [x] 实现图片上传接口
- [x] 配置文件存储(本地或云存储)
- [x] 测试上传和访问

#### Day 3: 前端界面
- [x] 更新类型定义
- [x] 创建 UI 组件(标签、输入框、图片上传)
- [x] 改造交易列表页
- [x] 改造标的详情页

### Phase 2: 体验优化 (预计 1-2 天)

- [ ] 批量导入支持理由
- [ ] 理由编辑专门页面(支持富文本/Markdown)
- [ ] 操作历史时间线视图
- [ ] 数据统计(各类操作次数分析)

### Phase 3: 自动K线 (预计 2-3 天)

- [x] 集成 Lightweight Charts 库
- [x] 实现 K线数据获取服务
- [x] 在详情页展示交互式K线图
- [x] 标注买卖点
- [x] 支持时间范围选择

### Phase 4: 完整计划系统 (可选,预计 5-7 天)

- [ ] 创建 `trading_plans` 和 `trading_actions` 表
- [ ] 实现计划创建和管理
- [ ] 交易与计划的关联
- [ ] 纪律检查和偏差分析
- [ ] 复盘报告生成

---

## 6. 数据示例

### 6.1 补录历史交易

```json
{
  "symbol": "BTCUSDT",
  "side": "buy",
  "quantity": 0.5,
  "price": 50000,
  "trade_time": "2024-01-15T10:30:00Z",
  "action_type": "open",
  "action_reason": "突破前高阻力位,MACD金叉,成交量放大,形态上看多头趋势确立。目标位55000,止损48000。",
  "chart_image_url": null
}
```

### 6.2 批量导入CSV

```csv
symbol,side,quantity,price,trade_time,action_type,action_reason
BTCUSDT,buy,0.5,50000,2024-01-15 10:30:00,open,"突破前高,MACD金叉"
BTCUSDT,buy,0.3,52000,2024-01-20 14:00:00,add,"回调支撑位企稳,继续看多"
BTCUSDT,sell,0.4,54000,2024-01-25 09:00:00,reduce,"达到目标位,减仓止盈"
BTCUSDT,sell,0.4,55000,2024-01-30 16:00:00,close,"突破目标位,全部获利了结"
```

---

## 7. 技术风险和注意事项

### 7.1 数据一致性

**风险**: 现有交易没有 `action_type`,新功能上线后混合展示可能混乱

**解决方案**:
1. 数据库字段设为 `nullable=True`
2. 前端处理空值情况,显示"-"或"未分类"
3. 提供批量推断工具,一键为历史数据补充 `action_type`

### 7.2 文件存储

**风险**: 大量图片上传可能占用大量磁盘空间

**解决方案**:
1. 限制单张图片大小(如 5MB)
2. 使用图片压缩(Pillow库)
3. 考虑使用对象存储(OSS/S3)而非本地存储
4. 定期清理未关联的图片文件

### 7.3 性能考虑

**风险**: K线数据API调用可能较慢,影响页面加载

**解决方案**:
1. 使用 Redis 缓存K线数据(TTL: 5分钟)
2. 前端懒加载K线图(只在用户点击时加载)
3. 提供"仅显示截图"选项,跳过API调用

---

## 8. 测试计划

### 8.1 单元测试

- [ ] `infer_action_type()` 各种场景测试(现货/合约,建仓/加仓/减仓/清仓)
- [ ] 文件上传接口测试(正常上传、文件类型验证、大小限制)
- [ ] API 端点测试(创建/更新/查询带理由的交易)

### 8.2 集成测试

- [ ] 完整流程测试:创建交易 → 自动推断类型 → 更新理由 → 上传图片
- [ ] 批量导入测试:CSV包含理由字段
- [ ] 前后端联调测试

### 8.3 用户验收测试

- [ ] 补录历史交易,验证理由保存和显示
- [ ] 上传K线图截图,验证图片显示和存储
- [ ] 查看标的详情页,验证操作历史时间线

---

## 9. 未来优化方向

1. **AI 辅助分析**
   - 自动分析K线图,提供技术指标建议
   - 根据历史理由,训练模型预测交易质量

2. **移动端支持**
   - 移动端理由输入(语音转文字)
   - 手机拍照直接上传K线图

3. **社交功能**
   - 分享交易理由和图表
   - 学习他人的优秀交易决策

4. **高级分析**
   - 理由质量评分(AI分析理由的完整性)
   - 建仓理由和最终结果的相关性分析

---

## 10. 文档维护

- **下次更新时间**: 完成 Phase 1 后
- **负责人**: [待填写]
- **关联文档**:
  - `docs/architecture.md` - 系统架构
  - `docs/development-plan.md` - 开发计划
  - `docs/api-reference.md` - API 文档(待创建)

---

## 附录

### A. 相关资源

- Lightweight Charts 文档: https://tradingview.github.io/lightweight-charts/
- 币安 K线API: https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data
- CCXT 文档: https://docs.ccxt.com/

### B. FAQ

**Q: 为什么不直接实现完整的计划系统?**
A: 遵循 KISS 原则,先实现简单方案快速验证需求,避免过度设计。

**Q: 手动上传的图片能否自动识别?**
A: Phase 1 不支持,未来可以考虑集成 OCR 识别K线图中的价格信息。

**Q: 是否支持多张K线图?**
A: Phase 1 只支持一张,Phase 2 可以扩展为数组字段支持多张。

**Q: 合约如何区分开多和开空的理由?**
A: 通过 `position_side` 字段区分,每笔交易的理由独立记录。
