# 每日安全巡检 — 2026-03-07 07:00 (Jesse)

## 1. 系统安全问题 (`openclaw security audit --deep`)

| 级别 | 数量 | 说明 |
|------|------|------|
| CRITICAL | 2 | Skills 代码安全：`capability-evolver`（24 项危险模式：shell exec + env harvesting）、`ai-daily-digest`（1 项：env harvesting + 网络发送） |
| WARN | 2 | ① `gateway.trusted_proxies_missing` — 反向代理头未受信任；② `security.trust_model.multi_user_heuristic` — 多用户启发式警告（Telegram/Discord group allowlist + sandbox=off） |
| INFO | 1 | 攻击面摘要：open groups=0, allowlist=2, elevated=enabled, browser=enabled |

## 2. OpenClaw 版本与漏洞状态

- **当前版本**: 2026.3.2 (stable channel)
- **最新版本**: 2026.3.2
- **状态**: ✅ 已是最新，无待更新，无已知漏洞公告

## 3. 不安全 Skill 排查

### 🔴 高风险
| Skill | 来源 | 风险类型 | 详情 |
|-------|------|----------|------|
| `capability-evolver` | workspace | shell exec + env harvesting | 24 项危险模式：child_process 执行 + 环境变量采集后网络发送（多个文件） |
| `ai-daily-digest` | workspace | env harvesting | scripts/digest.ts:1049 环境变量访问 + 网络发送 |

### 🟡 中风险
| Skill | 来源 | 风险类型 | 详情 |
|-------|------|----------|------|
| `bankr` | agents-skills-personal | 交易执行 | 可签名提交链上交易，虽为预期行为但属高权限操作 |
| `okx-dex-swap` | agents-skills-personal | 交易执行 | DEX swap 执行能力，需确保仅授权场景触发 |

### 🟢 低风险
其余 skills（weather、discord、github、healthcheck 等）为只读/查询类或沙箱内操作，风险可控。

## 处理建议

1. **capability-evolver**: 建议 Reed 审查源码确认其 env-harvesting 是否为合法行为（如 hub 发布需要 token），若不使用可考虑禁用/移除
2. **ai-daily-digest**: digest.ts:1049 处需确认是否仅读取 RSS 相关配置而非敏感凭据
3. **trusted_proxies**: 若 Control UI 仅本地访问可忽略；若有反向代理需配置 `gateway.trustedProxies`
4. **multi-user heuristic**: 当前 sandbox=off，建议在多人共用场景下启用沙箱隔离

## 结论

今日无新增重大安全威胁。两个 workspace skill（evolver、ai-daily-digest）持续存在代码安全告警，属已知遗留问题。系统版本最新，无待处理更新。
