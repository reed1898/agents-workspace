'use client';

import { Trade, ACTION_TYPE_CONFIG } from '@/types/trade';
import { Clock, TrendingUp, TrendingDown } from 'lucide-react';
import type { AccountType } from '@/lib/types/account';
import { formatMoney, formatPrice, formatQuantity } from '@/lib/format/number';

interface TradingTimelineProps {
  trades: Trade[];
  currencySymbol?: string;
  onReviewTrade?: (trade: Trade) => void;
}

export function TradingTimeline({ trades, currencySymbol = '$', onReviewTrade }: TradingTimelineProps) {
  const normalizedCurrencySymbol = currencySymbol.trim().toLowerCase();
  const isAStockTrade = (trade: Trade) =>
    trade.account_type === 'a_stock' || currencySymbol === '¥' || normalizedCurrencySymbol === 'rmb';

  const getTradeAccountType = (trade: Trade): AccountType => {
    if (trade.account_type) return trade.account_type as AccountType;
    return isAStockTrade(trade) ? 'a_stock' : 'us_stock';
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

  const formatTradeQuantity = (trade: Trade) =>
    formatQuantity(trade.quantity, { accountType: getTradeAccountType(trade), fallbackFractionDigits: 8 });

  const formatTradePrice = (trade: Trade) =>
    formatPrice(trade.price, { accountType: getTradeAccountType(trade), fallbackFractionDigits: 8 });

  const formatTradeAmount = (trade: Trade, value: string | number) =>
    formatMoney(value, { accountType: getTradeAccountType(trade), fallbackFractionDigits: 2 });

  const formatTradeFee = (trade: Trade) =>
    formatMoney(trade.fee, { accountType: getTradeAccountType(trade), fallbackFractionDigits: 4 });

  // 按时间正序排列(从旧到新)
  const sortedTrades = [...trades].sort((a, b) =>
    new Date(a.trade_time).getTime() - new Date(b.trade_time).getTime()
  );

  if (sortedTrades.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="inline-block p-4 bg-gray-100 rounded-full mb-4">
          <Clock className="w-8 h-8 text-gray-400" />
        </div>
        <p className="text-gray-500">暂无操作记录</p>
      </div>
    );
  }

  return (
    <div className="relative">
      {/* 时间线主轴 */}
      <div className="absolute left-8 top-0 bottom-0 w-0.5 bg-gradient-to-b from-blue-200 via-purple-200 to-pink-200"></div>

      {/* 时间线项目 */}
      <div className="space-y-6">
        {sortedTrades.map((trade) => {
          const actionConfig = trade.action_type ? ACTION_TYPE_CONFIG[trade.action_type] : null;
          const isBuy = trade.side === 'buy';
          const amount = parseFloat(trade.price) * parseFloat(trade.quantity);
          const hasReviewInfo = Boolean(
            trade.reviewed ||
              trade.action_reason ||
              trade.emotion_state ||
              trade.exit_strategy ||
              trade.planned_stop_loss ||
              trade.planned_take_profit ||
              trade.notes
          );

          return (
            <div key={trade.id} className="relative pl-20">
              {/* 时间线圆点和图标 */}
              <div className="absolute left-0 flex items-center">
                <div className={`w-16 h-16 rounded-full flex items-center justify-center shadow-lg ${
                  actionConfig ? actionConfig.bgColor : (isBuy ? 'bg-green-100' : 'bg-red-100')
                } border-4 border-white`}>
                  {actionConfig ? (
                    <span className="text-2xl">{actionConfig.icon}</span>
                  ) : isBuy ? (
                    <TrendingUp className="w-6 h-6 text-green-700" />
                  ) : (
                    <TrendingDown className="w-6 h-6 text-red-700" />
                  )}
                </div>
              </div>

              {/* 内容卡片 */}
              <div className="bg-white rounded-xl shadow-md hover:shadow-lg transition-all duration-200 overflow-hidden border border-gray-100">
                {/* 头部 */}
                <div className={`px-6 py-4 ${
                  actionConfig ? actionConfig.bgColor : (isBuy ? 'bg-green-50' : 'bg-red-50')
                }`}>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      {/* 操作类型标签 */}
                      {actionConfig && (
                        <span className={`px-3 py-1 rounded-full text-sm font-bold ${actionConfig.color} ${actionConfig.bgColor} border-2 border-current`}>
                          {actionConfig.label}
                        </span>
                      )}

                      {/* 买卖方向 */}
                      <span className={`px-3 py-1 rounded-full text-sm font-bold ${
                        isBuy ? 'bg-green-600 text-white' : 'bg-red-600 text-white'
                      }`}>
                        {isBuy ? '买入' : '卖出'}
                      </span>

                      {/* 合约类型 */}
                      {trade.position_side && (
                        <span className={`px-2 py-1 rounded text-xs font-medium ${
                          trade.position_side === 'LONG'
                            ? 'bg-green-600 text-white'
                            : 'bg-red-600 text-white'
                        }`}>
                          {trade.position_side === 'LONG' ? '多头' : '空头'}
                          {trade.leverage && ` ${trade.leverage}x`}
                        </span>
                      )}

                      {/* 复盘状态 */}
                      <span
                        className={`px-2 py-1 rounded text-xs font-bold ${
                          trade.reviewed
                            ? 'bg-emerald-600 text-white'
                            : hasReviewInfo
                              ? 'bg-blue-600 text-white'
                              : 'bg-gray-200 text-gray-700'
                        }`}
                      >
                        {trade.reviewed ? '已复盘' : hasReviewInfo ? '已补充' : '待复盘'}
                      </span>
                    </div>

                    {/* 时间 */}
                    <div className="flex items-center gap-3">
                      <div className="flex items-center gap-2 text-sm text-gray-600">
                        <Clock className="w-4 h-4" />
                        {formatDate(trade.trade_time)}
                      </div>
                      {onReviewTrade && (
                        <button
                          type="button"
                          onClick={() => onReviewTrade(trade)}
                          className={`px-3 py-1.5 rounded-md text-xs font-bold transition-colors ${
                            trade.reviewed
                              ? 'bg-emerald-700 text-white hover:bg-emerald-800'
                              : hasReviewInfo
                                ? 'bg-blue-700 text-white hover:bg-blue-800'
                                : 'bg-gray-700 text-white hover:bg-gray-800'
                          }`}
                          title={trade.reviewed ? '查看/编辑复盘' : '添加/编辑复盘'}
                        >
                          复盘
                        </button>
                      )}
                    </div>
                  </div>
                </div>

                {/* 交易详情 */}
                <div className="px-6 py-4">
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                    <div>
                      <div className="text-xs text-gray-500 mb-1">数量</div>
                      <div className="text-lg font-bold text-gray-900">
                        {formatTradeQuantity(trade)}
                      </div>
                    </div>
                    <div>
                      <div className="text-xs text-gray-500 mb-1">价格</div>
                      <div className="text-lg font-bold text-gray-900">
                        {formatTradePrice(trade)}
                      </div>
                    </div>
                    <div>
                      <div className="text-xs text-gray-500 mb-1">交易额</div>
                      <div className="text-lg font-bold text-gray-900">
                        {formatTradeAmount(trade, amount)}
                      </div>
                    </div>
                    <div>
                      <div className="text-xs text-gray-500 mb-1">手续费</div>
                      <div className="text-sm font-medium text-gray-700">
                        {formatTradeFee(trade)}
                      </div>
                    </div>
                  </div>

                  {/* 复盘摘要 */}
                  {(trade.emotion_state || trade.exit_strategy || trade.planned_stop_loss || trade.planned_take_profit || trade.action_strategy) && (
                    <div className="mt-4 pt-4 border-t border-gray-100">
                      <div className="flex flex-wrap gap-2 text-xs">
                        {trade.action_strategy && (
                          <span className="px-2 py-1 rounded bg-indigo-50 text-indigo-700 border border-indigo-100">
                            策略: {trade.action_strategy}
                          </span>
                        )}
                        {trade.emotion_state && (
                          <span className="px-2 py-1 rounded bg-amber-50 text-amber-800 border border-amber-100">
                            情绪: {trade.emotion_state}{trade.emotion_intensity ? `(${trade.emotion_intensity})` : ''}
                          </span>
                        )}
                        {trade.exit_strategy && (
                          <span className="px-2 py-1 rounded bg-rose-50 text-rose-700 border border-rose-100">
                            出场: {trade.exit_strategy}
                          </span>
                        )}
                        {trade.planned_stop_loss && (
                          <span className="px-2 py-1 rounded bg-gray-50 text-gray-700 border border-gray-100">
                            止损: {formatTradeMoney(trade, trade.planned_stop_loss, 2)}
                          </span>
                        )}
                        {trade.planned_take_profit && (
                          <span className="px-2 py-1 rounded bg-gray-50 text-gray-700 border border-gray-100">
                            止盈: {formatTradeMoney(trade, trade.planned_take_profit, 2)}
                          </span>
                        )}
                      </div>
                    </div>
                  )}

                  {/* 交易理由 */}
                  {trade.action_reason && (
                    <div className="mt-4 pt-4 border-t border-gray-100">
                      <div className="flex items-start gap-2">
                        <div className="flex-shrink-0 mt-1">
                          <svg className="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                          </svg>
                        </div>
                        <div className="flex-grow">
                          <div className="text-sm font-semibold text-gray-700 mb-1">交易理由</div>
                          <div className="text-sm text-gray-600 whitespace-pre-wrap bg-gray-50 rounded-lg p-3">
                            {trade.action_reason}
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* K线图 */}
                  {trade.chart_image_url && (
                    <div className="mt-4 pt-4 border-t border-gray-100">
                      <div className="text-sm font-semibold text-gray-700 mb-2">K线图</div>
                      <div className="rounded-lg overflow-hidden border border-gray-200">
                        <img
                          src={trade.chart_image_url}
                          alt="K线图"
                          className="w-full h-auto cursor-pointer hover:opacity-90 transition-opacity"
                          onClick={() => window.open(trade.chart_image_url, '_blank')}
                        />
                      </div>
                    </div>
                  )}

                  {/* 其他信息 */}
                  <div className="mt-4 pt-4 border-t border-gray-100 flex items-center gap-4 text-xs text-gray-500">
                    <span>来源: {
                      trade.sync_source === 'api' ? 'API同步' :
                      trade.sync_source === 'manual' ? '手动录入' :
                      trade.sync_source === 'import' ? 'CSV导入' : trade.sync_source
                    }</span>
                    {trade.trade_id_external && (
                      <span className="truncate">ID: {trade.trade_id_external}</span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
