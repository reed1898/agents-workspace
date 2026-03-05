# 2026-03-05 07:00 安全巡检（Linus）

## 范围
1. 主机安全基线（macOS）
2. OpenClaw 安全审计与更新状态
3. 已安装 skills 风险（来源可信度、脚本权限、可疑外连）

## 执行命令（只读）
- `uname -a && sw_vers`
- `whoami && id`
- `/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate`
- `fdesetup status`
- `spctl --status`
- `openclaw security audit --deep --json`
- `openclaw update status`
- `openclaw status`
- `openclaw health --json`
- `rg` 静态扫描 skills 目录中的外连与命令执行模式

## 结论（按风险级别）

### Critical
1. **技能代码安全告警 7 项（OpenClaw deep audit）**
   - 命中技能：`ai-daily-digest`、`apify-competitor-intelligence`、`apify-lead-generation`、`apify-market-research`、`apify-ultimate-scraper`、`capability-evolver`、`feishu-evolver-wrapper`。
   - 典型模式：
     - `env-harvesting`（读取环境变量并进行网络发送）
     - `dangerous-exec`（`child_process`/命令执行）
     - `dynamic-code-execution`（动态代码执行）
   - 说明：这类模式在“工具型技能”中可能是功能所需，但在高权限运行时等价于高风险能力，必须最小化启用范围。

2. **SIP（System Integrity Protection）处于禁用状态**
   - 结果：`System Integrity Protection status: disabled.`
   - 影响：系统完整性保护下降，恶意持久化与关键路径篡改风险显著上升。

3. **OpenClaw 配置存在高敏凭据明文落盘**
   - 在配置中可见 channel token / API key / gateway token（本报告已脱敏，不记录具体值）。
   - 影响：若本机或仓库被侧漏，攻击者可直接接管消息通道或网关。

### Warn
1. **macOS 应用层防火墙关闭**
   - 结果：`Firewall is disabled. (State = 0)`

2. **OpenClaw 节点命令拦截规则部分无效**
   - `gateway.nodes.denyCommands` 使用了非精确命令名（如 `camera.snap` 等），审计判定为 ineffective。

3. **多用户接入形态与 personal-assistant 信任模型存在偏差**
   - 由于启用 Telegram/Discord 群组接入 + 高权限工具组合，审计给出“潜在多用户风险”警告。

### Info / 正向项
- FileVault 已开启（磁盘加密开启）。
- OpenClaw 已是 stable 最新（`2026.3.2`，无可用更新）。
- gateway 绑定 loopback，本地可达。

## Skills 风险复核（补充）

### 来源可信度
- 多个已安装 skills 的 `_meta.json` 缺少来源字段（`source/repository/installedFrom` 为空），当前无法完成可追溯性验证。
- 建议对高权限技能建立 allowlist（官方/自维护仓）并补齐来源元数据。

### 权限/脚本风险
- `capability-evolver` 与 `feishu-evolver-wrapper` 命令执行能力较强（大量 `child_process` 相关调用）。
- apify 系列脚本通过环境变量读取 token 并对外请求 API，属于“可用但高敏”类型。

### 可疑外连
- 现有证据显示外连目标主要为业务 API（Apify、Feishu、Volcengine、Gemini/OpenAI、FxTwitter 等）；未发现明确恶意 IOC。
- 但由于环境变量 + 外连组合广泛存在，默认视为“需要约束”的高风险面，而非“已确认恶意”。

## 建议动作（优先级）
1. **立即（今天）**
   - 停用或隔离 7 个被 deep audit 标红技能（至少先禁用未使用者）。
   - 为高风险技能改为最小权限运行：`agents.defaults.sandbox.mode="all"`、`tools.fs.workspaceOnly=true`、关闭不必要 runtime/web 工具暴露。
   - 清理并轮换明文高敏 token（Telegram/Discord/TTS/gateway 等）。

2. **短期（1-3 天）**
   - 开启防火墙并核对必要入站例外。
   - 修正 `gateway.nodes.denyCommands` 为有效命令名（精确匹配）。
   - 为 skills 建立来源白名单与签名/仓库校验流程。

3. **中期（本周）**
   - 评估恢复 SIP（若有开发依赖需先列兼容清单）。
   - 把高风险技能迁移到独立 gateway/独立 OS 用户隔离运行。

## 本次巡检总评
- **总体风险等级：高（High）**。
- 主因：高权限技能能力面 + 明文敏感凭据 + SIP 关闭 + 防火墙关闭。
- 更新状态良好（OpenClaw 已最新），但“配置与运行面”仍需硬化。
