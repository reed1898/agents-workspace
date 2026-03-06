'use client';

import { useState, useEffect } from 'react';
import { KlineChart } from './KlineChart';
import { KlineData, Timeframe, TIMEFRAME_OPTIONS, TradeMarker } from '@/types/kline';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { apiClient } from '@/lib/api-client';
import { Trade } from '@/types/trade';
import { formatQuantity } from '@/lib/format/number';

interface KlineChartWithControlsProps {
  symbol: string;
  exchange?: string;
  trades?: Trade[];
  height?: number;
}

export function KlineChartWithControls({
  symbol,
  exchange = 'binance',
  trades = [],
  height = 400
}: KlineChartWithControlsProps) {
  const [timeframe, setTimeframe] = useState<Timeframe>('1h');
  const [klineData, setKlineData] = useState<KlineData[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // 加载K线数据
  const fetchKlineData = async () => {
    setLoading(true);
    setError(null);

    try {
      // 处理符号格式
      const formattedSymbol = symbol.includes('/') ? symbol : `${symbol}/USDT`;

      const response = await apiClient.get('/market/klines', {
        params: {
          symbol: formattedSymbol,
          timeframe,
          exchange,
          limit: 500,
        },
      });

      setKlineData(response.data.data);
    } catch (err: any) {
      console.error('Failed to fetch kline data:', err);
      setError(err.response?.data?.detail || '加载K线数据失败');
    } finally {
      setLoading(false);
    }
  };

  // 初始加载和时间框架变化时重新加载
  useEffect(() => {
    fetchKlineData();
  }, [symbol, timeframe, exchange]);

  // 生成交易标记
  const markers: TradeMarker[] = trades.map((trade) => {
    const isBuy = trade.side === 'buy';
    const tradeTimestamp = new Date(trade.trade_time).getTime() / 1000;

    return {
      time: tradeTimestamp,
      position: isBuy ? 'belowBar' : 'aboveBar',
      color: isBuy ? '#26a69a' : '#ef5350',
      shape: isBuy ? 'arrowUp' : 'arrowDown',
      text: `${isBuy ? '买' : '卖'} ${formatQuantity(trade.quantity, { accountType: trade.account_type, fallbackFractionDigits: 8 })}`,
    };
  });

  return (
    <div className="space-y-4">
      {/* 控制栏 */}
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium text-gray-700">时间框架:</span>
          <Select value={timeframe} onValueChange={(value) => setTimeframe(value as Timeframe)}>
            <SelectTrigger className="w-32">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {TIMEFRAME_OPTIONS.map((option) => (
                <SelectItem key={option.value} value={option.value}>
                  {option.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <Button
          variant="outline"
          size="sm"
          onClick={fetchKlineData}
          disabled={loading}
        >
          {loading ? '加载中...' : '刷新'}
        </Button>
      </div>

      {/* 错误提示 */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          <p className="text-sm">{error}</p>
        </div>
      )}

      {/* K线图 */}
      <KlineChart
        data={klineData}
        symbol={symbol}
        markers={markers}
        height={height}
        loading={loading}
      />

      {/* 图例说明 */}
      {trades.length > 0 && (
        <div className="flex items-center gap-4 text-xs text-gray-600">
          <div className="flex items-center gap-1">
            <span className="inline-block w-3 h-3 bg-green-500 rounded"></span>
            <span>买入</span>
          </div>
          <div className="flex items-center gap-1">
            <span className="inline-block w-3 h-3 bg-red-500 rounded"></span>
            <span>卖出</span>
          </div>
        </div>
      )}
    </div>
  );
}
