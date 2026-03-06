'use client';

import { useEffect, useState } from 'react';
import { useParams, useSearchParams } from 'next/navigation';
import { ArrowLeft, TrendingUp, Activity, Clock, ExternalLink } from 'lucide-react';
import { apiClient } from '@/lib/api-client';
import { Position } from '@/types/position';
import { Trade, TradeReviewData } from '@/types/trade';
import type { StrategySettings } from '@/types/strategy-settings';
import PageNav from '@/components/layout/PageNav';
import { Button } from '@/components/ui/button';
import { accountsApi } from '@/lib/api/accounts';
import type { AccountType } from '@/lib/types/account';
import { TradingTimeline } from '@/components/trades/trading-timeline';
import { ReviewTradeDialog } from '@/components/trades/review-trade-dialog';
import { ActionTypeBadge } from '@/components/trades/action-type-badge';
import { formatMoney, formatPrice, formatQuantity } from '@/lib/format/number';
import { usePageTitle } from '@/lib/use-page-title';

export default function SymbolDetailPage() {
  const params = useParams();
  const searchParams = useSearchParams();
  const symbol = params.symbol as string;
  const decodedSymbol = decodeURIComponent(symbol);
  const accountId = searchParams.get('account_id');

  const [position, setPosition] = useState<Position | null>(null);
  const [trades, setTrades] = useState<Trade[]>([]);
  const [accountName, setAccountName] = useState<string>('');
  const [accountType, setAccountType] = useState<AccountType>('crypto');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'timeline' | 'table'>('timeline');
  const [editingTrade, setEditingTrade] = useState<Trade | null>(null);
  const [strategySettings, setStrategySettings] = useState<StrategySettings | null>(null);

  useEffect(() => {
    if (symbol && accountId) {
      loadData();
      loadStrategySettings();
    }
  }, [symbol, accountId]);

  const symbolName = position?.symbol_name || trades.find((t) => t.symbol_name)?.symbol_name;
  const titleSymbol = symbolName ? `${symbolName} (${decodedSymbol})` : decodedSymbol;
  const pageTitle = accountName ? `${titleSymbol} - ${accountName}` : titleSymbol;

  usePageTitle(pageTitle);

  const loadStrategySettings = async () => {
    try {
      const settings = await apiClient.getStrategySettings();
      setStrategySettings(settings);
    } catch (err) {
      console.error('Failed to load strategy settings:', err);
    }
  };

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);

      // 获取账户信息
      const account = await accountsApi.getAccount(accountId!);
      setAccountName(account.account_name);
      setAccountType(account.account_type);

      // 获取持仓详情
      try {
        const positionData = await apiClient.getPositionBySymbol(
          decodedSymbol,
          accountId!
        );
        setPosition(positionData);
      } catch (err: any) {
        if (err.response?.status !== 404) {
          throw err;
        }
        // 如果没有持仓，继续加载交易记录
        setPosition(null);
      }

      // 获取该标的的历史交易记录
      const tradesResponse = await apiClient.getTrades({
        account_id: accountId!,
        symbol: decodedSymbol,
        page_size: 100,
      });
      setTrades(tradesResponse.trades);
    } catch (err: any) {
      setError(err.response?.data?.detail || '加载数据失败');
    } finally {
      setLoading(false);
    }
  };

  const handleSaveTradeReview = async (tradeId: string, reviewData: TradeReviewData) => {
    try {
      const updated = await apiClient.reviewTrade(tradeId, reviewData);
      setTrades((prev) => prev.map((t) => (t.id === tradeId ? updated : t)));
      setEditingTrade(null);
    } catch (err: any) {
      throw new Error(err.response?.data?.detail || '更新失败');
    }
  };

  const getCurrencySymbol = (type: AccountType) => {
    const currencyMap: Record<AccountType, string> = {
      'us_stock': '$',
      'crypto': '$',
      'a_stock': '¥',
      'hk_stock': 'HK$'
    };
    return currencyMap[type] || '$';
  };

  const formatCurrency = (value: string | number | undefined, decimals = 2) => {
    return formatMoney(value ?? 0, { accountType, fallbackFractionDigits: decimals });
  };

  const formatPercent = (value: string | number | undefined) => {
    if (value === undefined || value === null) return '0.00%';
    const num = parseFloat(value.toString());
    const color = num >= 0 ? 'text-green-600' : 'text-red-600';
    const sign = num >= 0 ? '+' : '';
    return <span className={color}>{sign}{num.toFixed(2)}%</span>;
  };

  const formatPnL = (value: string | number | undefined) => {
    if (value === undefined || value === null) return `${getCurrencySymbol(accountType)}0.00`;
    const num = parseFloat(value.toString());
    const color = num >= 0 ? 'text-green-600' : 'text-red-600';
    const sign = num >= 0 ? '+' : '-';
    return <span className={color}>{sign}{formatMoney(Math.abs(num), { accountType, fallbackFractionDigits: 2 })}</span>;
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getTradingViewUrl = (rawSymbol: string, type: AccountType) => {
    const symbol = rawSymbol.trim();
    if (!symbol) return 'https://www.tradingview.com/';
    if (symbol.includes(':')) {
      return `https://www.tradingview.com/chart/?symbol=${encodeURIComponent(symbol)}`;
    }

    if (type === 'crypto') {
      return `https://www.tradingview.com/chart/?symbol=${encodeURIComponent(`BINANCE:${symbol}`)}`;
    }

    if (type === 'hk_stock') {
      const digits = symbol.replace(/\D/g, '');
      const hkSymbol = digits ? digits.padStart(5, '0') : symbol;
      return `https://www.tradingview.com/chart/?symbol=${encodeURIComponent(`HKEX:${hkSymbol}`)}`;
    }

    if (type === 'a_stock') {
      const digits = symbol.replace(/\D/g, '');
      const exchange = digits.startsWith('6') ? 'SSE' : 'SZSE';
      return `https://www.tradingview.com/chart/?symbol=${encodeURIComponent(`${exchange}:${digits || symbol}`)}`;
    }

    // us_stock and fallback: let TradingView resolve by symbol
    return `https://www.tradingview.com/chart/?symbol=${encodeURIComponent(symbol)}`;
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center h-64">
          <div className="text-gray-500">加载中...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-50 border-l-4 border-red-500 rounded-lg p-4">
          <p className="text-red-800 font-medium">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <>
      <PageNav />
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50">
        <div className="container mx-auto px-4 py-8">
          {/* 返回按钮 */}
          <div className="mb-6">
            <Button
              variant="outline"
              onClick={() => window.history.back()}
              className="flex items-center space-x-2"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>返回</span>
            </Button>
          </div>

          {/* 页面标题 */}
          <div className="mb-8">
            <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
              <div className="flex items-center space-x-3">
                <div className="p-3 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl shadow-lg">
                  <TrendingUp className="w-8 h-8 text-white" />
                </div>
                <div>
                  <h1 className="text-4xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
                    {symbolName || decodedSymbol}
                  </h1>
                  <div className="mt-1 flex flex-wrap items-center gap-x-3 gap-y-1 text-gray-600">
                    {symbolName && <span className="font-mono text-sm">{decodedSymbol}</span>}
                    <span>{accountName}</span>
                  </div>
                </div>
              </div>

              <Button asChild variant="outline" className="self-start">
                <a
                  href={getTradingViewUrl(decodedSymbol, accountType)}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <ExternalLink className="w-4 h-4" />
                  TradingView
                </a>
              </Button>
            </div>
          </div>

          {/* 持仓信息卡片 */}
          {position && (
            <div className="mb-8 bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
              <div className="px-6 py-5 bg-gradient-to-r from-gray-50 to-gray-100 border-b border-gray-200">
                <h2 className="text-xl font-bold text-gray-800 flex items-center">
                  <div className="w-1 h-6 bg-gradient-to-b from-blue-500 to-indigo-600 rounded-full mr-3"></div>
                  当前持仓
                </h2>
              </div>
              <div className="p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {/* 数量 */}
                  <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-4">
                    <div className="text-sm text-gray-600 mb-1">持仓数量</div>
                    <div className="text-2xl font-bold text-gray-900">
                      {formatQuantity(Math.abs(parseFloat(position.quantity)), { accountType, fallbackFractionDigits: 8 })}
                    </div>
                    {position.position_type === 'futures' && (
                      <div className={`text-xs mt-1 font-medium ${
                        position.position_side === 'LONG' ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {position.position_side === 'LONG' ? '多头' : '空头'}
                      </div>
                    )}
                  </div>

                  {/* 成本价/开仓价 */}
                  <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-4">
                    <div className="text-sm text-gray-600 mb-1">
                      {position.position_type === 'futures' ? '开仓价' : '成本价'}
                    </div>
                    <div className="text-2xl font-bold text-gray-900">
                      {position.position_type === 'futures'
                        ? formatPrice(position.entry_price || '0', { accountType, fallbackFractionDigits: 8 })
                        : formatPrice(position.average_cost || '0', { accountType, fallbackFractionDigits: 8 })
                      }
                    </div>
                  </div>

                  {/* 当前价格 */}
                  <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl p-4">
                    <div className="text-sm text-gray-600 mb-1">当前价格</div>
                    <div className="text-2xl font-bold text-gray-900">
                      {position.current_price
                        ? formatPrice(position.current_price, { accountType, fallbackFractionDigits: 8 })
                        : '-'
                      }
                    </div>
                  </div>

                  {/* 未实现盈亏 */}
                  <div className={`rounded-xl p-4 ${
                    position.unrealized_pnl && parseFloat(position.unrealized_pnl.toString()) >= 0
                      ? 'bg-gradient-to-br from-green-50 to-emerald-50'
                      : 'bg-gradient-to-br from-red-50 to-rose-50'
                  }`}>
                    <div className="text-sm text-gray-600 mb-1">未实现盈亏</div>
                    <div className="text-2xl font-bold">
                      {formatPnL(position.unrealized_pnl)}
                    </div>
                    <div className="text-sm mt-1">
                      {position.position_type === 'futures' && position.roe_percent
                        ? formatPercent(position.roe_percent)
                        : formatPercent(position.unrealized_pnl_percent)
                      }
                    </div>
                  </div>
                </div>

                {/* 额外信息 */}
                <div className="mt-6 pt-6 border-t border-gray-200 grid grid-cols-1 md:grid-cols-3 gap-4">
                  {position.position_type === 'futures' && (
                    <>
                      <div className="flex items-center space-x-2">
                        <Activity className="w-5 h-5 text-gray-500" />
                        <div>
                          <div className="text-xs text-gray-600">杠杆倍数</div>
                          <div className="text-sm font-medium text-gray-900">{position.leverage || '1'}x</div>
                        </div>
                      </div>
                      {position.margin_used && (
                        <div className="flex items-center space-x-2">
                          <Activity className="w-5 h-5 text-gray-500" />
                          <div>
                            <div className="text-xs text-gray-600">占用保证金</div>
                            <div className="text-sm font-medium text-gray-900">
                              {formatCurrency(position.margin_used, 2)}
                            </div>
                          </div>
                        </div>
                      )}
                      {position.liquidation_price && (
                        <div className="flex items-center space-x-2">
                          <Activity className="w-5 h-5 text-red-500" />
                          <div>
                            <div className="text-xs text-gray-600">强平价</div>
                            <div className="text-sm font-medium text-red-600">
                              {formatPrice(position.liquidation_price, { accountType, fallbackFractionDigits: 8 })}
                            </div>
                          </div>
                        </div>
                      )}
                    </>
                  )}
                  {position.holding_days !== null && position.holding_days !== undefined && (
                    <div className="flex items-center space-x-2">
                      <Clock className="w-5 h-5 text-gray-500" />
                      <div>
                        <div className="text-xs text-gray-600">持仓天数</div>
                        <div className="text-sm font-medium text-gray-900">{position.holding_days} 天</div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* 历史交易记录 */}
          <div className="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
            <div className="px-6 py-5 bg-gradient-to-r from-gray-50 to-gray-100 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-bold text-gray-800 flex items-center">
                  <div className="w-1 h-6 bg-gradient-to-b from-blue-500 to-indigo-600 rounded-full mr-3"></div>
                  操作历史 ({trades.length})
                </h2>

                {/* 视图切换按钮 */}
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setViewMode('timeline')}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                      viewMode === 'timeline'
                        ? 'bg-blue-600 text-white shadow-md'
                        : 'bg-white text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    时间线
                  </button>
                  <button
                    onClick={() => setViewMode('table')}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                      viewMode === 'table'
                        ? 'bg-blue-600 text-white shadow-md'
                        : 'bg-white text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    表格
                  </button>
                </div>
              </div>
            </div>

            {/* 根据视图模式显示不同内容 */}
            {viewMode === 'timeline' ? (
              <div className="p-6">
                <TradingTimeline
                  trades={trades}
                  currencySymbol={getCurrencySymbol(accountType)}
                  onReviewTrade={(trade) => setEditingTrade(trade)}
                />
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gradient-to-r from-gray-100 to-gray-50">
                    <tr>
                      <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">
                        交易时间
                      </th>
                      <th className="px-6 py-4 text-center text-xs font-bold text-gray-700 uppercase tracking-wider">
                        方向
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">
                        数量
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">
                        价格
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">
                        手续费
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">
                        交易金额
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">
                        复盘
                      </th>
                      <th className="px-6 py-4 text-center text-xs font-bold text-gray-700 uppercase tracking-wider">
                        来源
                      </th>
                      <th className="px-6 py-4 text-center text-xs font-bold text-gray-700 uppercase tracking-wider">
                        操作
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-100">
                    {trades.length === 0 ? (
                      <tr>
                        <td colSpan={9} className="px-6 py-16 text-center">
                          <div className="flex flex-col items-center">
                            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                              <Activity className="w-8 h-8 text-gray-400" />
                            </div>
                            <p className="text-gray-500 font-medium">暂无交易记录</p>
                          </div>
                        </td>
                      </tr>
                    ) : (
                      trades.map((trade) => (
                        <tr
                          key={trade.id}
                          className="hover:bg-gradient-to-r hover:from-blue-50 hover:to-indigo-50 transition-all duration-200"
                        >
                          {/* 交易时间 */}
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                            {formatDate(trade.trade_time)}
                          </td>

                          {/* 方向 */}
                          <td className="px-6 py-4 whitespace-nowrap text-center">
                            <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${
                              trade.side === 'buy'
                                ? 'bg-green-100 text-green-800'
                                : 'bg-red-100 text-red-800'
                            }`}>
                              {trade.side === 'buy' ? '买入' : '卖出'}
                            </span>
                            {trade.position_side && (
                              <div className={`text-xs mt-1 ${
                                trade.position_side === 'LONG' ? 'text-green-600' : 'text-red-600'
                              }`}>
                                {trade.position_side === 'LONG' ? '多' : '空'}
                              </div>
                            )}
                          </td>

                          {/* 数量 */}
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-medium text-gray-700">
                            {formatQuantity(trade.quantity, { accountType, fallbackFractionDigits: 8 })}
                          </td>

                          {/* 价格 */}
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-medium text-gray-700">
                            {formatPrice(trade.price, { accountType, fallbackFractionDigits: 8 })}
                          </td>

                          {/* 手续费 */}
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-600">
                            {formatCurrency(trade.fee, 2)}
                          </td>

                          {/* 交易金额 */}
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-bold text-gray-900">
                            {formatCurrency(parseFloat(trade.price) * parseFloat(trade.quantity), 2)}
                          </td>

                          {/* 复盘 */}
                          <td className="px-6 py-4 text-sm text-gray-700">
                            <div className="flex items-center gap-2">
                              <ActionTypeBadge type={trade.action_type} />
                              <span
                                className={`px-2 py-1 rounded text-xs font-bold ${
                                  trade.reviewed
                                    ? 'bg-emerald-600 text-white'
                                    : trade.action_reason || trade.emotion_state || trade.exit_strategy
                                      ? 'bg-blue-600 text-white'
                                      : 'bg-gray-200 text-gray-700'
                                }`}
                                title={trade.reviewed_at ? `复盘时间: ${formatDate(trade.reviewed_at)}` : undefined}
                              >
                                {trade.reviewed ? '已复盘' : (trade.action_reason || trade.emotion_state || trade.exit_strategy) ? '已补充' : '待复盘'}
                              </span>
                            </div>
                            {(trade.action_strategy || trade.exit_strategy) && (
                              <div className="mt-1 text-xs text-gray-500 space-y-0.5">
                                {trade.action_strategy && <div className="truncate">策略: {trade.action_strategy}</div>}
                                {trade.exit_strategy && <div className="truncate">出场: {trade.exit_strategy}</div>}
                              </div>
                            )}
                            {trade.action_reason && (
                              <div className="mt-1 text-xs text-gray-600 truncate" title={trade.action_reason}>
                                理由: {trade.action_reason}
                              </div>
                            )}
                          </td>

                          {/* 来源 */}
                          <td className="px-6 py-4 whitespace-nowrap text-center">
                            <span className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-100 text-gray-700">
                              {trade.sync_source === 'api' ? 'API同步' :
                               trade.sync_source === 'manual' ? '手动' :
                               trade.sync_source === 'import' ? '导入' : trade.sync_source}
                            </span>
                          </td>

                          {/* 操作 */}
                          <td className="px-6 py-4 whitespace-nowrap text-center">
                            <button
                              type="button"
                              onClick={() => setEditingTrade(trade)}
                              className={`transition-colors ${
                                trade.reviewed
                                  ? 'text-emerald-600 hover:text-emerald-800'
                                  : trade.action_reason
                                    ? 'text-blue-600 hover:text-blue-800'
                                    : 'text-gray-500 hover:text-gray-700'
                              }`}
                              title={trade.reviewed ? '查看/编辑复盘' : '添加/编辑复盘'}
                            >
                              <svg className="w-5 h-5 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                              </svg>
                            </button>
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* 复盘对话框 */}
      {editingTrade && (
        <ReviewTradeDialog
          trade={editingTrade}
          isOpen={true}
          onClose={() => setEditingTrade(null)}
          onSave={handleSaveTradeReview}
          marketType={accountType}
          strategySettings={strategySettings}
        />
      )}
    </>
  );
}
