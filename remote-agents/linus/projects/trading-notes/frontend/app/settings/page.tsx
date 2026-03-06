'use client';

import { useEffect, useState } from 'react';
import PageNav from '@/components/layout/PageNav';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { apiClient } from '@/lib/api-client';
import type { AccountType } from '@/lib/types/account';
import { ACCOUNT_TYPE_LABELS } from '@/lib/types/account';
import type { StrategySettings, MarketStrategyConfig } from '@/types/strategy-settings';
import type { ActionType } from '@/types/trade';
import { ACTION_TYPE_CONFIG } from '@/types/trade';
import { usePageTitle } from '@/lib/use-page-title';

const ACTION_TYPES: ActionType[] = ['open', 'add', 'reduce', 'close'];
const MARKET_TYPES: AccountType[] = ['a_stock', 'us_stock', 'hk_stock', 'crypto'];
const DEFAULT_USD_CNY_RATE = 7.2;

const createEmptyMarketConfig = (): MarketStrategyConfig => ({
  open: [],
  add: [],
  reduce: [],
  close: []
});

const createDefaultSettings = (): StrategySettings => ({
  market_strategies: {
    a_stock: createEmptyMarketConfig(),
    us_stock: createEmptyMarketConfig(),
    hk_stock: createEmptyMarketConfig(),
    crypto: createEmptyMarketConfig()
  },
  currency_settings: {
    usd_cny_rate: DEFAULT_USD_CNY_RATE
  }
});

const normalizeSettings = (settings?: StrategySettings | null): StrategySettings => {
  const base = createDefaultSettings();
  if (settings?.currency_settings?.usd_cny_rate) {
    base.currency_settings.usd_cny_rate = settings.currency_settings.usd_cny_rate;
  }
  if (!settings?.market_strategies) {
    return base;
  }
  MARKET_TYPES.forEach((market) => {
    const incoming = settings.market_strategies[market];
    if (incoming) {
      base.market_strategies[market] = {
        open: incoming.open || [],
        add: incoming.add || [],
        reduce: incoming.reduce || [],
        close: incoming.close || []
      };
    }
  });
  return base;
};

const createEmptyDrafts = (): Record<AccountType, Record<ActionType, string>> => ({
  a_stock: { open: '', add: '', reduce: '', close: '' },
  us_stock: { open: '', add: '', reduce: '', close: '' },
  hk_stock: { open: '', add: '', reduce: '', close: '' },
  crypto: { open: '', add: '', reduce: '', close: '' }
});

