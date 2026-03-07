# OpenClaw 安全扫描报告（晚间）

- 时间: 2026-03-07 21:20 (Asia/Shanghai)
- 执行者: 小洪
- 范围: Gateway/配置/skills/cron/本地敏感暴露面

## 执行步骤与结果

1. **整体健康检查**
   - 命令: `openclaw status`
   - 结果: Gateway 正常运行，`127.0.0.1:18789`（loopback），token 鉴权启用。
   - `openclaw status`内置审计提示: `0 critical / 1 warn / 1 info`（多用户信任边界风险提示）。

2. **Gateway 配置安全检查**
   - 命令: `openclaw gateway status`
   - 结果: `bind=loopback`、端口 `18789`、本机可达；未发现公网监听。
   - 配置位置: `~/.openclaw/openclaw.json`

3. **`~/.openclaw/openclaw.json` 敏感信息暴露风险检查**
   - 发现配置内包含多类密钥字段（如 channel token、gateway token、talk apiKey、skill env token）。
   - 当前配置与备份权限均为 `600`，文件级权限合规。
   - 风险点在于“**明文存储 + 多处备份/镜像副本存在**”，非权限泄露，但属于凭据面扩大。

4. **skills 目录异常文件/权限检查**
   - 检查目录: `~/.openclaw/skills`
   - 结果: 未发现 world-writable 文件/目录；未发现明显权限异常。
   - 补充深度审计: `openclaw security audit --deep` 对已安装技能源码做危险模式扫描，命中多项高危（见下）。

5. **cron 任务异常新增检查**
   - 命令: `openclaw cron list`
   - 对比: `~/.openclaw/cron/jobs.json` vs `~/.openclaw/cron/jobs.json.bak`
   - 结果: 任务集合一致，未发现异常新增/删除。
   - 观察到 `daily-report` 最近一次状态为 `error`（稳定性问题，不是直接安全漏洞）。

6. **深度安全审计（附加）**
   - 命令: `openclaw security audit --deep`
   - 结果: `8 critical / 2 warn / 1 info`

## 风险分级

### 高风险（HIGH）

1. **多个第三方 skills 被命中高危代码模式（8 项 critical）**
   - 位置主要在: `/Users/rain/.agents/skills/*`
   - 类型包括:
     - `dangerous-exec`（调用 `child_process`）
     - `env-harvesting`（环境变量读取与网络发送组合）
   - 影响: 若 skill 来源不可信或被投毒，存在命令执行/凭据外传风险。
   - 代表项:
     - `baoyu-danger-x-to-markdown`
     - `baoyu-post-to-wechat`
     - `baoyu-post-to-x`
     - `baoyu-image-gen`

### 中风险（MEDIUM）

1. **多用户信任边界告警（trust model）**
   - OpenClaw 审计提示: 在共享/多用户可达场景下，当前 runtime/fs 工具面较大。
   - 当前 bind 为 loopback，外部暴露较低；但若未来接入共享通道或远程入口，风险会上升。

2. **凭据明文存储并在多个副本出现**
   - `~/.openclaw/openclaw.json` 与若干 `.bak` / sync staging / workspace snapshot 中存在明文敏感字段。
   - 当前权限为 `600`，但副本越多，泄露面越大（尤其当文件被误同步、误分享、误日志化时）。

### 低风险（LOW）

1. **`daily-report` cron 最近执行错误**
   - 归类为可用性/稳定性问题，建议单独排查日志，不构成立即安全漏洞。

## 自动修复（仅低风险）

- 已尝试自动修复低风险项：
  - 本次检查中未发现可安全自动修复且不影响现有流程的低风险权限问题（关键文件权限已是 `600`，skills 目录权限正常）。
  - 因此 **未进行自动改动**。

## 建议处置（按优先级）

1. **立即（高）**
   - 对命中 `critical` 的第三方 skills 做白名单化：未审计通过前禁用/移出可执行路径。
   - 若继续使用，至少将这些 skills 运行在更严格 sandbox 下，并隔离高敏环境变量。

2. **短期（中）**
   - 收敛凭据副本：清理不必要的历史快照/备份（保留最小必要集合），并避免把含密配置写入报告/日志。
   - 对共享通道场景启用更严格策略：`sandbox.mode=all`、`fs.workspaceOnly=true`、最小化 runtime 工具。

3. **持续（低）**
   - 复盘 `daily-report` 失败日志，避免未来脚本异常导致信息漏检。

## 结论

- 本次并非“全绿”：存在 **高风险技能代码告警（CRITICAL）**，需人工确认并收敛执行权限。
- Gateway 本身监听面与权限配置较稳健（loopback + token + 600）。

## 附：本次关键命令

- `openclaw status`
- `openclaw gateway status`
- `openclaw cron list`
- `openclaw security audit --deep`
- `stat -f '%Sp %Su %Sg %N' ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak ~/.openclaw/cron/jobs.json`
- `find ~/.openclaw/skills -type f -perm -0002 -ls`
- `find ~/.openclaw/skills -type d -perm -0002 -ls`
