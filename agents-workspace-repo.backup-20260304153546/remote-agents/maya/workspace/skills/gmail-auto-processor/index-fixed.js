#!/usr/bin/env node

/**
 * Gmail Auto Processor - 修复版本
 * 添加更好的超时处理和错误处理
 */

const { execSync } = require('child_process');
const path = require('path');

// 配置
const CONFIG_PATH = path.join(__dirname, 'config.json');

const DEFAULT_CONFIG = {
  auto_archive: {
    categories: ['promotions'],
    keywords: ['促销', '优惠', '限时', '团购', '折扣'],
    senders: ['newsletter@', 'no-reply@', 'marketing@']
  },
  important_alerts: {
    senders: ['mexc.com', 'binance.com', 'okx.com', 'matrixport.com'],
    keywords: ['下架', '冻结', '安全', '密码', '验证', '提币']
  },
  telegram: { enabled: true }
};

function loadConfig() {
  if (require('fs').existsSync(CONFIG_PATH)) {
    return JSON.parse(require('fs').readFileSync(CONFIG_PATH, 'utf8'));
  }
  return DEFAULT_CONFIG;
}

// 带超时的 mcporter 调用
function mcporterCall(tool, params, timeoutMs = 15000) {
  const paramStr = Object.entries(params)
    .map(([k, v]) => typeof v === 'string' ? `${k}="${v}"` : `${k}=${v}`)
    .join(' ');
  
  const cmd = `mcporter call --server google-workspace --tool "${tool}" ${paramStr}`;
  
  try {
    const result = execSync(cmd, { encoding: 'utf8', timeout: timeoutMs });
    return JSON.parse(result);
  } catch (error) {
    console.error(`⚠️  API调用失败 ${tool}:`, error.message?.substring(0, 50));
    return null;
  }
}

// 归档邮件
function archiveMessage(messageId) {
  const cmd = `mcporter call --server google-workspace --tool "gmail.modify" messageId="${messageId}" removeLabelIds='["INBOX","UNREAD"]'`;
  try {
    execSync(cmd, { encoding: 'utf8', timeout: 10000 });
    return true;
  } catch (error) {
    return false;
  }
}

// 标记已读
function markAsRead(messageId) {
  const cmd = `mcporter call --server google-workspace --tool "gmail.modify" messageId="${messageId}" removeLabelIds='["UNREAD"]'`;
  try {
    execSync(cmd, { encoding: 'utf8', timeout: 10000 });
    return true;
  } catch (error) {
    return false;
  }
}

// 分类邮件 - 基于搜索查询而不是获取详情
function classifyBySearch(messageId, config) {
  // 简化版本：直接使用搜索 API 判断分类
  // 避免获取完整邮件内容导致的超时
  
  // 检查是否是促销邮件（通过搜索验证）
  const promoCheck = mcporterCall('gmail.get', { messageId }, 8000);
  if (!promoCheck) return 'unknown';
  
  const labelIds = promoCheck.labelIds || [];
  const from = promoCheck.from || '';
  const subject = promoCheck.subject || '';
  
  // 重要邮件检查
  const isImportantSender = config.important_alerts.senders.some(s => 
    from.toLowerCase().includes(s.toLowerCase())
  );
  if (isImportantSender || labelIds.includes('IMPORTANT')) {
    return 'important';
  }
  
  // 促销邮件检查
  if (labelIds.includes('CATEGORY_PROMOTIONS')) {
    return 'promotion';
  }
  
  return 'other';
}

async function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');
  
  console.log('📧 Gmail Auto Processor (Fixed)');
  console.log('================================\n');
  
  const config = loadConfig();
  
  // 1. 搜索未读邮件
  console.log('🔍 搜索未读邮件...');
  const searchResult = mcporterCall('gmail.search', { query: 'is:unread', maxResults: 30 }, 20000);
  
  if (!searchResult || !searchResult.messages || searchResult.messages.length === 0) {
    console.log('✅ 没有未读邮件');
    return;
  }
  
  const messages = searchResult.messages;
  const totalUnread = searchResult.resultSizeEstimate || messages.length;
  
  console.log(`📨 找到 ${totalUnread} 封未读，处理前 ${messages.length} 封\n`);
  
  let archived = 0, markedRead = 0, failed = 0, important = 0;
  
  // 2. 处理每封邮件
  for (let i = 0; i < messages.length; i++) {
    const msg = messages[i];
    console.log(`\n[${i + 1}/${messages.length}] 处理: ${msg.id}`);
    
    // 分类（带超时保护）
    const category = classifyBySearch(msg.id, config);
    
    if (category === 'unknown') {
      console.log('  ⚠️  无法分类，跳过');
      failed++;
      continue;
    }
    
    console.log(`  分类: ${category}`);
    
    if (dryRun) {
      console.log(`  [预览] 将处理为 ${category}`);
      continue;
    }
    
    // 执行操作
    let success = false;
    
    if (category === 'promotion') {
      success = archiveMessage(msg.id);
      if (success) {
        archived++;
        console.log('  ✅ 已归档');
      }
    } else if (category === 'important') {
      success = markAsRead(msg.id);
      if (success) {
        important++;
        console.log('  ✅ 已标记已读（重要）');
      }
    } else {
      success = markAsRead(msg.id);
      if (success) {
        markedRead++;
        console.log('  ✅ 已标记已读');
      }
    }
    
    if (!success) {
      failed++;
      console.log('  ❌ 处理失败');
    }
    
    // 每5封休息500ms
    if ((i + 1) % 5 === 0 && i < messages.length - 1) {
      console.log('  ⏳ 休息500ms...');
      await new Promise(r => setTimeout(r, 500));
    }
  }
  
  // 3. 输出统计
  console.log('\n================================');
  console.log('📊 处理完成');
  console.log('================================');
  console.log(`总计未读: ${totalUnread}`);
  console.log(`本次处理: ${messages.length}`);
  console.log(`归档: ${archived}`);
  console.log(`重要: ${important}`);
  console.log(`标记已读: ${markedRead}`);
  console.log(`失败: ${failed}`);
  
  if (!dryRun && (archived + important + markedRead) > 0) {
    console.log(`\n💡 建议: 还有 ${totalUnread - archived - important - markedRead} 封未处理`);
    console.log('   可再次运行此脚本继续处理');
  }
}

main().catch(err => {
  console.error('❌ 错误:', err);
  process.exit(1);
});