export default function StrategySettingsPage() {
  const [settings, setSettings] = useState<StrategySettings>(createDefaultSettings());
  const [drafts, setDrafts] = useState<Record<AccountType, Record<ActionType, string>>>(createEmptyDrafts());
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  usePageTitle('策略设置');

  useEffect(() => {
    const loadSettings = async () => {
      try {
        setLoading(true);
        const data = await apiClient.getStrategySettings();
        setSettings(normalizeSettings(data));
      } catch (error) {
        setMessage('加载策略设置失败，请稍后再试。');
      } finally {
        setLoading(false);
      }
    };
    loadSettings();
  }, []);

  const handleDraftChange = (market: AccountType, actionType: ActionType, value: string) => {
    setDrafts((prev) => ({
      ...prev,
      [market]: {
        ...prev[market],
        [actionType]: value
      }
    }));
  };

  const handleFxRateChange = (value: string) => {
    const numeric = Number(value);
    if (!Number.isFinite(numeric) || numeric <= 0) {
      return;
    }
    setSettings((prev) => ({
      ...prev,
      currency_settings: {
        ...prev.currency_settings,
        usd_cny_rate: numeric
      }
    }));
  };

  const handleAddStrategy = (market: AccountType, actionType: ActionType) => {
    const raw = drafts[market][actionType].trim();
    if (!raw) return;

    setSettings((prev) => {
      const currentList = prev.market_strategies[market][actionType] || [];
      if (currentList.includes(raw)) {
        return prev;
      }
      return {
        ...prev,
        market_strategies: {
          ...prev.market_strategies,
          [market]: {
            ...prev.market_strategies[market],
            [actionType]: [...currentList, raw]
          }
        }
      };
    });

    handleDraftChange(market, actionType, '');
  };

  const handleRemoveStrategy = (market: AccountType, actionType: ActionType, value: string) => {
    setSettings((prev) => ({
      ...prev,
      market_strategies: {
        ...prev.market_strategies,
        [market]: {
          ...prev.market_strategies[market],
          [actionType]: prev.market_strategies[market][actionType].filter((item) => item !== value)
        }
      }
    }));
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      setMessage(null);
      const saved = await apiClient.updateStrategySettings(settings);
      setSettings(normalizeSettings(saved));
      setMessage('策略设置已保存。');
    } catch (error) {
      setMessage('保存失败，请检查网络或稍后再试。');
    } finally {
      setSaving(false);
    }
  };

  return (
    <>
      <PageNav />
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-amber-50 to-rose-50">
        <div className="container mx-auto px-4 py-8">
          <div className="flex flex-col gap-2 mb-8">
            <h1 className="text-3xl font-bold text-gray-900">策略设置</h1>
            <p className="text-gray-600">
              为不同市场配置建仓、加仓、减仓、清仓的操作策略选项。
            </p>
          </div>

          {message && (
            <div className="mb-6 rounded-lg border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-900">
              {message}
            </div>
          )}

          {loading ? (
            <div className="text-gray-500">正在加载...</div>
          ) : (
            <div className="space-y-6">
              <Card className="p-6 bg-white/80 backdrop-blur">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-xl font-semibold text-gray-900">汇率设置</h2>
                  <p className="text-sm text-gray-500">用于全部市场汇总时，将美元计价资产折算成人民币。</p>
                  </div>
                </div>
                <div className="mt-4 flex flex-col gap-2 md:flex-row md:items-center">
                  <label className="text-sm font-medium text-gray-700" htmlFor="usd-cny-rate">
                    美元兑人民币 (USD/CNY)
                  </label>
                  <input
                    id="usd-cny-rate"
                    type="number"
                    step="0.0001"
                    min="0.0001"
                    value={settings.currency_settings.usd_cny_rate}
                    onChange={(e) => handleFxRateChange(e.target.value)}
                    className="w-40 rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
                  />
                  <span className="text-xs text-gray-500">建议填入当前中间价，仅影响美元资产</span>
                </div>
              </Card>
              {MARKET_TYPES.map((market) => (
                <Card key={market} className="p-6 bg-white/80 backdrop-blur">
                  <div className="mb-4 flex items-center justify-between">
                    <div>
                      <h2 className="text-xl font-semibold text-gray-900">
                        {ACCOUNT_TYPE_LABELS[market]}
                      </h2>
                      <p className="text-sm text-gray-500">为该市场配置操作策略模板</p>
                    </div>
                  </div>

                  <div className="grid gap-4 md:grid-cols-2">
                    {ACTION_TYPES.map((actionType) => {
                      const config = ACTION_TYPE_CONFIG[actionType];
                      const strategies = settings.market_strategies[market][actionType];
                      return (
                        <div key={actionType} className="rounded-lg border border-gray-200 p-4">
                          <div className="flex items-center gap-2 mb-3">
                            <span className="text-lg">{config.icon}</span>
                            <span className="font-medium text-gray-900">{config.label}</span>
                          </div>

                          <div className="flex flex-wrap gap-2 mb-3">
                            {strategies.length === 0 && (
                              <span className="text-xs text-gray-400">暂无策略，添加一个吧。</span>
                            )}
                            {strategies.map((strategy) => (
                              <span
                                key={strategy}
                                className="inline-flex items-center gap-1 rounded-full border border-blue-200 bg-blue-50 px-3 py-1 text-xs text-blue-700"
                              >
                                {strategy}
                                <button
                                  type="button"
                                  onClick={() => handleRemoveStrategy(market, actionType, strategy)}
                                  className="text-blue-500 hover:text-blue-700"
                                >
                                  ×
                                </button>
                              </span>
                            ))}
                          </div>

                          <div className="flex gap-2">
                            <input
                              type="text"
                              value={drafts[market][actionType]}
                              onChange={(e) => handleDraftChange(market, actionType, e.target.value)}
                              placeholder={`添加${config.label}策略`}
                              className="flex-1 rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
                            />
                            <Button
                              type="button"
                              variant="outline"
                              onClick={() => handleAddStrategy(market, actionType)}
                            >
                              添加
                            </Button>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </Card>
              ))}
            </div>
          )}

          <div className="mt-8 flex justify-end">
            <Button onClick={handleSave} disabled={saving || loading}>
              {saving ? '保存中...' : '保存设置'}
            </Button>
          </div>
        </div>
      </div>
    </>
  );
}
