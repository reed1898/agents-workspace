'use client';

import { useEffect, useMemo, useState, Fragment } from 'react';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import { apiClient } from '@/lib/api-client';
import { Trade, TradeStats } from '@/types/trade';
import type { StrategySettings } from '@/types/strategy-settings';
import StatsNav from '@/components/layout/StatsNav';
import PageNav from '@/components/layout/PageNav';
import { accountsApi } from '@/lib/api/accounts';
import type { AccountType, TradeAccount } from '@/lib/types/account';
import { ACCOUNT_TYPE_LABELS, BROKER_OPTIONS } from '@/lib/types/account';
import { ActionTypeBadge } from '@/components/trades/action-type-badge';
import { ReviewTradeDialog } from '@/components/trades/review-trade-dialog';
import { ActionStatsCards } from '@/components/trades/action-stats-cards';
import type { TradeReviewData } from '@/types/trade';
import {
  formatMoney,
  formatNumber,
  formatPrice,
  formatQuantity as formatQuantityValue
} from '@/lib/format/number';
import { usePageTitle } from '@/lib/use-page-title';

type TimeRange = 'all' | 'today' | 'yesterday' | 'week' | 'month' | 'quarter';
type SortDirection = 'asc' | 'desc';
type SortKey = 'trade_time' | 'symbol' | 'quantity' | 'price' | 'total_amount' | 'fee';

const BROKER_LABEL_MAP: Record<string, string> = Object.values(BROKER_OPTIONS).reduce(
  (acc, options) => {
    (options as any[]).forEach((opt) => {
      acc[opt.value] = opt.label;
    });
    return acc;
  },
  {} as Record<string, string>
);

