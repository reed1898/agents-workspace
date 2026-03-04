# 安全巡检报告 - 测试执行

**巡检时间**: 2026-03-03 16:05 UTC  
**执行主机**: ip-172-31-21-161 (AWS EC2)  
**巡检类型**: 测试执行（非生产定时任务）  
**执行者**: Maya

---

## 1. 系统安全状态

### 1.1 操作系统信息
- **OS**: Ubuntu 24.04.3 LTS (Noble Numbat)
- **内核**: Linux 6.14.0-1018-aws
- **架构**: x86_64

### 1.2 网络暴露面
| 端口 | 服务 | 监听地址 | 风险等级 |
|------|------|----------|----------|
| 22 | SSH | 0.0.0.0:22 | 🔴 高 |
| 8080 | uvicorn | 0.0.0.0:8080 | 🟡 中 |
| 8000 | uvicorn | 0.0.0.0:8000 | 🟡 中 |
| 22000 | Syncthing | 0.0.0.0:22000 | 🟡 中 |
| 8384 | Syncthing | 127.0.0.1:8384 | 🟢 低 |
| 18789/18791/18792 | OpenClaw Gateway | 127.0.0.1 | 🟢 低 |

### 1.3 防火墙状态
- **UFW 状态**: ❌ **inactive（未启用）**
- **风险**: 主机防火墙未启用，依赖安全组/网络层防护

### 1.4 SSH 安全（需进一步检查）
- SSH 监听在 0.0.0.0:22，暴露于公网
- 建议检查：是否禁用密码登录、是否使用密钥认证、root 登录是否禁用

---

## 2. OpenClaw 安全状态

### 2.1 版本状态
| 项目 | 状态 |
|------|------|
| 安装方式 | pnpm |
| 更新通道 | stable (default) |
| 最新版本 | 2026.3.2 ✅ 已是最新 |

### 2.2 安全审计结果
**摘要**: 6 critical · 2 warn · 1 info

#### 🔴 Critical Issues（6项）

| Skill | 问题类型 | 详情 |
|-------|----------|------|
| clawra-selfie | env-harvesting | 环境变量访问 + 网络发送，可能泄露凭证 (scripts/clawra-selfie.ts:99) |
| ai-daily-digest | env-harvesting | 同上 (scripts/digest.ts:1049) |
| gmail-auto-processor | dangerous-exec | 10处 shell 命令执行 (child_process) |
| imap-smtp-email | env-harvesting | 环境变量访问 + 网络发送 (scripts/imap.js:23) |
| vercel-cli | dangerous-exec | shell 命令执行 (vercel-skill.js:17) |
| clawra-selfie (系统级) | env-harvesting | 同上，位于 ~/.openclaw/skills/ |

#### 🟡 Warning Issues（2项）

1. **gateway.trusted_proxies_missing**
   - gateway.bind 是 loopback，但 trustedProxies 为空
   - 如果通过反向代理暴露 Control UI，需要配置信任代理

2. **security.trust_model.multi_user_heuristic**
   - 检测到潜在多用户设置信号
   - Telegram/Discord 配置了 groupPolicy="allowlist"
   - Runtime/process 工具在无沙箱环境下暴露
   - **建议**: 如果用户之间互不信任，应拆分信任边界

#### ℹ️ Info
- Attack surface: groups open=0, allowlist=2
- Elevated tools: enabled
- Browser control: enabled
- Trust model: personal assistant

---

## 3. Skill 安全审查

### 3.1 高风险 Skill（建议审查）

| Skill | 风险类型 | 建议操作 |
|-------|----------|----------|
| gmail-auto-processor | 大量 shell 执行 | 🔴 审查代码，确认必要性 |
| clawra-selfie | 凭证收割模式 | 🔴 审查 env 访问逻辑 |
| ai-daily-digest | 凭证收割模式 | 🔴 审查 env 访问逻辑 |
| imap-smtp-email | 凭证收割模式 | 🔴 审查 env 访问逻辑 |
| vercel-cli | shell 执行 | 🟡 审查命令注入风险 |

### 3.2 已安装 Skill 总数
- 工作区 skills 目录: 45+ 个 skill
- 包含系统级 skills (~/.openclaw/skills/)

---

## 4. 定时任务审计

### 4.1 当前 Cron Jobs（6个）

| ID | 名称 | 调度 | 下次运行 | 状态 |
|----|------|------|----------|------|
| 23ce3f73 | Daily ClawHub Skill Sync | 08:00 | 7h后 | ✅ ok |
| 304fe3ba | Reed Agent OS Morning | 08:30 | 8h后 | ✅ ok |
| 8ca8c4dc | Daily AI Daily Digest | 11:00 | 10h后 | ✅ ok |
| e235b921 | Daily OpenClaw Community | 12:00 | 11h后 | ✅ ok |
| 00286c7f | Maya 日报 | 21:15 | 21h后 | ✅ ok |
| 1f815762 | Reed Agent OS Evening | 21:30 | 21h后 | ✅ ok |

### 4.2 建议新增
- **安全巡检**: 每日 07:00（待审批）

---

## 5. 风险汇总与建议

### 🔴 高优先级（立即处理）

1. **启用 UFW 防火墙**
   ```bash
   sudo ufw default deny incoming
   sudo ufw allow 22/tcp    # SSH
   sudo ufw allow 8080/tcp  # 如有必要
   sudo ufw enable
   ```

2. **审查高风险 Skill**
   - 特别是 gmail-auto-processor 的 10 处 shell 执行
   - 检查 clawra-selfie、ai-daily-digest 的 env 访问是否必要

3. **SSH 加固**
   - 检查 /etc/ssh/sshd_config:
     - `PasswordAuthentication no`
     - `PermitRootLogin no`
     - `PubkeyAuthentication yes`

### 🟡 中优先级（本周处理）

4. **配置 trustedProxies**
   - 如果使用反向代理，配置 gateway.trustedProxies

5. **评估多用户风险**
   - 确认当前信任模型是否符合预期
   - 考虑启用 sandbox 模式

### 🟢 低优先级（持续监控）

6. **定期安全审计**
   - 建议每日自动执行 `openclaw security audit --deep`
   - 监控 skill 代码变更

---

## 6. 报告元数据

- **巡检耗时**: ~2分钟
- **数据来源**: openclaw security audit, system commands
- **报告生成**: 2026-03-03 16:08 UTC
- **下次建议巡检**: 2026-03-04 07:00 UTC

---

*本报告由 OpenClaw 安全巡检系统自动生成*
