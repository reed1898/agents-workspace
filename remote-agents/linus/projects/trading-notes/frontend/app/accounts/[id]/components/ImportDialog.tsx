'use client';

import { useState, useRef } from 'react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Progress } from '@/components/ui/progress';
import { Upload, FileText, CheckCircle, AlertCircle, X } from 'lucide-react';
import { importApi, CSVImportResponse } from '@/lib/api/import';
import { toast } from 'sonner';

interface ImportDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  accountId: string;
  accountName: string;
  onImportSuccess?: () => void;
}

export default function ImportDialog({
  open,
  onOpenChange,
  accountId,
  accountName,
  onImportSuccess,
}: ImportDialogProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [importing, setImporting] = useState(false);
  const [result, setResult] = useState<CSVImportResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  // 处理文件选择
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const lowerName = file.name.toLowerCase();
      const isSupported = ['.csv', '.xls', '.xlsx'].some((ext) => lowerName.endsWith(ext));

      // 验证文件类型
      if (!isSupported) {
        setError('请选择CSV或Excel文件');
        return;
      }

      // 验证文件大小 (10MB)
      if (file.size > 10 * 1024 * 1024) {
        setError('文件大小不能超过10MB');
        return;
      }

      setSelectedFile(file);
      setError(null);

      // 一键导入: 自动触发导入流程
      handleImport(file);
    }
  };

  // 执行导入
  const handleImport = async (file: File) => {
    setImporting(true);
    setError(null);

    try {
      const response = await importApi.uploadCsv(accountId, file);
      setResult(response);

      // 显示成功提示
      if (response.success_count > 0) {
        toast.success('导入成功', {
          description: response.message,
        });

        // 调用成功回调
        if (onImportSuccess) {
          onImportSuccess();
        }
      } else {
        toast.error('导入失败', {
          description: response.message,
        });
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || '导入失败,请稍后重试';
      setError(errorMessage);

      toast.error('导入错误', {
        description: errorMessage,
      });
    } finally {
      setImporting(false);
    }
  };

  // 重新选择文件
  const handleReset = () => {
    setSelectedFile(null);
    setResult(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  // 关闭对话框
  const handleClose = () => {
    handleReset();
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={handleClose}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>导入交易记录</DialogTitle>
          <DialogDescription>
            为账户 <span className="font-semibold">{accountName}</span> 导入交易记录文件
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4 py-4">
          {/* 说明文字 */}
          {!result && (
            <Alert>
              <AlertDescription className="text-sm text-muted-foreground">
                系统将根据账户设置的券商类型自动选择对应的解析模板。
                <br />
                支持CSV/Excel文件,国信证券支持资金流水/历史成交查询Excel导入
              </AlertDescription>
            </Alert>
          )}

          {/* 文件上传区域 */}
          {!result && !importing && (
            <div className="space-y-2">
              <Label>选择CSV/Excel文件</Label>
              <div
                className="border-2 border-dashed rounded-lg p-8 text-center cursor-pointer hover:border-primary hover:bg-gray-50 transition-colors"
                onClick={() => fileInputRef.current?.click()}
              >
                <Upload className="mx-auto h-12 w-12 text-gray-400 mb-2" />
                <p className="text-sm font-medium text-gray-700 mb-1">
                  点击选择CSV/Excel文件或拖拽文件到此处
                </p>
                <p className="text-xs text-gray-500">
                  支持.csv/.xls/.xlsx格式,文件大小不超过10MB
                </p>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".csv,.xls,.xlsx"
                  onChange={handleFileChange}
                  className="hidden"
                />
              </div>
            </div>
          )}

          {/* 导入中状态 */}
          {importing && (
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <FileText className="h-5 w-5 text-blue-500" />
                <span className="text-sm font-medium">{selectedFile?.name}</span>
              </div>
              <div>
                <Progress value={50} className="h-2" />
                <p className="text-sm text-gray-600 mt-2 text-center">
                  正在导入交易记录,请稍候...
                </p>
              </div>
            </div>
          )}

          {/* 导入结果 */}
          {result && (
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <FileText className="h-5 w-5 text-blue-500" />
                  <span className="text-sm font-medium">{selectedFile?.name}</span>
                </div>
                <Button variant="ghost" size="sm" onClick={handleReset}>
                  <X className="h-4 w-4" />
                </Button>
              </div>

              {/* 成功统计 */}
              {result.success_count > 0 && (
                <Alert className="border-green-200 bg-green-50">
                  <CheckCircle className="h-4 w-4 text-green-600" />
                  <AlertDescription className="ml-2">
                    <div className="space-y-1">
                      <p className="font-semibold text-green-800">
                        成功导入 {result.success_count} 条交易记录
                      </p>
                      {result.duplicate_count > 0 && (
                        <p className="text-sm text-gray-600">
                          跳过重复记录 {result.duplicate_count} 条
                        </p>
                      )}
                    </div>
                  </AlertDescription>
                </Alert>
              )}

              {/* 失败统计 */}
              {result.failed_count > 0 && (
                <Alert className="border-yellow-200 bg-yellow-50">
                  <AlertCircle className="h-4 w-4 text-yellow-600" />
                  <AlertDescription className="ml-2">
                    <p className="font-semibold text-yellow-800">
                      {result.failed_count} 条记录导入失败
                    </p>
                    {result.error_details && result.error_details.length > 0 && (
                      <details className="mt-2">
                        <summary className="text-sm cursor-pointer text-gray-700">
                          查看错误详情
                        </summary>
                        <div className="mt-2 max-h-40 overflow-y-auto space-y-1">
                          {result.error_details.slice(0, 10).map((err, idx) => (
                            <p key={idx} className="text-xs text-gray-600">
                              第 {err.row} 行: {err.error}
                            </p>
                          ))}
                          {result.error_details.length > 10 && (
                            <p className="text-xs text-gray-500 italic">
                              ...还有 {result.error_details.length - 10} 个错误
                            </p>
                          )}
                        </div>
                      </details>
                    )}
                  </AlertDescription>
                </Alert>
              )}

              {/* 操作按钮 */}
              <div className="flex justify-end space-x-2">
                <Button variant="outline" onClick={handleReset}>
                  继续导入
                </Button>
                <Button onClick={handleClose}>完成</Button>
              </div>
            </div>
          )}

          {/* 错误提示 */}
          {error && !result && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}
