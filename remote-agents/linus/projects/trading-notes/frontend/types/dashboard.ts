export interface OverviewMetrics {
  total_market_value: string;
  total_cash_balance: string;
  total_assets: string;
  total_cost: string;
  total_pnl: string;
  total_pnl_percent: string;
  today_pnl?: string | null;
  today_pnl_percent?: string | null;
}

export interface MarketMetrics {
  value: string;
  pnl: string;
  count: number;
}

export interface PositionsSummaryMetrics {
  total_positions: number;
  profitable_count: number;
  losing_count: number;
  by_market: Record<string, MarketMetrics>;
}

export interface RecentTrade {
  id: string;
  symbol: string;
  symbol_name?: string;
  side: string;
  quantity: string;
  price: string;
  trade_time: string;
  account_name: string;
  account_type: string;
}

export interface QuickStats {
  trades_this_month: number;
  win_rate_this_month?: string | null;
}

export interface DashboardSummary {
  overview: OverviewMetrics;
  positions_summary: PositionsSummaryMetrics;
  recent_trades: RecentTrade[];
  discipline_score?: string | null;
  quick_stats: QuickStats;
}
