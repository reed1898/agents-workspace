# AvatarKit 项目记录

## 项目概述
- **名称**: AvatarKit
- **目标**: 为 OpenClaw Agent 提供统一的形象、声音、视频能力
- **分发方式**: skill.md 文件 (avatarkit.com/skill.md)

## 代码仓库要求
- **GitHub 账号**: https://github.com/reed1898
- **前端仓库**: `reed1898/avatarkit` (对外开源)
- **后端仓库**: 内部使用，不公开
- **建议结构**:
  ```
  avatarkit/
  ├── src/             # OpenClaw skill 源代码
  ├── SKILL.md         # Skill 定义文件
  ├── README.md        # 项目说明
  ├── package.json     # Node.js 配置
  └── docs/            # 使用文档
  ```

## 开发分工
| 模块 | 子代理 | 会话 Key |
|------|--------|----------|
| Skill (前端) | avatarkit-dev | agent:main:subagent:a1324750-545b-4b4d-824a-0067af267311 |
| API (后端) | avatarkit-api | agent:main:subagent:0321bd80-dc30-45a6-bddc-506ad1f05455 |

## 核心要求
1. **自然交互**: 非命令式，Agent 主动根据对话发图/语音
2. **角色记忆**: 记住用户喜欢的场景和互动方式
3. **GitHub 提交**: 开发完成后必须提交到 GitHub

## 时间线
- 2026-02-11: 项目启动，双线程开发

## 待办
- [ ] 确定 GitHub 仓库名
- [ ] 创建仓库
- [ ] Skill 开发完成并提交
- [ ] API 开发完成并提交
- [ ] 编写完整文档
