const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const CONFIG_PATH = path.join(__dirname, 'config.json');

// 默认配置
const DEFAULT_CONFIG = {
  vault_path: '',  // 需要用户配置
  daily_note_folder: 'Daily',
  email_folder: 'Emails/Analysis',
  important_email_folder: 'Emails/Important',
  newsletter_folder: 'Newsletter',
  inbox_folder: 'Inbox',
  auto_create_folders: true
};

class ObsidianIntegration {
  constructor() {
    this.config = this.loadConfig();
  }

  loadConfig() {
    if (fs.existsSync(CONFIG_PATH)) {
      return { ...DEFAULT_CONFIG, ...JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8')) };
    }
    fs.writeFileSync(CONFIG_PATH, JSON.stringify(DEFAULT_CONFIG, null, 2));
    console.log('✅ 已创建默认配置文件:', CONFIG_PATH);
    return DEFAULT_CONFIG;
  }

  // 确保目录存在
  ensureDir(dirPath) {
    if (!fs.existsSync(dirPath)) {
      fs.mkdirSync(dirPath, { recursive: true });
    }
  }

  // 获取今日日期
  getToday() {
    const now = new Date();
    return {
      date: now.toISOString().split('T')[0],
      datetime: now.toLocaleString('zh-CN'),
      year: now.getFullYear(),
      month: String(now.getMonth() + 1).padStart(2, '0'),
      day: String(now.getDate()).padStart(2, '0')
    };
  }

  // 清理文件名
  sanitizeFilename(str) {
    return str
      .replace(/[<>:"/\\|?*]/g, '-')
      .replace(/\s+/g, '-')
      .substring(0, 100);
  }

  // 保存邮件分析报告
  saveEmailReport(data) {
    if (!this.config.vault_path) {
      console.error('❌ 请先配置 Obsidian vault 路径');
      return false;
    }

    const today = this.getToday();
    const folderPath = path.join(this.config.vault_path, this.config.email_folder);
    
    if (this.config.auto_create_folders) {
      this.ensureDir(folderPath);
    }

    const filename = `${today.date}-邮件分析.md`;
    const filepath = path.join(folderPath, filename);

    const content = this.generateEmailReportContent(data, today);
    
    fs.writeFileSync(filepath, content);
    console.log(`✅ 已保存到: ${filepath}`);
    return filepath;
  }

  // 生成邮件分析报告内容
  generateEmailReportContent(data, today) {
    const { stats, important_emails = [], newsletters = [] } = data;
    
    let content = `---\n`;
    content += `date: ${today.date}\n`;
    content += `type: email-analysis\n`;
    content += `total: ${stats?.total || 0}\n`;
    content += `important: ${stats?.important || 0}\n`;
    content += `newsletter: ${stats?.newsletter || 0}\n`;
    content += `archived: ${stats?.archived || 0}\n`;
    content += `---\n\n`;
    
    content += `# ${today.date} 邮件分析报告\n\n`;
    content += `> 生成时间: ${today.datetime}\n\n`;
    
    // 统计
    content += `## 📊 统计\n\n`;
    content += `- **总计处理**: ${stats?.total || 0} 封\n`;
    content += `- **重要邮件**: ${stats?.important || 0} 封\n`;
    content += `- **Newsletter**: ${stats?.newsletter || 0} 封\n`;
    content += `- **归档**: ${stats?.archived || 0} 封\n`;
    content += `- **其他**: ${stats?.other || 0} 封\n\n`;
    
    // 重要邮件
    if (important_emails.length > 0) {
      content += `## 🔴 重要邮件\n\n`;
      important_emails.forEach((email, i) => {
        content += `### ${i + 1}. ${email.subject}\n\n`;
        content += `- **发件人**: ${email.from}\n`;
        content += `- **时间**: ${email.date}\n`;
        if (email.snippet) {
          content += `- **摘要**: ${email.snippet.substring(0, 200)}...\n`;
        }
        content += `\n`;
      });
    }
    
    // Newsletter
    if (newsletters.length > 0) {
      content += `## 📰 Newsletter\n\n`;
      newsletters.forEach((email, i) => {
        content += `### ${i + 1}. ${email.subject}\n\n`;
        content += `- **来源**: ${email.from?.split('<')[0]?.trim()}\n`;
        content += `- **时间**: ${email.date}\n`;
        if (email.snippet) {
          content += `- **摘要**: ${email.snippet.substring(0, 150)}...\n`;
        }
        content += `\n`;
      });
    }
    
    content += `---\n`;
    content += `*由 Gmail Auto Processor 自动生成*\n`;
    
    return content;
  }

  // 追加到 Daily Note
  appendToDailyNote(section) {
    if (!this.config.vault_path) {
      console.error('❌ 请先配置 Obsidian vault 路径');
      return false;
    }

    const today = this.getToday();
    const folderPath = path.join(this.config.vault_path, this.config.daily_note_folder);
    
    if (this.config.auto_create_folders) {
      this.ensureDir(folderPath);
    }

    const filename = `${today.date}.md`;
    const filepath = path.join(folderPath, filename);

    let content = '';
    if (fs.existsSync(filepath)) {
      content = fs.readFileSync(filepath, 'utf8');
    } else {
      // 新建 daily note
      content = `# ${today.date}\n\n`;
      content += `## 日志\n\n`;
    }

    // 追加内容
    content += `\n### ${section.time || today.datetime}\n\n`;
    content += section.content;
    content += `\n`;

    fs.writeFileSync(filepath, content);
    console.log(`✅ 已追加到 Daily Note: ${filepath}`);
    return filepath;
  }

  // 创建独立笔记
  createNote({ folder, title, content, tags = [] }) {
    if (!this.config.vault_path) {
      console.error('❌ 请先配置 Obsidian vault 路径');
      return false;
    }

    const folderPath = path.join(this.config.vault_path, folder);
    
    if (this.config.auto_create_folders) {
      this.ensureDir(folderPath);
    }

    const filename = `${this.sanitizeFilename(title)}.md`;
    const filepath = path.join(folderPath, filename);

    let frontmatter = `---\n`;
    frontmatter += `title: ${title}\n`;
    frontmatter += `date: ${this.getToday().date}\n`;
    if (tags.length > 0) {
      frontmatter += `tags: [${tags.join(', ')}]\n`;
    }
    frontmatter += `---\n\n`;

    fs.writeFileSync(filepath, frontmatter + content);
    console.log(`✅ 已创建笔记: ${filepath}`);
    return filepath;
  }

  // 配置检查
  checkConfig() {
    if (!this.config.vault_path) {
      console.log('⚠️  Obsidian vault 路径未配置');
      console.log('请编辑 config.json 设置 vault_path');
      console.log('示例: ~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Main');
      return false;
    }
    
    if (!fs.existsSync(this.config.vault_path)) {
      console.log('⚠️  配置的 vault 路径不存在:', this.config.vault_path);
      return false;
    }
    
    return true;
  }
}

// 导出单例
module.exports = new ObsidianIntegration();

// 如果直接运行
if (require.main === module) {
  const obsidian = new ObsidianIntegration();
  
  // 检查配置
  if (!obsidian.checkConfig()) {
    process.exit(1);
  }
  
  console.log('✅ Obsidian 集成配置正常');
  console.log('Vault 路径:', obsidian.config.vault_path);
}
