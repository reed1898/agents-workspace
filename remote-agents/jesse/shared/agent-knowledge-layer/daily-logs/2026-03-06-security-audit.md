# 每日安全巡检 — 2026-03-06 07:00 (Jesse)

## 1. 系统安全审计 (`openclaw security audit --deep`)

**总计：2 CRITICAL · 2 WARN · 1 INFO**

### CRITICAL
| 问题 | Skill | 详情 |
|------|-------|------|
| env-harvesting + dangerous-exec | `ai-daily-digest` | 1 critical issue — 环境变量访问+网络发送，可能凭据泄露 (scripts/digest.ts:1049) |
| env-harvesting + dangerous-exec | `capability-evolver` | 24 critical issues (62 files) — 大量 child_process 执行 + 环境变量网络外送模式 |

### WARN
| 问题 | 详情 |
|------|------|
| trusted_proxies_missing | 反向代理 header 未受信，如通过反代暴露 Control UI 需配置 trustedProxies |
| multi_user_heuristic | Telegram/Discord group allowlist 启用，sandbox=off，runtime 工具暴露无完全沙盒隔离 |

### INFO
- 攻击面总结：groups open=0, allowlist=2; elevated=enabled; webhooks=disabled; browser=enabled; trust model=personal-assistant

## 2. OpenClaw 版本状态 (`openclaw update status`)

- 当前版本：**2026.3.2**（stable channel）
- 安装方式：pnpm
- npm latest：2026.3.2
- ✅ 已是最新版本，无已知漏洞公告

## 3. Skill 安全排查

### 🔴 高风险
| Skill | 风险类型 | 建议 |
|-------|---------|------|
| `capability-evolver` | 24 个 dangerous-exec + env-harvesting，可任意执行 shell 命令并可能外送凭据 | **建议禁用或移除**，除非已完全审计源码且确认信任 |
| `ai-daily-digest` | env-harvesting（环境变量+网络发送） | 审查 digest.ts:1049 确认是否仅读取预期 key |

### 🟡 中风险
| Skill | 风险类型 | 建议 |
|-------|---------|------|
| `bankr` | 链上交易签名能力，可转移资产 | 确保仅在用户明确指令下触发交易 |
| `okx-dex-swap` | DEX 交易执行能力 | 同上 |
| `spot` (Binance) | 交易所 API 交易能力 | 确保 API key 权限最小化（只读+交易，禁提币） |

### 🟢 低风险
其余 skill（weather, discord, github, query-token-*, trading-signal 等）为只读查询或受限操作，风险可控。

## 结论

今日巡检发现 **2 个高风险 skill**（capability-evolver、ai-daily-digest）存在凭据泄露和任意命令执行风险。OpenClaw 版本已为最新。系统级 WARN 为反代配置和多用户隔离提醒，当前 personal-assistant 模式下风险可接受。

**建议下一步：** 审查 capability-evolver 是否仍需启用，若非必要建议移除；审查 ai-daily-digest digest.ts:1049 的 env-harvesting 代码路径。
