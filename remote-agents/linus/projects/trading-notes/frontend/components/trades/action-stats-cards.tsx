'use client';

import { Trade, ActionType, ACTION_TYPE_CONFIG } from '@/types/trade';
import { TrendingUp, FileText, BarChart3 } from 'lucide-react';

interface ActionStatsCardsProps {
  trades: Trade[];
}

export function ActionStatsCards({ trades }: ActionStatsCardsProps) {
  // 统计各操作类型的数量
  const actionStats = {
    open: trades.filter(t => t.action_type === 'open').length,
    add: trades.filter(t => t.action_type === 'add').length,
    reduce: trades.filter(t => t.action_type === 'reduce').length,
    close: trades.filter(t => t.action_type === 'close').length,
    unset: trades.filter(t => !t.action_type).length,
  };

  // 统计理由填写情况
  const withReason = trades.filter(t => t.action_reason && t.action_reason.trim() !== '').length;
  const withoutReason = trades.length - withReason;
  const reasonRate = trades.length > 0 ? (withReason / trades.length * 100) : 0;

  // 计算有操作类型标注的比例
  const withActionType = trades.filter(t => t.action_type).length;
  const actionTypeRate = trades.length > 0 ? (withActionType / trades.length * 100) : 0;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
      {/* 操作类型分布卡片 */}
      <div className="bg-white rounded-xl shadow-md border border-gray-100 overflow-hidden">
        <div className="px-6 py-4 bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-gray-200">
          <div className="flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-blue-600" />
            <h3 className="text-lg font-bold text-gray-800">操作类型分布</h3>
          </div>
        </div>
        <div className="p-6">
          <div className="space-y-3">
            {(['open', 'add', 'reduce', 'close'] as ActionType[]).map((type) => {
              const config = ACTION_TYPE_CONFIG[type];
              const count = actionStats[type];
              const percentage = withActionType > 0 ? (count / withActionType * 100) : 0;

              return (
                <div key={type} className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-xl">{config.icon}</span>
                    <span className={`text-sm font-medium ${config.color}`}>
                      {config.label}
                    </span>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="w-24 bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${config.bgColor}`}
                        style={{ width: `${percentage}%` }}
                      />
                    </div>
                    <span className="text-sm font-bold text-gray-900 w-12 text-right">
                      {count}
                    </span>
                  </div>
                </div>
              );
            })}

            {actionStats.unset > 0 && (
              <div className="flex items-center justify-between pt-2 border-t border-gray-200">
                <div className="flex items-center gap-2">
                  <span className="text-xl">❓</span>
                  <span className="text-sm font-medium text-gray-500">未标注</span>
                </div>
                <span className="text-sm font-bold text-gray-600">
                  {actionStats.unset}
                </span>
              </div>
            )}
          </div>

          <div className="mt-4 pt-4 border-t border-gray-200">
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">标注率</span>
              <span className={`font-bold ${
                actionTypeRate >= 80 ? 'text-green-600' :
                actionTypeRate >= 50 ? 'text-yellow-600' : 'text-red-600'
              }`}>
                {actionTypeRate.toFixed(1)}%
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* 理由填写率卡片 */}
      <div className="bg-white rounded-xl shadow-md border border-gray-100 overflow-hidden">
        <div className="px-6 py-4 bg-gradient-to-r from-green-50 to-emerald-50 border-b border-gray-200">
          <div className="flex items-center gap-2">
            <FileText className="w-5 h-5 text-green-600" />
            <h3 className="text-lg font-bold text-gray-800">理由填写情况</h3>
          </div>
        </div>
        <div className="p-6">
          {/* 圆形进度 */}
          <div className="flex items-center justify-center mb-6">
            <div className="relative w-32 h-32">
              <svg className="w-full h-full transform -rotate-90">
                <circle
                  cx="64"
                  cy="64"
                  r="56"
                  stroke="currentColor"
                  strokeWidth="8"
                  fill="none"
                  className="text-gray-200"
                />
                <circle
                  cx="64"
                  cy="64"
                  r="56"
                  stroke="currentColor"
                  strokeWidth="8"
                  fill="none"
                  strokeDasharray={`${2 * Math.PI * 56}`}
                  strokeDashoffset={`${2 * Math.PI * 56 * (1 - reasonRate / 100)}`}
                  className={
                    reasonRate >= 80 ? 'text-green-500' :
                    reasonRate >= 50 ? 'text-yellow-500' : 'text-red-500'
                  }
                  strokeLinecap="round"
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className={`text-2xl font-bold ${
                  reasonRate >= 80 ? 'text-green-600' :
                  reasonRate >= 50 ? 'text-yellow-600' : 'text-red-600'
                }`}>
                  {reasonRate.toFixed(0)}%
                </span>
              </div>
            </div>
          </div>

          {/* 详细统计 */}
          <div className="space-y-2">
            <div className="flex items-center justify-between p-2 bg-green-50 rounded-lg">
              <span className="text-sm text-gray-700">已填写理由</span>
              <span className="text-sm font-bold text-green-700">{withReason}</span>
            </div>
            <div className="flex items-center justify-between p-2 bg-gray-50 rounded-lg">
              <span className="text-sm text-gray-700">未填写理由</span>
              <span className="text-sm font-bold text-gray-700">{withoutReason}</span>
            </div>
          </div>

          {reasonRate < 50 && (
            <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
              <p className="text-xs text-yellow-800">
                💡 建议为更多交易添加理由,有助于复盘分析
              </p>
            </div>
          )}
        </div>
      </div>

      {/* 交易模式分析卡片 */}
      <div className="bg-white rounded-xl shadow-md border border-gray-100 overflow-hidden">
        <div className="px-6 py-4 bg-gradient-to-r from-purple-50 to-pink-50 border-b border-gray-200">
          <div className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-purple-600" />
            <h3 className="text-lg font-bold text-gray-800">交易模式</h3>
          </div>
        </div>
        <div className="p-6">
          <div className="space-y-4">
            {/* 建仓 vs 清仓比例 */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">建仓/清仓比</span>
                <span className="text-sm font-bold text-gray-900">
                  {actionStats.open} : {actionStats.close}
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-gradient-to-r from-green-500 to-red-500 h-2 rounded-full"
                  style={{
                    width: actionStats.open + actionStats.close > 0
                      ? `${(actionStats.open / (actionStats.open + actionStats.close)) * 100}%`
                      : '50%'
                  }}
                />
              </div>
            </div>

            {/* 加仓频率 */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">加仓次数</span>
                <span className="text-sm font-bold text-blue-600">{actionStats.add}</span>
              </div>
              <p className="text-xs text-gray-500">
                {actionStats.add > actionStats.open * 2
                  ? '⚠️ 加仓频繁,注意风险控制'
                  : actionStats.add > 0
                  ? '✓ 合理的加仓策略'
                  : '- 未使用加仓策略'}
              </p>
            </div>

            {/* 减仓频率 */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">减仓次数</span>
                <span className="text-sm font-bold text-orange-600">{actionStats.reduce}</span>
              </div>
              <p className="text-xs text-gray-500">
                {actionStats.reduce > actionStats.close
                  ? '✓ 善于分批止盈'
                  : actionStats.reduce > 0
                  ? '- 部分使用分批策略'
                  : '- 未使用分批止盈'}
              </p>
            </div>

            {/* 平均操作数 */}
            <div className="pt-3 border-t border-gray-200">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700">单标的平均操作数</span>
                <span className="text-sm font-bold text-purple-600">
                  {trades.length > 0
                    ? ((actionStats.open + actionStats.add + actionStats.reduce + actionStats.close) /
                        new Set(trades.map(t => t.symbol)).size).toFixed(1)
                    : '0'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
