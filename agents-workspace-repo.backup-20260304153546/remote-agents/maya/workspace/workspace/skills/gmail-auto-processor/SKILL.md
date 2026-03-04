---
name: gmail-auto-processor
description: |
  自动处理 Gmail 邮件：归档促销邮件、提醒重要通知、总结 Newsletter 内容。
  支持定时执行和手动触发，通过 Telegram 发送汇总报告。
metadata:
  version: "1.0.0"
  author: RainAssistant
  requires:
    - mcporter
    - google-workspace-mcp
---

# Gmail Auto Processor

自动分类、归档、总结 Gmail 邮件，减少信息噪音，突出重要内容。

## 功能

- **自动归档**: 促销邮件自动移出 Inbox
- **重要提醒**: 交易所/安全相关邮件 Telegram 通知
- **Newsletter 总结**: 自动提取核心内容，发送摘要
- **每日报告**: 处理结果汇总到 Telegram

## 安装

```bash
# 安装依赖
cd ~/.openclaw/workspace/skills/gmail-auto-processor
npm install

# 配置（首次运行会提示）
node index.js --config
```

## 使用方法

### 方式一：智能运行（推荐）
自动检测任务耗时，智能选择执行模式：
```bash
# 智能模式（自动判断使用 subagent 或直接执行）
npm run smart

# 智能预览模式
npm run smart-dry
```

### 方式二：Subagent 执行（不阻塞主会话）
```bash
# 后台异步处理，完成后 Telegram 通知
npm run subagent

# 预览模式（不修改邮件）
npm run subagent-dry
```

### 方式三：手动执行（适合少量邮件）
```bash
node index.js

# 预览模式
node index.js --dry-run
```

### 方式四：设置定时任务（cron）
```bash
# 每天下午 2 点执行（使用智能模式）
0 14 * * * cd ~/.openclaw/workspace/skills/gmail-auto-processor && node smart-run.js
```

## 配置文件

`config.json`:
```json
{
  "auto_archive": {
    "categories": ["promotions"],
    "keywords": ["促销", "优惠", "限时", "团购", "折扣"],
    "senders": ["newsletter@", "no-reply@", "marketing@"]
  },
  "important_alerts": {
    "senders": [
      "mexc.com",
      "binance.com", 
      "okx.com",
      "matrixport.com"
    ],
    "keywords": ["下架", "冻结", "安全", "密码", "验证", "提币", "登录"],
    "notify_via": "telegram"
  },
  "newsletter": {
    "senders": [
      "substack.com",
      "ycombinator.com",
      "seekingalpha.com",
      "diamandis.com"
    ],
    "action": "summarize",
    "max_summary_length": 500
  },
  "telegram": {
    "enabled": true,
    "summary_enabled": true
  }
}
```

## 处理流程

1. 搜索未读邮件
2. 分类邮件（重要/Newsletter/促销）
3. 执行相应动作
4. 生成汇总报告
5. 发送 Telegram 通知

## 报告示例

```
📧 Gmail 处理报告 (2026-02-09 14:00)

📊 统计:
• 已处理: 45 封
• 归档: 38 封 (促销)
• 重要: 2 封
• Newsletter: 5 封

🔴 重要提醒:
• MEXC: 代币下架通知
• Matrixport: VIP 客服联系

📰 Newsletter 摘要:
• Peter Diamandis: Big Ideas 2026 - AI、比特币、核能、机器人...
• Y Combinator: OpenClaw Creator 为什么 80% 的应用会消失...
```

## 依赖

- Node.js >= 18
- mcporter CLI (已配置 google-workspace server)
- Telegram Bot (用于发送通知)

## License

MIT
