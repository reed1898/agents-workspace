const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const DB_PATH = path.join(__dirname, '.task-monitor.json');

// 默认配置
const DEFAULT_CONFIG = {
  thresholds: {
    slow_task_ms: 30000,
    many_api_calls: 10
  },
  history: {},
  auto_rules: [
    { pattern: 'gmail|email|mail', mode: 'subagent', reason: 'Gmail API调用多，容易超时' },
    { pattern: 'batch|bulk|批量', mode: 'subagent', reason: '批处理量大' },
    { pattern: 'crawl|spider|爬虫', mode: 'subagent', reason: '网络IO耗时' },
    { pattern: 'analysis|分析', mode: 'subagent', reason: '数据分析耗时' }
  ]
};

class TaskMonitor {
  constructor() {
    this.db = this.loadDB();
  }

  loadDB() {
    if (fs.existsSync(DB_PATH)) {
      return { ...DEFAULT_CONFIG, ...JSON.parse(fs.readFileSync(DB_PATH, 'utf8')) };
    }
    return { ...DEFAULT_CONFIG };
  }

  saveDB() {
    fs.writeFileSync(DB_PATH, JSON.stringify(this.db, null, 2));
  }

  // 判断是否应该使用 subagent
  shouldUseSubagent(taskName, options = {}) {
    // 1. 检查历史记录
    const history = this.db.history[taskName];
    if (history && history.avg_time_ms > this.db.thresholds.slow_task_ms) {
      return { 
        useSubagent: true, 
        reason: `历史平均耗时 ${Math.round(history.avg_time_ms/1000)}秒`,
        confidence: 'high'
      };
    }

    // 2. 检查自动规则
    for (const rule of this.db.auto_rules) {
      if (taskName.match(new RegExp(rule.pattern, 'i'))) {
        return { 
          useSubagent: true, 
          reason: rule.reason,
          confidence: 'medium'
        };
      }
    }

    // 3. 检查预估 API 调用量
    if (options.apiCalls && options.apiCalls > this.db.thresholds.many_api_calls) {
      return { 
        useSubagent: true, 
        reason: `预估 API 调用 ${options.apiCalls} 次`,
        confidence: 'medium'
      };
    }

    return { useSubagent: false, confidence: 'low' };
  }

  // 记录任务执行
  recordTask(taskName, durationMs, metadata = {}) {
    if (!this.db.history[taskName]) {
      this.db.history[taskName] = { runs: [], recommended_mode: 'direct' };
    }
    
    const history = this.db.history[taskName];
    history.runs.push({
      time: new Date().toISOString(),
      duration_ms: durationMs,
      ...metadata
    });
    
    // 只保留最近10次
    history.runs = history.runs.slice(-10);
    
    // 计算平均耗时
    const avgTime = history.runs.reduce((a, b) => a + b.duration_ms, 0) / history.runs.length;
    history.avg_time_ms = avgTime;
    history.last_run = new Date().toISOString();
    
    // 自动推荐模式
    if (avgTime > this.db.thresholds.slow_task_ms) {
      history.recommended_mode = 'subagent';
    }
    
    this.saveDB();
    return { avgTime, recommendedMode: history.recommended_mode };
  }

  // 获取任务历史
  getTaskHistory(taskName) {
    return this.db.history[taskName] || null;
  }

  // 列出所有已知耗时任务
  listSlowTasks() {
    return Object.entries(this.db.history)
      .filter(([_, h]) => h.avg_time_ms > this.db.thresholds.slow_task_ms)
      .map(([name, h]) => ({
        name,
        avgTime: `${Math.round(h.avg_time_ms/1000)}s`,
        runs: h.runs.length,
        recommendedMode: h.recommended_mode
      }));
  }
}

module.exports = new TaskMonitor();
