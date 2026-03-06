import { apiClient } from './client';
import type { TradeAccount, TradeAccountCreate, TradeAccountUpdate } from '../types/account';

// Re-export types for convenience
export type { TradeAccount, TradeAccountCreate, TradeAccountUpdate };

export const accountsApi = {
  // 获取所有账户
  getAccounts: async (accountType?: string): Promise<TradeAccount[]> => {
    const params = accountType ? { account_type: accountType } : {};
    const response = await apiClient.get('/trade-accounts/', { params });
    return response.data;
  },

  // 获取单个账户
  getAccount: async (id: string): Promise<TradeAccount> => {
    const response = await apiClient.get(`/trade-accounts/${id}`);
    return response.data;
  },

  // 创建账户
  createAccount: async (data: TradeAccountCreate): Promise<TradeAccount> => {
    const response = await apiClient.post('/trade-accounts/', data);
    return response.data;
  },

  // 更新账户
  updateAccount: async (id: string, data: TradeAccountUpdate): Promise<TradeAccount> => {
    const response = await apiClient.put(`/trade-accounts/${id}`, data);
    return response.data;
  },

  // 删除账户
  deleteAccount: async (id: string): Promise<void> => {
    await apiClient.delete(`/trade-accounts/${id}`);
  },

  // 获取账户统计
  getAccountStats: async () => {
    const response = await apiClient.get('/trade-accounts/stats/by-type');
    return response.data;
  },

  // 手动同步账户 (异步任务)
  syncAccount: async (id: string): Promise<{
    status: string;
    message: string;
    task_id: string;
    account_id: string;
  }> => {
    const response = await apiClient.post(`/trade-accounts/${id}/sync`);
    return response.data;
  },

  // 查询同步任务状态
  getSyncTaskStatus: async (taskId: string): Promise<{
    task_id: string;
    status: string;
    message: string;
    result?: any;
    error?: string;
    meta?: any;
  }> => {
    const response = await apiClient.get(`/trade-accounts/sync/task/${taskId}`);
    return response.data;
  },

  // 轮询任务状态直到完成
  pollSyncTask: async (
    taskId: string,
    onProgress?: (status: string) => void,
    maxAttempts: number = 60,
    interval: number = 2000
  ): Promise<{
    success: boolean;
    result?: any;
    error?: string;
  }> => {
    for (let attempt = 0; attempt < maxAttempts; attempt++) {
      const taskStatus = await accountsApi.getSyncTaskStatus(taskId);

      if (onProgress) {
        onProgress(taskStatus.status);
      }

      if (taskStatus.status === 'SUCCESS') {
        return {
          success: true,
          result: taskStatus.result,
        };
      }

      if (taskStatus.status === 'FAILURE') {
        return {
          success: false,
          error: taskStatus.error || 'Task failed',
        };
      }

      // 等待后继续轮询
      await new Promise(resolve => setTimeout(resolve, interval));
    }

    // 超时
    return {
      success: false,
      error: 'Task polling timeout',
    };
  },

  // 清除账户数据
  clearAccountData: async (id: string): Promise<{
    status: string;
    message: string;
    account_id: string;
    deleted_count: number;
  }> => {
    const response = await apiClient.delete(`/trade-accounts/${id}/data`);
    return response.data;
  },
};
