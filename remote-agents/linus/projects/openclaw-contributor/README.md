# OpenClaw Contributor Project

## 目标
用 AI Agent 军团给 OpenClaw 开源项目持续做贡献，进入贡献者榜单。

## 架构
```
Reed（方向 + 质量把关）
  │
  ├── Linus（调度中枢 + 技术判断）
  │     ├── Coder Agent — 读源码、写补丁、跑测试
  │     └── Scout Agent — 扫 issue、分析社区动态、找机会
  │
  └── 未来扩展：Doc Agent / Review Agent
```

## Issue 来源
1. **Scout 扫描** — 定期从 GitHub issue 列表中筛选适合的目标
2. **Reed 提报** — Reed 日常使用中遇到的真实痛点和 bug
3. **社区发现** — Discord / Discussion 里的高频问题

## 路线图

### Phase 1：跑通单链路（本周）
- [ ] 扫 OpenClaw GitHub issue，筛出 3-5 个目标
- [ ] Reed 挑选一个切入点
- [ ] Spawn coding agent 读源码 + 写修复
- [ ] Review + 提交第一个 PR

### Phase 2：固化流程
- [ ] 模板化 Scout + Coder 流程
- [ ] 定期"机会报告"推送
- [ ] PR 质量检查清单

### Phase 3：扩大规模
- [ ] 加 Doc Agent（文档改进）
- [ ] 多 Coder 并行
- [ ] 每日汇总报告 + 审批流

## PR 记录
| # | 日期 | Issue | 类型 | 状态 | 链接 |
|---|------|-------|------|------|------|
| 1 | 2026-03-04 | Discord proxy 不生效 | feat | 已提交 PR | https://github.com/reed1898/openclaw/pull/new/fix/discord-carbon-proxy-support |

## 工作模式
- **自动循环**：扫 issue → 选目标 → spawn agent 写代码 → Linus review → push + 提 PR → 通知 Reed → 开始下一个
- **Linus 自主决策**：选 issue、写代码、提 PR 全部自主完成，不需要 Reed 确认
- **每完成一个 PR**：给 Reed 发简短通知（做了什么、PR 链接），写入项目知识库
- **每日工作记录**：写入 memory/YYYY-MM-DD.md
- **自动刹车**：
  - 一天最多 2-3 个 PR
  - 大改动或拿不准的先问 Reed
  - 有 PR 被拒或要求修改时，先处理反馈再开新的
- **全英文**：commit message、PR title、PR body 一律英文

## Issue 策略（价值优先，启动必读）
- **只做高 ROI**：优先核心能力、稳定性、安全、开发者体验的 P0/P1 问题。
- **明确过滤**：跳过纯文案、低影响边角、讨论型 issue；优先可复现、可验证、可快速合并。
- **执行节奏**：每轮先选 1-2 个最高价值目标，先交付最小可合并修复（small PR），再做增强。
- **质量门槛**：每个 PR 必带复现步骤、验证结果、风险说明；并发/全局副作用问题按最高优先级处理。
- **启动规则**：每次进入 `openclaw-contributor` 工作前，先按本节策略完成 issue 筛选，再进入编码与提交流程。

## 教训 & 原则
- **质量 > 速度**：天润翻车的教训，永远不给 Agent "越快越好"的指令
- **人类把关**：每个 PR 必须经过 Reed 最终确认再提交
- **风险可控**：先从小修复、文档改进入手，逐步提升难度
- **尊重社区**：不刷 PR、不骚扰维护者、不提低质量贡献
- **全英文**：commit message、PR title、PR body 一律英文
- **自动提交**：代码完成后直接 push + 创建 PR，不需要 Reed 手动操作
