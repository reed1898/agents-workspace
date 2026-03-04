# OpenClaw Security Report (Evening)

- Date: 2026-03-03 21:20 (Asia/Shanghai)
- Scope: host `Rain2025`, OpenClaw main workspace
- Operator: 小洪

## 1) `openclaw status` 健康检查

- Overall: Gateway 可达，LaunchAgent running，核心服务正常
- Dashboard: `http://127.0.0.1:18789/`
- Gateway: `ws://127.0.0.1:18789` (loopback)
- Security audit summary: `0 critical / 2 warn / 1 info`
- Update: 有新版本可升级（npm `2026.3.2`）

## 2) Gateway 配置安全性

检查项：
- `gateway.bind = loopback`（通过）
- `gateway.port = 18789`（本地端口，正常）
- `gateway.auth.token` 通过 CLI 为 redacted 输出（未直接暴露到命令输出）

结论：Gateway 当前未对公网监听，基础暴露面较低。

## 3) `~/.openclaw/openclaw.json` 敏感信息风险

检查方式：
- 权限检查：`-rw-------` (`600`)（通过）
- 结构审计：发现多处敏感字段为明文存储（文件内，非环境变量引用）

发现的敏感字段类型：
- Telegram bot token
- Discord token
- `talk.apiKey`
- `gateway.auth.token`
- `VOLC_ACCESS_TOKEN`

风险评估：
- 在当前 `600` 权限下，风险可控；但若主机被本地提权/误备份泄漏，存在凭据暴露风险。

## 4) skills 目录异常文件/权限

检查项：
- world-writable/suid/sgid 文件：未发现
- 非当前用户拥有文件：未发现
- 明显敏感字符串（常见 key/token 模式）扫描：未发现命中
- `openclaw security audit --deep` 标记：`reddit-research` 存在 1 条可疑模式（文件读取+网络发送）

说明：
- 该标记位于 `skills/reddit-search-but-free/scripts/reddit.ts`，属于能力逻辑可能触发的启发式告警，暂未发现明确恶意行为。

## 5) cron 任务异常新增检查

当前任务共 5 个：
- security-scan-evening
- security-scan-morning
- daily-report
- daily-agent-summary
- agent-network-sync

结果：
- 未发现明显异常命名/可疑外连脚本注入
- 需要关注：`security-scan-morning` 上一次状态为 `error`（"Message failed"），属于可靠性问题，不是安全入侵迹象

## 6) 按严重级别问题列表 + 自动修复

### 高风险
- 无

### 中风险
1. 多用户暴露面启发式告警（trust model）
   - 现状：runtime/process + fs 工具在默认上下文可用，且存在多渠道接入特征
   - 建议：若未来多人/不可信用户接入，拆分网关或强制 sandbox `all`，并最小化工具权限

2. 凭据明文存储于 `openclaw.json`
   - 现状：权限为 `600`，但凭据不走环境变量
   - 建议：迁移到环境变量或外部 secret store

### 低风险
1. skills 权限基线加固
   - 处理：已执行 `chmod -R go-w skills`
   - 结果：完成（防止组/其他用户误写）

2. `reddit-research` 可疑模式告警
   - 处理：已人工复核告警文件关键入口，暂未发现明显恶意行为
   - 结果：暂列观察项

## 7) 结论

- 本轮未发现高风险入侵迹象。
- 当前安全状态：可用，存在中风险配置改进空间。
- 结论语：安全检查通过（含改进建议）。
