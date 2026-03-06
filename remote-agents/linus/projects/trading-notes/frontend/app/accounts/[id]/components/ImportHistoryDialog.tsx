'use client';

import { useState, useEffect } from 'react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { importApi, ImportHistory } from '@/lib/api/import';
import { FileText, CheckCircle, XCircle, AlertCircle, Calendar } from 'lucide-react';

interface ImportHistoryDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  accountId: string;
  accountName: string;
}

const BROKER_LABELS: Record<string, string> = {
  tonghuashun: '同花顺',
  gtja: '国泰君安',
  guosen: '国信证券',
  moomoo: 'moomoo',
  ibkr: '盈透证券',
  generic: '通用格式',
};

export default function ImportHistoryDialog({
  open,
  onOpenChange,
  accountId,
  accountName,
}: ImportHistoryDialogProps) {
  const [histories, setHistories] = useState<ImportHistory[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (open) {
      loadImportHistory();
    }
  }, [open, accountId]);

  const loadImportHistory = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await importApi.getImportHistory(accountId, 0, 50);
      setHistories(response.imports);
    } catch (err: any) {
      setError(err.response?.data?.detail || '加载导入历史失败');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getStatusBadge = (history: ImportHistory) => {
    if (history.success_count === history.total_rows && history.failed_count === 0) {
      return (
        <Badge className="bg-green-100 text-green-800 hover:bg-green-100">
          <CheckCircle className="h-3 w-3 mr-1" />
          全部成功
        </Badge>
      );
    } else if (history.success_count > 0 && history.failed_count > 0) {
      return (
        <Badge className="bg-yellow-100 text-yellow-800 hover:bg-yellow-100">
          <AlertCircle className="h-3 w-3 mr-1" />
          部分成功
        </Badge>
      );
    } else if (history.failed_count === history.total_rows) {
      return (
        <Badge variant="destructive">
          <XCircle className="h-3 w-3 mr-1" />
          全部失败
        </Badge>
      );
    }
    return null;
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-3xl max-h-[80vh]">
        <DialogHeader>
          <DialogTitle>导入历史记录</DialogTitle>
          <DialogDescription>
            账户 <span className="font-semibold">{accountName}</span> 的文件导入历史
          </DialogDescription>
        </DialogHeader>

        <ScrollArea className="h-[500px] pr-4">
          {loading && (
            <div className="flex items-center justify-center py-12">
              <div className="text-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 mx-auto mb-2"></div>
                <p className="text-sm text-gray-500">加载中...</p>
              </div>
            </div>
          )}

          {error && (
            <div className="flex items-center justify-center py-12">
              <div className="text-center text-red-600">
                <AlertCircle className="h-8 w-8 mx-auto mb-2" />
                <p className="text-sm">{error}</p>
              </div>
            </div>
          )}

          {!loading && !error && histories.length === 0 && (
            <div className="flex flex-col items-center justify-center py-12 text-gray-500">
              <FileText className="h-12 w-12 mb-3 text-gray-300" />
              <p className="text-sm">暂无导入历史记录</p>
            </div>
          )}

          {!loading && !error && histories.length > 0 && (
            <div className="space-y-3">
              {histories.map((history) => (
                <div
                  key={history.id}
                  className="border rounded-lg p-4 hover:bg-gray-50 transition-colors"
                >
                  {/* 文件信息头 */}
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center space-x-2 flex-1">
                      <FileText className="h-5 w-5 text-blue-500 flex-shrink-0" />
                      <div className="min-w-0 flex-1">
                        <p className="font-medium text-sm truncate">
                          {history.filename}
                        </p>
                        <div className="flex items-center space-x-2 mt-1">
                          <Badge variant="outline" className="text-xs">
                            {BROKER_LABELS[history.broker_template] || history.broker_template}
                          </Badge>
                          {getStatusBadge(history)}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* 统计信息 */}
                  <div className="grid grid-cols-4 gap-4 mb-3 text-center">
                    <div className="bg-gray-50 rounded p-2">
                      <p className="text-xs text-gray-500 mb-1">总行数</p>
                      <p className="text-lg font-semibold">{history.total_rows}</p>
                    </div>
                    <div className="bg-green-50 rounded p-2">
                      <p className="text-xs text-gray-500 mb-1">成功</p>
                      <p className="text-lg font-semibold text-green-600">
                        {history.success_count}
                      </p>
                    </div>
                    <div className="bg-red-50 rounded p-2">
                      <p className="text-xs text-gray-500 mb-1">失败</p>
                      <p className="text-lg font-semibold text-red-600">
                        {history.failed_count}
                      </p>
                    </div>
                    <div className="bg-yellow-50 rounded p-2">
                      <p className="text-xs text-gray-500 mb-1">重复</p>
                      <p className="text-lg font-semibold text-yellow-600">
                        {history.duplicate_count}
                      </p>
                    </div>
                  </div>

                  {/* 时间信息 */}
                  <div className="flex items-center text-xs text-gray-500">
                    <Calendar className="h-3 w-3 mr-1" />
                    <span>导入时间: {formatDate(history.created_at)}</span>
                  </div>

                  {/* 错误详情 */}
                  {history.error_details && history.error_details.errors.length > 0 && (
                    <details className="mt-3">
                      <summary className="text-xs cursor-pointer text-gray-700 hover:text-gray-900">
                        查看错误详情 ({history.error_details.errors.length} 个错误)
                      </summary>
                      <div className="mt-2 max-h-32 overflow-y-auto bg-gray-50 rounded p-2 space-y-1">
                        {history.error_details.errors.slice(0, 10).map((err, idx) => (
                          <p key={idx} className="text-xs text-gray-600">
                            <span className="font-medium">第 {err.row} 行:</span> {err.error}
                          </p>
                        ))}
                        {history.error_details.errors.length > 10 && (
                          <p className="text-xs text-gray-500 italic">
                            ...还有 {history.error_details.errors.length - 10} 个错误未显示
                          </p>
                        )}
                      </div>
                    </details>
                  )}
                </div>
              ))}
            </div>
          )}
        </ScrollArea>
      </DialogContent>
    </Dialog>
  );
}
