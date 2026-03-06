import { apiClient } from '../api-client';

export interface IBKRImportRequest {
  token: string;
  query_id: string;
  save_credentials?: boolean;
}

export interface IBKRImportResponse {
  task_id: string;
  message: string;
  account_id: string;
}

export interface IBKRTaskStatus {
  task_id: string;
  status: 'PENDING' | 'PROGRESS' | 'SUCCESS' | 'FAILURE';
  progress: number;
  result?: {
    status: string;
    account_id: string;
    imported_count?: number;
    skipped_count?: number;
    error_count?: number;
    error?: string;
    completed_at: string;
  };
  error?: string;
}

/**
 * 使用 IBKR Flex API 导入交易数据
 */
export async function importIBKRTrades(
  accountId: string,
  request: IBKRImportRequest
): Promise<IBKRImportResponse> {
  const response = await apiClient.post(`/ibkr/${accountId}/import`, request);
  return response.data;
}

/**
 * 使用已保存的凭证导入 IBKR 交易数据
 */
export async function importIBKRWithSavedCredentials(
  accountId: string
): Promise<IBKRImportResponse> {
  console.log('importIBKRWithSavedCredentials called with accountId:', accountId);
  const url = `/ibkr/${accountId}/import-with-saved-credentials`;
  console.log('Request URL:', url);

  try {
    const response = await apiClient.post(url);
    console.log('API response:', response);
    return response.data;
  } catch (error: any) {
    console.error('API error:', error);
    console.error('Error response:', error.response);
    throw error;
  }
}

/**
 * 获取导入任务状态
 */
export async function getIBKRTaskStatus(taskId: string): Promise<IBKRTaskStatus> {
  const response = await apiClient.get(`/ibkr/task/${taskId}`);
  return response.data;
}

/**
 * 删除 IBKR Flex 凭证
 */
export async function deleteIBKRCredentials(accountId: string): Promise<void> {
  await apiClient.delete(`/ibkr/${accountId}/credentials`);
}

/**
 * 轮询任务状态直到完成
 */
export async function pollIBKRTaskStatus(
  taskId: string,
  onProgress?: (status: IBKRTaskStatus) => void,
  intervalMs: number = 2000,
  maxAttempts: number = 60
): Promise<IBKRTaskStatus> {
  let attempts = 0;

  while (attempts < maxAttempts) {
    const status = await getIBKRTaskStatus(taskId);

    if (onProgress) {
      onProgress(status);
    }

    if (status.status === 'SUCCESS' || status.status === 'FAILURE') {
      return status;
    }

    attempts++;
    await new Promise(resolve => setTimeout(resolve, intervalMs));
  }

  throw new Error('Task polling timeout');
}
