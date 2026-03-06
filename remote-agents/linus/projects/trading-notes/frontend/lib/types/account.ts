export type AccountType = 'us_stock' | 'a_stock' | 'hk_stock' | 'crypto';
export type CryptoSubType = 'binance_spot' | 'binance_futures';

export interface TradeAccount {
  id: string;
  user_id: string;
  account_name: string;
  account_type: AccountType;
  broker?: string;  // 券商/交易所: moomoo, interactive_brokers, binance, okx, etc.
  description?: string;
  tags?: string[];
  is_active: boolean;
  sync_start_date?: string;
  last_sync_at?: string;
  cash_balance?: string;
  cash_currency?: string;
  created_at: string;
  updated_at: string;
  extra_config?: Record<string, any>;
  has_api_credentials?: boolean;
  has_gmail_credentials?: boolean;
  ibkr_flex_token?: string;
  ibkr_flex_query_id?: string;
  gmail_address?: string;
  gmail_connected_at?: string;
}

export interface TradeAccountCreate {
  account_name: string;
  account_type: AccountType;
  broker?: string;  // 券商/交易所
  crypto_sub_type?: CryptoSubType;  // 新增:加密货币子类型
  description?: string;
  tags?: string[];
  sync_start_date?: string;
  api_key?: string;
  api_secret?: string;
  ibkr_flex_token?: string;
  ibkr_flex_query_id?: string;
  cash_balance?: string | number;
  cash_currency?: string;
  extra_config?: Record<string, any>;
}

export interface TradeAccountUpdate {
  account_name?: string;
  description?: string;
  tags?: string[];
  sync_start_date?: string;
  api_key?: string;
  api_secret?: string;
  ibkr_flex_token?: string;
  ibkr_flex_query_id?: string;
  is_active?: boolean;
  cash_balance?: string | number;
  cash_currency?: string;
  extra_config?: Record<string, any>;
}

export const ACCOUNT_TYPE_LABELS: Record<AccountType, string> = {
  us_stock: '美股',
  a_stock: 'A股',
  hk_stock: '港股',
  crypto: '加密货币'
};

export const ACCOUNT_TYPE_OPTIONS = [
  { value: 'crypto', label: '加密货币', description: '支持 Binance 等交易所' },
  { value: 'us_stock', label: '美股', description: 'Interactive Brokers' },
  { value: 'a_stock', label: 'A股', description: '同花顺、东方财富等' },
  { value: 'hk_stock', label: '港股', description: '富途、老虎等' },
] as const;

export const CRYPTO_SUB_TYPE_OPTIONS = [
  { value: 'binance_spot', label: '币安现货', description: '现货交易账户' },
  { value: 'binance_futures', label: '币安永续合约', description: '永续合约交易账户' },
] as const;

// 券商选项 - 按市场类型分类
export const BROKER_OPTIONS = {
  us_stock: [
    { value: 'moomoo', label: 'moomoo', description: 'moomoo美股' },
    { value: 'interactive_brokers', label: 'Interactive Brokers', description: 'IB盈透证券' },
    { value: 'generic', label: '其他', description: '通用CSV格式' },
  ],
  crypto: [
    { value: 'binance', label: 'Binance', description: '币安交易所' },
    { value: 'okx', label: 'OKX', description: 'OKX交易所' },
    { value: 'generic', label: '其他', description: '通用CSV格式' },
  ],
  a_stock: [
    { value: 'tonghuashun', label: '同花顺', description: '同花顺证券' },
    { value: 'gtja', label: '国泰君安', description: '国泰君安证券' },
    { value: 'guosen', label: '国信证券', description: '国信证券' },
    { value: 'generic', label: '其他', description: '通用CSV格式' },
  ],
  hk_stock: [
    { value: 'futu', label: '富途', description: '富途牛牛' },
    { value: 'tiger', label: '老虎', description: '老虎证券' },
    { value: 'generic', label: '其他', description: '通用CSV格式' },
  ],
} as const;
