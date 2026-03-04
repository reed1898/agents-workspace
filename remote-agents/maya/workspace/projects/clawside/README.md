# ClawSide

ClawSide 是一个 **Chrome MV3 浏览器侧边栏助手扩展**，直接连接 OpenClaw Gateway（`ws://` / `wss://`），不需要独立后端服务。

当前版本重点：
- 纯前端扩展架构（无本地 backend 进程）
- 多 Agent（独立网关地址 / token / sessionKey）
- 类 ChatGPT 的会话流聊天 UI（保留上下文）
- 可配置快捷动作（默认 3 个）
- Push / Overlay 布局模式

---

## 1. 功能概览

### 1.1 OpenClaw 直连
- 通过 Gateway WebSocket 协议直接连接 OpenClaw
- 支持 `ws://` / `wss://`，也接受 `http://` / `https://`（自动转换为 WS）
- 发送链路：`connect -> chat.send -> chat events`

### 1.2 多 Agent 管理
每个 Agent 独立配置：
- `name`：Agent 名称（用于区分“在和谁聊天”）
- `baseUrl`：Gateway 地址（建议本地用 `ws://127.0.0.1:18789`）
- `token`：Gateway token
- `sessionKey`：会话键（默认 `main`）

UI 交互：
- 顶部 Agent tabs 切换
- 图标按钮：编辑 / 新增
- 打开侧边面板进行保存、删除、连接测试

### 1.3 聊天区（Atlas 风格）
- 中间区为聊天气泡流，不再展示原始 JSON
- 保留完整上下文消息（按页面 + Agent 隔离）
- 助手气泡显示当前 Agent 名称
- 失败请求显示系统消息

### 1.4 输入区交互
- `Enter` 发送
- `Shift + Enter` 换行
- 左下 `+` 用于展开/收起快捷动作 chips（不再打开设置）
- 右下圆形发送按钮可点击发送

### 1.5 快捷动作（默认 3 个）
默认显示：
1. 转为 Skill
2. 总结主题
3. 保存知识库

每个快捷动作可在 Settings 中配置：
- Label
- Action（`chat` / `summarize` / `save-kb` / `todo`）
- Prompt

### 1.6 页面上下文与隐私
- `Context` 开关已移到 Settings 面板
- 默认勾选（开启）
- 开启时会附带页面上下文（URL、标题、选中内容、页面摘要片段）
- 同时受域名隐私策略约束（allow / deny + per-site）

### 1.7 页面布局模式
- `push`（默认）：展开侧栏时给页面右侧留空间
- `overlay`：侧栏覆盖在页面上，不挤压主内容

---

## 2. 项目结构

```text
clawside/
├─ manifest.json
├─ background.js         # Gateway 通信、权限、消息路由
├─ content.js            # 侧栏 UI、交互、状态持久化
├─ styles.css            # 侧栏与聊天 UI 样式
├─ options.html          # 扩展 options 页
├─ options.js            # options 页逻辑
├─ options.css
├─ icons/
│  ├─ icon16.png
│  ├─ icon32.png
│  ├─ icon48.png
│  └─ icon128.png
└─ README.md
```

---

## 3. 安装与启动

### 3.1 加载扩展
1. 打开 Chrome：`chrome://extensions`
2. 打开开发者模式（Developer mode）
3. 点击 `Load unpacked`
4. 选择本项目根目录

### 3.2 首次配置（建议）
在扩展侧栏中：
1. `Add` 新建一个 Agent
2. 填写：
   - `Gateway URL`: `ws://127.0.0.1:18789`（本地默认）
   - `Token`: 你的 OpenClaw token
   - `Session Key`: `main`
3. 点击 `Test` 测连
4. `Save Agent`

---

## 4. 使用说明

### 4.1 普通聊天
- 在输入框输入问题
- 回车发送
- 中间聊天区持续追加消息

### 4.2 使用快捷动作
- 点击输入框上方快捷 chip（例如“总结主题”）
- 会把快捷 Prompt（以及你输入框里的附加要求）发送给 OpenClaw

### 4.3 切换 Agent
- 顶部 tabs 点击不同 Agent
- 聊天区会切换到该 Agent 的上下文记录

### 4.4 设置入口
右上角 `⋯` 打开 Settings，可配置：
- 布局模式（push / overlay）
- Context 开关
- 三个快捷动作

---

## 5. 与 OpenClaw 的协议说明

### 5.1 连接
- 建立 WebSocket 到 `baseUrl`
- 发送 `connect` 请求
- 带 token（如有）进行鉴权

### 5.2 发送消息
- 调用 `chat.send`
- 参数包含 `sessionKey`、`message`、`idempotencyKey`

### 5.3 接收消息
- 监听 `chat` event
- 消费 `delta` / `final` / `error` / `aborted`
- 在 UI 中转换为用户可读聊天气泡

### 5.4 连接测试
- `connect` 成功后发 `health`
- 用于快速校验连通性与 token 有效性

---

## 6. 数据与存储

### 6.1 `chrome.storage.sync`
- `openclaw`：Agent 列表与当前 activeAgentId
- `clawsideUi`：布局模式
- `clawsideShortcuts`：快捷动作配置
- `privacy` / `siteSettings`：上下文隐私策略

### 6.2 `sessionStorage`
- 聊天时间线按 `页面 + Agent` 隔离存储
- 默认最多保留最近 300 条消息

---

## 7. 常见问题（Troubleshooting）

### 7.1 `wss://127.0.0.1:18789` 连接失败
如果报 SSL 版本错误，说明本地 Gateway 是明文 WS：
- 使用 `ws://127.0.0.1:18789`
- 若必须 `wss`，需要在前面加 TLS 终端（Nginx/Caddy/Cloudflare Tunnel）

### 7.2 连接测试失败（Unauthorized）
- 检查 token 是否正确
- 检查 Gateway auth 模式是否允许当前 token

### 7.3 打开 Context 但没带页面内容
- 检查域名是否被 deny
- 检查当前站点开关是否关闭

### 7.4 发送后没有回复
- 查看聊天区系统消息（会显示错误）
- 用 `Test` 按钮先确认网关连通

### 7.5 `chat.send failed: missing scope operator.write`
- 这是 Gateway token 权限模型与 WebSocket `chat.send` scope 不匹配导致
- ClawSide 现在会在该错误出现时自动从 WS 发送降级到 HTTP `POST /v1/responses`
- 连接测试（`connect + health`）仍走 WebSocket，测试通过不代表 WS `chat.send` scope 一定满足
- 如果仍失败：检查 token scope、Gateway ACL、以及 HTTP 路径是否可用

---

## 8. 开发说明

### 8.1 技术栈
- Chrome Extension Manifest V3
- 原生 JS + CSS（无框架）

### 8.2 关键设计原则
- 无后端依赖，直接走 OpenClaw Gateway
- UI 与存储尽量轻量，易定制
- 保持侧栏在网页中低侵入，支持 push/overlay 切换

---

## 9. Roadmap（可选）

可继续演进：
- 消息 Markdown 渲染（列表/代码块/链接）
- 交互式消息操作（重试、复制、引用）
- Agent tab 拖拽排序
- 更细粒度的快捷动作管理

---

## 10. 许可

如需开源发布，请补充 LICENSE（例如 MIT）。
