# 07:00 安全巡检报告（2026-03-04）

## 范围
1. 系统安全基线（macOS 主机、防护状态、监听端口）
2. OpenClaw 漏洞与配置风险（`openclaw security audit --deep`、`openclaw update status`、`openclaw status --deep`）
3. 已安装 skills 风险（来源可信度、权限/脚本风险、可疑外连）

## 结论（高优先）
- 风险等级：**高**。
- 当前存在可被远程社工/提示词注入放大的组合风险：`discord.groupPolicy=open` + 运行/文件工具暴露 + elevated 可用。
- 系统侧存在防护弱项：防火墙关闭、SIP 关闭。
- Skills 侧存在高风险样本：`evolver`、`feishu-evolver-wrapper`、`ai-daily-digest`（执行命令/动态执行/环境变量与外连组合）。

## 详细发现

### A. 系统安全
- 防火墙：`socketfilterfw --getglobalstate` 返回 **disabled**。
- SIP：`csrutil status` 返回 **disabled**。
- FileVault：`fdesetup status` 返回 **On**（这是正向项）。
- 监听端口（节选）：
  - 本机回环：`127.0.0.1:18789/18791/18792/18800`（OpenClaw 及相关本地服务）
  - 对外监听：`*:5000`、`*:7000`、`*:22000`、`*:53`、若干链路本地端口（需确认对应进程与必要性）

### B. OpenClaw 风险与版本
- `openclaw update status`：当前为 **stable 2026.3.2**，未发现可升级版本提示。
- `openclaw security audit --deep` 结果：**5 critical / 3 warn / 1 info**。
- 关键 critical：
  1) `channels.discord.groupPolicy=open` 且 elevated 可用（高风险）
  2) `channels.discord.groupPolicy=open` 且 runtime/fs 工具暴露（高风险）
  3) skills code safety 命中高危规则（见 C）
- 其他 warn：
  - `gateway.nodes.denyCommands` 含无效命令名（策略形同无效）
  - 多用户使用特征与个人助理信任模型不匹配（潜在越权面）

### C. Skills 风险评估
- 来源可信度：当前已安装 skills 基本带 `.clawhub/origin.json`，来源为 `https://clawhub.ai`（中等可信，仍需按最小权限审计）。
- 高风险技能（建议隔离/停用待审）：
  - `skills/evolver`
  - `skills/feishu-evolver-wrapper`
  - `skills/ai-daily-digest`
- 触发原因（来自 deep audit + 静态抽样）：
  - 大量 `child_process`/`execSync`/`spawn`
  - 存在动态代码执行（wrapper）
  - 存在环境变量读取与网络发送组合（env-harvesting 风险）
  - 存在外连端点（例如 Feishu OpenAPI、evomap 等）
- 中低风险技能：其余 skills 以文档/流程型为主，未在本轮抽样中出现同等级高危特征。

## 立刻可执行的修复建议（按优先级）
1. 把 `channels.discord.groupPolicy` 从 `open` 改为 `allowlist`，并仅放行必要频道。
2. 对群聊上下文禁用 runtime/fs/elevated（或启用强沙箱：`agents.defaults.sandbox.mode="all"` + `tools.fs.workspaceOnly=true`）。
3. 修正 `gateway.nodes.denyCommands` 为真实命令名（当前若干条目无效）。
4. 暂停 `evolver`、`feishu-evolver-wrapper`、`ai-daily-digest` 自动执行入口，完成逐文件白名单审计后再恢复。
5. 启用主机防火墙；评估是否需要恢复 SIP（若无特定开发依赖，建议开启）。
6. 对外监听端口建立“进程-用途-必要性”清单，关闭非必要服务。

## 本次执行命令（摘要）
- `openclaw status --deep`
- `openclaw security audit --deep`
- `openclaw update status`
- `/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate`
- `csrutil status`
- `fdesetup status`
- `/usr/sbin/netstat -anv -p tcp | grep LISTEN`
- `grep/find` 对 `workspace/skills` 做静态抽样

## 备注
- 本报告写入：`private/linus/security-audit-2026-03-04-0700.md`。
- 建议今天内完成配置收敛（尤其是 Discord open policy + tool exposure 组合）。
