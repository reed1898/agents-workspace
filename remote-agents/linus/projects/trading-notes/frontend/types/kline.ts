/**
 * K线数据类型定义
 */

export interface KlineData {
  time: number; // Unix timestamp in seconds
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export type Timeframe = '1m' | '5m' | '15m' | '1h' | '4h' | '1d' | '1w';

export interface KlineResponse {
  symbol: string;
  timeframe: Timeframe;
  exchange: string;
  data: KlineData[];
  count: number;
}

export interface KlineForTradeResponse {
  klines: KlineData[];
  trade_index: number | null;
  trade_timestamp: number;
  symbol: string;
  timeframe: Timeframe;
}

export interface TradeMarker {
  time: number;
  position: 'aboveBar' | 'belowBar';
  color: string;
  shape: 'circle' | 'square' | 'arrowUp' | 'arrowDown';
  text: string;
}

export const TIMEFRAME_OPTIONS: { value: Timeframe; label: string }[] = [
  { value: '1m', label: '1分钟' },
  { value: '5m', label: '5分钟' },
  { value: '15m', label: '15分钟' },
  { value: '1h', label: '1小时' },
  { value: '4h', label: '4小时' },
  { value: '1d', label: '1天' },
  { value: '1w', label: '1周' },
];
