# OpenClaw Bootstrap Hook 系统完全解析

> **Author**: huangserva (@servasyy_ai)
> **Source**: https://x.com/servasyy_ai/status/2029186874074644619
> **Date**: 2026-03-04 21:27 (UTC+8)
> **Replies**: 5 · **Retweets**: 3 · **Likes**: 15 · **Views**: 2395

---

## TLDR

这篇文章把 OpenClaw 中“Bootstrap 文件如何最终进入 LLM prompt”的路径拆清楚了：

- `agent:bootstrap`：文件级增删改/重排（最强控制）
- `bootstrap-extra-files`：仅追加额外文件（低侵入）
- `before_prompt_build`：最终 prompt 发送前动态改写
- `bootstrapMaxChars / bootstrapTotalMaxChars`：字符预算与截断策略

## Why It Matters

对日常使用最有价值的是：
1) 先选对改动层级（文件层、prompt 层、预算层）
2) 避免把所有需求都塞到一个 hook 里
3) 明确“可信代码”和“插件配置”的边界

---

## Original Content

原文为 X Article，标题：**OpenClaw Bootstrap Hook 系统完全解析**。
正文约 387 词，核心是机制梳理与作者反思（“技术问题必须查代码，不能靠猜”）。

