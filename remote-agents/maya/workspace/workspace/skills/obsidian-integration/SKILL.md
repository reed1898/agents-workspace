---
name: obsidian-integration
description: |
  将处理结果自动保存到 Obsidian 知识库。
  支持 Gmail 分析、日报、会议纪要等内容的结构化存储。
metadata:
  version: "1.0.0"
  requires:
    - obsidian-cli
---

# Obsidian Integration

自动将 AI 处理结果保存到 Obsidian 知识库，建立个人知识管理体系。

## 配置

编辑 `config.json`:
```json
{
  "vault_path": "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Main",
  "daily_note_folder": "Daily",
  "inbox_folder": "Inbox",
  "email_folder": "Emails",
  "auto_create_folders": true
}
```

## 使用方式

### 从 Gmail Processor 保存
```javascript
const obsidian = require('./obsidian-integration');

// 保存邮件分析报告
obsidian.saveEmailReport({
  date: '2026-02-09',
  stats: { total: 20, important: 2, newsletter: 9 },
  important_emails: [...],
  newsletters: [...]
});
```

### 保存到 Daily Note
```javascript
obsidian.appendToDailyNote({
  content: '## Gmail 处理\n- 处理了 20 封邮件\n- 2 封重要'
});
```

### 创建独立笔记
```javascript
obsidian.createNote({
  folder: 'Emails/Analysis',
  title: '2026-02-09 邮件分析',
  content: '...'
});
```

## 目录结构

```
Obsidian Vault/
├── Daily/
│   ├── 2026-02-09.md
│   └── 2026-02-08.md
├── Emails/
│   ├── Analysis/
│   │   └── 2026-02-09.md
│   └── Important/
│       └── MEXC-下架通知.md
├── Newsletter/
│   ├── Peter-Diamandis/
│   │   └── Big-Ideas-2026.md
│   └── Y-Combinator/
│       └── OpenClaw-Creator.md
└── Inbox/
    └── (待处理的临时内容)
```

## 自动化集成

在 Gmail Processor 中自动调用：
```bash
# 处理邮件并保存到 Obsidian
cd gmail-auto-processor && node index.js --save-to-obsidian
```
