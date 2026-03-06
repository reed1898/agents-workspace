/**
 * 导入API客户端
 */

import { apiClient } from './client';

/**
 * 导入历史记录
 */
export interface ImportHistory {
  id: string;
  account_id: string;
  user_id: string;
  filename: string;
  broker_template: string;
  import_source: string;
  total_rows: number;
  success_count: number;
  failed_count: number;
  duplicate_count: number;
  error_details?: {
    errors: Array<{
      row: number | string;
      error: string;
    }>;
  } | null;
  created_at: string;
  completed_at?: string | null;
}

/**
 * 导入响应
 */
export interface CSVImportResponse {
  import_id: string;
  total_rows: number;
  success_count: number;
  failed_count: number;
  duplicate_count: number;
  error_details?: Array<{
    row: number | string;
    error: string;
  }> | null;
  message: string;
}

export interface GmailSyncResponse {
  files_imported: number;
  files_skipped: number;
  files_failed: number;
  total_success_count: number;
  total_failed_count: number;
  total_duplicate_count: number;
  message: string;
  details?: Array<{
    filename: string;
    import_id?: string | null;
    success_count: number;
    failed_count: number;
    duplicate_count: number;
    message: string;
  }>;
}

export interface GmailOAuthStartResponse {
  auth_url: string;
}

/**
 * 导入历史列表响应
 */
export interface ImportHistoryListResponse {
  imports: ImportHistory[];
  total: number;
}

/**
 * 券商模板
 */
export interface BrokerTemplate {
  value: string;
  label: string;
  description: string;
}

/**
 * 导入API方法
 */
export const importApi = {
  /**
   * 上传CSV/Excel文件并导入交易记录
   * 会根据账户设置的券商类型自动选择解析模板
   */
  uploadCsv: async (
    accountId: string,
    file: File
  ): Promise<CSVImportResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('account_id', accountId);

    const response = await apiClient.post<CSVImportResponse>(
      '/import/csv-upload',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    return response.data;
  },

  /**
   * 获取指定账户的导入历史
   */
  getImportHistory: async (
    accountId: string,
    skip: number = 0,
    limit: number = 20
  ): Promise<ImportHistoryListResponse> => {
    const response = await apiClient.get<ImportHistoryListResponse>(
      `/import/history/${accountId}`,
      {
        params: { skip, limit },
      }
    );

    return response.data;
  },

  /**
   * 获取支持的券商模板列表
   */
  getSupportedTemplates: async (): Promise<BrokerTemplate[]> => {
    const response = await apiClient.get<BrokerTemplate[]>('/import/templates');
    return response.data;
  },

  /**
   * 从 Gmail 同步国泰海通邮件附件
   */
  syncGmail: async (
    accountId: string,
    sinceDays: number = 7
  ): Promise<GmailSyncResponse> => {
    const response = await apiClient.post<GmailSyncResponse>('/import/gmail-sync', null, {
      params: { account_id: accountId, since_days: sinceDays },
    });
    return response.data;
  },

  /**
   * 发起 Gmail OAuth 授权
   */
  startGmailOAuth: async (accountId: string): Promise<GmailOAuthStartResponse> => {
    const response = await apiClient.get<GmailOAuthStartResponse>('/import/gmail/oauth/start', {
      params: { account_id: accountId },
    });
    return response.data;
  },
};
