'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, TrendingUp, FileText, Wallet, Activity, Settings } from 'lucide-react';

interface NavItem {
  name: string;
  href: string;
  icon: React.ReactNode;
}

const navItems: NavItem[] = [
  {
    name: '首页',
    href: '/dashboard',
    icon: <Home className="w-5 h-5" />
  },
  {
    name: '持仓管理',
    href: '/positions',
    icon: <TrendingUp className="w-5 h-5" />
  },
  {
    name: '交易记录',
    href: '/trades',
    icon: <FileText className="w-5 h-5" />
  },
  {
    name: '纪律分析',
    href: '/analytics',
    icon: <Activity className="w-5 h-5" />
  },
  {
    name: '交易账户管理',
    href: '/accounts',
    icon: <Wallet className="w-5 h-5" />
  },
  {
    name: '策略设置',
    href: '/settings',
    icon: <Settings className="w-5 h-5" />
  }
];

export default function PageNav() {
  const pathname = usePathname();

  return (
    <nav className="bg-white border-b border-gray-200 mb-6">
      <div className="container mx-auto px-4">
        <div className="flex items-center space-x-1 overflow-x-auto">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`
                  flex items-center space-x-2 px-4 py-3 border-b-2 transition-colors whitespace-nowrap
                  ${isActive
                    ? 'border-blue-600 text-blue-600 font-medium'
                    : 'border-transparent text-gray-600 hover:text-gray-900 hover:border-gray-300'
                  }
                `}
              >
                {item.icon}
                <span>{item.name}</span>
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
}
