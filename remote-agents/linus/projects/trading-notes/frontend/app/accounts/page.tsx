'use client';

import { useState, useEffect } from 'react';
import { Plus, RefreshCcw, Wallet } from 'lucide-react';
import { accountsApi } from '@/lib/api/accounts';
import type { TradeAccount, AccountType } from '@/lib/types/account';
import { ACCOUNT_TYPE_LABELS } from '@/lib/types/account';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import AccountCard from './components/AccountCard';
import AddAccountDialog from './components/AddAccountDialog';
import StatsNav from '@/components/layout/StatsNav';
import PageNav from '@/components/layout/PageNav';
import { usePageTitle } from '@/lib/use-page-title';

export default function AccountsPage() {
  const [accounts, setAccounts] = useState<TradeAccount[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedType, setSelectedType] = useState<AccountType | 'all'>('all');
  const [showAddDialog, setShowAddDialog] = useState(false);

  usePageTitle('交易账户管理');

  const loadAccounts = async () => {
    try {
      setLoading(true);
      const data = await accountsApi.getAccounts(
        selectedType === 'all' ? undefined : selectedType
      );
      setAccounts(data);
    } catch (error) {
      console.error('Failed to load accounts:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAccounts();
  }, [selectedType]);

  const handleDelete = async (id: string) => {
    if (!confirm('确定要删除这个账户吗？')) return;

    try {
      await accountsApi.deleteAccount(id);
      await loadAccounts();
    } catch (error) {
      console.error('Failed to delete account:', error);
      alert('删除失败');
    }
  };

  const handleAddSuccess = () => {
    setShowAddDialog(false);
    loadAccounts();
  };

  // 按市场类型分组
  const groupedAccounts = accounts.reduce((acc, account) => {
    if (!acc[account.account_type]) {
      acc[account.account_type] = [];
    }
    acc[account.account_type].push(account);
    return acc;
  }, {} as Record<AccountType, TradeAccount[]>);

  return (
    <>
      <PageNav />
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-purple-50 to-pink-50">
        <div className="container mx-auto py-8 px-4">
          <div className="flex justify-between items-center mb-6">
            <div className="flex items-center space-x-3">
              <div className="p-3 bg-gradient-to-br from-purple-500 to-pink-600 rounded-xl shadow-lg">
                <Wallet className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-4xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
                  交易账户管理
                </h1>
                <p className="mt-1 text-gray-600">
                  管理您的交易账户，支持多个市场和交易所
                </p>
              </div>
            </div>
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="icon"
                onClick={loadAccounts}
                disabled={loading}
                className="hover:shadow-md transition-shadow"
              >
                <RefreshCcw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
              </Button>
              <Button
                onClick={() => setShowAddDialog(true)}
                className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 shadow-md"
              >
                <Plus className="h-4 w-4 mr-2" />
                添加账户
              </Button>
            </div>
          </div>

          {/* 统计导航栏 */}
          <StatsNav
            stats={[
              {
                label: '总账户数',
                value: accounts.length,
                icon: 'activity',
                trend: 'neutral'
              },
              {
                label: '币圈交易所',
                value: groupedAccounts['crypto']?.length || 0,
                icon: 'activity',
                trend: 'neutral'
              },
              {
                label: '美股账户',
                value: groupedAccounts['us_stock']?.length || 0,
                icon: 'activity',
                trend: 'neutral'
              },
              {
                label: 'A股账户',
                value: groupedAccounts['a_stock']?.length || 0,
                icon: 'activity',
                trend: 'neutral'
              },
              {
                label: '港股账户',
                value: groupedAccounts['hk_stock']?.length || 0,
                icon: 'activity',
                trend: 'neutral'
              }
            ]}
            variant="compact"
          />

          {/* 市场类型筛选 */}
          <div className="flex gap-2 mb-6 flex-wrap">
            <Button
              variant={selectedType === 'all' ? 'default' : 'outline'}
              onClick={() => setSelectedType('all')}
              size="sm"
              className={selectedType === 'all' ? 'bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 shadow-md' : 'hover:shadow-md transition-shadow'}
            >
              全部 ({accounts.length})
            </Button>
            {Object.entries(ACCOUNT_TYPE_LABELS).map(([type, label]) => {
              const count = groupedAccounts[type as AccountType]?.length || 0;
              return (
                <Button
                  key={type}
                  variant={selectedType === type ? 'default' : 'outline'}
                  onClick={() => setSelectedType(type as AccountType)}
                  size="sm"
                  className={selectedType === type ? 'bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 shadow-md' : 'hover:shadow-md transition-shadow'}
                >
                  {label} ({count})
                </Button>
              );
            })}
          </div>

          {loading ? (
            <div className="text-center py-12">
              <RefreshCcw className="h-8 w-8 animate-spin mx-auto text-muted-foreground" />
              <p className="text-muted-foreground mt-2">加载中...</p>
            </div>
          ) : accounts.length === 0 ? (
            <Card className="p-12 text-center bg-white/80 backdrop-blur-sm border-2 border-dashed shadow-lg">
              <div className="flex flex-col items-center">
                <div className="p-4 bg-gradient-to-br from-purple-100 to-pink-100 rounded-full mb-4">
                  <Wallet className="w-12 h-12 text-purple-600" />
                </div>
                <p className="text-muted-foreground mb-4 text-lg">
                  还没有添加任何交易账户
                </p>
                <Button
                  onClick={() => setShowAddDialog(true)}
                  className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 shadow-md"
                >
                  <Plus className="h-4 w-4 mr-2" />
                  添加第一个账户
                </Button>
              </div>
            </Card>
          ) : selectedType === 'all' ? (
            // 按市场分组显示
            <div className="space-y-8">
              {(Object.keys(ACCOUNT_TYPE_LABELS) as AccountType[]).map((type) => {
                const typeAccounts = groupedAccounts[type] || [];
                if (typeAccounts.length === 0) return null;

                return (
                  <div key={type}>
                    <div className="flex items-center mb-4">
                      <div className="w-1 h-6 bg-gradient-to-b from-purple-500 to-pink-600 rounded-full mr-3"></div>
                      <h2 className="text-xl font-bold text-gray-800">
                        {ACCOUNT_TYPE_LABELS[type]}
                      </h2>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {typeAccounts.map((account) => (
                        <AccountCard
                          key={account.id}
                          account={account}
                          onDelete={handleDelete}
                          onUpdate={loadAccounts}
                        />
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            // 单一类型显示
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {accounts.map((account) => (
                <AccountCard
                  key={account.id}
                  account={account}
                  onDelete={handleDelete}
                  onUpdate={loadAccounts}
                />
              ))}
            </div>
          )}

          <AddAccountDialog
            open={showAddDialog}
            onOpenChange={setShowAddDialog}
            onSuccess={handleAddSuccess}
          />
        </div>
      </div>
    </>
  );
}
