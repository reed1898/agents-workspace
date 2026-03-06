'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Upload, X, Loader2 } from 'lucide-react';
import Image from 'next/image';
import { toast } from 'sonner';

interface ChartImageUploadProps {
  tradeId?: string;
  currentUrl?: string;
  onUploadSuccess?: (url: string) => void;
  className?: string;
}

export function ChartImageUpload({
  tradeId,
  currentUrl,
  onUploadSuccess,
  className
}: ChartImageUploadProps) {
  const [uploading, setUploading] = useState(false);
  const [imageUrl, setImageUrl] = useState(currentUrl);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !tradeId) return;

    // 验证文件类型
    if (!file.type.startsWith('image/')) {
      toast.error('请选择图片文件');
      return;
    }

    // 验证文件大小 (5MB)
    if (file.size > 5 * 1024 * 1024) {
      toast.error('图片大小不能超过 5MB');
      return;
    }

    setUploading(true);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const token = localStorage.getItem('access_token');
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/trades/${tradeId}/upload-chart`,
        {
          method: 'POST',
          body: formData,
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      if (!response.ok) {
        throw new Error('上传失败');
      }

      const data = await response.json();
      const newUrl = `${process.env.NEXT_PUBLIC_API_URL}${data.chart_url}`;

      setImageUrl(newUrl);
      toast.success('K线图上传成功');

      if (onUploadSuccess) {
        onUploadSuccess(newUrl);
      }
    } catch (error) {
      console.error('Upload failed:', error);
      toast.error('上传失败，请重试');
    } finally {
      setUploading(false);
    }
  };

  const handleRemove = () => {
    setImageUrl(undefined);
    // 这里可以添加删除后端图片的逻辑
  };

  return (
    <div className={`space-y-3 ${className || ''}`}>
      <Label className="text-sm font-medium">K线图</Label>

      {imageUrl && (
        <div className="relative border rounded-lg p-2 bg-muted/20">
          <button
            onClick={handleRemove}
            className="absolute top-3 right-3 p-1 bg-background rounded-full shadow-sm hover:bg-destructive hover:text-destructive-foreground transition-colors"
            type="button"
          >
            <X className="w-4 h-4" />
          </button>
          <div className="relative w-full h-64">
            <Image
              src={imageUrl}
              alt="K线图"
              fill
              className="object-contain rounded"
            />
          </div>
        </div>
      )}

      <div>
        <input
          type="file"
          accept="image/*"
          onChange={handleUpload}
          className="hidden"
          id="chart-upload"
          disabled={uploading || !tradeId}
        />
        <Label htmlFor="chart-upload">
          <Button
            variant="outline"
            size="sm"
            asChild
            disabled={uploading || !tradeId}
          >
            <span className="cursor-pointer">
              {uploading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  上传中...
                </>
              ) : (
                <>
                  <Upload className="w-4 h-4 mr-2" />
                  {imageUrl ? '更换图片' : '上传K线图'}
                </>
              )}
            </span>
          </Button>
        </Label>
      </div>

      {!tradeId && (
        <p className="text-xs text-muted-foreground">
          请先保存交易记录后再上传图片
        </p>
      )}
    </div>
  );
}