export default function TradesPage() {
  const searchParams = useSearchParams();
  const [trades, setTrades] = useState<Trade[]>([]);
  const [stats, setStats] = useState<TradeStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [accountFilter, setAccountFilter] = useState<string>('');

  const [accounts, setAccounts] = useState<TradeAccount[]>([]);

  // 新增筛选状态
  const [selectedAccountType, setSelectedAccountType] = useState<AccountType | 'all'>('all');
  const [selectedTradeType, setSelectedTradeType] = useState<'all' | 'spot' | 'futures'>('all');
  const [selectedTimeRange, setSelectedTimeRange] = useState<TimeRange>('all');
  const [selectedBroker, setSelectedBroker] = useState<string>('all');
  const [accountTypeMap, setAccountTypeMap] = useState<Record<string, AccountType>>({});
  const [strategySettings, setStrategySettings] = useState<StrategySettings | null>(null);

  // 用于统计的所有账户类型计数
  const [accountTypeCounts, setAccountTypeCounts] = useState<Record<AccountType, number>>({
    crypto: 0,
    us_stock: 0,
    a_stock: 0,
    hk_stock: 0
  });

  // 展开理由的交易ID
  const [expandedTradeId, setExpandedTradeId] = useState<string | null>(null);

  // 交易详情对话框状态
  const [editingTrade, setEditingTrade] = useState<Trade | null>(null);

  // 表格排序状态（默认按成交时间从新到旧）
  const [sortKey, setSortKey] = useState<SortKey>('trade_time');
  const [sortDirection, setSortDirection] = useState<SortDirection>('desc');

  usePageTitle('交易记录');

  // 读取URL参数
  useEffect(() => {
    const accountIdParam = searchParams.get('account_id');
    if (accountIdParam) {
      setAccountFilter(accountIdParam);
    }
  }, [searchParams]);

  // 先加载账户信息，再加载交易记录
  useEffect(() => {
    const init = async () => {
      await loadAccounts();
      await loadStrategySettings();
      await loadTrades();
    };
    init();
  }, []);

  // 当筛选条件变化时，重新加载交易
  useEffect(() => {
    loadTrades();
  }, [page, accountFilter, selectedAccountType, selectedBroker, selectedTradeType, selectedTimeRange]);

  useEffect(() => {
    // 当 trades 数据变化时重新计算统计
    loadStats();
  }, [trades]);

  useEffect(() => {
    if (editingTrade) {
      loadStrategySettings();
    }
  }, [editingTrade]);

  const loadAccounts = async () => {
    try {
      const allAccounts = await accountsApi.getAccounts();
      setAccounts(allAccounts);
      const typeMap: Record<string, AccountType> = {};
      allAccounts.forEach((account) => {
        typeMap[account.id] = account.account_type;
      });
      setAccountTypeMap(typeMap);

      // 加载每种账户类型的交易计数
      await loadAccountTypeCounts(allAccounts);
    } catch (err) {
      console.error('Failed to load accounts:', err);
    }
  };

  const loadStrategySettings = async () => {
    try {
      const settings = await apiClient.getStrategySettings();
      setStrategySettings(settings);
    } catch (err) {
      console.error('Failed to load strategy settings:', err);
    }
  };

  const loadAccountTypeCounts = async (accounts: any[]) => {
    try {
      // 按账户类型分组
      const accountsByType: Record<AccountType, string[]> = {
        crypto: [],
        us_stock: [],
        a_stock: [],
        hk_stock: []
      };

      accounts.forEach(acc => {
        if (accountsByType[acc.account_type]) {
          accountsByType[acc.account_type].push(acc.id);
        }
      });

      // 为每种账户类型获取交易计数
      const counts: Record<AccountType, number> = {
        crypto: 0,
        us_stock: 0,
        a_stock: 0,
        hk_stock: 0
      };

      for (const [accountType, accountIds] of Object.entries(accountsByType)) {
        if (accountIds.length > 0) {
          // 获取该类型下所有账户的交易总数
          let typeTotal = 0;
          for (const accountId of accountIds) {
            try {
              const response = await apiClient.getTrades({
                account_id: accountId,
                page: 1,
                page_size: 1  // 只需要获取总数
              });
              typeTotal += response.total || 0;
            } catch (err) {
              console.error(`Failed to get count for account ${accountId}:`, err);
            }
          }
          counts[accountType as AccountType] = typeTotal;
        }
      }

      setAccountTypeCounts(counts);
    } catch (err) {
      console.error('Failed to load account type counts:', err);
    }
  };

  const getTimeRangeDates = (range: TimeRange): { start_date?: string; end_date?: string } => {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

    switch (range) {
      case 'today':
        return {
          start_date: today.toISOString(),
          end_date: now.toISOString()
        };
      case 'yesterday':
        const yesterday = new Date(today);
        yesterday.setDate(yesterday.getDate() - 1);
        return {
          start_date: yesterday.toISOString(),
          end_date: today.toISOString()
        };
      case 'week':
        const weekAgo = new Date(today);
        weekAgo.setDate(weekAgo.getDate() - 7);
        return {
          start_date: weekAgo.toISOString(),
          end_date: now.toISOString()
        };
      case 'month':
        const monthAgo = new Date(today);
        monthAgo.setMonth(monthAgo.getMonth() - 1);
        return {
          start_date: monthAgo.toISOString(),
          end_date: now.toISOString()
        };
      case 'quarter':
        const quarterAgo = new Date(today);
        quarterAgo.setMonth(quarterAgo.getMonth() - 3);
        return {
          start_date: quarterAgo.toISOString(),
          end_date: now.toISOString()
        };
      default:
        return {};
    }
  };

  const loadTrades = async () => {
    try {
      setLoading(true);
      const params: any = { page, page_size: 20 };

      if (accountFilter) {
        params.account_id = accountFilter;
      }

      if (selectedAccountType !== 'all') {
        params.account_type = selectedAccountType;
      }

      if (selectedBroker !== 'all') {
        params.broker = selectedBroker;
      }

      // 添加时间范围筛选
      const timeRange = getTimeRangeDates(selectedTimeRange);
      if (timeRange.start_date) {
        params.start_date = timeRange.start_date;
      }
      if (timeRange.end_date) {
        params.end_date = timeRange.end_date;
      }

      const response = await apiClient.getTrades(params);

      // 客户端筛选：按交易类型（现货/合约）
      let filteredTrades = response.trades;

      // 按交易类型筛选（现货/合约）
      if (selectedTradeType === 'spot') {
        filteredTrades = filteredTrades.filter(trade =>
          !trade.position_side || trade.position_side === null
        );
      } else if (selectedTradeType === 'futures') {
        filteredTrades = filteredTrades.filter(trade =>
          trade.position_side !== null && trade.position_side !== undefined
        );
      }

      setTrades(filteredTrades);
      setTotalPages(response.total_pages || 1);
      setTotalCount(response.total || filteredTrades.length);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || '加载交易记录失败');
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      // 基于筛选后的交易计算统计数据
      if (trades.length === 0) {
        setStats({
          total_trades: 0,
          buy_count: 0,
          sell_count: 0,
          total_volume: '0',
          total_fees: '0',
          unique_symbols: 0,
          first_trade_date: null,
          last_trade_date: null
        });
        return;
      }

      const buyCount = trades.filter(t => t.side === 'buy').length;
      const sellCount = trades.filter(t => t.side === 'sell').length;
      const totalVolume = trades.reduce((sum, t) =>
        sum + (parseFloat(t.price) * parseFloat(t.quantity)), 0
      );
      const totalFees = trades.reduce((sum, t) =>
        sum + parseFloat(t.fee || '0'), 0
      );
      const uniqueSymbols = new Set(trades.map(t => t.symbol)).size;

      const tradeDates = trades.map(t => new Date(t.trade_time)).filter(d => !isNaN(d.getTime()));
      const firstTradeDate = tradeDates.length > 0 ?
        new Date(Math.min(...tradeDates.map(d => d.getTime()))).toISOString() : null;
      const lastTradeDate = tradeDates.length > 0 ?
        new Date(Math.max(...tradeDates.map(d => d.getTime()))).toISOString() : null;

      setStats({
        total_trades: trades.length,
        buy_count: buyCount,
        sell_count: sellCount,
        total_volume: totalVolume.toString(),
        total_fees: totalFees.toString(),
        unique_symbols: uniqueSymbols,
        first_trade_date: firstTradeDate,
        last_trade_date: lastTradeDate
      });
    } catch (err) {
      console.error('Failed to calculate stats:', err);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getMarketType = (trade: Trade): AccountType | undefined => {
    return (trade.account_type || accountTypeMap[trade.account_id]) as AccountType | undefined;
  };

  const formatMoneyByMarket = (
    marketType: AccountType | undefined,
    value: unknown,
    fallbackFractionDigits: number
  ) => formatMoney(value, { accountType: marketType, fallbackFractionDigits });

  const formatTradePrice = (trade: Trade) => {
    const marketType = getMarketType(trade);
    return formatPrice(trade.price, {
      accountType: marketType,
      fallbackFractionDigits: marketType === 'crypto' ? 8 : 2,
    });
  };

  const formatTradeTotalAmount = (trade: Trade) => {
    const marketType = getMarketType(trade);
    const amount = trade.total_amount ?? 0;
    return formatMoneyByMarket(marketType, amount, 2);
  };

  const formatTradeFee = (trade: Trade) => {
    const marketType = getMarketType(trade);
    const fee = trade.fee ?? 0;
    return formatMoneyByMarket(marketType, fee, 2);
  };

  const formatTradeLeverage = (trade: Trade) =>
    formatNumber(trade.leverage, { maximumFractionDigits: 2, minimumFractionDigits: 0 });

  const formatTradeMargin = (trade: Trade) => {
    const marketType = getMarketType(trade);
    const margin = trade.margin ?? 0;
    return formatMoneyByMarket(marketType, margin, 2);
  };

  const formatQuantity = (trade: Trade) => {
    const marketType = getMarketType(trade);
    return formatQuantityValue(trade.quantity, { accountType: marketType, fallbackFractionDigits: 8 });
  };

  const statsMarketType = useMemo(() => {
    if (selectedAccountType !== 'all') return selectedAccountType;
    if (accountFilter && accountTypeMap[accountFilter]) return accountTypeMap[accountFilter];

    const marketTypes = new Set<AccountType>();
    trades.forEach((trade) => {
      const marketType = getMarketType(trade);
      if (marketType) marketTypes.add(marketType);
    });

    if (marketTypes.size === 1) return marketTypes.values().next().value;
    return undefined;
  }, [accountFilter, accountTypeMap, selectedAccountType, trades]);

  const accountById = useMemo(() => {
    const map: Record<string, TradeAccount> = {};
    accounts.forEach((account) => {
      map[account.id] = account;
    });
    return map;
  }, [accounts]);

  const sortedTrades = useMemo(() => {
    const getNumeric = (value: unknown) => {
      const parsed = Number.parseFloat(String(value ?? ''));
      return Number.isFinite(parsed) ? parsed : 0;
    };

    const compare = (a: Trade, b: Trade) => {
      switch (sortKey) {
        case 'trade_time': {
          const at = new Date(a.trade_time).getTime();
          const bt = new Date(b.trade_time).getTime();
          return (Number.isFinite(at) ? at : 0) - (Number.isFinite(bt) ? bt : 0);
        }
        case 'symbol':
          return (a.symbol || '').localeCompare(b.symbol || '');
        case 'quantity':
          return getNumeric(a.quantity) - getNumeric(b.quantity);
        case 'price':
          return getNumeric(a.price) - getNumeric(b.price);
        case 'total_amount':
          return getNumeric(a.total_amount) - getNumeric(b.total_amount);
        case 'fee':
          return getNumeric(a.fee) - getNumeric(b.fee);
        default:
          return 0;
      }
    };

    return trades
      .map((trade, index) => ({ trade, index }))
      .sort((x, y) => {
        const delta = compare(x.trade, y.trade);
        const adjusted = sortDirection === 'asc' ? delta : -delta;
        if (adjusted !== 0) return adjusted;
        return x.index - y.index;
      })
      .map(({ trade }) => trade);
  }, [sortDirection, sortKey, trades]);

  const toggleSort = (key: SortKey) => {
    if (key === sortKey) {
      setSortDirection((prev) => (prev === 'asc' ? 'desc' : 'asc'));
      return;
    }
    setSortKey(key);
    setSortDirection(key === 'trade_time' ? 'desc' : 'asc');
  };

  const SortIndicator = ({ columnKey }: { columnKey: SortKey }) => {
    if (columnKey !== sortKey) return null;
    return <span className="ml-1 inline-block">{sortDirection === 'asc' ? '▲' : '▼'}</span>;
  };

  const getSideBadge = (side: string) => {
    if (side === 'buy') {
      return (
        <span className="px-2 py-1 text-xs font-semibold rounded bg-green-100 text-green-800">
          买入
        </span>
      );
    }
    return (
      <span className="px-2 py-1 text-xs font-semibold rounded bg-red-100 text-red-800">
        卖出
      </span>
    );
  };

  const handleSaveTradeReview = async (tradeId: string, reviewData: TradeReviewData) => {
    try {
      // 调用API更新交易
      await apiClient.reviewTrade(tradeId, reviewData);

      // 重新加载交易列表
      await loadTrades();

      setEditingTrade(null);
    } catch (err: any) {
      throw new Error(err.response?.data?.detail || '更新失败');
    }
  };

  if (loading && trades.length === 0) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center h-64">
          <div className="text-gray-500">加载中...</div>
        </div>
      </div>
    );
  }

  const accountsForFilters = accounts.filter((account) => {
    if (selectedAccountType !== 'all' && account.account_type !== selectedAccountType) {
      return false;
    }
    if (selectedBroker !== 'all' && (account.broker || '').toLowerCase() !== selectedBroker.toLowerCase()) {
      return false;
    }
    return true;
  });

  const showAccountScopeFilters = selectedAccountType !== 'all' || Boolean(accountFilter);

  const availableBrokers = Array.from(
    new Set(
      accounts
        .filter((account) => selectedAccountType === 'all' || account.account_type === selectedAccountType)
        .map((account) => account.broker)
        .filter((b): b is string => Boolean(b && b.trim()))
        .map((b) => b.trim())
    )
  ).sort((a, b) => (BROKER_LABEL_MAP[a] || a).localeCompare(BROKER_LABEL_MAP[b] || b));

  return (
    <>
      <PageNav />
      <div className="container mx-auto px-4 py-8">
        {/* 页面标题 */}
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">交易记录</h1>
            <p className="mt-2 text-gray-600">查看和管理您的所有交易记录</p>
          </div>
          {/* 未复盘交易提示 */}
          {trades.length > 0 && (
            <div className="flex items-center gap-4">
              {(() => {
                const unreviewedCount = trades.filter(t => t.review_status !== 'reviewed').length;
                if (unreviewedCount > 0) {
                  return (
                    <div className="px-4 py-2 bg-amber-50 border border-amber-200 rounded-lg">
                      <div className="flex items-center gap-2">
                        <svg className="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                        </svg>
                        <span className="text-sm font-medium text-amber-800">
                          {unreviewedCount} 笔交易待复盘
                        </span>
                      </div>
                    </div>
                  );
                }
                return (
                  <div className="px-4 py-2 bg-green-50 border border-green-200 rounded-lg">
                    <div className="flex items-center gap-2">
                      <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <span className="text-sm font-medium text-green-800">
                        所有交易已复盘
                      </span>
                    </div>
                  </div>
                );
              })()}
            </div>
          )}
        </div>
      </div>

      {/* 错误提示 */}
      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* 统计导航栏 */}
      {stats && (
        <StatsNav
          stats={[
            {
              label: '总交易笔数',
              value: stats.total_trades || 0,
              icon: 'activity',
              trend: 'neutral'
            },
            {
              label: '买入笔数',
              value: stats.buy_count || 0,
              icon: 'trending-up',
              trend: 'up'
            },
            {
              label: '卖出笔数',
              value: stats.sell_count || 0,
              icon: 'trending-down',
              trend: 'down'
            },
            {
              label: '交易标的数',
              value: stats.unique_symbols || 0,
              icon: 'activity',
              trend: 'neutral'
            },
            {
              label: '总交易额',
              value: formatMoneyByMarket(statsMarketType, stats.total_volume?.toString() || '0', 2),
              icon: 'dollar',
              trend: 'neutral'
            },
            {
              label: '总手续费',
              value: formatMoneyByMarket(statsMarketType, stats.total_fees?.toString() || '0', 2),
              icon: 'dollar',
              trend: 'neutral'
            }
          ]}
          variant="compact"
        />
      )}

      {/* 操作类型和理由统计卡片 */}
      <ActionStatsCards trades={trades} />

      {/* 筛选栏 */}
      <div className="mb-6 flex items-center justify-between gap-4 flex-wrap">
        <div className="flex items-center gap-4 flex-wrap">
          {/* 账户类型筛选 */}
          <div className="flex items-center gap-2">
            <label className="text-sm font-medium text-gray-700">账户类型:</label>
            <select
              value={selectedAccountType}
              onChange={(e) => {
                setSelectedAccountType(e.target.value as AccountType | 'all');
                setSelectedBroker('all');
                setAccountFilter('');
                setPage(1); // 重置到第一页
              }}
              className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">全部 ({totalCount})</option>
              {(Object.keys(ACCOUNT_TYPE_LABELS) as AccountType[]).map((type) => {
                const count = accountTypeCounts[type] || 0;
                return (
                  <option key={type} value={type}>
                    {ACCOUNT_TYPE_LABELS[type]} ({count})
                  </option>
                );
              })}
            </select>
          </div>

          {showAccountScopeFilters && (
            <>
              {/* 交易所/券商筛选 */}
              <div className="flex items-center gap-2">
                <label className="text-sm font-medium text-gray-700">交易所/券商:</label>
                <select
                  value={selectedBroker}
                  onChange={(e) => {
                    setSelectedBroker(e.target.value);
                    setAccountFilter('');
                    setPage(1);
                  }}
                  className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="all">全部</option>
                  {availableBrokers.map((broker) => (
                    <option key={broker} value={broker}>
                      {BROKER_LABEL_MAP[broker] || broker}
                    </option>
                  ))}
                </select>
              </div>

              {/* 交易账户筛选 */}
              <div className="flex items-center gap-2">
                <label className="text-sm font-medium text-gray-700">交易账户:</label>
                <select
                  value={accountFilter || 'all'}
                  onChange={(e) => {
                    const value = e.target.value;
                    setAccountFilter(value === 'all' ? '' : value);
                    setPage(1);
                  }}
                  className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="all">全部</option>
                  {accountsForFilters.map((account) => (
                    <option key={account.id} value={account.id}>
                      {account.account_name}
                      {account.broker ? ` (${BROKER_LABEL_MAP[account.broker] || account.broker})` : ''}
                    </option>
                  ))}
                </select>
              </div>
            </>
          )}

          {/* 交易类型筛选 */}
          <div className="flex items-center gap-2">
            <label className="text-sm font-medium text-gray-700">交易类型:</label>
            <select
              value={selectedTradeType}
              onChange={(e) => {
                setSelectedTradeType(e.target.value as 'all' | 'spot' | 'futures');
                setPage(1);
              }}
              className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">全部</option>
              <option value="spot">现货</option>
              <option value="futures">合约</option>
            </select>
          </div>

          {/* 时间范围筛选 */}
          <div className="flex items-center gap-2">
            <label className="text-sm font-medium text-gray-700">时间范围:</label>
            <select
              value={selectedTimeRange}
              onChange={(e) => {
                setSelectedTimeRange(e.target.value as TimeRange);
                setPage(1);
              }}
              className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">全部</option>
              <option value="today">今天</option>
              <option value="yesterday">昨天</option>
              <option value="week">最近一周</option>
              <option value="month">最近一个月</option>
              <option value="quarter">最近三个月</option>
            </select>
          </div>
        </div>

        {/* 记录统计 */}
        <div className="text-sm text-gray-600">
          共 {totalCount} 条记录（本页 {trades.length} 条）
        </div>
      </div>

      {/* 交易记录表格 */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider w-12">

                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  <button
                    type="button"
                    onClick={() => toggleSort('trade_time')}
                    className="inline-flex items-center hover:text-gray-700"
                  >
                    时间
                    <SortIndicator columnKey="trade_time" />
                  </button>
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  账户
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  <button
                    type="button"
                    onClick={() => toggleSort('symbol')}
                    className="inline-flex items-center hover:text-gray-700"
                  >
                    标的
                    <SortIndicator columnKey="symbol" />
                  </button>
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  操作类型
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  类型/方向
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  <button
                    type="button"
                    onClick={() => toggleSort('quantity')}
                    className="inline-flex items-center hover:text-gray-700"
                  >
                    数量
                    <SortIndicator columnKey="quantity" />
                  </button>
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  <button
                    type="button"
                    onClick={() => toggleSort('price')}
                    className="inline-flex items-center hover:text-gray-700"
                  >
                    价格
                    <SortIndicator columnKey="price" />
                  </button>
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  <button
                    type="button"
                    onClick={() => toggleSort('total_amount')}
                    className="inline-flex items-center hover:text-gray-700"
                  >
                    金额
                    <SortIndicator columnKey="total_amount" />
                  </button>
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  <button
                    type="button"
                    onClick={() => toggleSort('fee')}
                    className="inline-flex items-center hover:text-gray-700"
                  >
                    杠杆/费用
                    <SortIndicator columnKey="fee" />
                  </button>
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  来源
                </th>
                <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                  操作
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {trades.length === 0 ? (
                <tr>
                  <td colSpan={12} className="px-6 py-12 text-center text-gray-500">
                    暂无交易记录
                  </td>
                </tr>
              ) : (
                sortedTrades.map((trade) => {
                  // 判断交易类型和操作
                  const isFutures = trade.position_side !== null && trade.position_side !== undefined;
                  const isLong = trade.position_side === 'LONG';
                  const isShort = trade.position_side === 'SHORT';

                  // 合约交易操作类型
                  let actionLabel = '';
                  if (isFutures) {
                    if (isLong && trade.side === 'buy') actionLabel = '开多';
                    else if (isLong && trade.side === 'sell') actionLabel = '平多';
                    else if (isShort && trade.side === 'sell') actionLabel = '开空';
                    else if (isShort && trade.side === 'buy') actionLabel = '平空';
                  }

                  const hasReason = trade.action_reason && trade.action_reason.trim() !== '';
                  const isExpanded = expandedTradeId === trade.id;

                  return (
                    <Fragment key={trade.id}>
                      <tr
                        className="hover:bg-gray-50 transition-colors"
                      >
                        {/* 展开按钮 */}
                        <td className="px-6 py-4 whitespace-nowrap text-center">
                          {hasReason && (
                            <button
                              onClick={() => setExpandedTradeId(isExpanded ? null : trade.id)}
                              className="text-gray-400 hover:text-gray-600 transition-colors"
                            >
                              {isExpanded ? (
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
                                </svg>
                              ) : (
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                                </svg>
                              )}
                            </button>
                          )}
                        </td>

                        {/* 时间 */}
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {formatDate(trade.trade_time)}
                        </td>

                        {/* 账户 */}
                        <td className="px-6 py-4 whitespace-nowrap">
                          {(() => {
                            const account = accountById[trade.account_id];
                            const accountName = account?.account_name || trade.account_id;
                            const accountType = account?.account_type || trade.account_type;
                            const brokerLabel = account?.broker
                              ? BROKER_LABEL_MAP[account.broker] || account.broker
                              : '';

                            return (
                              <div className="flex flex-col">
                                <Link
                                  href={`/accounts/${trade.account_id}`}
                                  className="text-sm font-medium text-blue-600 hover:text-blue-800 hover:underline"
                                >
                                  {accountName}
                                </Link>
                                {(accountType || brokerLabel) && (
                                  <div className="text-xs text-gray-500">
                                    {accountType ? ACCOUNT_TYPE_LABELS[accountType as AccountType] : ''}
                                    {accountType && brokerLabel ? ' · ' : ''}
                                    {brokerLabel}
                                  </div>
                                )}
                              </div>
                            );
                          })()}
                        </td>

                      {/* 标的 */}
                      <td
                        className="px-6 py-4 whitespace-nowrap cursor-pointer hover:bg-blue-50"
                        onClick={() => window.location.href = `/symbols/${encodeURIComponent(trade.symbol)}?account_id=${trade.account_id}`}
                      >
                        <div className="text-sm font-medium text-blue-600 hover:text-blue-800 hover:underline">
                          {trade.symbol}
                        </div>
                        {trade.symbol_name && (
                          <div className="text-xs text-gray-500">
                            {trade.symbol_name}
                          </div>
                        )}
                      </td>

                      {/* 操作类型 */}
                      <td className="px-6 py-4 whitespace-nowrap">
                        <ActionTypeBadge type={trade.action_type} />
                      </td>

                      {/* 类型/方向 */}
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex flex-col gap-1">
                          {isFutures ? (
                            <>
                              <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold ${
                                isLong
                                  ? 'bg-green-100 text-green-800'
                                  : 'bg-red-100 text-red-800'
                              }`}>
                                {actionLabel}
                              </span>
                              {trade.leverage && (
                                <span className="text-xs text-gray-500">
                                  {formatTradeLeverage(trade)}x
                                </span>
                              )}
                            </>
                          ) : (
                            getSideBadge(trade.side)
                          )}
                        </div>
                      </td>

                      {/* 数量 */}
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900">
                        {formatQuantity(trade)}
                      </td>

                      {/* 价格 */}
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900">
                        {formatTradePrice(trade)}
                      </td>

                      {/* 金额 */}
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-medium text-gray-900">
                        {formatTradeTotalAmount(trade)}
                      </td>

                      {/* 杠杆/费用 */}
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-right">
                        {isFutures && trade.margin ? (
                          <div>
                            <div className="text-gray-900 font-medium">
                              保证金: {formatTradeMargin(trade)}
                            </div>
                            <div className="text-xs text-gray-500">
                              费用: {formatTradeFee(trade)}
                            </div>
                          </div>
                        ) : (
                          <div className="text-gray-500">
                            {formatTradeFee(trade)}
                          </div>
                        )}
                      </td>

                      {/* 来源 */}
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {trade.sync_source === 'api' && '同步'}
                        {trade.sync_source === 'manual' && '手动'}
                        {trade.sync_source === 'import' && '导入'}
                      </td>

                      {/* 操作按钮 */}
                      <td className="px-6 py-4 whitespace-nowrap text-center">
                        <button
                          onClick={() => setEditingTrade(trade)}
                          className={`transition-colors ${
                            trade.review_status === 'reviewed'
                              ? 'text-green-600 hover:text-green-800'
                              : trade.action_reason
                              ? 'text-blue-600 hover:text-blue-800'
                              : 'text-gray-400 hover:text-gray-600'
                          }`}
                          title={
                            trade.review_status === 'reviewed'
                              ? '已复盘 - 点击查看/编辑'
                              : trade.action_reason
                              ? '有理由 - 点击编辑/补充复盘'
                              : '点击添加交易理由和复盘'
                          }
                        >
                          <svg className="w-5 h-5 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                          </svg>
                        </button>
                      </td>
                    </tr>

                    {/* 展开的理由行 */}
                    {isExpanded && hasReason && (
                      <tr className="bg-blue-50">
                        <td colSpan={12} className="px-6 py-4">
                          <div className="flex items-start gap-2">
                            <div className="flex-shrink-0">
                              <svg className="w-5 h-5 text-blue-500 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                              </svg>
                            </div>
                            <div className="flex-grow">
                              <div className="text-sm font-medium text-blue-900 mb-1">交易理由:</div>
                              <div className="text-sm text-gray-700 whitespace-pre-wrap">{trade.action_reason}</div>
                            </div>
                          </div>
                        </td>
                      </tr>
                    )}
                  </Fragment>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* 交易详情对话框 */}
      {editingTrade && (
        <ReviewTradeDialog
          trade={editingTrade}
          isOpen={true}
          onClose={() => setEditingTrade(null)}
          onSave={handleSaveTradeReview}
          marketType={editingTrade.account_type || accountTypeMap[editingTrade.account_id]}
          strategySettings={strategySettings}
        />
      )}

      {/* 分页 */}
      {totalPages > 1 && (
        <div className="mt-6 flex items-center justify-between">
          <button
            onClick={() => setPage(Math.max(1, page - 1))}
            disabled={page === 1}
            className="px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            上一页
          </button>

          <div className="text-sm text-gray-600">
            第 {page} / {totalPages} 页
          </div>

          <button
            onClick={() => setPage(Math.min(totalPages, page + 1))}
            disabled={page === totalPages}
            className="px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            下一页
          </button>
        </div>
      )}
      </div>
    </>
  );
}
