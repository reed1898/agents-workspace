import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
import { Trade, TradeCreate, TradeListResponse, TradeStats, ActionType, TradeReviewData, BatchReviewRequest } from '@/types/trade';
import { Position, PositionListResponse, PositionStats, PositionSummary } from '@/types/position';
import { DashboardSummary } from '@/types/dashboard';
import { StrategySettings } from '@/types/strategy-settings';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class APIClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: `${API_URL}/api/v1`,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // 请求拦截器 - 添加 Authorization header
    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // 响应拦截器 - 处理错误
    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          // Token 过期,尝试刷新
          const refreshToken = localStorage.getItem('refresh_token');
          if (refreshToken) {
            try {
              const response = await axios.post(
                `${API_URL}/api/v1/auth/refresh`,
                { refresh_token: refreshToken }
              );
              localStorage.setItem('access_token', response.data.access_token);
              localStorage.setItem('refresh_token', response.data.refresh_token);

              // 重试原请求
              error.config.headers.Authorization = `Bearer ${response.data.access_token}`;
              return this.client.request(error.config);
            } catch (refreshError) {
              // 刷新失败,清除 token 并跳转登录
              localStorage.removeItem('access_token');
              localStorage.removeItem('refresh_token');
              window.location.href = '/login';
            }
          } else {
            window.location.href = '/login';
          }
        }
        return Promise.reject(error);
      }
    );
  }

  // ========== Generic HTTP Methods ==========

  async get<T = any>(url: string, config?: AxiosRequestConfig): Promise<any> {
    return this.client.get(url, config);
  }

  async post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<any> {
    return this.client.post(url, data, config);
  }

  async put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<any> {
    return this.client.put(url, data, config);
  }

  async delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<any> {
    return this.client.delete(url, config);
  }

  // ========== Trade API ==========

  async getTrades(params?: {
    account_id?: string;
    account_type?: string;
    broker?: string;
    symbol?: string;
    side?: 'buy' | 'sell';
    sync_source?: string;
    start_date?: string;
    end_date?: string;
    page?: number;
    page_size?: number;
  }): Promise<TradeListResponse> {
    const response = await this.client.get('/trades/', { params });
    return response.data;
  }

  async getTrade(tradeId: string): Promise<Trade> {
    const response = await this.client.get(`/trades/${tradeId}`);
    return response.data;
  }

  async createTrade(data: TradeCreate): Promise<Trade> {
    const response = await this.client.post('/trades/', data);
    return response.data;
  }

  async updateTrade(tradeId: string, data: Partial<TradeCreate>): Promise<Trade> {
    const response = await this.client.put(`/trades/${tradeId}`, data);
    return response.data;
  }

  async deleteTrade(tradeId: string): Promise<void> {
    await this.client.delete(`/trades/${tradeId}`);
  }

  async getTradeStats(params?: {
    account_id?: string;
    start_date?: string;
    end_date?: string;
  }): Promise<TradeStats> {
    const response = await this.client.get('/trades/stats/summary', { params });
    return response.data;
  }

  async bulkCreateTrades(data: {
    account_id: string;
    trades: TradeCreate[];
    sync_source?: string;
    skip_duplicates?: boolean;
  }): Promise<{
    success_count: number;
    failed_count: number;
    duplicate_count: number;
    created_trades: Trade[];
  }> {
    const response = await this.client.post('/trades/bulk', data);
    return response.data;
  }

  async updateTradeRationale(
    tradeId: string,
    actionType: ActionType | null,
    actionReason: string
  ): Promise<Trade> {
    const params = new URLSearchParams();
    if (actionType) {
      params.append('action_type', actionType);
    }
    if (actionReason) {
      params.append('action_reason', actionReason);
    }

    const response = await this.client.put(`/trades/${tradeId}/rationale?${params.toString()}`);
    return response.data;
  }

  // ========== Phase 4: Trade Review API ==========

  async reviewTrade(tradeId: string, reviewData: TradeReviewData): Promise<Trade> {
    const response = await this.client.put(`/trades/${tradeId}/review`, reviewData);
    return response.data;
  }

  async batchReviewTrades(request: BatchReviewRequest): Promise<Trade[]> {
    const response = await this.client.post('/trades/batch-review', request);
    return response.data;
  }

  async getUnreviewedTrades(days: number = 7, accountId?: string): Promise<Trade[]> {
    const params: any = { days };
    if (accountId) {
      params.account_id = accountId;
    }
    const response = await this.client.get('/trades/unreviewed', { params });
    return response.data;
  }

  // ========== Strategy Settings API ==========

  async getStrategySettings(): Promise<StrategySettings> {
    const response = await this.client.get('/strategy-settings/');
    return response.data;
  }

  async updateStrategySettings(data: StrategySettings): Promise<StrategySettings> {
    const response = await this.client.put('/strategy-settings/', data);
    return response.data;
  }

  // ========== Position API ==========

  async getPositions(params?: {
    account_id?: string;
    account_type?: string;
    symbol?: string;
    is_closed?: boolean;
    page?: number;
    page_size?: number;
  }): Promise<PositionListResponse> {
    const response = await this.client.get('/positions/', { params });
    return response.data;
  }

  async getPosition(positionId: string): Promise<Position> {
    const response = await this.client.get(`/positions/${positionId}`);
    return response.data;
  }

  async refreshPositionPricesSelection(positionIds: string[]): Promise<{
    updated_count: number;
    failed_count: number;
    total_positions: number;
    message?: string;
  }> {
    const response = await this.client.post('/positions/refresh-prices/selection', {
      position_ids: positionIds
    });
    return response.data;
  }

  async updatePositionNotes(positionId: string, notes: string | null): Promise<Position> {
    const response = await this.client.patch(`/positions/${positionId}/notes`, { notes });
    return response.data;
  }

  async getPositionStats(accountId?: string): Promise<PositionStats> {
    const params = accountId ? { account_id: accountId } : {};
    const response = await this.client.get('/positions/stats/summary', { params });
    return response.data;
  }

  async updatePositionPrice(data: {
    symbol: string;
    current_price: string | number;
  }, accountId: string): Promise<Position> {
    const response = await this.client.post(
      `/positions/update-price?account_id=${accountId}`,
      data
    );
    return response.data;
  }

  async getPositionsSummary(): Promise<PositionSummary[]> {
    const response = await this.client.get('/positions/summary/by-account');
    return response.data;
  }

  async getPositionBySymbol(symbol: string, accountId: string): Promise<Position> {
    const response = await this.client.get(`/positions/symbol/${symbol}`, {
      params: { account_id: accountId }
    });
    return response.data;
  }

  async refreshPositionPrices(accountId?: string): Promise<{
    status?: string;
    task_id?: string;
    updated_count: number;
    failed_count: number;
    total_positions?: number;
    message: string;
  }> {
    const params = accountId ? { account_id: accountId } : {};
    const response = await this.client.post('/positions/refresh-prices', null, { params });
    return response.data;
  }

  async getRefreshPositionPricesTaskStatus(taskId: string): Promise<{
    task_id: string;
    status: string;
    message?: string;
    result?: {
      status?: string;
      updated_count?: number;
      failed_count?: number;
      total_positions?: number;
      completed_at?: string;
      error?: string;
    };
    error?: string;
  }> {
    const response = await this.client.get(`/positions/refresh-prices/task/${taskId}`);
    return response.data;
  }

  // ========== Trade Account API ==========

  async getTradeAccounts(accountType?: string) {
    const params = accountType ? { account_type: accountType } : {};
    const response = await this.client.get('/trade-accounts/', { params });
    return response.data;
  }

  async getTradeAccount(accountId: string) {
    const response = await this.client.get(`/trade-accounts/${accountId}`);
    return response.data;
  }

  async createTradeAccount(data: {
    account_name: string;
    account_type: string;
    api_key?: string;
    api_secret?: string;
    extra_config?: any;
  }) {
    const response = await this.client.post('/trade-accounts/', data);
    return response.data;
  }

  async updateTradeAccount(accountId: string, data: any) {
    const response = await this.client.put(`/trade-accounts/${accountId}`, data);
    return response.data;
  }

  async deleteTradeAccount(accountId: string): Promise<void> {
    await this.client.delete(`/trade-accounts/${accountId}`);
  }

  async syncTradeAccount(accountId: string) {
    const response = await this.client.post(`/trade-accounts/${accountId}/sync`);
    return response.data;
  }

  async clearTradeAccountData(accountId: string) {
    const response = await this.client.delete(`/trade-accounts/${accountId}/data`);
    return response.data;
  }

  // ========== Dashboard API ==========

  async getDashboardSummary(): Promise<DashboardSummary> {
    const response = await this.client.get('/dashboard/summary');
    return response.data;
  }
}

export const apiClient = new APIClient();
