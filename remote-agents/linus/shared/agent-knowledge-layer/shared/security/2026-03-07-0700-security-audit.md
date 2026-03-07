# 2026-03-07 07:06 安全巡检（Linus）

## 执行范围
1. 主机系统安全状态检查
2. OpenClaw 安全审计与更新状态（`openclaw security audit --deep`、`openclaw update status`）
3. 已安装 skills 风险检查（来源可信度、权限/脚本风险、可疑外连）

## 结论（TL;DR）
- **高风险（需处理）**：OpenClaw deep audit 报告 **7 critical / 3 warn / 1 info**，critical 全部来自本地已安装第三方 skill 代码模式。
- **系统侧风险**：macOS 应用层防火墙当前关闭；存在多个 `*:` 对外监听端口（5000/7000/22000）。
- **版本状态**：OpenClaw stable 已是最新（npm latest `2026.3.2`），当前无升级阻塞。

## 关键发现

### A. 系统安全
- OS: macOS 15.7.4 (Darwin 24.6.0)
- FileVault: **On**（磁盘加密已开启）
- Auto Update Check: **On**（自动检查更新已开启）
- Time Machine: **No destinations configured**（未配置备份目的地）
- 应用层防火墙：`socketfilterfw` 显示 **disabled**
- 监听端口（节选）：
  - `*:5000`, `*:7000`（ControlCe）
  - `*:22000`（syncthing）
  - OpenClaw 网关仍为 loopback（`127.0.0.1:18789`）

### B. OpenClaw 安全审计
- `openclaw security audit --deep`：**7 critical / 3 warn / 1 info**
- Critical（7 项）均为 skill code safety：
  1) `ai-daily-digest`（env-harvesting，`scripts/digest.ts:1049`）
  2) `apify-competitor-intelligence`（env-harvesting，`reference/scripts/run_actor.js:323`）
  3) `apify-lead-generation`（env-harvesting，`reference/scripts/run_actor.js:323`）
  4) `apify-market-research`（env-harvesting，`reference/scripts/run_actor.js:323`）
  5) `apify-ultimate-scraper`（env-harvesting，`reference/scripts/run_actor.js:323`）
  6) `capability-evolver`（多处 dangerous-exec + env-harvesting，共 26 处）
  7) `feishu-evolver-wrapper`（dangerous-exec/dynamic-code/env-harvesting，共 12 处）
- Warnings（重点）：
  - `gateway.trusted_proxies_missing`：reverse proxy trustedProxies 未设置
  - `gateway.nodes.deny_commands_ineffective`：`denyCommands` 使用了无效命令名（精确匹配失败）
  - `security.trust_model.multi_user_heuristic`：在潜在多用户可达场景下，默认运行能力偏强

### C. OpenClaw 更新状态
- `openclaw update status`：
  - Install: `pnpm`
  - Channel: `stable`
  - Update: `npm latest 2026.3.2`（已最新）

### D. Skills 来源可信度与外连风险
- 可确认来自 skill registry 且有 `_meta.json` 的示例：
  - `ai-daily-digest`（ownerId 存在）
  - `evolver`（ownerId 存在）
  - `feishu-evolver-wrapper`（ownerId 存在）
- 多个 apify 系列目录缺少 `_meta.json`，来源链路可追溯性较弱（建议补充来源记录/commit pin）
- 高风险模式主要集中在：
  - 读取环境变量并向外部网络请求发送（env-harvesting 告警）
  - `child_process` 执行 shell（dangerous-exec）
  - 动态代码执行（dynamic-code-execution）

## 优先级处置建议
1. **先隔离再使用**：对 7 个被标红 skills 采用默认禁用策略，仅在明确任务中临时启用。
2. **修复节点命令拦截**：把 `gateway.nodes.denyCommands` 改为 OpenClaw 可识别的精确命令名。
3. **收敛多用户面暴露**：若继续在群场景使用，收紧默认 sandbox 和 runtime/file tool 权限。
4. **启用主机防火墙并白名单化**：至少限制非必要 `*:` 端口入站。
5. **建立可恢复能力**：补齐 Time Machine（或等效）定期备份目的地。
6. **技能供应链治理**：为缺少 `_meta.json` 的技能建立来源台账（来源仓库、版本、hash、审计结论）。

## 审计命令（执行记录）
- `openclaw security audit --deep`
- `openclaw update status`
- `openclaw status --deep`（本次执行超时，未纳入结论）
- `uname -a && sw_vers`
- `/usr/sbin/lsof -nP -iTCP -sTCP:LISTEN`
- `/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate`
- `fdesetup status`
- `/usr/sbin/softwareupdate --schedule`
- `tmutil destinationinfo`

## 风险等级评估（本次）
- **总体：高**（主要由第三方 skills 的代码安全告警与主机侧防火墙关闭共同导致）
