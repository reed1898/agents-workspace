---
name: mission-control-push
description: Push activities to Mission Control dashboard when tasks are completed
allowed-tools: Bash(curl:*) Read Write
---

# Mission Control Push

Automatically push activities to your Mission Control dashboard when tasks complete.

## Setup

1. **Deploy Convex HTTP endpoint:**
   ```bash
   cd /Users/rain/.openclaw/workspace/mission-control
   npx convex dev
   # 按 Ctrl+C 退出（代码已部署）
   ```

2. **Verify endpoint is accessible:**
   ```bash
   curl -X POST "$MISSION_CONTROL_URL" \
     -H "Content-Type: application/json" \
     -d '{"type":"system","title":"测试","description":"连接测试"}'
   ```

## Environment Variables

```bash
MISSION_CONTROL_URL=https://graceful-kudu-361.convex.site/api/push-activity
```

## Usage

### Push a Task Completed Activity

```bash
curl -X POST "$MISSION_CONTROL_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "task_completed",
    "title": "完成 A股盘后分析",
    "description": "获取大盘数据并生成分析报告",
    "metadata": {
      "source": "openclaw",
      "sessionId": "agent:main:main"
    }
  }'
```

### Available Activity Types

| Type | When to Use |
|------|-------------|
| `task_completed` | 任务完成时 |
| `task_created` | 创建新任务时 |
| `document_created` | 创建文档/笔记时 |
| `document_updated` | 更新文档时 |
| `memory_added` | 添加记忆时 |
| `search_performed` | 执行搜索时 |
| `system` | 系统事件 |

## Integration Pattern

Add to any skill script after task completion:

```bash
#!/bin/bash
# Your task script here...

# Push to Mission Control
curl -s -X POST "$MISSION_CONTROL_URL" \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
    --arg title '任务标题' \
    --arg desc '任务描述' \
    '{type: "task_completed", title: $title, description: $desc, metadata: {source: "openclaw"}}')"
```

## Testing

```bash
export MISSION_CONTROL_URL=https://graceful-kudu-361.convex.site/api/push-activity

# Test push
curl -X POST "$MISSION_CONTROL_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "system",
    "title": "Mission Control 连接测试",
    "description": "OpenClaw 成功连接到 Mission Control"
  }'
```
