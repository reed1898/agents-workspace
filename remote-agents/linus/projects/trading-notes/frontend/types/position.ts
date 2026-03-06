export interface Position {
  id: string;
  account_id: string;
  symbol: string;
  symbol_name?: string;

  // 持仓类型和方向
  position_type: 'spot' | 'futures';
  position_side?: 'LONG' | 'SHORT' | null;

  // 数量和价格
  quantity: string;  // 现货:>0; 合约:正=多,负=空
  average_cost?: string;  // 现货使用
  entry_price?: string;  // 合约使用

  // 合约专用字段
  leverage?: string;
  margin_used?: string;
  liquidation_price?: string;

  // 通用字段
  current_price?: string;
  unrealized_pnl?: string;
  unrealized_pnl_percent?: string;
  roe_percent?: string;  // 合约ROE收益率
  first_buy_time?: string;
  notes?: string;

  holding_days?: number;
  last_updated: string;

  // 持仓状态
  is_closed: boolean;  // 是否已清仓
  closed_at?: string;  // 清仓时间
  final_price?: string;  // 清仓时的最终价格
  realized_pnl?: string;  // 已实现盈亏
  realized_pnl_percent?: string;  // 已实现盈亏百分比

  // 计算属性
  total_cost?: string;
  market_value?: string;
  is_profitable?: boolean;
}

export interface PositionListResponse {
  positions: Position[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface PositionStats {
  total_positions: number;
  total_cost: string;
  total_market_value: string;
  total_unrealized_pnl: string;
  total_unrealized_pnl_percent: string;
  total_realized_pnl: string;
  profitable_positions: number;
  losing_positions: number;
  average_holding_days?: number;
}

export interface PositionSummary {
  symbol: string;
  symbol_name?: string;
  quantity: string;
  average_cost: string;
  current_price?: string;
  market_value?: string;
  unrealized_pnl?: string;
  unrealized_pnl_percent?: string;
  holding_days?: number;
  account_name?: string;
  account_type?: string;
}
