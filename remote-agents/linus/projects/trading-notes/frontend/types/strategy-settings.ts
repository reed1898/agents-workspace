import type { ActionType } from '@/types/trade';
import type { AccountType } from '@/lib/types/account';

export type MarketStrategyConfig = Record<ActionType, string[]>;

export interface CurrencySettings {
  usd_cny_rate: number;
}

export interface StrategySettings {
  market_strategies: Record<AccountType, MarketStrategyConfig>;
  currency_settings: CurrencySettings;
}
