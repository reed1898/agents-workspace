'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { MoreVertical, Edit, Trash2, Tag, ExternalLink, RefreshCw, Database, TrendingUp } from 'lucide-react';
import { toast } from 'sonner';
import type { TradeAccount } from '@/lib/types/account';
import { ACCOUNT_TYPE_LABELS } from '@/lib/types/account';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import { Badge } from '@/components/ui/badge';
import EditAccountDialog from './EditAccountDialog';
import { accountsApi } from '@/lib/api/accounts';
import { importIBKRWithSavedCredentials, pollIBKRTaskStatus } from '@/lib/api/ibkr';

interface AccountCardProps {
  account: TradeAccount;
  onDelete: (id: string) => void;
  onUpdate: () => void;
}

export default function AccountCard({ account, onDelete, onUpdate }: AccountCardProps) {
  const router = useRouter();
  const [showEditDialog, setShowEditDialog] = useState(false);
  const [showClearDialog, setShowClearDialog] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [isSyncing, setIsSyncing] = useState(false);
  const [isClearing, setIsClearing] = useState(false);

  const handleViewDetail = (e?: React.MouseEvent) => {
    e?.stopPropagation();
    router.push(`/accounts/${account.id}`);
    setMenuOpen(false);
  };

  const handleEdit = (e?: React.MouseEvent) => {
    e?.stopPropagation();
    setShowEditDialog(true);
    setMenuOpen(false);
  };

  const handleEnterPositions = (e?: React.MouseEvent) => {
    e?.stopPropagation();
    router.push(`/positions?account_id=${account.id}`);
    setMenuOpen(false);
  };

  const handleSync = async (e: React.MouseEvent) => {
    e.stopPropagation();
    setMenuOpen(false);

    if (!account.has_api_credentials && account.account_type === 'crypto') {
      toast.error('同步失败', {
        description: '该账户未配置 API 凭证，无法同步',
      });
      return;
    }

    if (!account.ibkr_flex_token && account.broker === 'interactive_brokers') {
      toast.error('同步失败', {
        description: '该账户未配置 IBKR Flex 凭证，无法同步',
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
          // 可以根据状态更新提示信息
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
        // 显示成功提示
        const syncedCount = result.result?.synced_count || 0;
        toast.success('同步成功', {
          description: `已同步 ${syncedCount} 条交易记录`,
        });
        onUpdate(); // 刷新账户列表
      } else {
        toast.error('同步失败', {
          description: result.error || '同步任务执行失败',
        });
      }
    } catch (error: any) {
      // 关闭加载提示
      toast.dismiss('sync-loading');

      const errorMsg = error.response?.data?.detail || '同步失败，请稍后重试';
      toast.error('同步失败', {
        description: errorMsg,
      });
    } finally {
      setIsSyncing(false);
    }
  };

  const handleIBKRSync = async (e: React.MouseEvent) => {
    e.stopPropagation();
    setMenuOpen(false);

    console.log('=== IBKR Sync Debug ===');
    console.log('Account:', account);
    console.log('Account ID:', account.id);
    console.log('IBKR Flex Token:', account.ibkr_flex_token);
    console.log('IBKR Flex Query ID:', account.ibkr_flex_query_id);

    if (!account.ibkr_flex_token || !account.ibkr_flex_query_id) {
      console.error('IBKR credentials missing!');
      toast.error('同步失败', {
        description: '该账户未配置 IBKR Flex 凭证，无法同步',
      });
      return;
    }

    setIsSyncing(true);

    try {
      console.log('Calling importIBKRWithSavedCredentials...');
      // 提交异步任务
      const syncResponse = await importIBKRWithSavedCredentials(account.id);
      console.log('Sync response:', syncResponse);

      // 显示等待提示
      toast.loading('正在从 IBKR 同步交易数据...', {
        description: '后台任务进行中，请稍候',
        id: 'ibkr-sync-loading',
      });

      // 轮询任务状态
      const result = await pollIBKRTaskStatus(
        syncResponse.task_id,
        (status) => {
          if (status.status === 'PROGRESS') {
            toast.loading('正在从 IBKR 同步交易数据...', {
              description: `进度: ${status.progress}%`,
              id: 'ibkr-sync-loading',
            });
          }
        }
      );

      // 关闭加载提示
      toast.dismiss('ibkr-sync-loading');

      if (result.status === 'SUCCESS' && result.result) {
        const { imported_count = 0, skipped_count = 0, error_count = 0 } = result.result;
        toast.success('IBKR 同步成功', {
          description: `导入 ${imported_count} 条，跳过 ${skipped_count} 条${error_count > 0 ? `，失败 ${error_count} 条` : ''}`,
        });
        onUpdate(); // 刷新账户列表
      } else {
        toast.error('IBKR 同步失败', {
          description: result.error || result.result?.error || '同步任务执行失败',
        });
      }
    } catch (error: any) {
      // 关闭加载提示
      toast.dismiss('ibkr-sync-loading');

      console.error('=== IBKR Sync Error ===');
      console.error('Full error:', error);
      console.error('Error message:', error.message);
      console.error('Error response:', error.response);
      console.error('Error request:', error.request);
      console.error('Error config:', error.config);

      const errorMsg = error.response?.data?.detail || error.message || 'IBKR 同步失败，请稍后重试';
      toast.error('IBKR 同步失败', {
        description: errorMsg,
      });
    } finally {
      setIsSyncing(false);
    }
  };

  const handleClearData = async () => {
    setIsClearing(true);
    try {
      const result = await accountsApi.clearAccountData(account.id);
      toast.success('清除成功', {
        description: `已清除 ${result.deleted_count} 条交易记录`,
      });
      onUpdate(); // 刷新账户列表
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || '清除失败，请稍后重试';
      toast.error('清除失败', {
        description: errorMsg,
      });
    } finally {
      setIsClearing(false);
      setShowClearDialog(false);
    }
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return '从未同步';
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN');
  };

  return (
    <>
      <Card
        className="hover:shadow-xl transition-all duration-200 border-gray-100 bg-white/90 backdrop-blur-sm overflow-visible relative cursor-pointer"
        onClick={(e) => {
          // 只有点击卡片本身时才跳转,不要在菜单打开时或点击按钮时跳转
          if (menuOpen) return;
          if ((e.target as HTMLElement).closest('button')) return;
          handleViewDetail();
        }}
      >
        {/* 置灰遮罩层 - 只覆盖卡片内容,不覆盖操作菜单 */}
        {menuOpen && (
          <div className="absolute inset-0 bg-black/30 rounded-lg z-10 pointer-events-none" />
        )}

        <CardHeader className="pb-3 overflow-visible relative">
          <div className="flex justify-between items-start">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <h3 className="font-semibold text-lg">{account.account_name}</h3>
                <Badge variant="secondary" className="text-xs">
                  {ACCOUNT_TYPE_LABELS[account.account_type]}
                </Badge>
              </div>
              {account.description && (
                <p className="text-sm text-muted-foreground line-clamp-2">
                  {account.description}
                </p>
              )}
            </div>
            <div className="flex items-center gap-1">
              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8 relative z-20"
                onClick={(e) => handleEnterPositions(e)}
                title="进入持仓"
              >
                <TrendingUp className="h-4 w-4" />
              </Button>
              <DropdownMenu open={menuOpen} onOpenChange={setMenuOpen}>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="icon" className="h-8 w-8 relative z-20">
                    <MoreVertical className="h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" sideOffset={8} className="relative z-[100] bg-white">
                  <DropdownMenuItem onClick={(e) => handleEnterPositions(e)}>
                    <TrendingUp className="h-4 w-4 mr-2" />
                    进入持仓
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={(e) => handleViewDetail(e)}>
                    <ExternalLink className="h-4 w-4 mr-2" />
                    查看详情
                  </DropdownMenuItem>
                {account.account_type === 'crypto' && (
                  <DropdownMenuItem
                    onClick={handleSync}
                    disabled={isSyncing || !account.has_api_credentials}
                  >
                    <RefreshCw className={`h-4 w-4 mr-2 ${isSyncing ? 'animate-spin' : ''}`} />
                    {isSyncing ? '同步中...' : '手动同步'}
                    {!account.has_api_credentials && (
                      <span className="text-xs text-muted-foreground ml-1">(需配置API)</span>
                    )}
                  </DropdownMenuItem>
                )}
                {account.broker === 'interactive_brokers' && (
                  <DropdownMenuItem
                    onClick={handleIBKRSync}
                    disabled={isSyncing || !account.ibkr_flex_token || !account.ibkr_flex_query_id}
                  >
                    <RefreshCw className={`h-4 w-4 mr-2 ${isSyncing ? 'animate-spin' : ''}`} />
                    {isSyncing ? '同步中...' : '手动同步 (IBKR)'}
                    {(!account.ibkr_flex_token || !account.ibkr_flex_query_id) && (
                      <span className="text-xs text-muted-foreground ml-1">(需配置Flex凭证)</span>
                    )}
                  </DropdownMenuItem>
                )}
                <DropdownMenuItem onClick={(e) => handleEdit(e)}>
                  <Edit className="h-4 w-4 mr-2" />
                  编辑
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem
                  onClick={(e) => {
                    e.stopPropagation();
                    setMenuOpen(false);
                    setShowClearDialog(true);
                  }}
                  className="text-orange-600"
                >
                  <Database className="h-4 w-4 mr-2" />
                  清除数据
                </DropdownMenuItem>
                <DropdownMenuItem
                  onClick={(e) => {
                    e.stopPropagation();
                    setMenuOpen(false);
                    onDelete(account.id);
                  }}
                  className="text-destructive"
                >
                  <Trash2 className="h-4 w-4 mr-2" />
                  删除账户
                </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {/* 标签 */}
          {account.tags && account.tags.length > 0 && (
            <div className="flex items-center gap-1 mb-3 flex-wrap">
              <Tag className="h-3 w-3 text-muted-foreground" />
              {account.tags.map((tag, index) => (
                <Badge key={index} variant="outline" className="text-xs">
                  {tag}
                </Badge>
              ))}
            </div>
          )}

          {/* 状态信息 */}
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-muted-foreground">状态</span>
              <Badge variant={account.is_active ? 'default' : 'secondary'}>
                {account.is_active ? '活跃' : '禁用'}
              </Badge>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">最后同步</span>
              <span className="text-xs">{formatDate(account.last_sync_at)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">创建时间</span>
              <span className="text-xs">{formatDate(account.created_at)}</span>
            </div>
          </div>
        </CardContent>
      </Card>

      <EditAccountDialog
        open={showEditDialog}
        onOpenChange={setShowEditDialog}
        account={account}
        onSuccess={() => {
          setShowEditDialog(false);
          onUpdate();
        }}
      />

      <AlertDialog open={showClearDialog} onOpenChange={setShowClearDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>确认清除数据？</AlertDialogTitle>
            <AlertDialogDescription>
              此操作将删除账户 <strong>{account.account_name}</strong> 的所有交易记录和持仓数据。
              <br />
              <br />
              <span className="text-red-600 font-semibold">注意：此操作不可逆！</span>
              <br />
              <br />
              如果您配置了 API 凭证，可以稍后通过"手动同步"重新导入数据。
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel disabled={isClearing}>取消</AlertDialogCancel>
            <AlertDialogAction
              onClick={handleClearData}
              disabled={isClearing}
              className="bg-orange-600 hover:bg-orange-700"
            >
              {isClearing ? '清除中...' : '确认清除'}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  );
}
