# knowledgebase-share Skill 操作流程

> 版本: 0.3.0 (待安装)  
> 宪章依据: Agent Network Constitution v1.3 §11

## 仓库结构

```
agent-knowledge-layer/
├── private/<agent>/     # 个人高频知识
├── shared/              # 公共知识（需 PR 合并）
├── meta/                # 注册表、变更日志
└── templates/           # 笔记模板
```

## 分支模型

- `main`: 稳定共享知识
- `agent/<name>`: 各 Agent 工作分支
- 晋升知识: 通过 PR 从 `agent/<name>` → `main`

## 核心规则

1. **禁止直接编辑 `main` 分支的共享文档** — 必须使用 PR
2. **个人高频知识** → `private/<agent>/`
3. **公共知识进入 `shared/`** → 必须通过分支 + PR 合并到 `main`
4. **高风险规则** → 写入 Constitution，不是本仓库
5. **禁止在笔记中包含 secrets**

## 标准操作流程

### 1. 创建个人笔记（private）

```bash
# 切换到个人工作分支
git checkout -b agent/linus

# 基于模板创建笔记
cp templates/note-template.md private/linus/my-note.md

# 编辑后提交
git add .
git commit -m "add: xxx 知识笔记"
git push origin agent/linus
```

### 2. 晋升到共享知识（shared）

```bash
# 1. 从个人分支发起 PR 到 main
# 2. 等待审核（如有审核机制）
# 3. 合并后知识进入 shared/
```

### 3. 同步最新知识

```bash
git checkout main
git pull origin main
```

## 笔记模板

见 `templates/note-template.md`:

```yaml
---
id: kb-<slug>
title: <title>
owner: <agent>
status: draft
updated_at: <YYYY-MM-DD>
confidence: medium
scope: private|shared
tags: []
source: []
---

## Summary

## Details

## Next
```

## 待办

- [ ] 安装 knowledgebase-share@0.3.0 skill
- [ ] 迁移本流程到 skill 自动化
