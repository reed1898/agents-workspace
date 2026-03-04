#!/usr/bin/env node

/**
 * Gmail Auto Processor - 简化版
 * 自动处理 Gmail 邮件：归档促销、提醒重要、总结 Newsletter
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 尝试加载 Obsidian 集成
let obsidian;
try {
  obsidian = require('../obsidian-integration');
} catch (e) {
  obsidian = null;
}

const CONFIG_PATH = path.join(__dirname, 'config.json');

const DEFAULT_CONFIG = {
  auto_archive: {
    categories: ['promotions'],
    keywords: ['促销', '优惠', '限时', '团购', '折扣', '免费试用', '立即购买', '优惠码'],
    senders: ['newsletter@', 'no-reply@', 'marketing@', 'noreply@']
  },
  important_alerts: {
    senders: ['mexc.com', 'binance.com', 'okx.com', 'matrixport.com', 'google.com', 'github.com'],
    keywords: ['下架', '冻结', '安全', '密码', '验证', '提币', '登录', '异常', '警告', '风险'],
    notify_via: 'telegram'
  },
  newsletter: {
    senders: ['substack.com', 'ycombinator.com', 'seekingalpha.com', 'diamandis.com'],
    action: 'summarize',
    max_summary_length: 500
  },
  telegram: {
    enabled: true,
    summary_enabled: true
  }
};

function loadConfig() {
  if (fs.existsSync(CONFIG_PATH)) {
    return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
  }
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(DEFAULT_CONFIG, null, 2));
  console.log('✅ 已创建默认配置文件:', CONFIG_PATH);
  return DEFAULT_CONFIG;
}

function mcporterCall(tool, params) {
  const paramStr = Object.entries(params)
    .map(([k, v]) => {
      if (Array.isArray(v)) return `${k}='${JSON.stringify(v)}'`;
      return `${k}="${v}"`;
    })
    .join(' ');
  
  const cmd = `mcporter call --server google-workspace --tool "${tool}" ${paramStr}`;
  
  try {
    const result = execSync(cmd, { encoding: 'utf8', timeout: 30000 });
    return JSON.parse(result);
  } catch (error) {
    return null;
  }
}

function archiveMessage(messageId) {
  const cmd = `mcporter call --server google-workspace --tool "gmail.modify" messageId="${messageId}" removeLabelIds='["INBOX","UNREAD"]'`;
  try {
    execSync(cmd, { encoding: 'utf8', timeout: 10000 });
    return true;
  } catch (error) {
    return false;
  }
}

function markImportant(messageId) {
  const cmd = `mcporter call --server google-workspace --tool "gmail.modify" messageId="${messageId}" addLabelIds='["IMPORTANT"]'`;
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

function classifyEmail(email, config) {
  const from = email.from || '';
  const subject = email.subject || '';
  const snippet = email.snippet || '';
  
  const isImportantSender = config.important_alerts.senders.some(s => 
    from.toLowerCase().includes(s.toLowerCase())
  );
  const hasImportantKeyword = config.important_alerts.keywords.some(k => 
    subject.includes(k) || snippet.includes(k)
  );
  
  if (isImportantSender || hasImportantKeyword) {
    return 'important';
  }
  
  const isNewsletterSender = config.newsletter.senders.some(s => 
    from.toLowerCase().includes(s.toLowerCase())
  );
  
  if (isNewsletterSender) {
    return 'newsletter';
  }
  
  const isPromoCategory = email.labelIds?.includes('CATEGORY_PROMOTIONS');
  const hasPromoKeyword = config.auto_archive.keywords.some(k => 
    subject.includes(k) || snippet.includes(k)
  );
  const isPromoSender = config.auto_archive.senders.some(s => 
    from.toLowerCase().includes(s.toLowerCase())
  );
  
  if (isPromoCategory || hasPromoKeyword || isPromoSender) {
    return 'promotion';
  }
  
  return 'other';
}

async function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');
  
  console.log('📧 Gmail Auto Processor');
  console.log('========================\n');
  
  const config = loadConfig();
  
  if (dryRun) {
    console.log('🔍 预览模式（不修改邮件）\n');
  }
  
  const stats = { total: 0, archived: 0, important: 0, newsletter: 0, other: 0 };
  const importantEmails = [];
  const newsletterEmails = [];
  
  console.log('🔍 搜索未读邮件...');
  const result = mcporterCall('gmail.search', { query: 'is:unread', maxResults: 50 });
  
  if (!result || !result.messages) {
    console.log('✅ 没有未读邮件');
    return;
  }
  
  const messages = result.messages;
  console.log(`📨 找到 ${messages.length} 封未读邮件\n`);
  
  // 批量获取邮件详情
  const emails = [];
  for (const msg of messages.slice(0, 20)) { // 限制20封避免超时
    const email = mcporterCall('gmail.get', { messageId: msg.id });
    if (email) {
      emails.push({ ...email, id: msg.id });
    }
  }
  
  // 处理邮件
  for (const email of emails) {
    stats.total++;
    const category = classifyEmail(email, config);
    
    switch (category) {
      case 'important':
        stats.important++;
        importantEmails.push(email);
        if (!dryRun) {
          markImportant(email.id);
          markAsRead(email.id);
        }
        console.log(`${dryRun ? '[预览]' : '🔴'} 重要: ${email.subject?.substring(0, 50)}`);
        break;
        
      case 'newsletter':
        stats.newsletter++;
        newsletterEmails.push(email);
        if (!dryRun) {
          markAsRead(email.id);
        }
        console.log(`📰 Newsletter: ${email.subject?.substring(0, 50)}`);
        break;
        
      case 'promotion':
        stats.archived++;
        if (!dryRun) {
          archiveMessage(email.id);
          markAsRead(email.id);
        }
        console.log(`${dryRun ? '[预览]' : '📦'} 已归档: ${email.subject?.substring(0, 50)}`);
        break;
        
      default:
        stats.other++;
        if (!dryRun) {
          markAsRead(email.id);
        }
        console.log(`➡️  保留: ${email.subject?.substring(0, 50)}`);
    }
  }
  
  // 输出统计
  console.log('\n📊 处理统计:');
  console.log(`  总计: ${stats.total}`);
  console.log(`  归档 (促销): ${stats.archived}`);
  console.log(`  重要: ${stats.important}`);
  console.log(`  Newsletter: ${stats.newsletter}`);
  console.log(`  其他: ${stats.other}`);
  
  // Telegram 汇总
  if (config.telegram.enabled && !dryRun) {
    const now = new Date().toLocaleString('zh-CN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
    let message = `📧 Gmail 处理报告 (${now})\n\n`;
    message += `📊 统计:\n`;
    message += `• 已处理: ${stats.total} 封\n`;
    message += `• 归档: ${stats.archived} 封 (促销)\n`;
    message += `• 重要: ${stats.important} 封\n`;
    message += `• Newsletter: ${stats.newsletter} 封\n`;
    
    if (importantEmails.length > 0) {
      message += `\n🔴 重要提醒:\n`;
      importantEmails.slice(0, 5).forEach(email => {
        const subject = email.subject?.length > 35 ? email.subject.substring(0, 35) + '...' : email.subject;
        message += `• ${subject}\n`;
      });
    }
    
    if (newsletterEmails.length > 0) {
      message += `\n📰 Newsletter:\n`;
      newsletterEmails.slice(0, 5).forEach(email => {
        const subject = email.subject?.length > 30 ? email.subject.substring(0, 30) + '...' : email.subject;
        message += `• ${subject}\n`;
      });
    }
    
    console.log('\n' + '='.repeat(50));
    console.log('📨 Telegram 汇总:');
    console.log(message);
    console.log('='.repeat(50));
  }
  
  // 保存到 Obsidian
  if (!dryRun && obsidian && obsidian.checkConfig()) {
    console.log('\n📝 保存到 Obsidian...');
    try {
      obsidian.saveEmailReport({
        stats,
        important_emails: importantEmails,
        newsletters: newsletterEmails
      });
      
      // 同时追加到 Daily Note
      const today = obsidian.getToday();
      obsidian.appendToDailyNote({
        time: today.datetime,
        content: `## 📧 邮件处理\n\n- 处理: ${stats.total} 封\n- 重要: ${stats.important} 封\n- Newsletter: ${stats.newsletter} 封\n- 归档: ${stats.archived} 封\n\n[[${today.date}-邮件分析|查看详细报告]]`
      });
    } catch (e) {
      console.error('❌ Obsidian 保存失败:', e.message);
    }
  }
  
  console.log('\n✅ 处理完成');
}

main().catch(err => {
  console.error('❌ 错误:', err);
  process.exit(1);
});
