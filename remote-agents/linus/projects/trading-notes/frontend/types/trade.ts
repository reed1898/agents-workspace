import type { AccountType } from '@/lib/types/account';

// 操作类型枚举
export type ActionType = 'open' | 'add' | 'reduce' | 'close';

// 操作类型显示配置
export const ACTION_TYPE_CONFIG: Record<ActionType, {
  label: string;
  color: string;
  bgColor: string;
  icon: string;
}> = {
  open: {
    label: '建仓',
    color: 'text-green-700',
    bgColor: 'bg-green-100',
    icon: '🟢'
  },
  add: {
    label: '加仓',
    color: 'text-blue-700',
    bgColor: 'bg-blue-100',
    icon: '🔵'
  },
  reduce: {
    label: '减仓',
    color: 'text-orange-700',
    bgColor: 'bg-orange-100',
    icon: '🟠'
  },
  close: {
    label: '清仓',
    color: 'text-red-700',
    bgColor: 'bg-red-100',
    icon: '🔴'
  }
};

export interface Trade {
  id: string;
  account_id: string;
  account_type?: AccountType;
  symbol: string;
  symbol_name?: string;
  side: 'buy' | 'sell';
  quantity: string;
  price: string;
  fee: string;
  fee_currency?: string;
  trade_time: string;
  trade_id_external?: string;
  sync_source: 'api' | 'manual' | 'import';
  notes?: string;

  // 合约交易专用字段
  position_side?: 'LONG' | 'SHORT' | null;
  leverage?: string;
  margin?: string;

  // 交易理由和K线图字段 (Phase 3)
  action_type?: ActionType;
  action_reason?: string;
  action_strategy?: string;
  chart_image_url?: string;
  chart_data?: Record<string, unknown>;

  // 纪律分析字段 (Phase 4)
  emotion_state?: EmotionState;
  emotion_intensity?: number;
  planned_stop_loss?: string;
  actual_stop_loss?: string;
  stop_loss_executed?: boolean;
  planned_take_profit?: string;
  actual_take_profit?: string;
  entry_strategy?: EntryStrategy;
  exit_strategy?: ExitStrategy;
  reviewed?: boolean;
  reviewed_at?: string;

  created_at: string;
  updated_at: string;
  total_amount?: string;
  total_cost?: string;
}

export interface TradeCreate {
  account_id: string;
  symbol: string;
  side: 'buy' | 'sell';
  quantity: string | number;
  price: string | number;
  fee?: string | number;
  fee_currency?: string;
  trade_time: string;
  trade_id_external?: string;
  sync_source?: 'api' | 'manual' | 'import';
  notes?: string;

  // 合约字段
  position_side?: 'LONG' | 'SHORT';
  leverage?: string | number;
  margin?: string | number;

  // 交易理由和K线图字段
  action_type?: ActionType;
  action_reason?: string;
  action_strategy?: string;
  chart_image_url?: string;
}

export interface TradeListResponse {
  trades: Trade[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface TradeStats {
  total_trades: number;
  buy_count: number;
  sell_count: number;
  total_volume: string;
  total_fees: string;
  unique_symbols: number;
  first_trade_date?: string;
  last_trade_date?: string;
}

// ============ Phase 4: 纪律分析类型 ============

// 情绪状态枚举
export type EmotionState = 'calm' | 'confident' | 'fearful' | 'greedy' | 'fomo' | 'panic' | 'excited' | 'regretful';

// 入场策略枚举
export type EntryStrategy = '底部反转' | '形态突破' | '回调低吸' | '其他';

// 出场策略枚举
export type ExitStrategy = '止盈离场' | '止损离场' | '形态破坏' | '预期改变' | '其他';

// 情绪状态配置
export const EMOTION_CONFIG: Record<EmotionState, {
  label: string;
  emoji: string;
  color: string;
  bgColor: string;
}> = {
  calm: {
    label: '冷静',
    emoji: '😌',
    color: 'text-blue-700',
    bgColor: 'bg-blue-50'
  },
  confident: {
    label: '自信',
    emoji: '😎',
    color: 'text-green-700',
    bgColor: 'bg-green-50'
  },
  fearful: {
    label: '恐惧',
    emoji: '😰',
    color: 'text-purple-700',
    bgColor: 'bg-purple-50'
  },
  greedy: {
    label: '贪婪',
    emoji: '🤑',
    color: 'text-yellow-700',
    bgColor: 'bg-yellow-50'
  },
  fomo: {
    label: '害怕踏空',
    emoji: '😱',
    color: 'text-orange-700',
    bgColor: 'bg-orange-50'
  },
  panic: {
    label: '恐慌',
    emoji: '😨',
    color: 'text-red-700',
    bgColor: 'bg-red-50'
  },
  excited: {
    label: '兴奋',
    emoji: '🤩',
    color: 'text-pink-700',
    bgColor: 'bg-pink-50'
  },
  regretful: {
    label: '后悔',
    emoji: '😔',
    color: 'text-gray-700',
    bgColor: 'bg-gray-50'
  }
};

// 入场策略配置
export const ENTRY_STRATEGY_CONFIG: Record<EntryStrategy, {
  label: string;
  color: string;
  bgColor: string;
}> = {
  '底部反转': {
    label: '底部反转',
    color: 'text-green-700',
    bgColor: 'bg-green-100'
  },
  '形态突破': {
    label: '形态突破',
    color: 'text-blue-700',
    bgColor: 'bg-blue-100'
  },
  '回调低吸': {
    label: '回调低吸',
    color: 'text-purple-700',
    bgColor: 'bg-purple-100'
  },
  '其他': {
    label: '其他',
    color: 'text-gray-700',
    bgColor: 'bg-gray-100'
  }
};

// 出场策略配置
export const EXIT_STRATEGY_CONFIG: Record<ExitStrategy, {
  label: string;
  color: string;
  bgColor: string;
}> = {
  '止盈离场': {
    label: '止盈离场',
    color: 'text-green-700',
    bgColor: 'bg-green-100'
  },
  '止损离场': {
    label: '止损离场',
    color: 'text-red-700',
    bgColor: 'bg-red-100'
  },
  '形态破坏': {
    label: '形态破坏',
    color: 'text-orange-700',
    bgColor: 'bg-orange-100'
  },
  '预期改变': {
    label: '预期改变',
    color: 'text-purple-700',
    bgColor: 'bg-purple-100'
  },
  '其他': {
    label: '其他',
    color: 'text-gray-700',
    bgColor: 'bg-gray-100'
  }
};

// 兼容旧代码
export const STRATEGY_CONFIG = ENTRY_STRATEGY_CONFIG;

// 交易补录数据
export interface TradeReviewData {
  action_type?: ActionType;
  action_reason?: string;
  emotion_state?: EmotionState;
  emotion_intensity?: number;
  planned_stop_loss?: string | number;
  actual_stop_loss?: string | number;
  stop_loss_executed?: boolean;
  planned_take_profit?: string | number;
  actual_take_profit?: string | number;
  entry_strategy?: EntryStrategy;
  action_strategy?: string;
  exit_strategy?: ExitStrategy;
  notes?: string;
}

// 批量补录请求
export interface BatchReviewRequest {
  trade_ids: string[];
  common_data: Record<string, unknown>;
}
