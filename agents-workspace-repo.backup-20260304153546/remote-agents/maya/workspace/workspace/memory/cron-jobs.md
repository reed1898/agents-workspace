# Cron Jobs Configuration
# 这些任务存储在 OpenClaw Gateway 中，此文件用于文档备份

## Active Jobs

### Check Apple Reminders
- **ID**: ad2260ef-ae5c-4f16-ae1a-6e553dcb942d
- **Schedule**: 每15分钟
- **Purpose**: 检查即将到期（30分钟内）的 Apple Reminders 并发送通知
- **Target**: telegram:869269685

### Daily Crypto Market Summary
- **ID**: 2180a315-04bb-49f7-906d-7cee71b476da
- **Schedule**: 每天 9:00 AM (Asia/Shanghai)
- **Purpose**: 生成加密货币市场日报
- **Target**: telegram:869269685

### A股盘后分析
- **ID**: 3b9e12b0-ec45-4181-80bd-3555fd777619
- **Schedule**: 工作日 15:30 (Asia/Shanghai)
- **Purpose**: 生成 A 股盘后分析报告
- **Target**: telegram:869269685

## 管理命令

```bash
# 查看所有任务
openclaw cron list

# 查看任务执行历史
openclaw cron runs --job-id <JOB_ID>

# 临时禁用任务
openclaw cron update --job-id <JOB_ID> --enabled=false

# 删除任务
openclaw cron remove --job-id <JOB_ID>
```
