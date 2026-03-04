#!/usr/bin/env node

/**
 * Gmail Archive Test - 调试版本
 */

const { execSync } = require('child_process');

function mcporterCall(tool, params) {
  const paramStr = Object.entries(params)
    .map(([k, v]) => {
      if (typeof v === 'string') return `${k}="${v}"`;
      return `${k}=${v}`;
    })
    .join(' ');
  
  const cmd = `mcporter call --server google-workspace --tool "${tool}" ${paramStr}`;
  
  try {
    const result = execSync(cmd, { encoding: 'utf8', timeout: 30000 });
    return JSON.parse(result);
  } catch (error) {
    console.error(`❌ API调用失败: ${tool}`, error.stderr?.substring(0, 100));
    return null;
  }
}

function archiveMessage(messageId) {
  const cmd = `mcporter call --server google-workspace --tool "gmail.modify" messageId="${messageId}" removeLabelIds='["INBOX","UNREAD"]'`;
  try {
    execSync(cmd, { encoding: 'utf8', timeout: 15000 });
    return true;
  } catch (error) {
    return false;
  }
}

async function main() {
  console.log('📧 Gmail 归档测试');
  console.log('==================\n');
  
  // 1. 搜索未读邮件
  console.log('🔍 搜索未读邮件...');
  const result = mcporterCall('gmail.search', { query: 'is:unread', maxResults: 50 });
  
  if (!result || !result.messages || result.messages.length === 0) {
    console.log('✅ 没有未读邮件');
    return;
  }
  
  const totalCount = result.resultSizeEstimate || result.messages.length;
  console.log(`📨 总共 ${totalCount} 封未读，获取前 ${result.messages.length} 封详情\n`);
  
  // 2. 处理邮件 - 简化版本，直接归档所有 category:promotions
  let archived = 0;
  let failed = 0;
  let processed = 0;
  
  for (const msg of result.messages.slice(0, 30)) { // 一次处理30封
    processed++;
    
    // 获取邮件详情查看标签
    const email = mcporterCall('gmail.get', { messageId: msg.id });
    
    if (!email) {
      console.log(`❌ 获取详情失败: ${msg.id}`);
      failed++;
      continue;
    }
    
    const isPromo = email.labelIds?.includes('CATEGORY_PROMOTIONS');
    const subject = email.subject || '(无主题)';
    
    if (isPromo) {
      // 归档促销邮件
      const success = archiveMessage(msg.id);
      if (success) {
        console.log(`✅ 已归档: ${subject.substring(0, 50)}`);
        archived++;
      } else {
        console.log(`❌ 归档失败: ${subject.substring(0, 50)}`);
        failed++;
      }
    } else {
      console.log(`➡️  跳过 (非促销): ${subject.substring(0, 50)}`);
    }
    
    // 每5封暂停500ms，避免限流
    if (processed % 5 === 0) {
      await new Promise(r => setTimeout(r, 500));
    }
  }
  
  console.log('\n==================');
  console.log('📊 处理完成');
  console.log(`处理: ${processed} 封`);
  console.log(`归档: ${archived} 封`);
  console.log(`失败: ${failed} 封`);
  console.log(`剩余未读: ${totalCount - archived}`);
}

main().catch(console.error);
