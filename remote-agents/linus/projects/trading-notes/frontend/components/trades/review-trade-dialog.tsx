'use client';

import { useState } from 'react';
import { Trade, TradeReviewData, EmotionState, ExitStrategy, ActionType, EMOTION_CONFIG, EXIT_STRATEGY_CONFIG, ACTION_TYPE_CONFIG } from '@/types/trade';
import type { AccountType } from '@/lib/types/account';
import type { StrategySettings } from '@/types/strategy-settings';
import { Button } from '@/components/ui/button';
import { formatPrice, formatQuantity } from '@/lib/format/number';

interface ReviewTradeDialogProps {
  trade: Trade;
  isOpen: boolean;
  onClose: () => void;
  onSave: (tradeId: string, reviewData: TradeReviewData) => Promise<void>;
  marketType?: AccountType;
  strategySettings?: StrategySettings | null;
}

export function ReviewTradeDialog({ trade, isOpen, onClose, onSave, marketType, strategySettings }: ReviewTradeDialogProps) {
  // 交易理由字段
  const [actionType, setActionType] = useState<ActionType | ''>(trade.action_type || '');
  const [actionReason, setActionReason] = useState(trade.action_reason || '');
  const [actionStrategy, setActionStrategy] = useState(trade.action_strategy || '');

  // 复盘字段
  const [emotionState, setEmotionState] = useState<EmotionState | ''>(trade.emotion_state || '');
  const [emotionIntensity, setEmotionIntensity] = useState<number>(trade.emotion_intensity || 5);
  const [plannedStopLoss, setPlannedStopLoss] = useState(trade.planned_stop_loss || '');
  const [plannedTakeProfit, setPlannedTakeProfit] = useState(trade.planned_take_profit || '');
  const [stopLossExecuted, setStopLossExecuted] = useState<boolean | undefined>(trade.stop_loss_executed);
  const [exitStrategy, setExitStrategy] = useState<ExitStrategy | ''>(trade.exit_strategy || '');
  const [notes, setNotes] = useState(trade.notes || '');

  // 判断是入场还是出场操作
  const isEntry = actionType === '' || actionType === 'open' || actionType === 'add';
  const isExit = actionType === 'reduce' || actionType === 'close';
  const strategyOptions = actionType && marketType
    ? strategySettings?.market_strategies?.[marketType]?.[actionType as ActionType] || []
    : [];

  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleSave = async () => {
    try {
      setSaving(true);
      setError(null);

      const reviewData: TradeReviewData = {
        action_type: actionType === '' ? undefined : actionType as ActionType,
        action_reason: actionReason || undefined,
        action_strategy: actionStrategy || undefined,
        emotion_state: emotionState === '' ? undefined : emotionState as EmotionState,
        emotion_intensity: emotionIntensity,
        planned_stop_loss: plannedStopLoss || undefined,
        planned_take_profit: plannedTakeProfit || undefined,
        stop_loss_executed: stopLossExecuted,
        exit_strategy: exitStrategy === '' ? undefined : exitStrategy as ExitStrategy,
        notes: notes || undefined
      };

      await onSave(trade.id, reviewData);
      onClose();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : '保存失败');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        {/* 标题栏 */}
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold text-gray-900">交易记录与复盘</h2>
              <p className="text-sm text-gray-500 mt-1">
                {trade.symbol} · {trade.side === 'buy' ? '买入' : '卖出'}{' '}
                {formatQuantity(trade.quantity, { accountType: marketType ?? trade.account_type })}{' '}
                @ {formatPrice(trade.price, { accountType: marketType ?? trade.account_type })}
              </p>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        {/* 表单内容 */}
        <div className="px-6 py-4 space-y-6">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
              {error}
            </div>
          )}

          {/* 第一部分: 交易理由 */}
          <div className="space-y-4 pb-6 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">交易理由</h3>

            {/* 操作类型 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                操作类型
              </label>
              <div className="grid grid-cols-3 gap-2">
                <button
                  type="button"
                  onClick={() => setActionType('')}
                  className={`px-3 py-2 rounded-md border text-sm transition-all ${
                    actionType === ''
                      ? 'border-blue-500 bg-blue-50 text-blue-700 font-medium'
                      : 'border-gray-200 text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  未设置
                </button>
                {(['open', 'add', 'reduce', 'close'] as ActionType[]).map((type) => {
                  const config = ACTION_TYPE_CONFIG[type];
                  return (
                    <button
                      key={type}
                      type="button"
                      onClick={() => setActionType(type)}
                      className={`px-3 py-2 rounded-md border text-sm transition-all ${
                        actionType === type
                          ? 'border-blue-500 bg-blue-50 text-blue-700 font-medium'
                          : 'border-gray-200 text-gray-600 hover:bg-gray-50'
                      }`}
                    >
                      <span className="mr-1">{config.icon}</span>
                      {config.label}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* 操作策略 */}
            {actionType && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  操作策略
                </label>
                {strategyOptions.length > 0 ? (
                  <div className="grid grid-cols-2 gap-2 mb-2">
                    {strategyOptions.map((option) => (
                      <button
                        key={option}
                        type="button"
                        onClick={() => setActionStrategy(option)}
                        className={`px-4 py-2 rounded-md border text-sm transition-all ${
                          actionStrategy === option
                            ? 'border-blue-500 bg-blue-50 text-blue-700 font-medium'
                            : 'border-gray-200 text-gray-600 hover:bg-gray-50'
                        }`}
                      >
                        {option}
                      </button>
                    ))}
                  </div>
                ) : (
                  <p className="text-xs text-gray-500 mb-2">
                    该市场还没有配置策略，可先在设置中添加或手动输入。
                  </p>
                )}
                <input
                  type="text"
                  value={actionStrategy}
                  onChange={(e) => setActionStrategy(e.target.value)}
                  placeholder="手动输入策略名称"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            )}

            {/* 交易理由 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                交易理由
                <span className="text-gray-400 font-normal ml-1 text-xs">(建议包括入场信号、技术分析、基本面等)</span>
              </label>
              <textarea
                value={actionReason}
                onChange={(e) => setActionReason(e.target.value)}
                rows={4}
                placeholder="例如：突破前高阻力位，MACD金叉，成交量放大，市场情绪转好..."
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              />
              <div className="mt-1 text-xs text-gray-500">
                {actionReason.length} 字符
              </div>
            </div>
          </div>

          {/* 第二部分: 纪律复盘 */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900">纪律复盘</h3>

          {/* 情绪状态 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              情绪状态
            </label>
            <div className="grid grid-cols-4 gap-2">
              {Object.entries(EMOTION_CONFIG).map(([key, config]) => (
                <button
                  key={key}
                  type="button"
                  onClick={() => setEmotionState(key as EmotionState)}
                  className={`px-3 py-2 rounded-md border text-sm transition-all ${
                    emotionState === key
                      ? `${config.bgColor} ${config.color} border-current`
                      : 'border-gray-200 text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  <span className="mr-1">{config.emoji}</span>
                  {config.label}
                </button>
              ))}
            </div>
          </div>

          {/* 情绪强度 */}
          {emotionState && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                情绪强度: {emotionIntensity}
              </label>
              <input
                type="range"
                min="1"
                max="10"
                value={emotionIntensity}
                onChange={(e) => setEmotionIntensity(Number(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>轻微</span>
                <span>强烈</span>
              </div>
            </div>
          )}

          {/* 出场策略 - 只在出场操作时显示 */}
          {isExit && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                出场策略
              </label>
              <div className="grid grid-cols-2 gap-2">
                {Object.entries(EXIT_STRATEGY_CONFIG).map(([key, config]) => (
                  <button
                    key={key}
                    type="button"
                    onClick={() => setExitStrategy(key as ExitStrategy)}
                    className={`px-4 py-2 rounded-md border text-sm transition-all ${
                      exitStrategy === key
                        ? `${config.bgColor} ${config.color} border-current font-medium`
                        : 'border-gray-200 text-gray-600 hover:bg-gray-50'
                    }`}
                  >
                    {config.label}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* 止损止盈 - 只在入场操作时显示 */}
          {isEntry && (
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  计划止损价
                </label>
                <input
                  type="number"
                  step="any"
                  value={plannedStopLoss}
                  onChange={(e) => setPlannedStopLoss(e.target.value)}
                  placeholder="可选"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  计划止盈价
                </label>
                <input
                  type="number"
                  step="any"
                  value={plannedTakeProfit}
                  onChange={(e) => setPlannedTakeProfit(e.target.value)}
                  placeholder="可选"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>
          )}

          {/* 止损执行情况 */}
          {plannedStopLoss && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                是否执行止损?
              </label>
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={() => setStopLossExecuted(true)}
                  className={`px-4 py-2 rounded-md border text-sm ${
                    stopLossExecuted === true
                      ? 'bg-green-50 text-green-700 border-green-300 font-medium'
                      : 'border-gray-200 text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  是,已执行
                </button>
                <button
                  type="button"
                  onClick={() => setStopLossExecuted(false)}
                  className={`px-4 py-2 rounded-md border text-sm ${
                    stopLossExecuted === false
                      ? 'bg-red-50 text-red-700 border-red-300 font-medium'
                      : 'border-gray-200 text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  否,未执行
                </button>
              </div>
            </div>
          )}

          {/* 补充备注 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              补充备注
            </label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              rows={3}
              placeholder="可选,记录其他重要信息..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            />
          </div>
          </div>
        </div>

        {/* 底部按钮 */}
        <div className="px-6 py-4 border-t border-gray-200 flex justify-end gap-3">
          <Button
            variant="outline"
            onClick={onClose}
            disabled={saving}
          >
            取消
          </Button>
          <Button
            onClick={handleSave}
            disabled={saving}
            className="bg-blue-600 hover:bg-blue-700 text-white"
          >
            {saving ? '保存中...' : '保存'}
          </Button>
        </div>
      </div>
    </div>
  );
}
