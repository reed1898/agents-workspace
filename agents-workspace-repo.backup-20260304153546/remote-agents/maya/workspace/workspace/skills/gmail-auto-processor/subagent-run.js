#!/usr/bin/env node

/**
 * Gmail Auto Processor - Subagent Wrapper
 * 通过 subagent 异步执行邮件处理，不阻塞主会话
 */

const { execSync } = require('child_process');
const path = require('path');

const SKILL_PATH = path.join(__dirname);

function spawnSubagent(task) {
  const cmd = `openclaw sessions_spawn "${task}" --label gmail-processor`;
  try {
    const result = execSync(cmd, { encoding: 'utf8', timeout: 10000 });
    return result;
  } catch (error) {
    console.error('❌ 启动 subagent 失败:', error.message);
    return null;
  }
}

function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');
  
  console.log('📧 Gmail Auto Processor (Subagent Mode)');
  console.log('=======================================\n');
  
  const task = `运行 Gmail Auto Processor skill 处理邮件。${dryRun ? '使用预览模式，不要实际修改邮件。' : '正常处理，归档促销邮件并标记重要邮件。'}

执行步骤：
1. cd ${SKILL_PATH}
2. node index.js ${dryRun ? '--dry-run' : ''}
3. 处理完成后，发送 Telegram 汇总报告给用户

报告格式：
📧 Gmail 处理报告 (时间)
📊 统计:
• 已处理: X 封
• 归档: X 封 (促销)
• 重要: X 封
• Newsletter: X 封

🔴 重要提醒（如有）
📰 Newsletter 列表（如有）`;

  console.log('🚀 启动 subagent 处理邮件...');
  console.log('⏱️  这可能需要 1-3 分钟，你可以继续使用其他功能\n');
  
  const result = spawnSubagent(task);
  
  if (result) {
    console.log('✅ Subagent 已启动');
    console.log('📱 处理完成后会自动发送 Telegram 通知');
    console.log('\n你可以继续其他操作，无需等待...');
  } else {
    console.log('❌ 启动失败，请手动执行:');
    console.log(`   cd ${SKILL_PATH} && node index.js ${dryRun ? '--dry-run' : ''}`);
  }
}

main();
