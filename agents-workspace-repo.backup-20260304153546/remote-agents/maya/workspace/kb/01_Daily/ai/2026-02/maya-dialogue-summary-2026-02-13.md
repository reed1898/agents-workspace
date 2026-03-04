# 与 Maya 的对话复盘（UTC 2026-02-13｜截取到可见片段）

> 说明：本总结基于当前可读取到的 `agent:main:main` 会话片段（消息较长，可能未覆盖全部）。重点提炼“你当时在推动什么、做对了什么、踩了什么坑、可复用规则”。

## 1) 今天你和 Maya 主要在推进什么

### A. 本地与云端工作区打通（Syncthing）
- 你在本地 Mac 上把 Syncthing 配置进了 `workspace-reed` 的 folder：
  - folder id：`oc-workspace-reed`
  - path：`/Users/rain/.openclaw/workspace-reed`
  - 确认 `.stfolder` 已存在
- 结论：这是在为“分身 Agent 的私有工作区”做可靠同步底座（后续对话/产出/模板可以在本地和云端一致维护）。

### B. Gateway 配置加载 / bindings 修复（最关键的工程动作）
- 你在添加 Reed bot 绑定时，出现过一次 **bindings 被覆盖/路由风险**。
- Maya 侧通过 `gateway config.patch` 把 bindings 恢复为完整集合：
  - Telegram：maya / jesse / linus / reed
  - Discord：多条 channel bindings
- 随后用 `openclaw status --deep` 验证 **Telegram accounts 4/4 OK**，并确认 `@reed_oc_bot` 连通。
- 这一步本质是在做“配置真源 + 最小回归验证”。

### C. 通道错乱排查：多 bot 并存时的 UX 问题
- 你觉得消息“错乱”，Maya 侧采用 **A/B 测试消息**定位问题：
  - 从 Maya bot 发测试消息让你回 1
  - 从 Reed bot 发测试消息让你回 2
- 结论：两条你都能收到 → 通道不是断的，主要是：
  1) 你在不同 bot 私聊窗口之间切换导致上下文断档；
  2) Telegram 的 reply 引用在跨 bot/跨上下文时会失败（出现过 replyTo not found），造成“视觉串线”。
- 你最终选择方案 A：保留两个入口，按分工使用。

### D. “超级助理能做什么”的能力边界与安全策略
- 你问了“能帮我做什么”以及“对外聊天如何安全实现”。
- Maya 给了一个相对工程化的答案：
  - 分层权限（只聊/可读白名单/可执行需审批）
  - 对外动作必须确认 + 可审计
  - 需要升级给你的场景（钱/隐私/承诺/冲突等）

### E. 自拍技能试运行（clawra-selfie）
- Maya 拉取 `clawra-selfie` 的配置并调用图像编辑 API 生成一张自拍图，并通过 Telegram 发送。
- 过程中尝试 reply 引用失败 → 加深了“跨上下文 reply 的不稳定性”这一结论。

## 2) 今天最值钱的经验（可直接写成 SOP）

1) **配置变更必须用 patch 而不是覆盖**：尤其是 `bindings` 这种“路由真源”，任何覆盖都可能造成“消息串台/丢路由”。
2) **改完立刻做最小回归验证**：`openclaw status --deep` + 发一条测试消息，是最便宜的冒烟测试。
3) **多 bot 并行=必须有分工协议**：否则用户端体验必然“像串台”。
4) **对外动作要有回执链路**：发帖/发图这种动作，不仅要执行，还要能确认“已发/链接是什么/失败原因”。
5) **reply 引用别当可靠机制**：跨 bot/跨 session 的 reply 很容易失败；关键消息要用“明确引用文本/手动标注上下文”替代。

## 3) 可落地的下一步（建议）

- 把「bindings patch + 回归验证」写成一段固定流程文档（并加到 KB/或运维 SOP）。
- 把「多 bot 分工协议」写进两个 bot 的固定开场提示（减少你自己切窗口的认知负担）。
- 对“发布类动作”（X 发帖）补一个“发布后抓链接”的回执步骤，避免以后再出现“点了但无法确认”。
