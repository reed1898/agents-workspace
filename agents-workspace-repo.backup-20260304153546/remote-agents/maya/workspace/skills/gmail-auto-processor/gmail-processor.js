#!/usr/bin/env node
/**
 * Gmail 自动处理脚本
 * 分类：促销邮件归档、重要邮件提醒、Newsletter 总结
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// 配置
const CONFIG = {
  auto_archive: {
    keywords: ['促销', '优惠', '限时', '团购', '折扣', '免费试用', '立即购买', '优惠码', 'sale', 'discount', 'promo'],
    senders: ['newsletter@', 'no-reply@', 'marketing@', 'noreply@', 'promotions@']
  },
  important_alerts: {
    senders: ['mexc.com', 'binance.com', 'okx.com', 'matrixport.com', 'google.com', 'github.com'],
    keywords: ['下架', '冻结', '安全', '密码', '验证', '提币', '登录', '异常', '警告', '风险', 'withdraw', 'security']
  },
  newsletter: {
    senders: ['substack.com', 'ycombinator.com', 'seekingalpha.com', 'diamandis.com', 'newsletter']
  }
};

// 颜色输出
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m'
};

function log(msg, color = 'reset') {
  console.log(`${colors[color]}${msg}${colors.reset}`);
}

// 调用 MCP 工具
function callMCP(tool, params) {
  const cmd = `mcporter call google-workspace ${tool} '${JSON.stringify(params)}' 2>/dev/null`;
  try {
    const result = execSync(cmd, { encoding: 'utf-8', timeout: 30000 });
    return JSON.parse(result);
  } catch (e) {
    return { error: e.message };
  }
}

// 获取邮件详情
function getMessage(messageId) {
  return callMCP('gmail.get', { messageId, format: 'full' });
}

// 修改邮件（归档/标签）
function modifyMessage(messageId, addLabelIds = [], removeLabelIds = []) {
  return callMCP('gmail.modify', { messageId, addLabelIds, removeLabelIds });
}

// 分类邮件
function classifyEmail(email) {
  const subject = email.subject || '';
  const from = email.from || '';
  const text = (subject + ' ' + from).toLowerCase();
  
  // 检查重要邮件
  const isImportant = CONFIG.important_alerts.senders.some(s => from.toLowerCase().includes(s)) ||
                     CONFIG.important_alerts.keywords.some(k => text.includes(k.toLowerCase()));
  if (isImportant) return 'important';
  
  // 检查 Newsletter
  const isNewsletter = CONFIG.newsletter.senders.some(s => from.toLowerCase().includes(s)) ||
                      subject.toLowerCase().includes('newsletter');
  if (isNewsletter) return 'newsletter';
  
  // 检查促销邮件
  const isPromotion = CONFIG.auto_archive.keywords.some(k => text.includes(k.toLowerCase())) ||
                     CONFIG.auto_archive.senders.some(s => from.toLowerCase().includes(s));
  if (isPromotion) return 'promotion';
  
  return 'other';
}

// 主处理流程
async function main() {
  log('📧 Gmail 自动处理器', 'cyan');
  log('='.repeat(50), 'cyan');
  
  const startTime = Date.now();
  const today = new Date().toISOString().split('T')[0];
  
  // 统计
  const stats = {
    total: 0,
    processed: 0,
    archived: [],
    important: [],
    newsletters: [],
    others: []
  };
  
  // 搜索未读邮件
  log('\n🔍 搜索未读邮件...', 'blue');
  const searchResult = callMCP('gmail.search', { query: 'is:unread', maxResults: 50 });
  
  if (searchResult.error || !searchResult.messages) {
    log('❌ 搜索失败: ' + (searchResult.error || '未知错误'), 'red');
    process.exit(1);
  }
  
  const messages = searchResult.messages;
  stats.total = searchResult.resultSizeEstimate || messages.length;
  log(`📨 找到 ${stats.total} 封未读邮件，处理前 ${messages.length} 封`, 'green');
  
  // 处理每封邮件
  for (let i = 0; i < messages.length; i++) {
    const msg = messages[i];
    process.stdout.write(`\r🔄 处理中... ${i + 1}/${messages.length}`);
    
    const email = getMessage(msg.id);
    if (email.error) continue;
    
    // 提取基本信息
    const headers = email.payload?.headers || [];
    const subject = headers.find(h => h.name === 'Subject')?.value || '(无主题)';
    const from = headers.find(h => h.name === 'From')?.value || '';
    const date = headers.find(h => h.name === 'Date')?.value || '';
    
    const emailInfo = { id: msg.id, subject, from, date, snippet: email.snippet };
    
    // 分类
    const category = classifyEmail(emailInfo);
    
    switch (category) {
      case 'important':
        stats.important.push(emailInfo);
        break;
      case 'newsletter':
        stats.newsletters.push(emailInfo);
        break;
      case 'promotion':
        stats.archived.push(emailInfo);
        // 归档：移除 INBOX 标签
        modifyMessage(msg.id, [], ['INBOX']);
        break;
      default:
        stats.others.push(emailInfo);
    }
    
    stats.processed++;
  }
  
  console.log(''); // 换行
  
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
  log('\n' + '='.repeat(50), 'cyan');
  log('📊 处理完成!', 'green');
  log(`   总计: ${stats.total} 封未读`, 'reset');
  log(`   已处理: ${stats.processed} 封`, 'green');
  log(`   归档: ${stats.archived.length} 封促销邮件`, 'yellow');
  log(`   重要: ${stats.important.length} 封`, 'red');
  log(`   Newsletter: ${stats.newsletters.length} 封`, 'blue');
  log(`   其他: ${stats.others.length} 封`, 'reset');
  log(`\n💾 报告已保存: ${archiveFile}`, 'cyan');
  
  const duration = ((Date.now() - startTime) / 1000).toFixed(1);
  log(`⏱️  耗时: ${duration}秒`, 'reset');
  
  return stats;
}

// 生成报告
function generateReport(stats, date) {
  const time = new Date().toLocaleString('zh-CN', { hour12: false });
  
  let report = `# Gmail 处理报告 - ${date}\n\n`;
  report += `**生成时间**: ${time}\n\n`;
  
  report += `## 📊 统计\n\n`;
  report += `- **总计未读**: ${stats.total} 封\n`;
  report += `- **已处理**: ${stats.processed} 封\n`;
  report += `- **归档** (促销): ${stats.archived.length} 封\n`;
  report += `- **重要提醒**: ${stats.important.length} 封\n`;
  report += `- **Newsletter**: ${stats.newsletters.length} 封\n`;
  report += `- **其他**: ${stats.others.length} 封\n\n`;
  
  if (stats.important.length > 0) {
    report += `## 🔴 重要邮件\n\n`;
    stats.important.forEach((e, i) => {
      report += `${i + 1}. **${escapeMd(e.subject)}**\n`;
      report += `   - From: ${e.from}\n`;
      report += `   - Snippet: ${e.snippet?.substring(0, 100) || ''}...\n\n`;
    });
  }
  
  if (stats.newsletters.length > 0) {
    report += `## 📰 Newsletter\n\n`;
    stats.newsletters.forEach((e, i) => {
      report += `${i + 1}. **${escapeMd(e.subject)}**\n`;
      report += `   - From: ${e.from}\n\n`;
    });
  }
  
  if (stats.archived.length > 0) {
    report += `## 📦 已归档促销邮件\n\n`;
    report += `<details>\n<summary>点击查看 (${stats.archived.length} 封)</summary>\n\n`;
    stats.archived.forEach((e, i) => {
      report += `${i + 1}. ${escapeMd(e.subject)} - ${e.from}\n`;
    });
    report += `\n</details>\n\n`;
  }
  
  return report;
}

function escapeMd(text) {
  return (text || '').replace(/[|\\*_{}[\]]/g, '\\$&');
}

main().catch(console.error);
