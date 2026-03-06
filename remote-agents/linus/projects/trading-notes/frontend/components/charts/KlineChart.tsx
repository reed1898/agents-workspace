'use client';

import { useEffect, useRef, useState } from 'react';
import { createChart, IChartApi, ISeriesApi, CandlestickData, Time } from 'lightweight-charts';
import { KlineData, TradeMarker } from '@/types/kline';

interface KlineChartProps {
  data: KlineData[];
  symbol: string;
  markers?: TradeMarker[];
  height?: number;
  loading?: boolean;
}

export function KlineChart({
  data,
  symbol,
  markers = [],
  height = 400,
  loading = false
}: KlineChartProps) {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const candlestickSeriesRef = useRef<ISeriesApi<'Candlestick'> | null>(null);

  useEffect(() => {
    if (!chartContainerRef.current || data.length === 0) return;

    // 创建图表
    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: height,
      layout: {
        background: { color: '#ffffff' },
        textColor: '#333',
      },
      grid: {
        vertLines: { color: '#f0f0f0' },
        horzLines: { color: '#f0f0f0' },
      },
      crosshair: {
        mode: 1, // Normal crosshair
      },
      rightPriceScale: {
        borderColor: '#cccccc',
      },
      timeScale: {
        borderColor: '#cccccc',
        timeVisible: true,
        secondsVisible: false,
      },
    });

    chartRef.current = chart;

    // 添加K线系列
    const candlestickSeries = chart.addCandlestickSeries({
      upColor: '#26a69a',
      downColor: '#ef5350',
      borderVisible: false,
      wickUpColor: '#26a69a',
      wickDownColor: '#ef5350',
    });

    candlestickSeriesRef.current = candlestickSeries;

    // 转换数据格式
    const formattedData: CandlestickData[] = data.map((item) => ({
      time: item.time as Time,
      open: item.open,
      high: item.high,
      low: item.low,
      close: item.close,
    }));

    candlestickSeries.setData(formattedData);

    // 添加交易标记
    if (markers.length > 0) {
      candlestickSeries.setMarkers(
        markers.map((marker) => ({
          time: marker.time as Time,
          position: marker.position,
          color: marker.color,
          shape: marker.shape,
          text: marker.text,
        }))
      );
    }

    // 自动调整可见范围
    chart.timeScale().fitContent();

    // 响应式处理
    const handleResize = () => {
      if (chartContainerRef.current) {
        chart.applyOptions({
          width: chartContainerRef.current.clientWidth,
        });
      }
    };

    window.addEventListener('resize', handleResize);

    // 清理
    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, [data, markers, height]);

  if (loading) {
    return (
      <div
        className="flex items-center justify-center bg-gray-50 rounded-lg border"
        style={{ height: `${height}px` }}
      >
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-2"></div>
          <p className="text-sm text-gray-600">加载K线数据中...</p>
        </div>
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div
        className="flex items-center justify-center bg-gray-50 rounded-lg border"
        style={{ height: `${height}px` }}
      >
        <div className="text-center">
          <p className="text-gray-600">暂无K线数据</p>
          <p className="text-sm text-gray-400 mt-1">请选择其他时间范围或标的</p>
        </div>
      </div>
    );
  }

  return (
    <div className="border rounded-lg overflow-hidden">
      <div className="bg-gray-50 px-4 py-2 border-b">
        <h3 className="text-sm font-semibold text-gray-700">{symbol} K线图</h3>
      </div>
      <div ref={chartContainerRef} />
    </div>
  );
}
