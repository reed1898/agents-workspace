'use client';

import { useEffect, useMemo, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { TrendingUp, RefreshCw, ArrowUpDown, ArrowUp, ArrowDown, Pencil } from 'lucide-react';
import { apiClient } from '@/lib/api-client';
import { Position, PositionStats } from '@/types/position';
import StatsNav from '@/components/layout/StatsNav';
import PageNav from '@/components/layout/PageNav';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { accountsApi, TradeAccount } from '@/lib/api/accounts';
import type { AccountType } from '@/lib/types/account';
import { ACCOUNT_TYPE_LABELS } from '@/lib/types/account';
import { useToast } from '@/hooks/use-toast';
import { formatMoney, formatPrice, formatQuantity as formatQuantityValue } from '@/lib/format/number';
import { usePageTitle } from '@/lib/use-page-title';

type SortKey = 'symbol' | 'quantity' | 'cost' | 'current_price' | 'value' | 'pnl' | 'pnl_percent' | 'holding_days';
type SortConfig = { key: SortKey; direction: 'asc' | 'desc' };
type ClosedSortKey = 'symbol' | 'quantity' | 'cost' | 'open_value' | 'final_price' | 'holding_days' | 'realized_pnl' | 'realized_pnl_percent' | 'first_buy_time' | 'closed_at';
type ClosedSortConfig = { key: ClosedSortKey; direction: 'asc' | 'desc' };

export default function PositionsPage() {
  const searchParams = useSearchParams();
  const { toast } = useToast();
  const [positions, setPositions] = useState<Position[]>([]);
  const [allPositions, setAllPositions] = useState<Position[]>([]);
  const [closedPositions, setClosedPositions] = useState<Position[]>([]);
  const [allClosedPositions, setAllClosedPositions] = useState<Position[]>([]);
  const [stats, setStats] = useState<PositionStats | null>(null);
  const [tradeStats, setTradeStats] = useState<{ totalFees: number; totalVolume: number } | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedType, setSelectedType] = useState<AccountType | 'all'>('all');
  const [selectedAccountId, setSelectedAccountId] = useState<string>('all');
  const [accounts, setAccounts] = useState<TradeAccount[]>([]);
  const [accountTypeMap, setAccountTypeMap] = useState<Record<string, AccountType>>({});
  const [usdCnyRate, setUsdCnyRate] = useState<number>(0);
  const [refreshing, setRefreshing] = useState(false);
  const [noteDialogOpen, setNoteDialogOpen] = useState(false);
  const [notePosition, setNotePosition] = useState<Position | null>(null);
  const [noteDraft, setNoteDraft] = useState('');
  const [noteSaving, setNoteSaving] = useState(false);
  const [sortConfig, setSortConfig] = useState<SortConfig>({ key: 'holding_days', direction: 'asc' });
  const [closedSortConfig, setClosedSortConfig] = useState<ClosedSortConfig>({ key: 'closed_at', direction: 'desc' });
  const [viewTab, setViewTab] = useState<'open' | 'closed'>('open');

  usePageTitle('持仓管理');

  const useUnifiedCurrency = selectedType === 'all' && usdCnyRate > 0;
  const usdBasedAccountTypes: AccountType[] = ['us_stock', 'crypto'];

  const getFxRate = (accountType?: AccountType) => {
    if (!useUnifiedCurrency || !accountType) {
      return 1;
    }
    return usdBasedAccountTypes.includes(accountType) ? usdCnyRate : 1;
  };

  useEffect(() => {
    // Check URL parameter for account_type / account_id
    const typeParam = searchParams.get('account_type');
    if (typeParam && typeParam !== 'all') {
      setSelectedType(typeParam as AccountType);
    }
    const accountParam = searchParams.get('account_id');
    if (accountParam && accountParam !== 'all') {
      setSelectedAccountId(accountParam);
    }
  }, [searchParams]);

  useEffect(() => {
    loadPositions();
  }, [selectedType, selectedAccountId]);

  useEffect(() => {
    loadFxSettings();
  }, []);

  useEffect(() => {
    if (selectedAccountId === 'all') {
      return;
    }
    const selectedAccount = accounts.find((account) => account.id === selectedAccountId);
    if (!selectedAccount) {
      setSelectedAccountId('all');
      return;
    }
    if (selectedType !== 'all' && selectedAccount.account_type !== selectedType) {
      setSelectedAccountId('all');
    }
  }, [accounts, selectedAccountId, selectedType]);

  useEffect(() => {
    // Recalculate stats whenever positions change
    loadStats();
  }, [positions, usdCnyRate, selectedType, accountTypeMap]);

  const loadFxSettings = async () => {
    try {
      const settings = await apiClient.getStrategySettings();
      const rateValue = Number(settings.currency_settings?.usd_cny_rate ?? 0);
      setUsdCnyRate(Number.isFinite(rateValue) ? rateValue : 0);
    } catch (err) {
      setUsdCnyRate(0);
    }
  };

  const loadPositions = async () => {
    try {
      setLoading(true);

      // Get all accounts to build account type mapping
      const allAccounts = await accountsApi.getAccounts();
      setAccounts(allAccounts);
      const typeMap: Record<string, AccountType> = {};
      allAccounts.forEach(acc => {
        typeMap[acc.id] = acc.account_type;
      });
      setAccountTypeMap(typeMap);

      await loadTradeStats(allAccounts);

      // Get all positions
      const accountParam = selectedAccountId !== 'all' ? selectedAccountId : undefined;
      const accountTypeParam = selectedType !== 'all' ? selectedType : undefined;
      const response = await apiClient.getPositions({
        page_size: 100,
        account_id: accountParam,
        account_type: accountTypeParam
      });
      setAllPositions(response.positions);

      // Filter by account type if selected
      const filteredPositions = response.positions.filter((pos) => {
        const matchType = selectedType === 'all' || typeMap[pos.account_id] === selectedType;
        const matchAccount = selectedAccountId === 'all' || pos.account_id === selectedAccountId;
        return matchType && matchAccount;
      });
      setPositions(filteredPositions);

      await loadClosedPositions(typeMap);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || '加载持仓失败');
    } finally {
      setLoading(false);
    }
  };

  const fetchAllClosedPositions = async (accountParam?: string, accountTypeParam?: AccountType) => {
    const pageSize = 200;
    const firstPage = await apiClient.getPositions({
      page_size: pageSize,
      page: 1,
      is_closed: true,
      account_id: accountParam,
      account_type: accountTypeParam
    });
    const totalPages = firstPage.total_pages || 1;
    if (totalPages <= 1) {
      return firstPage.positions;
    }

    const requests = [];
    for (let page = 2; page <= totalPages; page += 1) {
      requests.push(apiClient.getPositions({
        page_size: pageSize,
        page,
        is_closed: true,
        account_id: accountParam,
        account_type: accountTypeParam
      }));
    }

    const rest = await Promise.all(requests);
    const extra = rest.flatMap((response) => response.positions);
    return [...firstPage.positions, ...extra];
  };

  const loadTradeStats = async (accountsList?: TradeAccount[]) => {
    try {
      const list = accountsList || accounts;
      if (selectedAccountId !== 'all') {
        const statsResponse = await apiClient.getTradeStats({ account_id: selectedAccountId });
        setTradeStats({
          totalFees: Number(statsResponse.total_fees ?? 0),
          totalVolume: Number(statsResponse.total_volume ?? 0),
        });
        return;
      }

      if (selectedType === 'all') {
        const statsResponse = await apiClient.getTradeStats();
        setTradeStats({
          totalFees: Number(statsResponse.total_fees ?? 0),
          totalVolume: Number(statsResponse.total_volume ?? 0),
        });
        return;
      }

      const filteredAccounts = list.filter((account) => account.account_type === selectedType);
      if (filteredAccounts.length === 0) {
        setTradeStats({ totalFees: 0, totalVolume: 0 });
        return;
      }

      const statsList = await Promise.all(
        filteredAccounts.map(async (account) => {
          try {
            return await apiClient.getTradeStats({ account_id: account.id });
          } catch (err) {
            console.error('加载交易统计失败:', err);
            return null;
          }
        })
      );

      const totalFees = statsList.reduce((sum, stat) => {
        if (!stat) return sum;
        return sum + Number(stat.total_fees ?? 0);
      }, 0);
      const totalVolume = statsList.reduce((sum, stat) => {
        if (!stat) return sum;
        return sum + Number(stat.total_volume ?? 0);
      }, 0);

      setTradeStats({ totalFees, totalVolume });
    } catch (err) {
      console.error('加载交易统计失败:', err);
      setTradeStats({ totalFees: 0, totalVolume: 0 });
    }
  };

  const loadClosedPositions = async (typeMapOverride?: Record<string, AccountType>) => {
    try {
      const accountParam = selectedAccountId !== 'all' ? selectedAccountId : undefined;
      const accountTypeParam = selectedType !== 'all' ? selectedType : undefined;
      const allClosed = await fetchAllClosedPositions(accountParam, accountTypeParam);
      setAllClosedPositions(allClosed);
      const typeMap = typeMapOverride || accountTypeMap;

      const filteredPositions = allClosed.filter((pos) => {
        const matchType = selectedType === 'all' || typeMap[pos.account_id] === selectedType;
        const matchAccount = selectedAccountId === 'all' || pos.account_id === selectedAccountId;
        return matchType && matchAccount;
      });
      setClosedPositions(filteredPositions);
    } catch (error) {
      console.error('加载已清仓持仓失败:', error);
    }
  };

  const loadStats = async () => {
    try {
      // Calculate stats from filtered positions
      const positionsToCalculate = positions.length > 0 ? positions : [];

      if (positionsToCalculate.length === 0) {
        setStats({
          total_positions: 0,
          total_cost: '0',
          total_market_value: '0',
          total_realized_pnl: '0',
          total_unrealized_pnl: '0',
          total_unrealized_pnl_percent: '0',
          profitable_positions: 0,
          losing_positions: 0,
          average_holding_days: 0
        });
        return;
      }

      const getCostPrice = (position: Position) => (
        position.position_type === 'futures'
          ? parseFloat(position.entry_price || '0')
          : parseFloat(position.average_cost || '0')
      );

      let totalCost = 0;
      let totalMarketValue = 0;
      let totalUnrealizedPnl = 0;

      positionsToCalculate.forEach((position) => {
        const accountType = accountTypeMap[position.account_id];
        const fxRate = getFxRate(accountType);
        const quantity = parseFloat(position.quantity);
        const quantityAbs = Math.abs(quantity);
        const costPrice = getCostPrice(position);
        const costValue = quantityAbs * costPrice;
        totalCost += costValue * fxRate;

        const price = position.current_price ? parseFloat(position.current_price) : costPrice;
        const marketValue = quantity * price;
        totalMarketValue += marketValue * fxRate;

        if (position.unrealized_pnl !== undefined && position.unrealized_pnl !== null) {
          totalUnrealizedPnl += parseFloat(position.unrealized_pnl) * fxRate;
          return;
        }

        if (!position.current_price) {
          return;
        }

        totalUnrealizedPnl += (marketValue - costValue) * fxRate;
      });
      const totalUnrealizedPnlPercent = totalCost > 0 ? (totalUnrealizedPnl / totalCost * 100) : 0;

      const profitablePositions = positionsToCalculate.filter(p =>
        p.unrealized_pnl && parseFloat(p.unrealized_pnl) > 0
      ).length;

      const losingPositions = positionsToCalculate.filter(p =>
        p.unrealized_pnl && parseFloat(p.unrealized_pnl) < 0
      ).length;

      const holdingDaysList = positionsToCalculate
        .map(p => p.holding_days)
        .filter(d => d !== undefined && d !== null) as number[];

      const averageHoldingDays = holdingDaysList.length > 0
        ? Math.floor(holdingDaysList.reduce((sum, d) => sum + d, 0) / holdingDaysList.length)
        : 0;

      setStats({
        total_positions: positionsToCalculate.length,
        total_cost: totalCost.toFixed(2),
        total_market_value: totalMarketValue.toFixed(2),
        total_realized_pnl: '0',
        total_unrealized_pnl: totalUnrealizedPnl.toFixed(2),
        total_unrealized_pnl_percent: totalUnrealizedPnlPercent.toFixed(2),
        profitable_positions: profitablePositions,
        losing_positions: losingPositions,
        average_holding_days: averageHoldingDays
      });
    } catch (err) {
      console.error('Failed to calculate stats:', err);
    }
  };

  const handleRefreshPrices = async () => {
    if (viewTab === 'closed') {
      toast({
        title: '已清仓列表不刷新价格',
        description: '请切换到“持仓中”后再刷新当前持仓价格',
      });
      return;
    }

    const visiblePositions = positions;
    if (visiblePositions.length === 0) {
      toast({
        title: '暂无可刷新的持仓',
        description: '当前列表没有需要刷新的标的',
      });
      return;
    }

    try {
      setRefreshing(true);
      const result = await apiClient.refreshPositionPricesSelection(
        visiblePositions.map((position) => position.id)
      );

      toast({
        title: '价格刷新成功',
        description: `已更新 ${result.updated_count} 个持仓的价格`,
      });

      await loadPositions();
    } catch (err: any) {
      const message = err?.message || err.response?.data?.detail || '刷新价格时出错';
      console.error('Error refreshing prices:', err);
      toast({
        title: '价格刷新失败',
        description: message,
        variant: 'destructive',
      });
    } finally {
      setRefreshing(false);
    }
  };

  // 获取市场对应的货币符号
  const getCurrencySymbol = (accountType?: AccountType | 'all') => {
    if (!accountType || accountType === 'all') return useUnifiedCurrency ? '¥' : '$';

    const currencyMap: Record<AccountType, string> = {
      'us_stock': '$',
      'crypto': '$',
      'a_stock': '¥',
      'hk_stock': 'HK$'
    };
    return currencyMap[accountType] || '$';
  };

  const formatNumber = (value: string | number | undefined, decimals = 2) => {
    if (value === undefined || value === null) return decimals === 0 ? '0' : '0.00';
    const parsed = Number(value);
    if (Number.isNaN(parsed)) return decimals === 0 ? '0' : '0.00';
    return parsed.toLocaleString('en-US', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals,
    });
  };

  const formatQuantity = (value: string | number | undefined, accountType?: AccountType) => {
    if (value === undefined || value === null) return '0';
    return formatQuantityValue(value, { accountType, fallbackFractionDigits: 8 });
  };

  const formatCurrency = (value: string | number | undefined, accountType?: AccountType | 'all', decimals = 2) => {
    if (accountType === 'a_stock') {
      return formatMoney(value ?? 0, { accountType: 'a_stock', fallbackFractionDigits: decimals });
    }
    if (value === undefined || value === null) return `${getCurrencySymbol(accountType)}0.00`;
    const symbol = getCurrencySymbol(accountType);
    return `${symbol}${formatNumber(value, decimals)}`;
  };

  const formatPercent = (value: string | number | undefined) => {
    if (value === undefined || value === null) return '0.00%';
    const num = parseFloat(value.toString());
    const color = num >= 0 ? 'text-green-600' : 'text-red-600';
    const sign = num >= 0 ? '+' : '';
    return <span className={color}>{sign}{num.toFixed(2)}%</span>;
  };

  const formatPnL = (value: string | number | undefined, accountType?: AccountType | 'all') => {
    if (value === undefined || value === null) return `${getCurrencySymbol(accountType)}0.00`;
    const num = parseFloat(value.toString());
    const color = num >= 0 ? 'text-green-600' : 'text-red-600';
    const sign = num >= 0 ? '+' : '-';
    if (accountType && accountType !== 'all') {
      return (
        <span className={color}>
          {sign}
          {formatMoney(Math.abs(num), { accountType, fallbackFractionDigits: 2 })}
        </span>
      );
    }
    const symbol = getCurrencySymbol(accountType);
    return <span className={color}>{sign}{symbol}{formatNumber(Math.abs(num), 2)}</span>;
  };

  const formatDateTime = (value: string | undefined) => {
    if (!value) return '-';
    return new Date(value).toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleSort = (key: SortKey) => {
    setSortConfig((prevConfig) => {
      if (prevConfig.key === key) {
        return {
          key,
          direction: prevConfig.direction === 'asc' ? 'desc' : 'asc'
        };
      }
      return { key, direction: 'asc' };
    });
  };

  const handleClosedSort = (key: ClosedSortKey) => {
    setClosedSortConfig((prevConfig) => {
      if (prevConfig.key === key) {
        return {
          key,
          direction: prevConfig.direction === 'asc' ? 'desc' : 'asc'
        };
      }
      return { key, direction: 'asc' };
    });
  };

  const getCostPrice = (position: Position) => (
    position.position_type === 'futures'
      ? parseFloat(position.entry_price || '0')
      : parseFloat(position.average_cost || '0')
  );

  const getHoldingDays = (position: Position) => {
    if (position.holding_days !== undefined && position.holding_days !== null) {
      return position.holding_days;
    }
    if (position.first_buy_time && position.closed_at) {
      const startTime = new Date(position.first_buy_time).getTime();
      const endTime = new Date(position.closed_at).getTime();
      const diffDays = Math.floor((endTime - startTime) / (1000 * 60 * 60 * 24));
      return diffDays >= 0 ? diffDays : 0;
    }
    return null;
  };

  const calculateClosedStats = (closed: Position[]) => {
    if (closed.length === 0) {
      return {
        total_positions: 0,
        total_cost: 0,
        total_market_value: 0,
        total_unrealized_pnl: 0,
        total_unrealized_pnl_percent: 0,
        profitable_positions: 0,
        losing_positions: 0,
        average_holding_days: 0,
        win_rate: 0
      };
    }

    let totalCost = 0;
    let totalProceeds = 0;
    let totalRealizedPnl = 0;
    let profitablePositions = 0;
    let losingPositions = 0;

    const holdingDaysList = closed
      .map(position => getHoldingDays(position))
      .filter((value): value is number => value !== null);

    closed.forEach((position) => {
      const accountType = accountTypeMap[position.account_id];
      const fxRate = getFxRate(accountType);
      const quantity = Math.abs(parseFloat(position.quantity || '0'));
      const costPrice = getCostPrice(position);
      const costValue = quantity * costPrice;
      totalCost += costValue * fxRate;

      let realizedPnl = 0;
      if (position.realized_pnl !== undefined && position.realized_pnl !== null) {
        realizedPnl = parseFloat(position.realized_pnl);
      } else if (position.final_price !== undefined && position.final_price !== null) {
        const finalPrice = parseFloat(position.final_price);
        realizedPnl = (finalPrice - costPrice) * quantity;
      }

      totalRealizedPnl += realizedPnl * fxRate;
      if (realizedPnl > 0) {
        profitablePositions += 1;
      } else if (realizedPnl < 0) {
        losingPositions += 1;
      }

      if (position.final_price !== undefined && position.final_price !== null) {
        totalProceeds += parseFloat(position.final_price) * quantity * fxRate;
      } else {
        totalProceeds += costValue * fxRate;
      }
    });

    const totalRealizedPnlPercent = totalCost > 0 ? (totalRealizedPnl / totalCost * 100) : 0;
    const averageHoldingDays = holdingDaysList.length > 0
      ? Math.floor(holdingDaysList.reduce((sum, value) => sum + value, 0) / holdingDaysList.length)
      : 0;

    const winRate = (profitablePositions + losingPositions) > 0
      ? (profitablePositions / (profitablePositions + losingPositions)) * 100
      : 0;

    return {
      total_positions: closed.length,
      total_cost: totalCost,
      total_market_value: totalProceeds,
      total_unrealized_pnl: totalRealizedPnl,
      total_unrealized_pnl_percent: totalRealizedPnlPercent,
      profitable_positions: profitablePositions,
      losing_positions: losingPositions,
      average_holding_days: averageHoldingDays,
      win_rate: winRate
    };
  };

  const getSortValue = (position: Position, key: SortKey): number | string | null => {
    switch (key) {
      case 'symbol':
        return position.symbol || '';
      case 'quantity':
        return Math.abs(parseFloat(position.quantity || '0'));
      case 'cost':
        return getCostPrice(position);
      case 'current_price':
        return position.current_price !== undefined && position.current_price !== null
          ? parseFloat(position.current_price)
          : null;
      case 'value':
        if (position.position_type === 'futures') {
          return position.leverage !== undefined && position.leverage !== null
            ? parseFloat(position.leverage)
            : null;
        }
        if (position.market_value !== undefined && position.market_value !== null) {
          return parseFloat(position.market_value);
        }
        if (position.current_price !== undefined && position.current_price !== null) {
          return parseFloat(position.quantity) * parseFloat(position.current_price);
        }
        return null;
      case 'pnl':
        return position.unrealized_pnl !== undefined && position.unrealized_pnl !== null
          ? parseFloat(position.unrealized_pnl)
          : null;
      case 'pnl_percent':
        if (position.position_type === 'futures' && position.roe_percent !== undefined && position.roe_percent !== null) {
          return parseFloat(position.roe_percent);
        }
        return position.unrealized_pnl_percent !== undefined && position.unrealized_pnl_percent !== null
          ? parseFloat(position.unrealized_pnl_percent)
          : null;
      case 'holding_days':
        return getHoldingDays(position);
      default:
        return null;
    }
  };

  const sortedPositions = useMemo(() => {
    const sorted = [...positions].sort((a, b) => {
      const valueA = getSortValue(a, sortConfig.key);
      const valueB = getSortValue(b, sortConfig.key);

      if (valueA === null && valueB === null) return 0;
      if (valueA === null) return 1;
      if (valueB === null) return -1;

      if (typeof valueA === 'string' && typeof valueB === 'string') {
        return valueA.localeCompare(valueB, 'zh-CN', { numeric: true, sensitivity: 'base' });
      }

      return (valueA as number) - (valueB as number);
    });
    return sortConfig.direction === 'asc' ? sorted : sorted.reverse();
  }, [positions, sortConfig]);

  const getClosedSortValue = (position: Position, key: ClosedSortKey): number | string | null => {
    switch (key) {
      case 'symbol':
        return position.symbol || '';
      case 'quantity':
        return Math.abs(parseFloat(position.quantity || '0'));
      case 'cost':
        return getCostPrice(position);
      case 'open_value': {
        const quantity = Math.abs(parseFloat(position.quantity || '0'));
        const costPrice = getCostPrice(position);
        return quantity * costPrice;
      }
      case 'final_price':
        return position.final_price !== undefined && position.final_price !== null
          ? parseFloat(position.final_price)
          : null;
      case 'holding_days':
        return position.holding_days ?? null;
      case 'realized_pnl':
        return position.realized_pnl !== undefined && position.realized_pnl !== null
          ? parseFloat(position.realized_pnl)
          : null;
      case 'realized_pnl_percent':
        return position.realized_pnl_percent !== undefined && position.realized_pnl_percent !== null
          ? parseFloat(position.realized_pnl_percent)
          : null;
      case 'first_buy_time':
        return position.first_buy_time ? new Date(position.first_buy_time).getTime() : null;
      case 'closed_at':
        return position.closed_at ? new Date(position.closed_at).getTime() : null;
      default:
        return null;
    }
  };

  const sortedClosedPositions = useMemo(() => {
    const sorted = [...closedPositions].sort((a, b) => {
      const valueA = getClosedSortValue(a, closedSortConfig.key);
      const valueB = getClosedSortValue(b, closedSortConfig.key);

      if (valueA === null && valueB === null) return 0;
      if (valueA === null) return 1;
      if (valueB === null) return -1;

      if (typeof valueA === 'string' && typeof valueB === 'string') {
        return valueA.localeCompare(valueB, 'zh-CN', { numeric: true, sensitivity: 'base' });
      }

      return (valueA as number) - (valueB as number);
    });
    return closedSortConfig.direction === 'asc' ? sorted : sorted.reverse();
  }, [closedPositions, closedSortConfig]);

  const closedStats = useMemo(
    () => calculateClosedStats(closedPositions),
    [closedPositions, usdCnyRate, selectedType, accountTypeMap]
  );
  const statsToDisplay = viewTab === 'closed' ? closedStats : stats;
  const allActivePositions = viewTab === 'closed' ? allClosedPositions : allPositions;

  const selectedAccount = useMemo(() => {
    if (selectedAccountId === 'all') return null;
    return accounts.find((account) => account.id === selectedAccountId) || null;
  }, [accounts, selectedAccountId]);

  const getSymbolPrimarySecondary = (position: Position, accountType?: AccountType) => {
    const hasName = Boolean(position.symbol_name);
    const isAStock = accountType === 'a_stock';
    if (isAStock && hasName) {
      return { primary: position.symbol_name as string, secondary: position.symbol };
    }
    return { primary: position.symbol, secondary: position.symbol_name || '' };
  };

  const renderSortIcon = (key: SortKey) => {
    if (sortConfig.key !== key) {
      return <ArrowUpDown className="ml-1 h-3 w-3 text-gray-400" />;
    }
    return sortConfig.direction === 'asc'
      ? <ArrowUp className="ml-1 h-3 w-3 text-gray-700" />
      : <ArrowDown className="ml-1 h-3 w-3 text-gray-700" />;
  };

  const renderClosedSortIcon = (key: ClosedSortKey) => {
    if (closedSortConfig.key !== key) {
      return <ArrowUpDown className="ml-1 h-3 w-3 text-gray-400" />;
    }
    return closedSortConfig.direction === 'asc'
      ? <ArrowUp className="ml-1 h-3 w-3 text-gray-700" />
      : <ArrowDown className="ml-1 h-3 w-3 text-gray-700" />;
  };

  const toNumber = (value: string | number | undefined | null) => Number(value ?? 0);
  const openNoteDialog = (position: Position) => {
    setNotePosition(position);
    setNoteDraft(position.notes ?? '');
    setNoteDialogOpen(true);
  };

  const closeNoteDialog = () => {
    setNoteDialogOpen(false);
    setNotePosition(null);
    setNoteDraft('');
  };

  const updateNoteInList = (list: Position[], positionId: string, notes: string | undefined | null) => (
    list.map((item) => item.id === positionId ? { ...item, notes: notes ?? undefined } : item)
  );

  const handleSaveNote = async () => {
    if (!notePosition) return;
    try {
      setNoteSaving(true);
      const trimmed = noteDraft.trim();
      const updated = await apiClient.updatePositionNotes(notePosition.id, trimmed ? trimmed : null);
      setPositions((prev) => updateNoteInList(prev, updated.id, updated.notes));
      setAllPositions((prev) => updateNoteInList(prev, updated.id, updated.notes));
      setClosedPositions((prev) => updateNoteInList(prev, updated.id, updated.notes));
      setAllClosedPositions((prev) => updateNoteInList(prev, updated.id, updated.notes));
      toast({ title: '备注已保存' });
      closeNoteDialog();
    } catch (error: any) {
      toast({
        title: '备注保存失败',
        description: error.response?.data?.detail || '请稍后重试',
        variant: 'destructive'
      });
    } finally {
      setNoteSaving(false);
    }
  };

  const getPnlValueClass = (value?: number | null) => {
    if (value === null || value === undefined) return 'text-gray-900';
    if (value > 0) return 'text-green-600';
    if (value < 0) return 'text-red-600';
    return 'text-gray-900';
  };
  const statsNumeric = statsToDisplay ? {
    totalCost: toNumber(statsToDisplay.total_cost),
    totalMarketValue: toNumber(statsToDisplay.total_market_value),
    totalPnl: toNumber(statsToDisplay.total_unrealized_pnl),
    totalPnlPercent: toNumber(statsToDisplay.total_unrealized_pnl_percent)
  } : null;
  const pnlValueClass = getPnlValueClass(statsNumeric?.totalPnl);

  const accountsForCapital =
    selectedAccountId !== 'all'
      ? accounts.filter((account) => account.id === selectedAccountId)
      : selectedType === 'all'
        ? accounts
        : accounts.filter((account) => account.account_type === selectedType);

  const cashBalance = accountsForCapital.reduce((sum, account) => {
    const parsed = Number(account.cash_balance ?? 0);
    if (!Number.isFinite(parsed)) {
      return sum;
    }
    return sum + parsed * getFxRate(account.account_type);
  }, 0);

  const securitiesCapital = viewTab === 'closed' ? 0 : (statsNumeric?.totalMarketValue || 0);
  const totalCapital = securitiesCapital + cashBalance;
  const positionRatio = totalCapital > 0 ? securitiesCapital / totalCapital : 0;

  if (loading && positions.length === 0) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center h-64">
          <div className="text-gray-500">加载中...</div>
        </div>
      </div>
    );
  }

  return (
    <>
      <PageNav />
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50">
        <div className="container mx-auto px-4 py-8">
          {/* 页面标题 */}
          <div className="mb-8">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="p-3 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl shadow-lg">
                  <TrendingUp className="w-8 h-8 text-white" />
                </div>
                <div>
                  <h1 className="text-4xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
                    持仓管理
                  </h1>
                  <p className="mt-1 text-gray-600">查看您的当前持仓和盈亏情况</p>
                </div>
              </div>
              <Button
                onClick={handleRefreshPrices}
                disabled={refreshing}
                className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 shadow-md"
              >
                <RefreshCw className={`w-4 h-4 mr-2 ${refreshing ? 'animate-spin' : ''}`} />
                {refreshing ? '刷新中...' : '刷新价格'}
              </Button>
            </div>
          </div>

          {/* 错误提示 */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg shadow-sm">
              <p className="text-red-800 font-medium">{error}</p>
            </div>
          )}

          {/* 统计导航栏 */}
          {statsToDisplay && (
            <StatsNav
              variant="compact"
              stats={viewTab === 'closed'
                ? [
                    {
                      label: '已清仓数量',
                      value: statsToDisplay.total_positions,
                      icon: 'activity',
                      trend: 'neutral'
                    },
                    {
                      label: '总成本',
                      value: formatCurrency(statsNumeric?.totalCost || 0, selectedType, 2),
                      icon: 'dollar',
                      trend: 'neutral'
                    },
                    {
                      label: '回收金额',
                      value: formatCurrency(statsNumeric?.totalMarketValue || 0, selectedType, 2),
                      icon: 'dollar',
                      trend: (statsNumeric?.totalMarketValue || 0) >= (statsNumeric?.totalCost || 0) ? 'up' : 'down'
                    },
                    {
                      label: '已实现盈亏',
                      value: formatCurrency(statsNumeric?.totalPnl || 0, selectedType, 2),
                      valueClassName: pnlValueClass,
                      change: statsNumeric?.totalPnlPercent || 0,
                      icon: 'trending-up',
                      trend: (statsNumeric?.totalPnl || 0) >= 0 ? 'up' : 'down'
                    },
                    {
                      label: '胜率',
                      value: `${(statsToDisplay.win_rate || 0).toFixed(2)}%`,
                      icon: 'percent',
                      trend: 'neutral'
                    },
                    {
                      label: '交易费用',
                      value: formatCurrency(tradeStats?.totalFees || 0, selectedType, 2),
                      icon: 'dollar',
                      trend: 'neutral'
                    },
                    {
                      label: '总交易量',
                      value: formatCurrency(tradeStats?.totalVolume || 0, selectedType, 2),
                      icon: 'dollar',
                      trend: 'neutral'
                    }
                  ]
                : [
                    {
                      label: '总持仓数',
                      value: statsToDisplay.total_positions,
                      icon: 'activity',
                      trend: 'neutral'
                    },
                    {
                      label: '总成本',
                      value: formatCurrency(statsNumeric?.totalCost || 0, selectedType, 2),
                      icon: 'dollar',
                      trend: 'neutral'
                    },
                    {
                      label: '证券资本',
                      value: formatCurrency(securitiesCapital, selectedType, 2),
                      icon: 'dollar',
                      trend: (statsNumeric?.totalMarketValue || 0) >= (statsNumeric?.totalCost || 0) ? 'up' : 'down'
                    },
                    {
                      label: '剩余资金',
                      value: formatCurrency(cashBalance, selectedType, 2),
                      icon: 'dollar',
                      trend: 'neutral'
                    },
                    {
                      label: '总资本',
                      value: formatCurrency(totalCapital, selectedType, 2),
                      icon: 'dollar',
                      trend: 'neutral'
                    },
                    {
                      label: '仓位',
                      value: `${(positionRatio * 100).toFixed(2)}%`,
                      icon: 'percent',
                      trend: 'neutral'
                    },
                    {
                      label: '未实现盈亏',
                      value: formatCurrency(statsNumeric?.totalPnl || 0, selectedType, 2),
                      valueClassName: pnlValueClass,
                      change: statsNumeric?.totalPnlPercent || 0,
                      icon: 'trending-up',
                      trend: (statsNumeric?.totalPnl || 0) >= 0 ? 'up' : 'down'
                    },
                    {
                      label: '交易费用',
                      value: formatCurrency(tradeStats?.totalFees || 0, selectedType, 2),
                      icon: 'dollar',
                      trend: 'neutral'
                    }
                  ]}
            />
          )}

          {/* 市场类型筛选 */}
          <div className="flex gap-3 mb-6 flex-wrap">
            <Button
              variant={selectedType === 'all' ? 'default' : 'outline'}
              onClick={() => setSelectedType('all')}
              size="sm"
              className={selectedType === 'all' ? 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 shadow-md' : 'hover:shadow-md transition-shadow'}
            >
              全部 ({allActivePositions.length})
            </Button>
            {(Object.keys(ACCOUNT_TYPE_LABELS) as AccountType[]).map((type) => {
              const count = allActivePositions.filter(pos =>
                accountTypeMap[pos.account_id] === type
              ).length;
              return (
                <Button
                  key={type}
                  variant={selectedType === type ? 'default' : 'outline'}
                  onClick={() => setSelectedType(type)}
                  size="sm"
                  className={selectedType === type ? 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 shadow-md' : 'hover:shadow-md transition-shadow'}
                >
                  {ACCOUNT_TYPE_LABELS[type]} ({count})
                </Button>
              );
            })}
          </div>

          {/* 交易账户筛选 */}
          <div className="flex items-center gap-2 mb-8 flex-wrap">
            <span className="text-sm font-medium text-gray-700">交易账户:</span>
            <select
              value={selectedAccountId}
              onChange={(e) => setSelectedAccountId(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">全部账户</option>
              {selectedType === 'all'
                ? (Object.keys(ACCOUNT_TYPE_LABELS) as AccountType[]).map((type) => {
                    const typeAccounts = accounts.filter((account) => account.account_type === type);
                    if (typeAccounts.length === 0) return null;
                    return (
                      <optgroup key={type} label={ACCOUNT_TYPE_LABELS[type]}>
                        {typeAccounts.map((account) => (
                          <option key={account.id} value={account.id}>
                            {account.account_name}
                          </option>
                        ))}
                      </optgroup>
                    );
                  })
                : accounts
                    .filter((account) => account.account_type === selectedType)
                    .map((account) => (
                      <option key={account.id} value={account.id}>
                        {account.account_name}
                      </option>
                    ))}
            </select>
            {selectedAccountId !== 'all' && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => (window.location.href = `/accounts/${selectedAccountId}`)}
                className="hover:shadow-md transition-shadow"
              >
                进入账户详情
              </Button>
            )}
          </div>

          {/* 持仓列表 */}
          <div className="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
            <div className="px-6 py-5 bg-gradient-to-r from-gray-50 to-gray-100 border-b border-gray-200 flex items-center justify-between">
              <h2 className="text-xl font-bold text-gray-800 flex items-center">
                <div className="w-1 h-6 bg-gradient-to-b from-blue-500 to-indigo-600 rounded-full mr-3"></div>
                持仓明细
              </h2>
              <div className="flex items-center gap-2">
                <Button
                  variant={viewTab === 'open' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setViewTab('open')}
                  className={viewTab === 'open' ? 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 shadow-md' : 'hover:shadow-md transition-shadow'}
                >
                  持仓中 ({positions.length})
                </Button>
                <Button
                  variant={viewTab === 'closed' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setViewTab('closed')}
                  className={viewTab === 'closed' ? 'bg-gradient-to-r from-gray-600 to-gray-700 hover:from-gray-700 hover:to-gray-800 shadow-md' : 'hover:shadow-md transition-shadow'}
                >
                  已清仓 ({closedPositions.length})
                </Button>
              </div>
            </div>

            <div className="overflow-x-auto">
              {viewTab === 'open' ? (
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gradient-to-r from-gray-100 to-gray-50">
                    <tr>
                      <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider whitespace-nowrap">
                        <button
                          type="button"
                          onClick={() => handleSort('symbol')}
                          className="inline-flex items-center hover:text-gray-900"
                        >
                          标的/方向
                          {renderSortIcon('symbol')}
                        </button>
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider whitespace-nowrap">
                        <button
                          type="button"
                          onClick={() => handleSort('quantity')}
                          className="inline-flex items-center hover:text-gray-900"
                        >
                          数量
                          {renderSortIcon('quantity')}
                        </button>
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider whitespace-nowrap">
                        <button
                          type="button"
                          onClick={() => handleSort('cost')}
                          className="inline-flex items-center hover:text-gray-900"
                        >
                          成本价/开仓价
                          {renderSortIcon('cost')}
                        </button>
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider whitespace-nowrap">
                        <button
                          type="button"
                          onClick={() => handleSort('current_price')}
                          className="inline-flex items-center hover:text-gray-900"
                        >
                          当前价格
                          {renderSortIcon('current_price')}
                        </button>
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider whitespace-nowrap">
                        <button
                          type="button"
                          onClick={() => handleSort('value')}
                          className="inline-flex items-center hover:text-gray-900"
                        >
                          杠杆/市值
                          {renderSortIcon('value')}
                        </button>
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider whitespace-nowrap">
                        <button
                          type="button"
                          onClick={() => handleSort('pnl')}
                          className="inline-flex items-center hover:text-gray-900"
                        >
                          盈亏
                          {renderSortIcon('pnl')}
                        </button>
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider whitespace-nowrap">
                        <button
                          type="button"
                          onClick={() => handleSort('pnl_percent')}
                          className="inline-flex items-center hover:text-gray-900"
                        >
                          盈亏率/ROE
                          {renderSortIcon('pnl_percent')}
                        </button>
                      </th>
                      <th className="px-6 py-4 text-center text-xs font-bold text-gray-700 uppercase tracking-wider whitespace-nowrap">
                        <button
                          type="button"
                          onClick={() => handleSort('holding_days')}
                          className="inline-flex items-center hover:text-gray-900"
                        >
                          持仓天数
                          {renderSortIcon('holding_days')}
                        </button>
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider whitespace-nowrap">备注</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-100">
                    {sortedPositions.length === 0 ? (
                      <tr>
                        <td colSpan={9} className="px-6 py-16 text-center">
                          <div className="flex flex-col items-center">
                            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                              <TrendingUp className="w-8 h-8 text-gray-400" />
                            </div>
                            <p className="text-gray-500 font-medium">暂无持仓</p>
                          </div>
                        </td>
                      </tr>
                    ) : (
	                      sortedPositions.map((position) => {
	                        const posAccountType = accountTypeMap[position.account_id];
	                        const currencyType = selectedType === 'all' ? posAccountType : selectedType;
	                        const { primary, secondary } = getSymbolPrimarySecondary(position, posAccountType);

	                        return (
	                          <tr
	                            key={position.id}
	                            className="hover:bg-gradient-to-r hover:from-blue-50 hover:to-indigo-50 transition-all duration-200 cursor-pointer"
	                            onClick={() => window.location.href = `/symbols/${encodeURIComponent(position.symbol)}?account_id=${position.account_id}`}
	                          >
	                            <td className="px-6 py-4 whitespace-nowrap">
	                              <div className="flex items-center">
	                                {/* Professional Logo Style Avatar */}
	                                <div className="relative mr-3">
                                  {/* Outer shadow ring */}
                                  <div className="absolute inset-0 rounded-full bg-gradient-to-br from-gray-200 to-gray-300 blur-sm opacity-50"></div>

                                  {/* Main avatar circle */}
                                  <div className={`relative w-11 h-11 bg-gradient-to-br ${
                                    position.position_type === 'futures'
                                      ? (position.position_side === 'LONG'
                                          ? 'from-emerald-400 via-green-500 to-emerald-600'
                                          : 'from-rose-400 via-red-500 to-rose-600')
                                      : 'from-blue-400 via-indigo-500 to-blue-600'
                                  } rounded-full flex items-center justify-center shadow-lg border-2 border-white`}>
                                    {/* Inner glow effect */}
                                    <div className="absolute inset-0 rounded-full bg-gradient-to-t from-white/0 to-white/20"></div>

                                    {/* Symbol text */}
                                    <span className="relative text-white font-extrabold text-xs tracking-tight drop-shadow-sm">
                                      {position.symbol.length <= 4
                                        ? position.symbol
                                        : position.symbol.substring(0, position.symbol.length <= 6 ? 3 : 2)}
                                    </span>
                                  </div>

                                  {/* Bottom highlight */}
                                  <div className={`absolute -bottom-0.5 left-1/2 -translate-x-1/2 w-8 h-1 rounded-full ${
                                    position.position_type === 'futures'
                                      ? (position.position_side === 'LONG' ? 'bg-green-400' : 'bg-red-400')
                                      : 'bg-indigo-400'
                                  } opacity-60 blur-sm`}></div>
                                </div>

                                <div>
                                  <div className="text-sm font-bold text-gray-900">{primary}</div>
                                  {secondary && <div className="text-xs text-gray-500">{secondary}</div>}
                                  {position.position_type === 'futures' && (
                                    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium shadow-sm ${
                                      position.position_side === 'LONG'
                                        ? 'bg-gradient-to-r from-green-50 to-emerald-50 text-green-700 border border-green-200'
                                        : 'bg-gradient-to-r from-red-50 to-rose-50 text-red-700 border border-red-200'
                                    }`}>
                                      {position.position_side === 'LONG' ? '多头' : '空头'}
                                    </span>
                                  )}
	                                </div>
	                              </div>
	                            </td>

	                            {/* 数量 */}
	                            <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-medium text-gray-700">
	                              {formatQuantity(Math.abs(parseFloat(position.quantity)), posAccountType)}
                            </td>

                            {/* 成本价/开仓价 */}
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-medium text-gray-700">
                              {position.position_type === 'futures'
                                ? formatPrice(position.entry_price || '0', { accountType: currencyType, fallbackFractionDigits: 8 })
                                : formatPrice(position.average_cost || '0', { accountType: currencyType, fallbackFractionDigits: 8 })
                              }
                            </td>

                            {/* 当前价格 */}
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-medium text-gray-700">
                              {position.current_price
                                ? formatPrice(position.current_price, { accountType: currencyType, fallbackFractionDigits: 8 })
                                : '-'
                              }
                            </td>

                            {/* 杠杆/市值 */}
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-right">
                              {position.position_type === 'futures' ? (
                                <div>
                                  <div className="font-bold text-gray-900">{position.leverage || '1'}x</div>
                                  {position.margin_used && (
                                    <div className="text-xs text-gray-500">
                                      保证金: {formatCurrency(position.margin_used, currencyType, 2)}
                                    </div>
                                  )}
                                </div>
                              ) : (
                                <div className="font-bold text-gray-900">
                                  {formatCurrency(
                                    position.market_value || (parseFloat(position.quantity) * parseFloat(position.average_cost || '0')),
                                    currencyType,
                                    2
                                  )}
                                </div>
                              )}
                            </td>

                            {/* 盈亏 */}
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-bold">
                              {formatPnL(position.unrealized_pnl, currencyType)}
                            </td>

                            {/* 盈亏率/ROE */}
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-bold">
                              {position.position_type === 'futures' && position.roe_percent
                                ? formatPercent(position.roe_percent)
                                : formatPercent(position.unrealized_pnl_percent)
                              }
                            </td>

                            {/* 持仓天数 */}
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-center">
                              <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700">
                                {position.holding_days || 0} 天
                              </span>
                            </td>

                            {/* 备注 */}
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-left" onClick={(event) => event.stopPropagation()}>
                              <div className="flex items-center gap-2 max-w-[200px]">
                                <Button
                                  type="button"
                                  variant="ghost"
                                  size="icon"
                                  className="h-7 w-7"
                                  onClick={() => openNoteDialog(position)}
                                >
                                  <Pencil className="h-4 w-4" />
                                </Button>
                                <span className="text-xs text-gray-600 truncate">
                                  {position.notes ? position.notes : '添加备注'}
                                </span>
                              </div>
                            </td>
                          </tr>
                        );
                      })
                    )}
                  </tbody>
                </table>
              ) : (
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gradient-to-r from-gray-100 to-gray-50">
                    <tr>
                      <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider whitespace-nowrap">
                        <button
                          type="button"
                          onClick={() => handleClosedSort('symbol')}
                          className="inline-flex items-center hover:text-gray-900"
                        >
                          标的/方向
                          {renderClosedSortIcon('symbol')}
                        </button>
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider whitespace-nowrap">
                        <button
                          type="button"
                          onClick={() => handleClosedSort('quantity')}
                          className="inline-flex items-center hover:text-gray-900"
                        >
                          数量
                          {renderClosedSortIcon('quantity')}
                        </button>
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider whitespace-nowrap">
                        <button
                          type="button"
                          onClick={() => handleClosedSort('cost')}
                          className="inline-flex items-center hover:text-gray-900"
                        >
                          成本价/开仓价
                          {renderClosedSortIcon('cost')}
                        </button>
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider whitespace-nowrap">
                        <button
                          type="button"
                          onClick={() => handleClosedSort('open_value')}
                          className="inline-flex items-center hover:text-gray-900"
                        >
                          开仓市值
                          {renderClosedSortIcon('open_value')}
                        </button>
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider whitespace-nowrap">
                        <button
                          type="button"
                          onClick={() => handleClosedSort('final_price')}
                          className="inline-flex items-center hover:text-gray-900"
                        >
                          清仓价
                          {renderClosedSortIcon('final_price')}
                        </button>
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider whitespace-nowrap">当前价格</th>
                      <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider whitespace-nowrap">
                        <button
                          type="button"
                          onClick={() => handleClosedSort('holding_days')}
                          className="inline-flex items-center hover:text-gray-900"
                        >
                          持仓天数
                          {renderClosedSortIcon('holding_days')}
                        </button>
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider whitespace-nowrap">
                        <button
                          type="button"
                          onClick={() => handleClosedSort('realized_pnl')}
                          className="inline-flex items-center hover:text-gray-900"
                        >
                          已实现盈亏
                          {renderClosedSortIcon('realized_pnl')}
                        </button>
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider whitespace-nowrap">
                        <button
                          type="button"
                          onClick={() => handleClosedSort('realized_pnl_percent')}
                          className="inline-flex items-center hover:text-gray-900"
                        >
                          盈亏率
                          {renderClosedSortIcon('realized_pnl_percent')}
                        </button>
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider whitespace-nowrap">
                        <button
                          type="button"
                          onClick={() => handleClosedSort('first_buy_time')}
                          className="inline-flex items-center hover:text-gray-900"
                        >
                          开仓时间
                          {renderClosedSortIcon('first_buy_time')}
                        </button>
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider whitespace-nowrap">
                        <button
                          type="button"
                          onClick={() => handleClosedSort('closed_at')}
                          className="inline-flex items-center hover:text-gray-900"
                        >
                          清仓时间
                          {renderClosedSortIcon('closed_at')}
                        </button>
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider whitespace-nowrap">备注</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-100">
                    {sortedClosedPositions.length === 0 ? (
                      <tr>
                        <td colSpan={12} className="px-6 py-12 text-center text-gray-500">
                          暂无已清仓持仓
                        </td>
                      </tr>
                    ) : (
	                      sortedClosedPositions.map((position) => {
	                        const posAccountType = accountTypeMap[position.account_id];
	                        const currencyType = selectedType === 'all' ? posAccountType : selectedType;
	                        const { primary, secondary } = getSymbolPrimarySecondary(position, posAccountType);
	                        const costPrice = position.position_type === 'futures'
	                          ? (position.entry_price || '0')
	                          : (position.average_cost || '0');
	                        const holdingDays = getHoldingDays(position);

                        return (
                          <tr
	                            key={position.id}
	                            className="hover:bg-gradient-to-r hover:from-gray-50 hover:to-gray-100 transition-all duration-200 cursor-pointer"
	                            onClick={() => window.location.href = `/symbols/${encodeURIComponent(position.symbol)}?account_id=${position.account_id}`}
	                          >
	                            <td className="px-6 py-4 whitespace-nowrap">
	                              <div className="text-sm font-bold text-gray-900">{primary}</div>
	                              {secondary && <div className="text-xs text-gray-500">{secondary}</div>}
	                              {position.position_type === 'futures' && (
                                <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600 border border-gray-200 mt-1">
                                  {position.position_side === 'LONG' ? '多头' : '空头'}
                                </span>
	                              )}
	                            </td>

	                            <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-medium text-gray-700">
	                              {formatQuantity(Math.abs(parseFloat(position.quantity)), posAccountType)}
	                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-700">
                              {formatPrice(costPrice, { accountType: currencyType, fallbackFractionDigits: 8 })}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-700 font-medium">
                              {formatCurrency(
                                Math.abs(parseFloat(position.quantity)) * parseFloat(costPrice),
                                currencyType,
                                2
                              )}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-700 font-medium">
                              {position.final_price !== undefined && position.final_price !== null
                                ? formatPrice(position.final_price, { accountType: currencyType, fallbackFractionDigits: 8 })
                                : '-'
                              }
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-700 font-medium">
                              {position.current_price !== undefined && position.current_price !== null
                                ? formatPrice(position.current_price, { accountType: currencyType, fallbackFractionDigits: 8 })
                                : '-'
                              }
                            </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-600">
                            {holdingDays !== null
                              ? `${holdingDays}天`
                              : '-'
                            }
                          </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-medium">
                              {position.realized_pnl !== undefined && position.realized_pnl !== null
                                ? formatPnL(position.realized_pnl, currencyType)
                                : '-'
                              }
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-medium">
                              {position.realized_pnl_percent !== undefined && position.realized_pnl_percent !== null
                                ? formatPercent(position.realized_pnl_percent)
                                : '-'
                              }
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-600">
                              {formatDateTime(position.first_buy_time)}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-600">
                              {formatDateTime(position.closed_at)}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-xs text-left" onClick={(event) => event.stopPropagation()}>
                              <div className="flex items-center gap-2 max-w-[120px]">
                                <Button
                                  type="button"
                                  variant="ghost"
                                  size="icon"
                                  className="h-6 w-6"
                                  onClick={() => openNoteDialog(position)}
                                >
                                  <Pencil className="h-3.5 w-3.5" />
                                </Button>
                                <span className="text-[11px] text-gray-600 truncate">
                                  {position.notes ? position.notes : '添加备注'}
                                </span>
                              </div>
                            </td>
                          </tr>
                        );
                      })
                    )}
                  </tbody>
                </table>
              )}
            </div>
          </div>

    
          <Dialog open={noteDialogOpen} onOpenChange={(open) => {
            if (!open) {
              closeNoteDialog();
            }
          }}>
            <DialogContent className="max-w-lg">
              <DialogHeader>
                <DialogTitle>持仓备注</DialogTitle>
              </DialogHeader>
              <div className="space-y-3">
                <div className="text-sm text-gray-600">
                  {notePosition ? `${notePosition.symbol_name || notePosition.symbol}` : ''}
                </div>
                <Textarea
                  value={noteDraft}
                  onChange={(event) => setNoteDraft(event.target.value)}
                  placeholder="记录本次交易的成败得失..."
                  rows={6}
                />
                <div className="flex justify-end gap-2">
                  <Button type="button" variant="outline" onClick={closeNoteDialog} disabled={noteSaving}>
                    取消
                  </Button>
                  <Button type="button" onClick={handleSaveNote} disabled={noteSaving}>
                    {noteSaving ? '保存中...' : '保存'}
                  </Button>
                </div>
              </div>
            </DialogContent>
          </Dialog>

      {/* 操作提示 */}
          {viewTab === 'open' && positions.length === 0 && (
            <div className="mt-8 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-8 text-center border border-blue-100 shadow-sm">
              <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <TrendingUp className="w-10 h-10 text-white" />
              </div>
              <p className="text-gray-700 font-medium mb-4 text-lg">
                您还没有任何持仓
              </p>
              <p className="text-gray-600 mb-6">
                添加交易记录后，系统会自动计算持仓
              </p>
              <button
                onClick={() => window.location.href = '/trades'}
                className="px-8 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-medium rounded-lg hover:from-blue-700 hover:to-indigo-700 transition-all shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
              >
                前往交易记录
              </button>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
