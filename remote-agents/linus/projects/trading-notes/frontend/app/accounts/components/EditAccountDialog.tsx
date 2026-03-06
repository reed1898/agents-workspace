'use client';

import { useState, useEffect } from 'react';
import { X } from 'lucide-react';
import { accountsApi } from '@/lib/api/accounts';
import type { TradeAccount, TradeAccountUpdate } from '@/lib/types/account';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Switch } from '@/components/ui/switch';
import { Badge } from '@/components/ui/badge';

interface EditAccountDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  account: TradeAccount;
  onSuccess: () => void;
}

export default function EditAccountDialog({
  open,
  onOpenChange,
  account,
  onSuccess,
}: EditAccountDialogProps) {
  const getDefaultCashCurrency = (accountType: string) => {
    if (accountType === 'a_stock') return '人民币';
    if (accountType === 'hk_stock') return 'HKD';
    return 'USD';
  };

  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState<TradeAccountUpdate>({
    account_name: account.account_name,
    description: account.description || '',
    tags: account.tags || [],
    is_active: account.is_active,
    sync_start_date: account.sync_start_date ? account.sync_start_date.split('T')[0] : undefined,
    api_key: '',
    api_secret: '',
    ibkr_flex_token: account.ibkr_flex_token || '',
    ibkr_flex_query_id: account.ibkr_flex_query_id || '',
    cash_balance: account.cash_balance ?? '',
    cash_currency: account.cash_currency ?? '',
  });
  const [tagInput, setTagInput] = useState('');

  useEffect(() => {
    // Extract just the date part from datetime string (yyyy-MM-dd)
    const syncStartDate = account.sync_start_date
      ? account.sync_start_date.split('T')[0]
      : undefined;

    setFormData({
      account_name: account.account_name,
      description: account.description || '',
      tags: account.tags || [],
      is_active: account.is_active,
      sync_start_date: syncStartDate,
      api_key: '',
      api_secret: '',
      ibkr_flex_token: account.ibkr_flex_token || '',
      ibkr_flex_query_id: account.ibkr_flex_query_id || '',
      cash_balance: account.cash_balance ?? '',
      cash_currency: account.cash_currency ?? '',
    });
  }, [account]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.account_name?.trim()) {
      alert('请输入账户名称');
      return;
    }

    try {
      setLoading(true);

      // 只在填写了新的 API 凭证时才发送
      const updateData: TradeAccountUpdate = {
        account_name: formData.account_name,
        description: formData.description,
        tags: formData.tags,
        is_active: formData.is_active,
        sync_start_date: formData.sync_start_date,
      };

      const cashBalanceRaw = (formData.cash_balance ?? '').toString().trim();
      const cashCurrencyRaw = (formData.cash_currency ?? '').toString().trim();
      if (cashBalanceRaw) {
        const normalized = cashBalanceRaw.replace(/,/g, '');
        if (Number.isNaN(Number(normalized))) {
          alert('剩余资金格式不正确，请输入数字');
          setLoading(false);
          return;
        }
        updateData.cash_balance = normalized;
        updateData.cash_currency = cashCurrencyRaw || getDefaultCashCurrency(account.account_type);
      }

      if (cashCurrencyRaw) {
        updateData.cash_currency = cashCurrencyRaw;
      }

      if (formData.api_key && formData.api_key.trim()) {
        updateData.api_key = formData.api_key;
      }

      if (formData.api_secret && formData.api_secret.trim()) {
        updateData.api_secret = formData.api_secret;
      }

      // IBKR Flex 凭证
      if (formData.ibkr_flex_token && formData.ibkr_flex_token.trim()) {
        updateData.ibkr_flex_token = formData.ibkr_flex_token;
      }

      if (formData.ibkr_flex_query_id && formData.ibkr_flex_query_id.trim()) {
        updateData.ibkr_flex_query_id = formData.ibkr_flex_query_id;
      }

      await accountsApi.updateAccount(account.id, updateData);
      onSuccess();
    } catch (error: any) {
      console.error('Failed to update account:', error);
      alert(error.response?.data?.detail || '更新失败');
    } finally {
      setLoading(false);
    }
  };

  const handleAddTag = () => {
    const tag = tagInput.trim();
    if (tag && !formData.tags?.includes(tag)) {
      setFormData({
        ...formData,
        tags: [...(formData.tags || []), tag],
      });
      setTagInput('');
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setFormData({
      ...formData,
      tags: formData.tags?.filter((tag) => tag !== tagToRemove),
    });
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddTag();
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>编辑交易账户</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* 账户名称 */}
          <div>
            <Label htmlFor="account_name">
              账户名称 <span className="text-destructive">*</span>
            </Label>
            <Input
              id="account_name"
              value={formData.account_name}
              onChange={(e) =>
                setFormData({ ...formData, account_name: e.target.value })
              }
              placeholder="例如: Binance 主账户"
              required
            />
          </div>

          {/* 描述 */}
          <div>
            <Label htmlFor="description">描述</Label>
            <Textarea
              id="description"
              value={formData.description}
              onChange={(e) =>
                setFormData({ ...formData, description: e.target.value })
              }
              placeholder="账户用途、备注等"
              rows={3}
            />
          </div>

          {/* 标签 */}
          <div>
            <Label htmlFor="tags">标签</Label>
            <div className="flex gap-2 mb-2">
              <Input
                id="tags"
                value={tagInput}
                onChange={(e) => setTagInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="输入标签后按回车添加"
              />
              <Button type="button" onClick={handleAddTag} variant="outline">
                添加
              </Button>
            </div>
            {formData.tags && formData.tags.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {formData.tags.map((tag) => (
                  <Badge key={tag} variant="secondary" className="pl-2 pr-1">
                    {tag}
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      className="h-4 w-4 ml-1 hover:bg-transparent"
                      onClick={() => handleRemoveTag(tag)}
                    >
                      <X className="h-3 w-3" />
                    </Button>
                  </Badge>
                ))}
              </div>
            )}
          </div>

          {/* 账户状态 */}
          <div className="flex items-center justify-between">
            <Label htmlFor="is_active">账户状态</Label>
            <div className="flex items-center gap-2">
              <span className="text-sm text-muted-foreground">
                {formData.is_active ? '活跃' : '禁用'}
              </span>
              <Switch
                id="is_active"
                checked={formData.is_active}
                onCheckedChange={(checked) =>
                  setFormData({ ...formData, is_active: checked })
                }
              />
            </div>
          </div>

          {/* 余额设置 */}
          <div className="space-y-3 pt-4 border-t">
            <h4 className="font-medium text-sm">余额设置 (可选)</h4>
            <p className="text-xs text-muted-foreground">
              剩余资金用于资产汇总展示。部分券商导入不会自动更新，请在此手动维护。
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              <div className="md:col-span-2">
                <Label htmlFor="cash_balance">剩余资金</Label>
                <Input
                  id="cash_balance"
                  value={(formData.cash_balance ?? '').toString()}
                  onChange={(e) =>
                    setFormData({ ...formData, cash_balance: e.target.value })
                  }
                  placeholder="例如: 81618.03"
                />
              </div>
              <div>
                <Label htmlFor="cash_currency">币种</Label>
                <Input
                  id="cash_currency"
                  value={(formData.cash_currency ?? '').toString()}
                  onChange={(e) =>
                    setFormData({ ...formData, cash_currency: e.target.value })
                  }
                  placeholder={getDefaultCashCurrency(account.account_type)}
                />
              </div>
            </div>
          </div>

          {/* 同步设置 */}
          <div className="space-y-3 pt-4 border-t">
            <h4 className="font-medium text-sm">同步设置 (可选)</h4>

            <div>
              <Label htmlFor="sync_start_date">同步起始日期</Label>
              <Input
                id="sync_start_date"
                type="date"
                value={formData.sync_start_date || ''}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    sync_start_date: e.target.value || undefined
                  })
                }
              />
              <p className="text-xs text-muted-foreground mt-1">
                只同步此日期之后的交易数据,留空则同步所有历史数据
              </p>
            </div>
          </div>

          {/* API 凭证 */}
          <div className="space-y-3 pt-4 border-t">
            <h4 className="font-medium text-sm">API 凭证 (可选)</h4>
            <p className="text-xs text-muted-foreground">
              更新 API 密钥后可以自动同步交易数据。留空则保持原有密钥不变。密钥将被加密存储。
            </p>

            <div>
              <Label htmlFor="api_key">API Key</Label>
              <Input
                id="api_key"
                type="password"
                value={formData.api_key}
                onChange={(e) =>
                  setFormData({ ...formData, api_key: e.target.value })
                }
                placeholder="留空保持不变"
              />
            </div>

            <div>
              <Label htmlFor="api_secret">API Secret</Label>
              <Input
                id="api_secret"
                type="password"
                value={formData.api_secret}
                onChange={(e) =>
                  setFormData({ ...formData, api_secret: e.target.value })
                }
                placeholder="留空保持不变"
              />
            </div>
          </div>

          {/* IBKR Flex 凭证 (仅美股账户显示) */}
          {account.account_type === 'us_stock' && account.broker === 'interactive_brokers' && (
            <div className="space-y-3 pt-4 border-t">
              <h4 className="font-medium text-sm">IBKR Flex Query 凭证 (可选)</h4>
              <p className="text-xs text-muted-foreground">
                配置后可通过 IBKR Flex API 自动同步交易数据。
                <a
                  href="https://portal.interactivebrokers.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-primary hover:underline ml-1"
                >
                  获取 Token 和 Query ID
                </a>
              </p>

              <div>
                <Label htmlFor="ibkr_flex_token">Flex Query Token</Label>
                <Input
                  id="ibkr_flex_token"
                  type="text"
                  value={formData.ibkr_flex_token}
                  onChange={(e) =>
                    setFormData({ ...formData, ibkr_flex_token: e.target.value })
                  }
                  placeholder="留空保持不变"
                />
              </div>

              <div>
                <Label htmlFor="ibkr_flex_query_id">Flex Query ID</Label>
                <Input
                  id="ibkr_flex_query_id"
                  type="text"
                  value={formData.ibkr_flex_query_id}
                  onChange={(e) =>
                    setFormData({ ...formData, ibkr_flex_query_id: e.target.value })
                  }
                  placeholder="留空保持不变"
                />
              </div>
            </div>
          )}


          {/* 按钮 */}
          <div className="flex justify-end gap-2 pt-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
              disabled={loading}
            >
              取消
            </Button>
            <Button type="submit" disabled={loading}>
              {loading ? '保存中...' : '保存'}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
