'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';
import axios from 'axios';
import { toast } from 'sonner';
import { usePageTitle } from '@/lib/use-page-title';

export default function Home() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [isLoading, setIsLoading] = useState(true);

  usePageTitle('登录');

  const clientId = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID!;
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://trading-notes.westgardensupply.com';

  // 检查是否已登录
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      router.push('/dashboard');
      return;
    }

    if (searchParams.get('login') === '1') {
      toast('请先登录', {
        description: '使用 Google 账户登录后继续',
      });
      router.replace('/');
    }

    setIsLoading(false);
  }, [router, searchParams, toast]);

  const handleSuccess = async (credentialResponse: any) => {
    try {
      // 发送 ID token 到后端验证
      const response = await axios.post(
        `${apiUrl}/api/v1/auth/google`,
        null,
        {
          params: {
            id_token_str: credentialResponse.credential
          }
        }
      );

      // 保存 tokens
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('refresh_token', response.data.refresh_token);

      // 跳转到 dashboard
      router.push('/dashboard');
    } catch (error) {
      console.error('Login failed:', error);
      alert('登录失败，请重试');
    }
  };

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="text-lg text-gray-600">加载中...</div>
      </div>
    );
  }

  return (
    <GoogleOAuthProvider clientId={clientId}>
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="w-full max-w-md space-y-8 rounded-2xl bg-white p-10 shadow-2xl">
          {/* Logo and Title */}
          <div className="text-center">
            <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-r from-blue-500 to-indigo-600">
              <svg className="h-8 w-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h1 className="text-4xl font-bold text-gray-900">Trading Notes</h1>
            <p className="mt-3 text-base text-gray-600">
              专业的交易日志和纪律分析工具
            </p>
          </div>

          {/* Features */}
          <div className="space-y-3 border-t border-b border-gray-200 py-6">
            <div className="flex items-center space-x-3">
              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100">
                <svg className="h-5 w-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span className="text-sm text-gray-700">多市场交易记录同步</span>
            </div>
            <div className="flex items-center space-x-3">
              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100">
                <svg className="h-5 w-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span className="text-sm text-gray-700">交易计划与执行跟踪</span>
            </div>
            <div className="flex items-center space-x-3">
              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100">
                <svg className="h-5 w-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span className="text-sm text-gray-700">纪律分析与复盘</span>
            </div>
          </div>

          {/* Google Login Button */}
          <div className="space-y-4">
            <div className="text-center text-sm text-gray-600">
              使用 Google 账户登录
            </div>
            <div className="flex justify-center">
              <GoogleLogin
                onSuccess={handleSuccess}
                onError={() => {
                  console.error('Login Failed');
                  alert('登录失败，请检查网络连接');
                }}
                theme="filled_blue"
                size="large"
                text="signin_with"
                shape="rectangular"
              />
            </div>
          </div>

          {/* Footer */}
          <div className="text-center text-xs text-gray-500">
            登录即表示您同意我们的服务条款和隐私政策
          </div>
        </div>
      </div>
    </GoogleOAuthProvider>
  );
}
