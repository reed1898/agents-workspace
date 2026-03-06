"use client"

import { useState, useEffect } from "react"
import { BarChart3, TrendingUp, TrendingDown, AlertTriangle, Brain } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { PieChart, Pie, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from "recharts"
import { apiClient } from "@/lib/api-client"
import PageNav from "@/components/layout/PageNav"
import { usePageTitle } from "@/lib/use-page-title"

type TimeRange = "7d" | "30d" | "90d" | "all"

interface StopLossData {
  total_cycles: number
  executed_count: number
  violated_count: number
  execution_rate: number
  violations: Array<{
    cycle_id: string
    symbol: string
    loss: number
    holding_hours: number
    emotion: string
    open_time: string
  }>
  insight: string
}

interface EmotionData {
  emotion_stats: Record<string, {
    cycle_count: number
    win_rate: number
    avg_roi: number
    avg_holding_hours: number
    total_pnl: number
  }>
  insight: string
}

interface StrategyData {
  strategy_stats: Record<string, {
    cycle_count: number
    win_rate: number
    avg_roi: number
    avg_holding_hours: number
    best_case: { symbol: string; roi: number } | null
    worst_case: { symbol: string; roi: number } | null
  }>
  insight: string
}

interface HoldingTimeData {
  profitable_trades: {
    count: number
    avg_holding_hours: number
    median_holding_hours: number
  }
  loss_trades: {
    count: number
    avg_holding_hours: number
    median_holding_hours: number
  }
  insight: string
}

interface DashboardData {
  time_range: string
  stop_loss_discipline: StopLossData
  emotion_impact: EmotionData
  strategy_effectiveness: StrategyData
  holding_time_pattern: HoldingTimeData
}

const EMOTION_NAMES: Record<string, string> = {
  calm: "冷静",
  fearful: "恐惧",
  greedy: "贪婪",
  fomo: "害怕踏空",
  panic: "恐慌",
  confident: "自信",
  excited: "兴奋",
  regretful: "后悔"
}

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#8884D8", "#82ca9d", "#ffc658", "#ff7c7c"]

export default function AnalyticsPage() {
  const [timeRange, setTimeRange] = useState<TimeRange>("30d")
  const [data, setData] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)

  usePageTitle("交易纪律分析")

  useEffect(() => {
    loadDashboard()
  }, [timeRange])

  const loadDashboard = async () => {
    try {
      setLoading(true)
      const response = await apiClient.get(`/analytics/discipline-dashboard?time_range=${timeRange}`)
      setData(response.data)
    } catch (error) {
      console.error("Failed to load dashboard:", error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <>
        <PageNav />
        <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50">
          <div className="container mx-auto px-4 py-8">
            <div className="flex items-center justify-center h-64">
              <div className="text-gray-500">加载中...</div>
            </div>
          </div>
        </div>
      </>
    )
  }

  if (!data) {
    return (
      <>
        <PageNav />
        <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50">
          <div className="container mx-auto px-4 py-8">
            <Alert className="bg-red-50 border-red-200 shadow-md">
              <AlertTriangle className="h-4 w-4 text-red-600" />
              <AlertDescription className="text-red-800">无法加载数据,请稍后重试</AlertDescription>
            </Alert>
          </div>
        </div>
      </>
    )
  }

  const stopLossChartData = [
    { name: "执行", value: data.stop_loss_discipline.executed_count },
    { name: "违背", value: data.stop_loss_discipline.violated_count }
  ]

  const emotionChartData = Object.entries(data.emotion_impact.emotion_stats).map(([emotion, stats]) => ({
    emotion: EMOTION_NAMES[emotion] || emotion,
    avg_roi: stats.avg_roi,
    cycle_count: stats.cycle_count,
    win_rate: stats.win_rate
  }))

  const strategyChartData = Object.entries(data.strategy_effectiveness.strategy_stats).map(([strategy, stats]) => ({
    strategy,
    win_rate: stats.win_rate,
    avg_roi: stats.avg_roi,
    cycle_count: stats.cycle_count
  }))

  return (
    <>
      <PageNav />
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50">
        <div className="container mx-auto px-4 py-8 space-y-8">
          {/* 页面标题 */}
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div className="flex items-center space-x-3">
              <div className="p-3 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-xl shadow-lg">
                <BarChart3 className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-4xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
                  交易纪律分析
                </h1>
                <p className="mt-1 text-gray-600">深度分析您的交易行为和纪律执行情况</p>
              </div>
            </div>

            <Tabs value={timeRange} onValueChange={(v) => setTimeRange(v as TimeRange)}>
              <TabsList className="bg-white shadow-md">
                <TabsTrigger value="7d">近7天</TabsTrigger>
                <TabsTrigger value="30d">近30天</TabsTrigger>
                <TabsTrigger value="90d">近90天</TabsTrigger>
                <TabsTrigger value="all">全部</TabsTrigger>
              </TabsList>
            </Tabs>
          </div>

          {/* 止损纪律 */}
          <Card className="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
            <CardHeader className="px-6 py-5 bg-gradient-to-r from-gray-50 to-gray-100 border-b border-gray-200">
              <div className="flex items-center space-x-2">
                <div className="w-1 h-6 bg-gradient-to-b from-red-500 to-red-600 rounded-full"></div>
                <div>
                  <CardTitle className="text-xl font-bold text-gray-800">止损执行纪律</CardTitle>
                  <CardDescription className="text-gray-600">分析止损计划的执行情况</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent className="p-6 space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                {/* 饼图 */}
                <div className="bg-gradient-to-br from-gray-50 to-white p-6 rounded-xl border border-gray-100">
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={stopLossChartData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, percent }) => `${name} ${(((percent ?? 0) * 100)).toFixed(0)}%`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {stopLossChartData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={index === 0 ? "#00C49F" : "#FF8042"} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                  <div className="text-center mt-4">
                    <div className="text-4xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
                      {data.stop_loss_discipline.execution_rate}%
                    </div>
                    <div className="text-sm text-gray-600 mt-1">止损执行率</div>
                  </div>
                </div>

                {/* 违规列表 */}
                <div>
                  <h4 className="font-semibold mb-3 text-gray-800 flex items-center">
                    <AlertTriangle className="w-4 h-4 mr-2 text-red-500" />
                    违规案例(最严重的10个)
                  </h4>
                  <div className="space-y-2 max-h-[340px] overflow-y-auto pr-2 custom-scrollbar">
                    {data.stop_loss_discipline.violations.map((v) => (
                      <div key={v.cycle_id} className="flex justify-between py-3 px-4 bg-gradient-to-r from-red-50 to-orange-50 border border-red-100 rounded-lg hover:shadow-md transition-shadow">
                        <div>
                          <div className="font-bold text-gray-900">{v.symbol}</div>
                          <div className="text-xs text-gray-500 mt-1">
                            {v.emotion || "未记录情绪"}
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-red-600 font-bold">${v.loss.toFixed(2)}</div>
                          <div className="text-xs text-gray-500 mt-1">{v.holding_hours}小时</div>
                        </div>
                      </div>
                    ))}
                    {data.stop_loss_discipline.violations.length === 0 && (
                      <div className="flex flex-col items-center justify-center py-12 text-center">
                        <TrendingUp className="w-12 h-12 text-green-400 mb-3" />
                        <p className="text-sm text-gray-600 font-medium">暂无违规记录</p>
                        <p className="text-xs text-gray-400 mt-1">保持良好的纪律!</p>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              <Alert className="bg-blue-50 border-blue-200">
                <Brain className="h-4 w-4 text-blue-600" />
                <AlertDescription className="text-blue-900">{data.stop_loss_discipline.insight}</AlertDescription>
              </Alert>
            </CardContent>
          </Card>

          {/* 情绪影响 */}
          <Card className="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
            <CardHeader className="px-6 py-5 bg-gradient-to-r from-gray-50 to-gray-100 border-b border-gray-200">
              <div className="flex items-center space-x-2">
                <div className="w-1 h-6 bg-gradient-to-b from-purple-500 to-indigo-600 rounded-full"></div>
                <div>
                  <CardTitle className="text-xl font-bold text-gray-800">情绪与收益关系</CardTitle>
                  <CardDescription className="text-gray-600">分析不同情绪状态下的交易表现</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent className="p-6 space-y-6">
              <div className="bg-gradient-to-br from-gray-50 to-white p-6 rounded-xl border border-gray-100">
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={emotionChartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis dataKey="emotion" stroke="#6b7280" />
                    <YAxis stroke="#6b7280" />
                    <Tooltip contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }} />
                    <Legend />
                    <Bar dataKey="avg_roi" fill="#8b5cf6" name="平均收益率 (%)" radius={[8, 8, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <Alert className="bg-purple-50 border-purple-200">
                <Brain className="h-4 w-4 text-purple-600" />
                <AlertDescription className="text-purple-900">{data.emotion_impact.insight}</AlertDescription>
              </Alert>
            </CardContent>
          </Card>

          {/* 策略有效性 */}
          <Card className="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
            <CardHeader className="px-6 py-5 bg-gradient-to-r from-gray-50 to-gray-100 border-b border-gray-200">
              <div className="flex items-center space-x-2">
                <div className="w-1 h-6 bg-gradient-to-b from-blue-500 to-indigo-600 rounded-full"></div>
                <div>
                  <CardTitle className="text-xl font-bold text-gray-800">策略胜率对比</CardTitle>
                  <CardDescription className="text-gray-600">分析不同交易策略的效果</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent className="p-6 space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                {/* 胜率图 */}
                <div className="bg-gradient-to-br from-gray-50 to-white p-6 rounded-xl border border-gray-100">
                  <ResponsiveContainer width="100%" height={250}>
                    <BarChart data={strategyChartData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                      <XAxis dataKey="strategy" stroke="#6b7280" />
                      <YAxis stroke="#6b7280" />
                      <Tooltip contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }} />
                      <Legend />
                      <Bar dataKey="win_rate" fill="#10b981" name="胜率 (%)" radius={[8, 8, 0, 0]} />
                      <Bar dataKey="avg_roi" fill="#3b82f6" name="平均收益率 (%)" radius={[8, 8, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>

                {/* 策略详情 */}
                <div className="space-y-3">
                  {Object.entries(data.strategy_effectiveness.strategy_stats).map(([strategy, stats]) => (
                    <div key={strategy} className="p-4 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-100 rounded-xl hover:shadow-md transition-shadow">
                      <h4 className="font-bold text-gray-900 mb-3">{strategy}</h4>
                      <div className="grid grid-cols-2 gap-3 text-sm">
                        <div className="flex items-center">
                          <TrendingUp className="w-4 h-4 text-green-600 mr-2" />
                          <span className="text-gray-600">胜率:</span>
                          <span className="ml-auto font-semibold text-gray-900">{stats.win_rate.toFixed(2)}%</span>
                        </div>
                        <div className="flex items-center">
                          <span className="text-gray-600">平均收益:</span>
                          <span className="ml-auto font-semibold text-gray-900">{stats.avg_roi.toFixed(2)}%</span>
                        </div>
                        <div className="flex items-center">
                          <span className="text-gray-600">交易次数:</span>
                          <span className="ml-auto font-semibold text-gray-900">{stats.cycle_count}</span>
                        </div>
                        <div className="flex items-center">
                          <span className="text-gray-600">平均持仓:</span>
                          <span className="ml-auto font-semibold text-gray-900">{stats.avg_holding_hours.toFixed(1)}h</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <Alert className="bg-blue-50 border-blue-200">
                <Brain className="h-4 w-4 text-blue-600" />
                <AlertDescription className="text-blue-900">{data.strategy_effectiveness.insight}</AlertDescription>
              </Alert>
            </CardContent>
          </Card>

          {/* 持仓时间模式 */}
          <Card className="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
            <CardHeader className="px-6 py-5 bg-gradient-to-r from-gray-50 to-gray-100 border-b border-gray-200">
              <div className="flex items-center space-x-2">
                <div className="w-1 h-6 bg-gradient-to-b from-yellow-500 to-orange-600 rounded-full"></div>
                <div>
                  <CardTitle className="text-xl font-bold text-gray-800">持仓时间模式</CardTitle>
                  <CardDescription className="text-gray-600">对比盈利与亏损交易的持仓时长</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent className="p-6 space-y-6">
              <div className="grid md:grid-cols-2 gap-8">
                <div className="text-center p-8 bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200 rounded-2xl shadow-lg hover:shadow-xl transition-shadow">
                  <TrendingUp className="w-12 h-12 text-green-600 mx-auto mb-4" />
                  <div className="text-5xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent mb-2">
                    {data.holding_time_pattern.profitable_trades.avg_holding_hours.toFixed(1)}h
                  </div>
                  <div className="text-sm font-semibold text-gray-700 mb-1">盈利交易平均持仓</div>
                  <div className="text-xs text-gray-500 inline-flex items-center px-3 py-1 bg-white rounded-full">
                    ({data.holding_time_pattern.profitable_trades.count} 笔交易)
                  </div>
                </div>

                <div className="text-center p-8 bg-gradient-to-br from-red-50 to-orange-50 border-2 border-red-200 rounded-2xl shadow-lg hover:shadow-xl transition-shadow">
                  <TrendingDown className="w-12 h-12 text-red-600 mx-auto mb-4" />
                  <div className="text-5xl font-bold bg-gradient-to-r from-red-600 to-orange-600 bg-clip-text text-transparent mb-2">
                    {data.holding_time_pattern.loss_trades.avg_holding_hours.toFixed(1)}h
                  </div>
                  <div className="text-sm font-semibold text-gray-700 mb-1">亏损交易平均持仓</div>
                  <div className="text-xs text-gray-500 inline-flex items-center px-3 py-1 bg-white rounded-full">
                    ({data.holding_time_pattern.loss_trades.count} 笔交易)
                  </div>
                </div>
              </div>

              <Alert className="bg-yellow-50 border-yellow-200">
                <Brain className="h-4 w-4 text-yellow-600" />
                <AlertDescription className="text-yellow-900">{data.holding_time_pattern.insight}</AlertDescription>
              </Alert>
            </CardContent>
          </Card>
        </div>
      </div>
    </>
  )
}
