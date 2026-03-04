# openclaw-paid-idea-skill (MVP)

一个面向 OpenClaw Builder 的最小可运行项目：
每天抓取 Hacker News 热门话题，计算“可收费产品匹配度”，输出当天可执行的开发方向报告。

## 场景
- 用于每日 3AM 自动化研发任务前置选题
- 目标是选出一个 **当天能交付的收费功能切片**

## 快速开始

```bash
cd /home/ubuntu/.openclaw/projects/openclaw-paid-idea-skill
python3 src/idea_report.py --top 5
```

如果网络受限，脚本会自动降级到本地样例；也可强制离线：

```bash
python3 src/idea_report.py --top 5 --offline
```

JSON 输出：

```bash
python3 src/idea_report.py --top 3 --json
```

## 输出说明
- `hn_score`: Hacker News 热度
- `monetization_score`: 关键词变现匹配分
- `total_score`: 综合优先级（用于选当日MVP）
- `builder_angle`: 建议的收费切入方式

## 下一步（计划）
1. 增加历史去重（避免连续几天重复主题）
2. 增加本地“已做MVP”记录，优先推荐未覆盖赛道
3. 生成可直接粘贴到 cron delivery 的日报模板
