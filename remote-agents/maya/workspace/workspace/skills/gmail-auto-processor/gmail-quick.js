#!/usr/bin/env node
/**
 * Gmail 快速处理脚本 (简化版)
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// 配置
const CONFIG = {
  auto_archive: {
    keywords: ['促销', '优惠', '限时', '团购', '折扣', 'sale', 'discount', 'promo', 'unsubscribe'],
    senders: ['newsletter@', 'no-reply@', 'marketing@', 'noreply@', 'promotions@']
  },
  important_alerts: {
    senders: ['mexc.com', 'binance.com', 'okx.com', 'matrixport.com', 'google.com', 'github.com'],
    keywords: ['下架', '冻结', '安全', '密码', '验证', '提币', '登录', '异常', '警告', 'withdraw', 'security']
  },
  newsletter: {
    senders: ['substack.com', 'ycombinator.com', 'seekingalpha.com', 'diamandis.com']
  }
};

function log(msg) {
  console.log(msg);
}

function callMCP(tool, params) {
  const cmd = `mcporter call google-workspace ${tool} '${JSON.stringify(params)}' 2>/dev/null`;
  try {
    const result = execSync(cmd, { encoding: 'utf-8', timeout: 30000 });
    return JSON.parse(result);
  } catch (e) {
    return { error: e.message };
  }
}

function classifyEmail(subject, from) {
  const text = (subject + ' ' + from).toLowerCase();
  
  if (CONFIG.important_alerts.senders.some(s => from.toLowerCase().includes(s)) ||
      CONFIG.important_alerts.keywords.some(k => text.includes(k.toLowerCase()))) {
    return 'important';
  }
  
  if (CONFIG.newsletter.senders.some(s => from.toLowerCase().includes(s))) {
    return 'newsletter';
  }
  
  if (CONFIG.auto_archive.keywords.some(k => text.includes(k.toLowerCase())) ||
      CONFIG.auto_archive.senders.some(s => from.toLowerCase().includes(s))) {
    return 'promotion';
  }
  
  return 'other';
}

async function main() {
  log('📧 Gmail 自动处理器 (简化版)');
  log('='.repeat(50));
  
  const today = new Date().toISOString().split('T')[0];
  const stats = { total: 0, processed: 0, archived: [], important: [], newsletters: [], others: [] };
  
  // 搜索未读邮件
  log('\n🔍 搜索未读邮件...');
  const searchResult = callMCP('gmail.search', { query: 'is:unread', maxResults: 30 });
  
  if (searchResult.error || !searchResult.messages) {
    log('❌ 搜索失败');
    process.exit(1);
  }
  
  const messages = searchResult.messages.slice(0, 30);
  stats.total = searchResult.resultSizeEstimate || messages.length;
  log(`📨 找到 ${stats.total} 封未读邮件，处理前 ${messages.length} 封\n`);
  
  // 处理每封邮件
  for (let i = 0; i < messages.length; i++) {
    const msg = messages[i];
    const email = callMCP('gmail.get', { messageId: msg.id, format: 'metadata' });
    if (email.error) continue;
    
    const headers = email.payload?.headers || [];
    const subject = headers.find(h => h.name === 'Subject')?.value || '(无主题)';
    const from = headers.find(h => h.name === 'From')?.value || '';
    
    const category = classifyEmail(subject, from);
    const emailInfo = { id: msg.id, subject: subject.substring(0, 80), from: from.substring(0, 60) };
    
    switch (category) {
      case 'important':
        stats.important.push(emailInfo);
        log(`🔴 [重要] ${emailInfo.subject}`);
        break;
      case 'newsletter':
        stats.newsletters.push(emailInfo);
        log(`📰 [Newsletter] ${emailInfo.subject}`);
        break;
      case 'promotion':
        stats.archived.push(emailInfo);
        // 归档
        callMCP('gmail.modify', { messageId: msg.id, removeLabelIds: ['INBOX'] });
        log(`📦 [归档] ${emailInfo.subject}`);
        break;
      default:
        stats.others.push(emailInfo);
    }
    
    stats.processed++;
  }
  
  // 生成报告
  const report = generateReport(stats, today);
  
  // 保存到归档目录
  const archiveDir = path.join(__dirname, '../../kb/gmail-archive');
  if (!fs.existsSync(archiveDir)) {
    fs.mkdirSync(archiveDir, { recursive: true });
  }
  
  const archiveFile = path.join(archiveDir, `${today}.md`);
  fs.writeFileSync(archiveFile, report);
  
  // 输出结果
  log('\n' + '='.repeat(50));
  log('📊 处理完成!');
  log(`   总计未读: ${stats.total} 封`);
  log(`   已处理: ${stats.processed} 封`);
  log(`   📦 归档: ${stats.archived.length} 封促销邮件`);
  log(`   🔴 重要: ${stats.important.length} 封`);
  log(`   📰 Newsletter: ${stats.newsletters.length} 封`);
  log(`   📄 其他: ${stats.others.length} 封`);
  log(`\n💾 报告已保存: ${archiveFile}`);
  
  return stats;
}

function generateReport(stats, date) {
  const time = new Date().toLocaleString('zh-CN', { hour12: false });
  
  let report = `# Gmail 处理报告 - ${date}\n\n`;
  report += `**生成时间**: ${time}\n\n`;
  
  report += `## 📊 统计\n\n`;
  report += `- **总计未读**: ${stats.total} 封\n`;
  report += `- **已处理**: ${stats.processed} 封\n`;
  report += `- **已归档** (促销): ${stats.archived.length} 封\n`;
  report += `- **重要提醒**: ${stats.important.length} 封\n`;
  report += `- **Newsletter**: ${stats.newsletters.length} 封\n`;
  report += `- **其他**: ${stats.others.length} 封\n\n`;
  
  if (stats.important.length > 0) {
    report += `## 🔴 重要邮件\n\n`;
    stats.important.forEach((e, i) => {
      report += `${i + 1}. **${e.subject}**\n   - From: ${e.from}\n\n`;
    });
  }
  
  if (stats.newsletters.length > 0) {
    report += `## 📰 Newsletter\n\n`;
    stats.newsletters.forEach((e, i) => {
      report += `${i + 1}. **${e.subject}**\n   - From: ${e.from}\n\n`;
    });
  }
  
  if (stats.archived.length > 0) {
    report += `## 📦 已归档促销邮件 (${stats.archived.length} 封)\n\n`;
    report += `<details>\n<summary>点击查看列表</summary>\n\n`;
    stats.archived.forEach((e, i) => {
      report += `${i + 1}. ${e.subject}\n`;
    });
    report += `\n</details>\n\n`;
  }
  
  return report;
}

main().catch(console.error);
