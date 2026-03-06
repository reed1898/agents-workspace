'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { usePageTitle } from '@/lib/use-page-title';

export default function LoginRedirectPage() {
  const router = useRouter();

  usePageTitle('登录');

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      router.replace('/dashboard');
      return;
    }
    router.replace('/?login=1');
  }, [router]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="text-lg text-gray-600">跳转中...</div>
    </div>
  );
}
