'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Home, LogOut, Wallet } from 'lucide-react';
import { apiClient } from '@/lib/api-client';
import { DashboardSummary } from '@/types/dashboard';
import { PieChart, Pie, BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import PageNav from '@/components/layout/PageNav';
import { Button } from '@/components/ui/button';
import { formatPrice, formatQuantity } from '@/lib/format/number';
import { usePageTitle } from '@/lib/use-page-title';

const MARKET_NAMES: Record<string, string> = {
  'crypto': '加密货币',
  'us_stock': '美股',
  'a_stock': 'A股',
  'hk_stock': '港股',
};

const MARKET_COLORS: Record<string, string> = {
  'crypto': '#F59E0B',
  'us_stock': '#3B82F6',
  'a_stock': '#EF4444',
  'hk_stock': '#8B5CF6',
};

export default function Dashboard() {
  const router = useRouter();
  const [userEmail, setUserEmail] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [dashboardData, setDashboardData] = useState<DashboardSummary | null>(null);
  const [summaryCurrencySymbol, setSummaryCurrencySymbol] = useState('¥');

  usePageTitle('首页概览');

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      router.push('/');
      return;
    }

    try {
      const payload = JSON.parse(atob(token.split('.')[1])) as { email?: string; sub?: string };
      setUserEmail(payload.email || payload.sub || '用户');
    } catch (error) {
      console.error('Failed to parse token:', error);
    }

    loadDashboardData();
  }, [router]);

  const loadDashboardData = async () => {
    setIsLoading(true);
    try {
      const data = await apiClient.getDashboardSummary();
      setDashboardData(data);
      try {
        const settings = await apiClient.getStrategySettings();
        const rateValue = Number(settings.currency_settings?.usd_cny_rate ?? 0);
        setSummaryCurrencySymbol(Number.isFinite(rateValue) && rateValue > 0 ? '¥' : '$');
      } catch {
        setSummaryCurrencySymbol('$');
      }
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    router.push('/');
  };

  const formatSummaryCurrency = (value: string | number | undefined) => {
    if (!value) return `${summaryCurrencySymbol}0.00`;
    return `${summaryCurrencySymbol}${parseFloat(value.toString()).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  };

  const formatCurrency = (value: string | number | undefined) => {
    if (!value) return '$0.00';
    return `$${parseFloat(value.toString()).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  };

  const formatPercent = (value: string | number | undefined) => {
    if (!value) return '0.00%';
    const num = parseFloat(value.toString());
    const sign = num >= 0 ? '+' : '';
    return `${sign}${num.toFixed(2)}%`;
  };

  const formatDateTime = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  // Prepare chart data
  const getPieChartData = () => {
    if (!dashboardData) return [];

    return Object.entries(dashboardData.positions_summary.by_market).map(([market, metrics]) => ({
      name: MARKET_NAMES[market] || market,
      value: parseFloat(metrics.value),
      market,
    }));
  };

  const getBarChartData = () => {
    if (!dashboardData) return [];

    return Object.entries(dashboardData.positions_summary.by_market).map(([market, metrics]) => ({
      name: MARKET_NAMES[market] || market,
      市值: parseFloat(metrics.value),
      盈亏: parseFloat(metrics.pnl),
      market,
    }));
  };

  if (isLoading) {
    return (
      <>
        <PageNav />
        <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50">
          <div className="container mx-auto px-4 py-8">
            <div className="flex items-center justify-center h-64">
              <div className="text-gray-500">加载中...</div>
            </div>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <PageNav />
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50">
        <main className="container mx-auto px-4 py-8">
          <div className="mb-8">
            <div className="flex items-center justify-between flex-wrap gap-4">
              <div className="flex items-center space-x-3">
                <div className="p-3 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl shadow-lg">
                  <Home className="w-8 h-8 text-white" />
                </div>
                <div>
                  <h1 className="text-4xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
                    首页概览
                  </h1>
                  <p className="mt-1 text-gray-600">欢迎回来{userEmail ? `，${userEmail}` : ''}。您的交易数据概览</p>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  asChild
                  className="hover:shadow-md transition-shadow bg-white/80"
                >
                  <Link href="/accounts">
                    <Wallet className="w-4 h-4" />
                    账户管理
                  </Link>
                </Button>
                <Button
                  variant="outline"
                  onClick={handleLogout}
                  className="hover:shadow-md transition-shadow bg-white/80"
                >
                  <LogOut className="w-4 h-4" />
                  退出登录
                </Button>
              </div>
            </div>
          </div>

        {/* Overview Cards */}
        <div className="mb-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          <div className="rounded-2xl bg-white p-6 shadow-md border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">总资产</p>
                <p className="mt-2 text-3xl font-bold text-gray-900">
                  {formatSummaryCurrency(dashboardData?.overview.total_assets)}
                </p>
                <p className="text-sm text-gray-500">
                  证券资产 {formatSummaryCurrency(dashboardData?.overview.total_market_value)} · 剩余资金{' '}
                  {formatSummaryCurrency(dashboardData?.overview.total_cash_balance)}
                </p>
              </div>
              <div className="rounded-full bg-blue-100 p-3">
                <svg className="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
          </div>

          <div className="rounded-2xl bg-white p-6 shadow-md border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">未实现盈亏</p>
                <p className={`mt-2 text-3xl font-bold ${
                  dashboardData && parseFloat(dashboardData.overview.total_pnl) >= 0
                    ? 'text-green-600'
                    : 'text-red-600'
                }`}>
                  {formatSummaryCurrency(dashboardData?.overview.total_pnl)}
                </p>
                <p className="text-sm text-gray-500">
                  {formatPercent(dashboardData?.overview.total_pnl_percent)}
                </p>
              </div>
              <div className="rounded-full bg-green-100 p-3">
                <svg className="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
            </div>
          </div>

          <div className="rounded-2xl bg-white p-6 shadow-md border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">持仓数量</p>
                <p className="mt-2 text-3xl font-bold text-gray-900">
                  {dashboardData?.positions_summary.total_positions || 0}
                </p>
                <p className="text-sm text-gray-500">
                  盈利 {dashboardData?.positions_summary.profitable_count || 0} / 亏损 {dashboardData?.positions_summary.losing_count || 0}
                </p>
              </div>
              <div className="rounded-full bg-purple-100 p-3">
                <svg className="h-6 w-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
              </div>
            </div>
          </div>

          <div className="rounded-2xl bg-white p-6 shadow-md border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">纪律评分</p>
                <p className="mt-2 text-3xl font-bold text-gray-900">
                  {dashboardData?.discipline_score ? parseFloat(dashboardData.discipline_score).toFixed(0) : '--'}
                </p>
                <p className="text-sm text-gray-500">满分 100</p>
              </div>
              <div className="rounded-full bg-yellow-100 p-3">
                <svg className="h-6 w-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
          </div>
        </div>

        {/* Charts Section */}
        {dashboardData && Object.keys(dashboardData.positions_summary.by_market).length > 0 && (
          <div className="mb-8 grid gap-6 lg:grid-cols-2">
            {/* Pie Chart */}
            <div className="rounded-2xl bg-white p-6 shadow-md border border-gray-100">
              <h3 className="mb-4 text-lg font-bold text-gray-900">持仓分布（按市场）</h3>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={getPieChartData()}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name}: ${(((percent ?? 0) * 100)).toFixed(1)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {getPieChartData().map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={MARKET_COLORS[entry.market] || '#888888'} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value: unknown) => formatSummaryCurrency(
                    typeof value === 'number' || typeof value === 'string' ? value : undefined
                  )} />
                </PieChart>
              </ResponsiveContainer>
            </div>

            {/* Bar Chart */}
            <div className="rounded-2xl bg-white p-6 shadow-md border border-gray-100">
              <h3 className="mb-4 text-lg font-bold text-gray-900">市值与盈亏对比</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={getBarChartData()}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip formatter={(value: unknown) => formatSummaryCurrency(
                    typeof value === 'number' || typeof value === 'string' ? value : undefined
                  )} />
                  <Legend />
                  <Bar dataKey="市值" fill="#3B82F6" />
                  <Bar dataKey="盈亏" fill="#10B981" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        <div className="mb-8 grid gap-6 lg:grid-cols-2">
          {/* Recent Trades */}
          <div className="rounded-2xl bg-white p-6 shadow-md border border-gray-100">
            <h3 className="mb-4 text-lg font-bold text-gray-900">最近交易</h3>
            {dashboardData && dashboardData.recent_trades.length > 0 ? (
              <div className="space-y-3">
                {dashboardData.recent_trades.map((trade) => (
                  <div key={trade.id} className="flex items-center justify-between border-b border-gray-100 pb-3 last:border-0">
                    <div>
                      <div className="font-medium text-gray-900">{trade.symbol}</div>
                      {trade.symbol_name && (
                        <div className="text-xs text-gray-500">{trade.symbol_name}</div>
                      )}
                      <div className="text-sm text-gray-500">
                        {trade.account_name} · {formatDateTime(trade.trade_time)}
                      </div>
                    </div>
                    <div className="text-right">
                      <div className={`font-medium ${trade.side === 'buy' ? 'text-green-600' : 'text-red-600'}`}>
                        {trade.side === 'buy' ? '买入' : '卖出'}
                      </div>
                      <div className="text-sm text-gray-500">
                        {formatQuantity(trade.quantity, { accountType: trade.account_type })} @{' '}
                        {formatPrice(trade.price, { accountType: trade.account_type })}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-center text-gray-500 py-8">暂无交易记录</p>
            )}
          </div>

        </div>

        {/* Quick Stats */}
        <div className="mb-8 rounded-2xl bg-white p-6 shadow-md border border-gray-100">
          <h3 className="mb-4 text-lg font-bold text-gray-900">快速统计</h3>
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="bg-gradient-to-br from-gray-50 to-white p-4 rounded-xl border border-gray-100">
              <p className="text-sm text-gray-600">本月交易次数</p>
              <p className="mt-2 text-2xl font-bold text-gray-900">
                {dashboardData?.quick_stats.trades_this_month || 0}
              </p>
            </div>
            <div className="bg-gradient-to-br from-gray-50 to-white p-4 rounded-xl border border-gray-100">
              <p className="text-sm text-gray-600">本月胜率</p>
              <p className="mt-2 text-2xl font-bold text-gray-900">
                {dashboardData?.quick_stats.win_rate_this_month
                  ? formatPercent(dashboardData.quick_stats.win_rate_this_month)
                  : '--'
                }
              </p>
            </div>
          </div>
        </div>

        </main>
      </div>
    </>
  );
}
