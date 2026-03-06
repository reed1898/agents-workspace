'use client';

import { useState } from 'react';
import { X } from 'lucide-react';
import { accountsApi } from '@/lib/api/accounts';
import type { TradeAccountCreate, AccountType, CryptoSubType } from '@/lib/types/account';
import { ACCOUNT_TYPE_OPTIONS, CRYPTO_SUB_TYPE_OPTIONS, BROKER_OPTIONS } from '@/lib/types/account';
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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';

interface AddAccountDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSuccess: () => void;
}

export default function AddAccountDialog({
  open,
  onOpenChange,
  onSuccess,
}: AddAccountDialogProps) {
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState<TradeAccountCreate>({
    account_name: '',
    account_type: 'crypto',
    crypto_sub_type: 'binance_spot',  // 默认为现货
    description: '',
    tags: [],
    sync_start_date: undefined,
    api_key: '',
    api_secret: '',
  });
  const [tagInput, setTagInput] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.account_name.trim()) {
      alert('请输入账户名称');
      return;
    }

    try {
      setLoading(true);
      await accountsApi.createAccount(formData);
      onSuccess();
      // 重置表单
      setFormData({
        account_name: '',
        account_type: 'crypto',
        description: '',
        tags: [],
        sync_start_date: undefined,
        api_key: '',
        api_secret: '',
      });
      setTagInput('');
    } catch (error: any) {
      console.error('Failed to create account:', error);
      alert(error.response?.data?.detail || '创建失败');
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
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-visible">
        <DialogHeader>
          <DialogTitle>添加交易账户</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4 max-h-[calc(90vh-8rem)] overflow-y-auto pr-2">
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

          {/* 市场类型 */}
          <div>
            <Label htmlFor="account_type">
              市场类型 <span className="text-destructive">*</span>
            </Label>
            <Select
              value={formData.account_type}
              onValueChange={(value) =>
                setFormData({ ...formData, account_type: value as AccountType })
              }
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {ACCOUNT_TYPE_OPTIONS.map((option) => (
                  <SelectItem key={option.value} value={option.value}>
                    <div>
                      <div className="font-medium">{option.label}</div>
                      <div className="text-xs text-muted-foreground">
                        {option.description}
                      </div>
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* 券商/交易所选择 */}
          {BROKER_OPTIONS[formData.account_type as keyof typeof BROKER_OPTIONS] && (
            <div>
              <Label htmlFor="broker">
                券商/交易所
              </Label>
              <Select
                value={formData.broker || ''}
                onValueChange={(value) =>
                  setFormData({ ...formData, broker: value })
                }
              >
                <SelectTrigger>
                  <SelectValue placeholder="选择券商/交易所" />
                </SelectTrigger>
                <SelectContent>
                  {BROKER_OPTIONS[formData.account_type as keyof typeof BROKER_OPTIONS].map((option) => (
                    <SelectItem key={option.value} value={option.value}>
                      <div>
                        <div className="font-medium">{option.label}</div>
                        <div className="text-xs text-muted-foreground">
                          {option.description}
                        </div>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          )}

          {/* 币安账户类型 - 只在选择了 crypto 时显示 */}
          {formData.account_type === 'crypto' && (
            <div>
              <Label htmlFor="crypto_sub_type">
                交易类型 <span className="text-destructive">*</span>
              </Label>
              <Select
                value={formData.crypto_sub_type || 'binance_spot'}
                onValueChange={(value) =>
                  setFormData({ ...formData, crypto_sub_type: value as CryptoSubType })
                }
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {CRYPTO_SUB_TYPE_OPTIONS.map((option) => (
                    <SelectItem key={option.value} value={option.value}>
                      <div>
                        <div className="font-medium">{option.label}</div>
                        <div className="text-xs text-muted-foreground">
                          {option.description}
                        </div>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          )}

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
              添加 API 密钥后可以自动同步交易数据。密钥将被加密存储。
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
                placeholder="输入 API Key"
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
                placeholder="输入 API Secret"
              />
            </div>
          </div>

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
              {loading ? '创建中...' : '创建账户'}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
