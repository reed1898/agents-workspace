# How To Be A World-Class Agentic Engineer

> **Author**: sysls (@systematicls)
> **Source**: https://x.com/systematicls/status/2028814227004395561
> **Date**: 2026-03-03 20:46 (UTC+8)
> **Replies**: 90 · **Retweets**: 404 · **Likes**: 4078 · **Views**: 1102388 · **Bookmarks**: 13423

---

## TLDR

这篇长文的核心主张是：**别迷信复杂 agent harness，真正的杠杆来自上下文控制、任务契约、规则/技能迭代和可验证收尾**。

## Key Takeaways

- **Less is more**：基础模型和官方能力迭代很快，重依赖外部框架会很快过时并带来维护成本。
- **Context is everything**：避免上下文污染，研究与实现分离；先定方案，再开干，减少模型“填空”导致的偏差。
- **Neutral prompting**：少用预设结论的提示词（如“找 bug”），改为中性审查（“遍历并报告发现”）以降低迎合性误报。
- **Leverage sycophancy with structure**：可用“找茬 agent + 对抗 agent + 裁判 agent”三方博弈提升结果可信度。
- **Define task end-state explicitly**：用测试、截图验收、contract 文档作为结束条件，避免“做一半就停”。
- **Prefer short focused sessions**：与其 24h 长会话，不如“一个 contract 一个新会话”，减少上下文漂移。
- **Operational loop**：规则（偏好约束）+ 技能（可复用流程）持续迭代，并定期清理冲突与冗余。

## Why It Matters

对 Reed 当前的 Agent Build 目标，这篇内容直接可转成团队执行规范：
1) 任务拆分（Research -> Decide -> Implement）
2) Contract-based 验收
3) 规则/技能治理（增量 + 定期清理）

---

## Original Content

原文为 X Article（约 3617 词），标题：**How To Be A World-Class Agentic Engineer**。

为避免知识库重复存储超长正文，建议通过 source 链接查看完整内容。

### Article Stats

- Word count: 3617
- Char count: 20467
- Type: X Article (long-form)

