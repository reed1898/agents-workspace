# Backlog — 待处理 Issue

## 来自 Reed（日常痛点）

### #001 Discord channel 不支持原生 proxy 配置
- **描述**：中国区用户配置 Discord 需要走代理，但 OpenClaw 的 `channels.discord.proxy` 配置不生效。Telegram channel 可以正常配置 proxy，Discord 不行。目前需要手动 patch `@buape/carbon` 的 `RequestClient.js` 才能让 Discord 走代理。
- **严重程度**：高（中国区用户核心痛点，影响 Discord 可用性）
- **来源**：Reed 提报
- **状态**：待分析
- **相关文件**：
  - 补丁目标：`node_modules/@buape/carbon/dist/src/classes/RequestClient.js`
  - 现有 patch：`~/.openclaw/patches/carbon-proxy.patch`
- **期望**：openclaw.json 里配置 `channels.discord.proxy` 就能直接生效，不需要手动 patch

<!-- 格式：
### 标题
- 描述：xxx
- 严重程度：高/中/低
- 来源：Reed 提报 / Scout / 社区
- 状态：待分析 / 进行中 / 已提 PR / 已合并
-->

## 来自 Scout（GitHub issue 扫描）
_2026-03-04 第一次扫描_

### #S01 Matrix plugin Docker import path broken (#33266)
- **描述**：Matrix plugin 在 Docker 里因为 import 路径问题加载失败。`send-queue.ts` 引用了 `openclaw/plugin-sdk/keyed-async-queue` 子路径，但 Docker 构建后这个子路径不存在。修复只需改成 `openclaw/plugin-sdk` 主入口。
- **严重程度**：高（所有 Docker Matrix 用户受影响）
- **来源**：Scout - GitHub #33266
- **状态**：待评估
- **适合度**：⭐⭐⭐⭐⭐ 一行改动，清晰明确，作者已给出修复方案
- **链接**：https://github.com/openclaw/openclaw/issues/33266

### #S02 Windows: plugins install fails with spawn EINVAL (#7631)
- **描述**：Windows 上 `openclaw plugins install` 报 `spawn EINVAL`，因为 spawn .cmd 文件时没加 `shell: true`
- **严重程度**：高（Windows 用户无法安装插件）
- **来源**：Scout - GitHub #7631
- **状态**：待评估
- **适合度**：⭐⭐⭐⭐ 改动小，但需要注意跨平台兼容性测试
- **链接**：https://github.com/openclaw/openclaw/issues/7631

### #S03 Web UI: Unsupported schema node in Accounts section (#1749)
- **描述**：Web UI 的 Nodes/Accounts 显示 "Unsupported schema node" 错误
- **严重程度**：中（UI 问题，raw mode 可用）
- **来源**：Scout - GitHub #1749 (21 comments, 3 👍)
- **状态**：待评估
- **适合度**：⭐⭐⭐ 需要了解 Web UI schema 渲染逻辑，中等复杂度
- **链接**：https://github.com/openclaw/openclaw/issues/1749

## 来自社区（Discord / Discussion）
_待收集_
