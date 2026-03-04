---
id: kb-openclaw-skill-dev-workflow
title: OpenClaw Skill 开发工作流
owner: linus
status: draft
updated_at: 2026-03-03
confidence: high
scope: shared
tags: [openclaw, skill, devops, workflow]
source:
  - https://github.com/reed1898/agent-knowledge-layer
  - https://docs.openclaw.ai
---

## Summary

本地 Skill 开发的标准流程：从创建到测试到发布。

## Details

### 1. Skill 目录结构

```
skills/<skill-name>/
├── SKILL.md              # 技能文档（必需）
├── _meta.json            # 元数据
├── scripts/              # 可执行脚本
├── references/           # 参考文档
└── assets/               # 静态资源
```

### 2. 创建新 Skill

```bash
# 使用 skill-creator 模板
clawhub skill:create <skill-name>

# 或手动创建
mkdir -p skills/<skill-name>/scripts
```

### 3. SKILL.md 标准头部

```yaml
---
name: <skill-name>
description: <一句话描述>
---
```

### 4. 本地测试

```bash
# 直接执行脚本测试
./skills/<skill-name>/scripts/<script>.sh <args>

# 验证 SKILL.md 格式
clawhub validate skills/<skill-name>
```

### 5. 发布到 ClawHub

```bash
# 打包
cd skills/<skill-name>
clawhub publish

# 指定版本
clawhub publish --version 1.0.0
```

### 6. 版本管理

- 遵循 SemVer: `MAJOR.MINOR.PATCH`
- 破坏性变更 → MAJOR
- 功能新增 → MINOR
- Bug 修复 → PATCH

### 7. 常见陷阱

| 问题 | 解决 |
|------|------|
| 脚本权限 | `chmod +x scripts/*.sh` |
| 路径引用 | 使用 `{baseDir}` 占位符 |
| macOS/Linux 兼容 | 避免 GNU 特有参数，如 `base64 -w` |

## Next

- [ ] 补充 ACP harness 集成测试流程
- [ ] 添加 skill 间依赖管理规范
