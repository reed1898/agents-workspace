# Leo

> **Author**: Leo
> **Source**: https://x.com/runes_leo/status/2028990557331112363
> **Date**: 2026-03-05 11:40
> **Replies**: 24 · **Retweets**: 217 · **Likes**: 1044 · **Views**: 66416

---

## TLDR

**TLDR** — 作者把自己在 Claude Code 里摸索出的文件分层实践，映射到论文《Everything is Context》的术语体系，本质是在解决 token 窗口下的上下文装配问题。

**Key Points**
- 作者把文件语义“翻译”为学术概念：`today.md` 对应 **Scratchpad**，`MEMORY.md` 对应 **Fact Memory**，`patterns.md` 对应 **Experiential Memory**。
- `rules/`（自动加载）与 `docs/`（按需加载）被理解为 **Context Constructor** 的选择性加载策略。
- 推文强调 **token window** 是核心约束：全量加载会导致上下文爆炸，分层后更稳定。
- 传达的方法论是 **实践先行、命名后置**：先踩坑，再用理论框架解释和沉淀经验。

**Process / Steps**
1. 按用途拆分上下文载体：临时工作区、项目事实记忆、跨项目经验。
2. 根据 **token 预算** 设计加载策略：高优先内容自动加载，其余按需注入。
3. 用论文术语回标工程实践，形成可解释、可复用的上下文管理方法。

**Fact Check**
- 论文《Everything is Context: Agentic File System Abstraction for Context Engineering》及 arXiv 编号 `2512.05470` 确实存在。结论：**verifiable**（来源：https://arxiv.org/abs/2512.05470）。
- 论文正文确实包含 **Scratchpad**、**Fact Memory**、**Experiential Memory**、**Context Constructor**、**bounded reasoning capacity** 等术语。结论：**verifiable**（来源：https://ar5iv.labs.arxiv.org/html/2512.05470v1）。
- “`rules/` 自动加载 vs `docs/` 按需加载 = Context Constructor”是作者对论文框架的解释映射，不是论文逐字定义。结论：**partially verifiable**。
- “使用 Claude Code 三个月、分两层后稳定”属于个人经历，外部无法独立核实。结论：**unverifiable**。
- “实践在前，命名在后”属于观点表达。结论：**opinion**。  
Credibility: 8/10 — 核心论文与术语可验证，关键延伸主要是个人实践与解释。

---

## Original Content

用 Claude Code 三个月，目录越建越多，rules/ docs/ memory/ skills/ 各种分层，但一直说不清自己在搭什么。

直到看到这篇论文 "Everything is Context"，把我的文件夹结构翻译成了学术语言：


http://
today.md → 论文叫 Scratchpad（临时工作区）

http://
MEMORY.md → Fact Memory（项目级事实记忆）

http://
patterns.md → Experiential Memory（跨项目经验）
rules/ 自动加载 vs docs/ 按需加载 → Context Constructor（在 token 预算内选择性加载）

最有共鸣的是 token window 约束那段。我之前 rules/ 全量加载，context 直接爆炸。后来拆成两层才稳住。论文管这个叫"bounded reasoning capacity"——原来我解决的是这个问题。

实践在前，命名在后。先踩坑，再读论文，发现踩的坑都有名字。

论文原文 
http://
arxiv.org/abs/2512.05470

### Referenced Links

- [https://t.co/yLgyWe7Yok](https://t.co/yLgyWe7Yok)
- [https://t.co/JGWY6bfFWC](https://t.co/JGWY6bfFWC)
- [https://t.co/rXvVbuAt4e](https://t.co/rXvVbuAt4e)
- [https://t.co/hEAdtb3tcW](https://t.co/hEAdtb3tcW)
