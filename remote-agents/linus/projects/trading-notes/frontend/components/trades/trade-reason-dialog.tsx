'use client';

import { useState } from 'react';
import { Trade, ActionType } from '@/types/trade';
import { Button } from '@/components/ui/button';
import { ACTION_TYPE_CONFIG } from '@/types/trade';
import { formatPrice, formatQuantity } from '@/lib/format/number';

interface TradeReasonDialogProps {
  trade: Trade;
  isOpen: boolean;
  onClose: () => void;
  onSave: (tradeId: string, actionType: ActionType | null, actionReason: string) => Promise<void>;
}

export function TradeReasonDialog({ trade, isOpen, onClose, onSave }: TradeReasonDialogProps) {
  const [actionType, setActionType] = useState<ActionType | ''>(trade.action_type || '');
  const [actionReason, setActionReason] = useState(trade.action_reason || '');
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleSave = async () => {
    try {
      setSaving(true);
      setError(null);
      await onSave(
        trade.id,
        actionType === '' ? null : actionType as ActionType,
        actionReason
      );
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
            <h2 className="text-xl font-semibold text-gray-900">编辑交易理由</h2>
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

        {/* 交易信息 */}
        <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-500">标的:</span>
              <span className="ml-2 font-medium text-gray-900">{trade.symbol}</span>
            </div>
            <div>
              <span className="text-gray-500">方向:</span>
              <span className={`ml-2 px-2 py-0.5 rounded text-xs font-semibold ${
                trade.side === 'buy' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
              }`}>
                {trade.side === 'buy' ? '买入' : '卖出'}
              </span>
            </div>
            <div>
              <span className="text-gray-500">数量:</span>
              <span className="ml-2 font-medium text-gray-900">
                {formatQuantity(trade.quantity, { accountType: trade.account_type, fallbackFractionDigits: 4 })}
              </span>
            </div>
            <div>
              <span className="text-gray-500">价格:</span>
              <span className="ml-2 font-medium text-gray-900">
                {formatPrice(trade.price, { accountType: trade.account_type, fallbackFractionDigits: 8 })}
              </span>
            </div>
          </div>
        </div>

        {/* 表单内容 */}
        <div className="px-6 py-4 space-y-4">
          {/* 错误提示 */}
          {error && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          )}

          {/* 操作类型选择 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              操作类型
            </label>
            <div className="grid grid-cols-2 gap-3">
              <button
                onClick={() => setActionType('')}
                className={`px-4 py-3 rounded-lg border-2 transition-all ${
                  actionType === ''
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <span className="text-sm font-medium">未设置</span>
              </button>
              {(['open', 'add', 'reduce', 'close'] as ActionType[]).map((type) => {
                const config = ACTION_TYPE_CONFIG[type];
                return (
                  <button
                    key={type}
                    onClick={() => setActionType(type)}
                    className={`px-4 py-3 rounded-lg border-2 transition-all ${
                      actionType === type
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <div className="flex items-center gap-2">
                      <span className="text-lg">{config.icon}</span>
                      <span className="text-sm font-medium">{config.label}</span>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* 交易理由输入 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              交易理由
              <span className="text-gray-400 font-normal ml-1">(建议包括入场信号、技术分析、基本面等)</span>
            </label>
            <textarea
              value={actionReason}
              onChange={(e) => setActionReason(e.target.value)}
              rows={6}
              placeholder="例如：突破前高阻力位，MACD金叉，成交量放大，市场情绪转好..."
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            />
            <div className="mt-1 text-xs text-gray-500">
              {actionReason.length} 字符
            </div>
          </div>
        </div>

        {/* 底部按钮 */}
        <div className="px-6 py-4 border-t border-gray-200 flex justify-end gap-3">
          <Button
            onClick={onClose}
            variant="outline"
            disabled={saving}
          >
            取消
          </Button>
          <Button
            onClick={handleSave}
            disabled={saving}
          >
            {saving ? '保存中...' : '保存'}
          </Button>
        </div>
      </div>
    </div>
  );
}
