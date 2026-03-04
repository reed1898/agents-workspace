#!/usr/bin/env node

/**
 * Gmail Auto Processor - 焦虑终结版
 * 核心目标：处理过的邮件都标记已读，只保留真正重要的
 */

const { execSync } = require('child_process');
const path = require('path');

const CONFIG_PATH = path.join(__dirname, 'config.json');

const DEFAULT_CONFIG = {
  important_senders: [
    'mexc.com', 'binance.com', 'okx.com', 'matrixport.com',
    'google.com', 'github.com'
  ],
  important_keywords: [
    '下架', '冻结', '安全', '密码', '验证', '提币', '登录', '异常', 
    '警告', '风险', '审核', 'KYC', '手续费', '到账'
  ]
};

function loadConfig() {
  try {
    const fs = require('fs');
    if (fs.existsSync(CONFIG_PATH)) {
      const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
      return {
        important_senders: config.important_senders || DEFAULT_CONFIG.important_senders,
        important_keywords: config.important_keywords || DEFAULT_CONFIG.important_keywords
      };
    }
  } catch (e) {}
  return DEFAULT_CONFIG;
}

// 带超时的 API 调用
function mcporterCall(tool, params, timeoutMs = 15000) {
  const paramStr = Object.entries(params)
    .map(([k, v]) => typeof v === 'string' ? `${k}="${v}"` : `${k}=${v}`)
    .join(' ');
  
  const cmd = `mcporter call --server google-workspace --tool "${tool}" ${paramStr}`;
  
  try {
    const result = execSync(cmd, { encoding: 'utf8', timeout: timeoutMs });
    return JSON.parse(result);
  } catch (error) {
    return null;
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

// 归档邮件（移出 Inbox）
function archiveMessage(messageId) {
  const cmd = `mcporter call --server google-workspace --tool "gmail.modify" messageId="${messageId}" removeLabelIds='["INBOX","UNREAD"]'`;
  try {
    execSync(cmd, { encoding: 'utf8', timeout: 10000 });
    return true;
  } catch (error) {
    // 如果归档失败，至少尝试标记已读
    return markAsRead(messageId);
  }
}

// 判断是否是重要邮件
function isImportant(email, config) {
  const from = (email.from || '').toLowerCase();
  const subject = (email.subject || '').toLowerCase();
  const snippet = (email.snippet || '').toLowerCase();
  
  // 检查发件人
  const importantSender = config.important_senders.some(s => from.includes(s.toLowerCase()));
  if (importantSender) return true;
  
  // 检查关键词
  const importantKeyword = config.important_keywords.some(k => 
    subject.includes(k) || snippet.includes(k)
  );
  if (importantKeyword) return true;
  
  // 检查是否有 IMPORTANT 标签
  if (email.labelIds?.includes('IMPORTANT')) return true;
  
  return false;
}

async function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');
  const maxEmails = args.includes('--max') ? parseInt(args[args.indexOf('--max') + 1]) || 50 : 50;
  
  console.log('📧 Gmail 焦虑终结器');
  console.log('====================');
  console.log(`模式: ${dryRun ? '预览' : '执行'} | 最大处理: ${maxEmails} 封\n`);
  
  const config = loadConfig();
  
  // 1. 搜索未读邮件
  console.log('🔍 搜索未读邮件...');
  const searchResult = mcporterCall('gmail.search', { query: 'is:unread', maxResults: maxEmails }, 20000);
  
  if (!searchResult || !searchResult.messages || searchResult.messages.length === 0) {
    console.log('✅ 没有未读邮件，真棒！');
    return;
  }
  
  const messages = searchResult.messages;
  const totalUnread = searchResult.resultSizeEstimate || messages.length;
  
  console.log(`📨 总共 ${totalUnread} 封未读，本次处理 ${messages.length} 封\n`);
  
  let important = 0, archived = 0, markedRead = 0, failed = 0;
  const importantEmails = [];
  
  // 2. 处理每封邮件
  for (let i = 0; i < messages.length; i++) {
    const msg = messages[i];
    
    // 获取邮件基本信息（带超时）
    const email = mcporterCall('gmail.get', { messageId: msg.id }, 8000);
    
    if (!email) {
      console.log(`[${i + 1}/${messages.length}] ❌ 获取失败: ${msg.id}`);
      failed++;
      continue;
    }
    
    const subject = email.subject || '(无主题)';
    const shortSubject = subject.length > 40 ? subject.substring(0, 40) + '...' : subject;
    
    // 判断是否重要
    const importantMail = isImportant(email, config);
    
    if (importantMail) {
      // 重要邮件：保留在 Inbox，但标记为已读
      console.log(`[${i + 1}/${messages.length}] 🔴 重要: ${shortSubject}`);
      importantEmails.push(email);
      
      if (!dryRun) {
        // 重要邮件只标记已读，不移出 Inbox，这样你仍然能看到
        const success = markAsRead(msg.id);
        if (success) {
          markedRead++;
          important++;
        } else {
          failed++;
        }
      }
    } else {
      // 非重要邮件：归档 + 标记已读
      console.log(`[${i + 1}/${messages.length}] 📦 归档: ${shortSubject}`);
      
      if (!dryRun) {
        const success = archiveMessage(msg.id);
        if (success) {
          archived++;
        } else {
          failed++;
        }
      }
    }
    
    // 每5封休息300ms，避免API限流
    if ((i + 1) % 5 === 0 && i < messages.length - 1) {
      await new Promise(r => setTimeout(r, 300));
    }
  }
  
  // 3. 输出结果
  console.log('\n====================');
  console.log('📊 处理完成');
  console.log('====================');
  console.log(`处理邮件: ${messages.length} 封`);
  console.log(`🔴 重要: ${important} 封（已读但保留）`);
  console.log(`📦 归档: ${archived} 封`);
  console.log(`❌ 失败: ${failed} 封`);
  
  const processed = important + archived;
  const remaining = totalUnread - processed;
  
  console.log(`\n✅ 成功处理: ${processed}/${messages.length}`);
  
  if (remaining > 0) {
    console.log(`📨 剩余未读: ${remaining} 封`);
    if (!dryRun && remaining > 0) {
      console.log('\n💡 提示: 可以再次运行此脚本继续处理');
      console.log('   命令: node index-anxiety-free.js');
    }
  } else {
    console.log('\n🎉 太棒了！本次处理的邮件已全部清理');
  }
  
  // 4. 显示重要邮件列表
  if (importantEmails.length > 0) {
    console.log('\n🔴 重要邮件列表:');
    importantEmails.forEach((email, i) => {
      console.log(`  ${i + 1}. ${email.subject?.substring(0, 50)}`);
    });
  }
}

main().catch(err => {
  console.error('❌ 错误:', err.message);
  process.exit(1);
});
