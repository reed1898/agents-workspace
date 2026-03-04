#!/usr/bin/env node

/**
 * Gmail Batch Processor - 批量处理所有未读邮件
 * 循环处理直到没有未读邮件为止
 */

const { execSync } = require('child_process');
const path = require('path');

const SKILL_PATH = path.join(__dirname);

function getUnreadCount() {
  try {
    const cmd = `mcporter call --server google-workspace --tool "gmail.search" query="is:unread" maxResults=1`;
    const result = execSync(cmd, { encoding: 'utf8', timeout: 10000 });
    const data = JSON.parse(result);
    return data.resultSizeEstimate || 0;
  } catch (e) {
    return 0;
  }
}

function processBatch() {
  try {
    const cmd = `cd ${SKILL_PATH} && node index.js 2>&1`;
    const result = execSync(cmd, { encoding: 'utf8', timeout: 120000 });
    return result;
  } catch (e) {
    return e.stdout || e.message;
  }
}

function main() {
  console.log('📧 Gmail 批量处理器');
  console.log('====================\n');
  
  let initialCount = getUnreadCount();
  console.log(`📨 初始未读邮件: ${initialCount} 封\n`);
  
  if (initialCount === 0) {
    console.log('✅ 没有未读邮件需要处理');
    return;
  }
  
  let batch = 0;
  let processed = 0;
  
  while (true) {
    batch++;
    const before = getUnreadCount();
    
    if (before === 0) {
      console.log('\n✅ 所有邮件处理完成！');
      break;
    }
    
    console.log(`\n🔄 第 ${batch} 批处理 (${before} 封未读)...`);
    const result = processBatch();
    
    // 统计本批处理数量
    const after = getUnreadCount();
    const batchProcessed = before - after;
    processed += batchProcessed;
    
    console.log(`✅ 本批处理: ${batchProcessed} 封`);
    console.log(`📊 累计处理: ${processed} 封`);
    console.log(`📨 剩余未读: ${after} 封`);
    
    // 如果连续两次没有减少，可能有问题，退出
    if (batchProcessed === 0) {
      console.log('\n⚠️ 本批未处理任何邮件，停止循环');
      break;
    }
    
    // 最多处理10批，避免无限循环
    if (batch >= 10) {
      console.log('\n⏹️ 已达到最大批次限制，停止处理');
      break;
    }
    
    // 间隔2秒，避免API限流
    console.log('⏳ 等待2秒...');
    execSync('sleep 2');
  }
  
  const finalCount = getUnreadCount();
  console.log('\n====================');
  console.log('📊 最终报告');
  console.log('====================');
  console.log(`初始未读: ${initialCount} 封`);
  console.log(`已处理: ${processed} 封`);
  console.log(`剩余未读: ${finalCount} 封`);
  console.log(`处理率: ${Math.round((processed / initialCount) * 100)}%`);
  
  if (finalCount > 0) {
    console.log(`\n💡 还有 ${finalCount} 封邮件未处理，可能是:`);
    console.log('  - 新收到的邮件');
    console.log('  - 处理失败的邮件');
    console.log('  - 需要手动处理的邮件');
  }
}

main();
