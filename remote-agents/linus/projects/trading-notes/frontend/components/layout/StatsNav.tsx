'use client';

import { Card } from '@/components/ui/card';
import { TrendingUp, TrendingDown, Activity, DollarSign, Percent, Calendar } from 'lucide-react';

export interface StatItem {
  label: string;
  value: string | number;
  change?: number;
  trend?: 'up' | 'down' | 'neutral';
  icon?: 'trending-up' | 'trending-down' | 'activity' | 'dollar' | 'percent' | 'calendar';
  valueClassName?: string;
}

interface StatsNavProps {
  stats: StatItem[];
  variant?: 'default' | 'compact';
}

const iconComponents = {
  'trending-up': TrendingUp,
  'trending-down': TrendingDown,
  'activity': Activity,
  'dollar': DollarSign,
  'percent': Percent,
  'calendar': Calendar,
};

export default function StatsNav({ stats, variant = 'default' }: StatsNavProps) {
  const getTrendColor = (trend?: 'up' | 'down' | 'neutral') => {
    switch (trend) {
      case 'up':
        return 'text-green-600';
      case 'down':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  const getTrendIcon = (trend?: 'up' | 'down' | 'neutral') => {
    switch (trend) {
      case 'up':
        return <TrendingUp className="w-4 h-4" />;
      case 'down':
        return <TrendingDown className="w-4 h-4" />;
      default:
        return null;
    }
  };

  const formatChange = (change: number) => {
    const rounded = Math.round(change * 100) / 100;
    const normalized = Object.is(rounded, -0) ? 0 : rounded;
    const sign = normalized > 0 ? '+' : '';
    return `${sign}${normalized.toFixed(2)}%`;
  };

  if (variant === 'compact') {
    return (
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        {stats.map((stat, index) => {
          const IconComponent = stat.icon ? iconComponents[stat.icon] : Activity;
          return (
            <Card key={index} className="p-4 hover:shadow-md transition-shadow">
              <div className="flex items-center space-x-3">
                <IconComponent className="w-5 h-5 text-gray-500" />
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-gray-600 truncate">{stat.label}</p>
                  <p className={`text-3xl font-bold truncate leading-tight ${stat.valueClassName ?? 'text-gray-900'}`}>{stat.value}</p>
                </div>
              </div>
            </Card>
          );
        })}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 mb-6">
      {stats.map((stat, index) => {
        const IconComponent = stat.icon ? iconComponents[stat.icon] : Activity;
        return (
          <Card key={index} className="p-4 hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <p className="text-sm text-gray-500 mb-1">{stat.label}</p>
                <p className={`text-2xl font-bold ${stat.valueClassName ?? 'text-gray-900'}`}>{stat.value}</p>
                {stat.change !== undefined && (
                  <div className={`flex items-center space-x-1 mt-2 text-sm ${getTrendColor(stat.trend)}`}>
                    {getTrendIcon(stat.trend)}
                    <span>{formatChange(stat.change)}</span>
                  </div>
                )}
              </div>
              <div className="ml-4">
                <div className={`p-2 rounded-lg ${
                  stat.trend === 'up' ? 'bg-green-100' :
                  stat.trend === 'down' ? 'bg-red-100' :
                  'bg-gray-100'
                }`}>
                  <IconComponent className={`w-6 h-6 ${
                    stat.trend === 'up' ? 'text-green-600' :
                    stat.trend === 'down' ? 'text-red-600' :
                    'text-gray-600'
                  }`} />
                </div>
              </div>
            </div>
          </Card>
        );
      })}
    </div>
  );
}
