'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { accountsApi, TradeAccount } from '@/lib/api/accounts';
import { apiClient } from '@/lib/api-client';
import { Position } from '@/types/position';
import { Trade } from '@/types/trade';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Upload, History, ArrowLeft, RefreshCw, TrendingUp, Activity, Pencil } from 'lucide-react';
import ImportDialog from './components/ImportDialog';
import ImportHistoryDialog from './components/ImportHistoryDialog';
import EditAccountDialog from '../components/EditAccountDialog';
import { toast } from 'sonner';
import { importIBKRWithSavedCredentials, pollIBKRTaskStatus } from '@/lib/api/ibkr';
import { importApi } from '@/lib/api/import';
import { formatMoney, formatQuantity } from '@/lib/format/number';
import { usePageTitle } from '@/lib/use-page-title';

const ACCOUNT_TYPE_LABELS: Record<string, string> = {
  crypto: '加密货币',
  us_stock: '美股',
  a_stock: 'A股',
  hk_stock: '港股',
};

export default function AccountDetailPage() {
  const params = useParams();
  const router = useRouter();
  const accountId = params.id as string;

  const [account, setAccount] = useState<TradeAccount | null>(null);
  const [positions, setPositions] = useState<Position[]>([]);
  const [closedPositions, setClosedPositions] = useState<Position[]>([]);
  const [trades, setTrades] = useState<Trade[]>([]);
  const [positionStats, setPositionStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [showImportDialog, setShowImportDialog] = useState(false);
  const [showHistoryDialog, setShowHistoryDialog] = useState(false);
  const [showEditDialog, setShowEditDialog] = useState(false);
  const [isSyncing, setIsSyncing] = useState(false);
  const [isGmailSyncing, setIsGmailSyncing] = useState(false);
  const [isGmailAuthorizing, setIsGmailAuthorizing] = useState(false);

  usePageTitle(account?.account_name ?? '账户详情');

  // 加载账户详情
  useEffect(() => {
    loadAccountDetails();
    loadPositions();
    loadClosedPositions();
    loadTrades();
    loadPositionStats();
  }, [accountId]);

  const loadAccountDetails = async () => {
    try {
      setLoading(true);
      // 获取所有账户并筛选
      const accounts = await accountsApi.getAccounts();
      const foundAccount = accounts.find((acc) => acc.id === accountId);

      if (foundAccount) {
        setAccount(foundAccount);
      } else {
        // 账户不存在,返回列表页
        router.push('/accounts');
      }
    } catch (error) {
      console.error('加载账户详情失败:', error);
      router.push('/accounts');
    } finally {
      setLoading(false);
    }
  };

  const loadPositions = async () => {
    try {
      const response = await apiClient.getPositions({
        account_id: accountId,
        is_closed: false,  // 只加载持仓中的
        page_size: 100
      });
      setPositions(response.positions);
    } catch (error) {
      console.error('加载持仓失败:', error);
    }
  };

  const loadClosedPositions = async () => {
    try {
      const response = await apiClient.getPositions({
        account_id: accountId,
        is_closed: true,  // 只加载已清仓的
        page_size: 100
      });
      setClosedPositions(response.positions);
    } catch (error) {
      console.error('加载已清仓持仓失败:', error);
    }
  };

  const loadTrades = async () => {
    try {
      const response = await apiClient.getTrades({
        account_id: accountId,
        page_size: 20
      });
      setTrades(response.trades);
    } catch (error) {
      console.error('加载交易记录失败:', error);
    }
  };

  const loadPositionStats = async () => {
    try {
      const stats = await apiClient.getPositionStats(accountId);
      setPositionStats(stats);
    } catch (error) {
      console.error('加载持仓统计失败:', error);
    }
  };

  // 同步账户数据
  const handleSync = async () => {
    if (!account) return;

    // 检查是否为 IBKR 账户
    const isIBKR = account.account_type === 'us_stock' && account.broker === 'interactive_brokers';

    if (isIBKR) {
      // 使用 IBKR Flex API 同步
      await handleIBKRSync();
    } else {
      // 使用通用同步（币安等）
      await handleGeneralSync();
    }
  };

  // IBKR 同步
  const handleIBKRSync = async () => {
    if (!account) return;

    // 检查是否配置了 Flex 凭证
    if (!account.ibkr_flex_token || !account.ibkr_flex_query_id) {
      toast.error('同步失败', {
        description: '该账户未配置 IBKR Flex 凭证，请先在账户设置中配置',
      });
      return;
    }

    setIsSyncing(true);

    try {
      // 提交异步任务
      const syncResponse = await importIBKRWithSavedCredentials(account.id);

      // 显示等待提示
      toast.loading('正在从 IBKR 同步交易数据...', {
        description: '后台任务进行中，请稍候',
        id: 'sync-loading',
      });

      // 轮询任务状态
      const result = await pollIBKRTaskStatus(
        syncResponse.task_id,
        (status) => {
          // 根据状态更新提示信息
          if (status.status === 'PROGRESS') {
            const progress = status.progress || 0;
            toast.loading(`正在同步交易数据... ${progress}%`, {
              description: '同步进行中...',
              id: 'sync-loading',
            });
          }
        }
      );

      // 关闭加载提示
      toast.dismiss('sync-loading');

      if (result.status === 'SUCCESS' && result.result) {
        // 显示成功提示
        const imported = result.result.imported_count || 0;
        const skipped = result.result.skipped_count || 0;
        toast.success('同步成功', {
          description: `导入 ${imported} 条交易，跳过 ${skipped} 条重复记录`,
        });

        // 刷新数据
        loadAccountDetails();
        loadPositions();
        loadTrades();
      } else {
        toast.error('同步失败', {
          description: result.error || '同步任务执行失败',
        });
      }
    } catch (error: any) {
      toast.dismiss('sync-loading');
      toast.error('同步错误', {
        description: error.response?.data?.detail || '同步失败，请稍后重试',
      });
    } finally {
      setIsSyncing(false);
    }
  };

  const handleGmailSync = async () => {
    if (!account) return;

    if (!account.has_gmail_credentials) {
      toast.error('同步失败', {
        description: '请先在账户设置中配置 Gmail 同步凭证',
      });
      return;
    }

    setIsGmailSyncing(true);

    try {
      const result = await importApi.syncGmail(account.id);
      toast.success('同步完成', {
        description: result.message,
      });

      loadAccountDetails();
      loadPositions();
      loadTrades();
    } catch (error: any) {
      toast.error('同步失败', {
        description: error.response?.data?.detail || '同步失败，请稍后重试',
      });
    } finally {
      setIsGmailSyncing(false);
    }
  };

  const handleGmailConnect = async () => {
    if (!account) return;

    setIsGmailAuthorizing(true);

    try {
      const result = await importApi.startGmailOAuth(account.id);
      const authWindow = window.open(
        result.auth_url,
        'gmail-oauth',
        'width=500,height=700'
      );

      if (!authWindow) {
        throw new Error('无法打开授权窗口，请检查浏览器弹窗设置');
      }

      const timer = window.setInterval(() => {
        if (authWindow.closed) {
          window.clearInterval(timer);
          setIsGmailAuthorizing(false);
          accountsApi.getAccount(account.id).then((updatedAccount) => {
            setAccount(updatedAccount);
            if (updatedAccount.has_gmail_credentials) {
              toast.success('Gmail 已连接', {
                description: '可以开始同步国泰海通邮件',
              });
            } else {
              toast.error('授权未完成', {
                description: '未检测到有效授权，请重试',
              });
            }
          }).catch(() => {
            loadAccountDetails();
          });
        }
      }, 1000);
    } catch (error: any) {
      setIsGmailAuthorizing(false);
      toast.error('授权失败', {
        description: error.response?.data?.detail || error.message || '无法完成 Gmail 授权',
      });
    }
  };

  // 通用同步（币安等）
  const handleGeneralSync = async () => {
    if (!account) return;

    if (!account.has_api_credentials) {
      toast.error('同步失败', {
        description: '该账户未配置 API 凭证，无法同步',
      });
      return;
    }

    setIsSyncing(true);

    try {
      // 提交异步任务
      const syncResponse = await accountsApi.syncAccount(account.id);

      // 显示等待提示
      toast.loading('正在同步交易数据...', {
        description: '后台任务进行中，请稍候',
        id: 'sync-loading',
      });

      // 轮询任务状态
      const result = await accountsApi.pollSyncTask(
        syncResponse.task_id,
        (status) => {
          if (status === 'PROGRESS') {
            toast.loading('正在同步交易数据...', {
              description: '同步进行中...',
              id: 'sync-loading',
            });
          }
        }
      );

      // 关闭加载提示
      toast.dismiss('sync-loading');

      if (result.success) {
        const syncedCount = result.result?.synced_count || 0;
        toast.success('同步成功', {
          description: `已同步 ${syncedCount} 条交易记录`,
        });

        // 刷新数据
        loadAccountDetails();
        loadPositions();
        loadTrades();
      } else {
        toast.error('同步失败', {
          description: result.error || '同步任务执行失败',
        });
      }
    } catch (error: any) {
      toast.dismiss('sync-loading');
      toast.error('同步错误', {
        description: error.response?.data?.detail || '同步失败，请稍后重试',
      });
    } finally {
      setIsSyncing(false);
    }
  };

  const getCurrencySymbol = (accountType: string) => {
    const currencyMap: Record<string, string> = {
      'us_stock': '$',
      'crypto': '$',
      'a_stock': '¥',
      'hk_stock': 'HK$'
    };
    return currencyMap[accountType] || '$';
  };

  const formatNumber = (value: string | number | undefined, decimals = 2) => {
    if (value === undefined || value === null) return '0.00';
    return parseFloat(value.toString()).toFixed(decimals);
  };

  const formatCurrency = (value: string | number | undefined, decimals = 2) => {
    if (!account) return '$0.00';
    if (account.account_type === 'a_stock') {
      return formatMoney(value, { accountType: 'a_stock', fallbackFractionDigits: decimals });
    }
    const symbol = getCurrencySymbol(account.account_type);
    return `${symbol}${formatNumber(value, decimals)}`;
  };

  const formatPercent = (value: string | number | undefined) => {
    if (value === undefined || value === null) return '0.00%';
    const num = parseFloat(value.toString());
    const color = num >= 0 ? 'text-green-600' : 'text-red-600';
    const sign = num >= 0 ? '+' : '';
    return <span className={color}>{sign}{num.toFixed(2)}%</span>;
  };

  const formatPnL = (value: string | number | undefined) => {
    if (value === undefined || value === null || !account) return `${getCurrencySymbol(account?.account_type || 'crypto')}0.00`;
    const num = parseFloat(value.toString());
    const color = num >= 0 ? 'text-green-600' : 'text-red-600';
    const sign = num >= 0 ? '+' : '-';
    if (account.account_type === 'a_stock') {
      return (
        <span className={color}>
          {sign}
          {formatMoney(Math.abs(num), { accountType: 'a_stock', fallbackFractionDigits: 2 })}
        </span>
      );
    }
    const symbol = getCurrencySymbol(account.account_type);
    return <span className={color}>{sign}{symbol}{Math.abs(num).toFixed(2)}</span>;
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

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <RefreshCw className="h-8 w-8 animate-spin mx-auto mb-2 text-gray-400" />
          <p className="text-sm text-gray-500">加载中...</p>
        </div>
      </div>
    );
  }

  if (!account) {
    return null;
  }

  const securitiesValue =
    positionStats?.total_market_value !== undefined && positionStats?.total_market_value !== null
      ? Number(positionStats.total_market_value)
      : null;
  const cashBalanceValue =
    account.cash_balance !== undefined && account.cash_balance !== null
      ? Number(account.cash_balance)
      : null;
  const totalAssetValue =
    securitiesValue !== null && cashBalanceValue !== null ? securitiesValue + cashBalanceValue : null;
  const positionRatio =
    totalAssetValue !== null && totalAssetValue > 0 && securitiesValue !== null
      ? securitiesValue / totalAssetValue
      : null;

  const securitiesLabel = securitiesValue === null ? '暂无' : formatCurrency(securitiesValue);
  const cashBalanceLabel = cashBalanceValue === null ? '暂无' : formatCurrency(cashBalanceValue);
  const positionRatioLabel = positionRatio === null ? '暂无' : `${(positionRatio * 100).toFixed(2)}%`;

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50">
      <div className="container mx-auto py-8 px-4 space-y-6">
        {/* 页头 - 返回按钮和账户信息 */}
        <div className="flex items-center justify-between flex-wrap gap-4">
          <div className="flex items-center space-x-4">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => router.push('/accounts')}
              className="flex items-center hover:bg-white/80"
            >
              <ArrowLeft className="h-4 w-4 mr-1" />
              返回
            </Button>

            <div>
              <div className="flex items-center space-x-3 flex-wrap">
                <h1 className="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
                  {account.account_name}
                </h1>
                <Badge
                  variant={account.is_active ? 'default' : 'secondary'}
                  className={account.is_active ? 'bg-green-500 hover:bg-green-600' : ''}
                >
                  {account.is_active ? '活跃' : '已停用'}
                </Badge>
                <Badge variant="outline" className="border-blue-300 text-blue-700">
                  {ACCOUNT_TYPE_LABELS[account.account_type] || account.account_type}
                </Badge>
              </div>
              {account.description && (
                <p className="text-sm text-gray-600 mt-2">{account.description}</p>
              )}
            </div>
          </div>

          {/* 操作按钮区 */}
          <div className="flex items-center space-x-2">
            {/* 同步按钮 - 仅对配置了凭证的账户显示 */}
            {(account.has_api_credentials || (account.ibkr_flex_token && account.ibkr_flex_query_id)) && (
              <Button
                variant="outline"
                size="sm"
                onClick={handleSync}
                disabled={isSyncing}
                className="flex items-center bg-white hover:bg-gray-50 shadow-sm"
              >
                <RefreshCw className={`h-4 w-4 mr-1 ${isSyncing ? 'animate-spin' : ''}`} />
                {isSyncing ? '同步中...' : '同步数据'}
              </Button>
            )}

            {account.broker === 'gtja' && (
              <Button
                variant="outline"
                size="sm"
                onClick={handleGmailConnect}
                disabled={isGmailAuthorizing}
                className="flex items-center bg-white hover:bg-gray-50 shadow-sm"
              >
                <RefreshCw className={`h-4 w-4 mr-1 ${isGmailAuthorizing ? 'animate-spin' : ''}`} />
                {isGmailAuthorizing
                  ? '授权中...'
                  : (account.has_gmail_credentials ? '重新授权 Gmail' : '连接 Gmail')}
              </Button>
            )}

            {account.broker === 'gtja' && (
              <Button
                variant="outline"
                size="sm"
                onClick={handleGmailSync}
                disabled={isGmailSyncing || !account.has_gmail_credentials}
                className="flex items-center bg-white hover:bg-gray-50 shadow-sm"
              >
                <RefreshCw className={`h-4 w-4 mr-1 ${isGmailSyncing ? 'animate-spin' : ''}`} />
                {isGmailSyncing ? '邮箱同步中...' : '邮箱同步'}
              </Button>
            )}

            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowHistoryDialog(true)}
              className="flex items-center bg-white hover:bg-gray-50 shadow-sm"
            >
              <History className="h-4 w-4 mr-1" />
              导入历史
            </Button>

            <Button
              size="sm"
              onClick={() => setShowImportDialog(true)}
              className="flex items-center bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 shadow-md"
            >
              <Upload className="h-4 w-4 mr-1" />
              导入交易记录
            </Button>
          </div>
        </div>

        {/* 账户统计卡片 */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card className="border-none shadow-lg bg-white/80 backdrop-blur">
            <CardHeader className="pb-3">
              <CardDescription className="text-gray-600">账户类型</CardDescription>
              <CardTitle className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                {ACCOUNT_TYPE_LABELS[account.account_type]}
              </CardTitle>
            </CardHeader>
          </Card>

          <Card className="border-none shadow-lg bg-white/80 backdrop-blur">
            <CardHeader className="pb-3">
              <CardDescription className="text-gray-600">创建时间</CardDescription>
              <CardTitle className="text-2xl font-bold text-gray-900">
                {new Date(account.created_at).toLocaleDateString('zh-CN')}
              </CardTitle>
            </CardHeader>
          </Card>

          <Card className="border-none shadow-lg bg-white/80 backdrop-blur">
            <CardHeader className="pb-3">
              <CardDescription className="text-gray-600">最后同步</CardDescription>
              <CardTitle className="text-xl font-bold text-gray-900">
                {account.last_sync_at
                  ? new Date(account.last_sync_at).toLocaleString('zh-CN', {
                      month: '2-digit',
                      day: '2-digit',
                      hour: '2-digit',
                      minute: '2-digit'
                    })
                  : '从未同步'}
              </CardTitle>
            </CardHeader>
          </Card>

          <Card className="border-none shadow-lg bg-white/80 backdrop-blur">
            <CardHeader className="pb-3">
              <CardDescription className="text-gray-600">证券资产总额</CardDescription>
              <CardTitle className="text-2xl font-bold text-gray-900">
                {securitiesLabel}
              </CardTitle>
            </CardHeader>
          </Card>

          <Card className="border-none shadow-lg bg-white/80 backdrop-blur">
            <CardHeader className="pb-3">
              <div className="flex items-start justify-between gap-2">
                <CardDescription className="text-gray-600">剩余资金</CardDescription>
                <Button
                  type="button"
                  variant="ghost"
                  size="icon"
                  className="h-8 w-8"
                  onClick={() => setShowEditDialog(true)}
                  title="编辑剩余资金"
                >
                  <Pencil className="h-4 w-4" />
                </Button>
              </div>
              <CardTitle className="text-2xl font-bold text-gray-900">
                {cashBalanceLabel}
              </CardTitle>
            </CardHeader>
          </Card>

          <Card className="border-none shadow-lg bg-white/80 backdrop-blur">
            <CardHeader className="pb-3">
              <CardDescription className="text-gray-600">仓位</CardDescription>
              <CardTitle className="text-2xl font-bold text-gray-900">
                {positionRatioLabel}
              </CardTitle>
            </CardHeader>
          </Card>
        </div>

        {/* 盈亏汇总卡片 */}
        {positionStats && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card className="border-none shadow-lg bg-gradient-to-br from-green-50 to-emerald-50">
              <CardHeader className="pb-3">
                <CardDescription className="text-gray-600">已实现盈亏</CardDescription>
                <CardTitle className="text-3xl font-bold">
                  {formatPnL(positionStats.total_realized_pnl)}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-600">来自已清仓持仓</p>
              </CardContent>
            </Card>

            <Card className="border-none shadow-lg bg-gradient-to-br from-blue-50 to-indigo-50">
              <CardHeader className="pb-3">
                <CardDescription className="text-gray-600">未实现盈亏</CardDescription>
                <CardTitle className="text-3xl font-bold">
                  {formatPnL(positionStats.total_unrealized_pnl)}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-1">
                  <p className="text-sm text-gray-600">
                    当前持仓: {positionStats.total_positions} 个标的
                  </p>
                  <p className="text-sm text-gray-600">
                    盈亏率: {formatPercent(positionStats.total_unrealized_pnl_percent)}
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

      {/* 当前持仓 */}
      <Card className="border-none shadow-xl bg-white/90 backdrop-blur">
        <CardHeader className="bg-gradient-to-r from-gray-50 to-gray-100 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg shadow-md">
                <TrendingUp className="h-5 w-5 text-white" />
              </div>
              <CardTitle className="text-xl font-bold text-gray-800">当前持仓</CardTitle>
            </div>
            <Badge variant="outline" className="bg-white border-blue-200 text-blue-700 font-semibold">
              {positions.length} 个标的
            </Badge>
          </div>
        </CardHeader>
        <CardContent className="p-0">
          {positions.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <TrendingUp className="h-12 w-12 mx-auto mb-2 text-gray-300" />
              <p>暂无持仓</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gradient-to-r from-gray-100 to-gray-50">
                  <tr>
                    <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">标的</th>
                    <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">数量</th>
                    <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">成本价</th>
                    <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">当前价</th>
                    <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">持仓天数</th>
                    <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">盈亏</th>
                    <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">盈亏率</th>
                    <th className="px-6 py-4 text-center text-xs font-bold text-gray-700 uppercase tracking-wider">操作</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-100">
                  {positions.map((position) => (
                    <tr
                      key={position.id}
                      className="hover:bg-gradient-to-r hover:from-blue-50 hover:to-indigo-50 transition-all duration-200"
                    >
                      <td className="px-4 py-3 text-sm font-medium">
                        <button
                          onClick={() => router.push(`/symbols/${encodeURIComponent(position.symbol)}?account_id=${accountId}`)}
                          className="text-blue-600 hover:text-blue-800 hover:underline font-medium"
                        >
                          {position.symbol}
                        </button>
                        {position.position_type === 'futures' && (
                          <Badge variant={position.position_side === 'LONG' ? 'default' : 'destructive'} className="ml-2">
                            {position.position_side === 'LONG' ? '多' : '空'}
                          </Badge>
                        )}
                      </td>
                      <td className="px-4 py-3 text-sm text-right text-gray-700">
                        {formatQuantity(Math.abs(parseFloat(position.quantity)), { accountType: account.account_type, fallbackFractionDigits: 2 })}
                      </td>
                      <td className="px-4 py-3 text-sm text-right text-gray-700">
                        {position.position_type === 'futures'
                          ? formatCurrency(position.entry_price || '0', 2)
                          : formatCurrency(position.average_cost || '0', 2)
                        }
                      </td>
                      <td className="px-4 py-3 text-sm text-right text-gray-700">
                        {position.current_price ? formatCurrency(position.current_price, 2) : '-'}
                      </td>
                      <td className="px-4 py-3 text-sm text-right text-gray-700">
                        {position.holding_days !== null && position.holding_days !== undefined ? `${position.holding_days}天` : '-'}
                      </td>
                      <td className="px-4 py-3 text-sm text-right font-medium">
                        {formatPnL(position.unrealized_pnl)}
                      </td>
                      <td className="px-4 py-3 text-sm text-right font-medium">
                        {position.position_type === 'futures' && position.roe_percent
                          ? formatPercent(position.roe_percent)
                          : formatPercent(position.unrealized_pnl_percent)
                        }
                      </td>
                      <td className="px-4 py-3 text-center">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => router.push(`/symbols/${encodeURIComponent(position.symbol)}?account_id=${accountId}`)}
                        >
                          查看
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>

      {/* 已清仓持仓 */}
      {closedPositions.length > 0 && (
        <Card className="border-none shadow-xl bg-white/90 backdrop-blur">
          <CardHeader className="bg-gradient-to-r from-gray-50 to-gray-100 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-gradient-to-br from-gray-500 to-gray-600 rounded-lg shadow-md">
                  <TrendingUp className="h-5 w-5 text-white" />
                </div>
                <CardTitle className="text-xl font-bold text-gray-800">已清仓持仓</CardTitle>
              </div>
              <Badge variant="outline" className="bg-white border-gray-300 text-gray-700 font-semibold">
                {closedPositions.length} 个标的
              </Badge>
            </div>
          </CardHeader>
          <CardContent className="p-0">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gradient-to-r from-gray-100 to-gray-50">
                  <tr>
                    <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">标的</th>
                    <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">数量</th>
                    <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">成本价</th>
                    <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">清仓价</th>
                    <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">持仓天数</th>
                    <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">已实现盈亏</th>
                    <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">盈亏率</th>
                    <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">开仓时间</th>
                    <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">清仓时间</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-100">
                  {closedPositions.map((position) => {
                    // 获取成本价：合约用 entry_price，现货用 average_cost
                    const costPrice = position.position_type === 'futures'
                      ? (position.entry_price || '0')
                      : (position.average_cost || '0');

                    return (
                      <tr
                        key={position.id}
                        className="hover:bg-gradient-to-r hover:from-gray-50 hover:to-gray-100 transition-all duration-200"
                      >
                        <td className="px-4 py-3 text-sm font-medium">
                          <button
                            onClick={() => router.push(`/symbols/${encodeURIComponent(position.symbol)}?account_id=${accountId}`)}
                            className="text-blue-600 hover:text-blue-800 hover:underline font-medium"
                          >
                            {position.symbol}
                          </button>
                          {position.position_type === 'futures' && (
                            <Badge variant="outline" className="ml-2 text-gray-600">
                              {position.position_side === 'LONG' ? '多' : '空'}
                            </Badge>
                          )}
                        </td>
                        <td className="px-4 py-3 text-sm text-right text-gray-700">
                          {formatQuantity(Math.abs(parseFloat(position.quantity)), { accountType: account.account_type, fallbackFractionDigits: 2 })}
                        </td>
                        <td className="px-4 py-3 text-sm text-right text-gray-600">
                          {formatCurrency(costPrice, 2)}
                        </td>
                        <td className="px-4 py-3 text-sm text-right text-gray-700 font-medium">
                          {position.final_price ? formatCurrency(position.final_price, 2) : '-'}
                        </td>
                        <td className="px-4 py-3 text-sm text-right text-gray-600">
                          {position.holding_days !== null && position.holding_days !== undefined ? `${position.holding_days}天` : '-'}
                        </td>
                        <td className="px-4 py-3 text-sm text-right font-medium">
                          {position.realized_pnl ? formatPnL(position.realized_pnl) : '-'}
                        </td>
                        <td className="px-4 py-3 text-sm text-right font-medium">
                          {position.realized_pnl_percent ? formatPercent(position.realized_pnl_percent) : '-'}
                        </td>
                        <td className="px-4 py-3 text-sm text-right text-gray-600">
                          {position.first_buy_time ? new Date(position.first_buy_time).toLocaleDateString('zh-CN') : '-'}
                        </td>
                        <td className="px-4 py-3 text-sm text-right text-gray-600">
                          {position.closed_at ? formatDate(position.closed_at) : '-'}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      )}

      {/* 历史交易记录 */}
      <Card className="border-none shadow-xl bg-white/90 backdrop-blur">
        <CardHeader className="bg-gradient-to-r from-gray-50 to-gray-100 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg shadow-md">
                <Activity className="h-5 w-5 text-white" />
              </div>
              <CardTitle className="text-xl font-bold text-gray-800">最近交易记录</CardTitle>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={() => router.push(`/trades?account_id=${accountId}`)}
              className="bg-white hover:bg-gray-50 shadow-sm"
            >
              查看全部
            </Button>
          </div>
        </CardHeader>
        <CardContent className="p-0">
          {trades.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <Activity className="h-12 w-12 mx-auto mb-2 text-gray-300" />
              <p>暂无交易记录</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gradient-to-r from-gray-100 to-gray-50">
                  <tr>
                    <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">时间</th>
                    <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">标的</th>
                    <th className="px-6 py-4 text-center text-xs font-bold text-gray-700 uppercase tracking-wider">方向</th>
                    <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">数量</th>
                    <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">价格</th>
                    <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">金额</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-100">
                  {trades.map((trade) => (
                    <tr key={trade.id} className="hover:bg-gradient-to-r hover:from-blue-50 hover:to-indigo-50 transition-all duration-200">
                      <td className="px-4 py-3 text-sm text-gray-700">
                        {formatDate(trade.trade_time)}
                      </td>
                      <td
                        className="px-4 py-3 text-sm font-medium text-blue-600 cursor-pointer hover:underline"
                        onClick={() => router.push(`/symbols/${encodeURIComponent(trade.symbol)}?account_id=${accountId}`)}
                      >
                        <div className="text-sm font-medium text-blue-600">
                          {trade.symbol}
                        </div>
                        {trade.symbol_name && (
                          <div className="text-xs text-gray-500">
                            {trade.symbol_name}
                          </div>
                        )}
                      </td>
                      <td className="px-4 py-3 text-center">
                        <Badge variant={trade.side === 'buy' ? 'default' : 'destructive'}>
                          {trade.side === 'buy' ? '买入' : '卖出'}
                        </Badge>
                        {trade.position_side && (
                          <Badge variant="outline" className="ml-1">
                            {trade.position_side === 'LONG' ? '多' : '空'}
                          </Badge>
                        )}
                      </td>
                      <td className="px-4 py-3 text-sm text-right text-gray-700">
                        {formatQuantity(trade.quantity, { accountType: account.account_type, fallbackFractionDigits: 8 })}
                      </td>
                      <td className="px-4 py-3 text-sm text-right text-gray-700">
                        {formatCurrency(trade.price, 2)}
                      </td>
                      <td className="px-4 py-3 text-sm text-right font-medium text-gray-900">
                        {formatCurrency(parseFloat(trade.price) * parseFloat(trade.quantity), 2)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>

      <EditAccountDialog
        open={showEditDialog}
        onOpenChange={setShowEditDialog}
        account={account}
        onSuccess={() => {
          setShowEditDialog(false);
          loadAccountDetails();
        }}
      />

      {/* 导入对话框 */}
      <ImportDialog
        open={showImportDialog}
        onOpenChange={setShowImportDialog}
        accountId={accountId}
        accountName={account.account_name}
        onImportSuccess={() => {
          loadAccountDetails();
          loadPositions();
          loadClosedPositions();
          loadTrades();
          loadPositionStats();
        }}
      />

      {/* 导入历史对话框 */}
      <ImportHistoryDialog
        open={showHistoryDialog}
        onOpenChange={setShowHistoryDialog}
        accountId={accountId}
        accountName={account.account_name}
      />
      </div>
    </div>
  );
}
