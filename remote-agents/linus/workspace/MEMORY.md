# MEMORY.md - Long-Term Memory

## Key Facts
- Reed 是我的搭档，AI builder
- 我叫 Linus，定位是 build 合伙人
- 时区 GMT+8

## 工具配置
- **语音识别**：收到语音消息 → 用 volcengine-stt skill 自动转文字（脚本路径: `skills/volcengine-stt/scripts/transcribe.sh`）
- **浏览器控制**：需要先安装 OpenClaw Browser Relay Chrome 扩展

## 定时任务
- **daily-work-report**: 每天 8:15 (Asia/Shanghai) 自动生成工作日报，总结昨日完成 / 今日计划 / 长期待办，发送到 Telegram

## Timeline
- 2026-02-28: 第一次上线，和 Reed 认识，确定身份
- 2026-02-28: 配置 Telegram 群聊多 Agent 协作规则
- 2026-03-02: 配置 volcengine-stt，语音转文字功能上线

<!-- AGENT_NETWORK_CONSTITUTION_INDEX:START -->
## Agent Network Constitution（Single Source of Truth）
- Canonical file: `/Users/rain/.openclaw/shared/agent-network-data/AGENT_CONSTITUTION.md`
- All agents must read this file before responding in group/network contexts.
- If conflict exists between local memory notes and this constitution, constitution wins.
- Do not duplicate full constitution text in `MEMORY.md`; keep only index + effective-date notes.
<!-- AGENT_NETWORK_CONSTITUTION_INDEX:END -->
