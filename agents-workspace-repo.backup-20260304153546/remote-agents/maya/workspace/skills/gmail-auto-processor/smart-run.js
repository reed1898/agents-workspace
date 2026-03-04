#!/usr/bin/env node

/**
 * Gmail Auto Processor - Smart Runner with Task Monitor
 * 自动检测耗时任务，智能决定是否使用 subagent
 */

const { execSync } = require('child_process');
const path = require('path');

const SKILL_PATH = path.join(__dirname);
const monitor = require('./task-monitor');

function spawnSubagent(task, label = 'gmail-processor') {
  const cmd = `openclaw sessions_spawn "${task.replace(/"/g, '\\"')}" --label ${label}`;
  try {
    const result = execSync(cmd, { encoding: 'utf8', timeout: 10000 });
    return { success: true, output: result };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

function runDirect() {
  const cmd = `cd ${SKILL_PATH} && node index.js`;
  try {
    const start = Date.now();
    const result = execSync(cmd, { encoding: 'utf8', timeout: 120000 });
    const duration = Date.now() - start;
    return { success: true, output: result, duration };
  } catch (error) {
    return { success: false, error: error.message, duration: Date.now() };
  }
}

function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');
  const forceDirect = args.includes('--direct');
  const forceSubagent = args.includes('--subagent');
  
  const taskName = 'gmail-auto-processor';
  
  console.log('📧 Gmail Auto Processor (Smart Runner)');
  console.log('======================================\n');
  
  // 检查历史记录
  const history = monitor.getTaskHistory(taskName);
  const recommendation = monitor.shouldUseSubagent(taskName, { apiCalls: 50 });
  
  // 显示历史信息
  if (history) {
    console.log(`📊 历史记录: ${history.runs?.length || 0} 次执行`);
    console.log(`⏱️  平均耗时: ${Math.round(history.avg_time_ms/1000)} 秒`);
    console.log(`🎯 推荐模式: ${history.recommended_mode}\n`);
  }
  
  // 决定执行模式
  let mode = 'direct';
  let reason = '首次执行或历史耗时较短';
  
  if (forceSubagent) {
    mode = 'subagent';
    reason = '用户强制使用 subagent';
  } else if (forceDirect) {
    mode = 'direct';
    reason = '用户强制直接执行';
  } else if (recommendation.useSubagent) {
    mode = 'subagent';
    reason = recommendation.reason;
  }
  
  console.log(`🚀 执行模式: ${mode === 'subagent' ? 'Subagent（后台）' : '直接执行'}`);
  console.log(`📝 原因: ${reason}\n`);
  
  if (mode === 'subagent') {
    // 使用 subagent
    const task = `处理 Gmail 邮件分析任务。

执行步骤：
1. cd ${SKILL_PATH}
2. node index.js ${dryRun ? '--dry-run' : ''}
3. 处理完成后，发送 Telegram 汇总报告

处理规则：
- 促销邮件：归档 + 标记已读
- 重要邮件：标记 IMPORTANT + 标记已读
- Newsletter：保留 + 标记已读
- 其他邮件：保留 + 标记已读

报告格式：
📧 Gmail 处理报告 (时间)
📊 统计:
• 已处理: X 封
• 归档: X 封 (促销)
• 重要: X 封
• Newsletter: X 封

🔴 重要提醒（如有）
📰 Newsletter 列表（如有）`;

    console.log('⏳ 启动 subagent 后台处理...');
    const result = spawnSubagent(task);
    
    if (result.success) {
      console.log('✅ Subagent 已启动，后台处理中...');
      console.log('📱 完成后会自动发送 Telegram 通知');
      console.log('💡 你可以继续其他操作，无需等待\n');
    } else {
      console.log('❌ Subagent 启动失败:', result.error);
      console.log('🔄 回退到直接执行模式...\n');
      // 回退到直接执行
      const directResult = runDirect();
      console.log(directResult.output);
    }
  } else {
    // 直接执行
    console.log('⏳ 直接执行中...\n');
    const start = Date.now();
    const result = runDirect();
    const duration = Date.now() - start;
    
    // 记录执行时间
    monitor.recordTask(taskName, duration, { dryRun });
    
    if (result.success) {
      console.log(result.output);
      console.log(`\n⏱️  本次耗时: ${Math.round(duration/1000)} 秒`);
      
      // 如果耗时过长，提示下次会用 subagent
      if (duration > 30000) {
        console.log('\n⚠️  检测到耗时较长，下次将自动使用 subagent 模式');
      }
    } else {
      console.log('❌ 执行失败:', result.error);
    }
  }
}

main();
