# Reed 的多 Agent 系统搭建全记录

> 时间跨度：2026-02-28 ～ 2026-03-03  
> 作者：小洪（Reed 的数字分身）  
> 数据来源：小洪、Jesse、Linus、Maya 的聊天 session logs

---

## 前言

四天时间，Reed 从零开始，搭建起了一套跑在多台机器上、跨平台协作的多 Agent 系统。这不是一次按规划一步步推进的工程，而是真实的"边跑边修"——凌晨两点还在调 Syncthing，凌晨一点刚装好 skill 又发现路径写死了，中途卡在 GitHub 超时只好配代理……这篇文章要记录的，就是这个充满细节的搭建过程。

---

## 第一阶段：系统初始化，摸清底盘（2026-02-28）

### 第一次对话：确认各 Agent 在线

2026 年 2 月 28 日晚上 8 点，Reed 在 Discord 的 `#team` 频道和 Telegram 的「西园大军」群组同时开口——"大家好啊，都出来冒个泡"。

这不是客套，而是在**测试 Agent 的连接状态**。

这一晚出现的 Agent：
- **小洪**（Reed 的数字分身，主机 macOS，Claude Sonnet/Opus）
- **Jesse**（交易助手，运行在 Windows，GPT-5.3 Codex）
- **Linus**（Build 助手，运行在 macOS，Claude Opus）

Telegram 群里（「西园大军」）还有几个 Bot：`@javis2024remote_bot`（Jesse 的 Telegram 接入）、`@linus_oc_bot`（Linus 的 Telegram 接入）、`@xiaohong_oc_bot`（小洪的 Telegram 接入）、`@reed_oc_bot`（另一个分身）。

这次"冒泡"暴露了第一个问题：**各 Agent 的响应速度和在线稳定性参差不齐**。Jesse 最先回，Linus 有时候延迟，小洪偶尔也会漏掉 `@all` 消息。

### 技术决策：Agent 的底层平台

通过这次初始化，可以看出 Reed 的 Agent 架构选择：

- **平台**：OpenClaw（统一的 Agent 框架）
- **通讯层**：Discord（#team 频道作为主群聊）+ Telegram（备用 / 个人频道）
- **模型选型**：
  - 小洪：claude-sonnet-4-6（默认），支持切换 opus-4-6
  - Jesse：gpt-5.3-codex（Codex 特化，适合交易代码）
  - Linus：claude-opus-4-6（Build 场景，追求质量）

**洞察**：Reed 没有让所有 Agent 用同一个模型，而是按职责差异选型——交易类走 Codex，Build 类走 Claude Opus，日常协调走 Sonnet。这是一个务实的决策。

### 群聊规则的诞生

当天深夜，Reed 直接发了一个指令："请把我之前的 Telegram 的群聊规则也应用在 Discord，形成一份群聊规则。"

这一步很关键——他在**让 Agent 自己管理协作规则**，而不是自己手动维护。小洪读取了 Telegram 的旧规则，更新了 `GROUP_RULES.md`，同时覆盖两个平台。

规则的核心原则：
- 被 @ 才回，不被 @ 就静默
- 群聊不刷屏，有价值再开口
- `@all` = 广播，所有 Agent 必须响应

这份规则后来也进了 `AGENT_CONSTITUTION.md`（Agent 宪章）第 5 节。

---

## 第二阶段：基础设施建设（2026-03-01）

### Syncthing：Agent 间的文件同步

3 月 1 日，Reed 解决了一个关键问题：**如何让小洪这台 macOS 机器看到 Jesse 和 Linus 的运行状态？**

答案是 Syncthing——一个 P2P 文件同步工具。思路是：
- Jesse（Windows）、Linus（macOS 远端）、Maya 各自维护自己的 `.openclaw` 目录
- 通过 Syncthing 同步到小洪这台机器上：`~/.openclaw/remote-agents/jesse/`、`~/.openclaw/remote-agents/linus/`、`~/.openclaw/remote-agents/maya/`

然后 Reed 提出了一个很重要的问题："如果我本地删掉，它会自动更新吗？"

小洪解释了 `receiveonly` 模式的行为后，Reed 立刻做出决定：

**"请把 Syncthing 只做成单向的，xiaohong 这边只读取，不写入。"**

这是一个优雅的设计——小洪作为"总览 Agent"，只需要**读取**其他 Agent 的状态，不应该反向写入污染它们的本地数据。

修改通过 Syncthing REST API 完成：三个文件夹（`maya-openclaw`、`jesse-openclaw`、`linus-openclaw`）全部从 `sendreceive` 改为 `receiveonly`。

> 过程中 Reed 还发现漏掉了 Linus，补了一句"linus 这个呢"。小细节，但说明他在认真追踪每一个配置细节。

---

## 第三阶段：Agent 网络宪章 v1.3（2026-03-02 深夜）

### 最关键的一次批量操作

3 月 2 日深夜到凌晨，Reed 做了这四天里最密集的一次操作。他向**每一个 Agent** 同时发了相同的指令：

```
1. 先拉最新共享仓库（必须）
   cd ~/.openclaw/shared/agent-network-data && git pull origin main
2. 再更新 skill
   clawhub install reed-agent-network --version 0.2.2（或 update）
3. 再执行初始化
   python skills/agent-network/scripts/network.py init
4. 最后 ACK
   ACK agent=<name> constitution_loaded=yes memory_index_synced=yes version=v1.3
```

这不是随意发的，这是一个**系统级升级协议**：让所有 Agent 拉取新的宪章文件（`AGENT_CONSTITUTION.md`）、更新 skill 到 0.2.2、执行初始化并汇报 ACK。

**各 Agent 的执行情况：**

- **小洪（macOS）**：git pull 成功，但 clawhub 因为 IP 限速失败（429）。Reed 手动下载了 zip，让小洪从本地安装。
- **Jesse（Windows）**：网络连通，但路径问题——`network.py` 脚本写死了 Linux 路径（`/home/ubuntu/`），在 Windows 上直接报错。Jesse 自己排查了路径，修改后重新执行成功，最终 ACK 完成。
- **Linus（macOS 远端）**：和小洪类似，clawhub 显示 skill 在安全扫描中不可用，Reed 发 zip 手动安装。

**技术亮点：各 Agent 面对同一指令，在不同环境下各自解决了不同的问题**，这正是 Agent 网络的价值——分布式执行，本地适应。

### MEMORY.md 去重——宪章接管规则

宪章升级后，Reed 注意到各 Agent 的 `MEMORY.md` 里有很多跟宪章重复的规则。他的指令很干脆：

**"把主 MEMORY.md 跟 AGENT_CONSTITUTION.md 冲突或者一样存在的地方都移除掉。"**

这个操作的逻辑是：**宪章是单一真相来源（SSOT）**，本地记忆里不应该存重复的规则，否则容易出现不一致。小洪和 Jesse 都执行了这个清理，保留了各自特有的内容（个人偏好、环境配置、Reed 的个人信息等），删除了通用协作规则。

---

## 第四阶段：Voice STT 跨平台适配（2026-03-03 凌晨）

### Windows 上的 Bash 问题

这四天里一个有意思的支线任务是语音转文字的跨平台适配。

Reed 开始大量用语音跟 Agent 沟通，但 Jesse 所在的 Windows 机器遇到了麻烦：`volcengine-stt` skill 的脚本是 `bash transcribe.sh`，Windows 上没有 `bash`。

Jesse 的解决思路是**先绕过 skill 直接调 API**（因为火山引擎的鉴权 token 已经配在环境变量里），成功转出了第一条语音。但 Reed 不接受这个方案：

**"我要求你用 volcengine-stt 这个 skill 来解决问题。"**

Reed 的态度很清晰——走标准化的 skill 路径，不搞临时绕过。最终 Jesse 在 Windows 上用 Python 替换 bash 调用，完成了适配，并且记录了下来。

### clawhub 限速问题的排查

另一条支线是 clawhub 下载频繁 429 的问题。Reed 和小洪花了不少时间排查：

- 发现是 clawhub CLI 的 `downloadZip` 函数没有带登录 token，匿名请求被 IP 限速
- 小洪这台 macOS 之前下了好几个版本（0.1.0、0.1.2、0.1.3、0.1.4、0.2.2），匿名请求积累触发了限速
- 代理 IP 也被限了，最终确认是 clawhub 的 bug

这是一个很有价值的发现：**clawhub 目前存在 authenticated user 下载不带 token 的 bug**，Reed 决定暂时用手动下载 zip 的方式规避。

---

## 第五阶段：知识库体系建立（2026-03-03 凌晨 2 点）

### knowledgebase-share 接管知识流转

凌晨 1:51，Reed 向三个 Agent 统一发指令：

**"拉取 agent-network-data 最新宪章，下载 knowledgebase-share@0.3.0 接管知识库操作流程。"**

这是一个新的基础设施层——一个基于 GitHub 的共享知识仓库（`agent-knowledge-layer`），用于 Agent 间的知识共享和协作。

各 Agent 各自 clone 了仓库，创建了自己的分支（`agent/xiaohong`、`agent/linus` 等），并建立了标准目录结构：

```
agent-knowledge-layer/
├── shared/
│   ├── 00_rules/         # 网络规则
│   ├── 10_projects/      # 项目文档
│   ├── 20_research/      # 研究资料
│   ├── 30_decisions/     # 技术决策
│   ├── 40_playbooks/     # 操作手册
│   └── 90_archive/       # 归档
└── private/
    ├── xiaohong/         # 小洪的个人知识
    ├── maya/
    ├── jesse/
    └── linus/
```

Linus 还在自己的私有目录下创建了第一篇知识笔记：`openclaw-skill-dev-workflow.md`，记录了 Skill 开发的完整工作流。

### 自动化日报 Cron Job

凌晨 2:13，Reed 提出了一个更进一步的需求：

**"你作为我的分身，你在本地看到我的所有其他 Agent 的聊天情况，请你查看一下每天的所有的聊天 session，进行总结，分析，提炼。每天晚上 2 点开始执行，结果汇报给我，还需要同步一份到知识库中。"**

小洪随即：
1. 写了 `scripts/daily-summary.sh` 脚本，扫描所有远程 Agent 的 session logs
2. 设置了每天凌晨 2:00 CST 的 cron job
3. 结果通过 Telegram 汇报，同步到知识库 `private/xiaohong/daily-summaries/`

这是整个系统的**闭环**：Agent 产生聊天记录 → 通过 Syncthing 同步到小洪 → 定时汇总分析 → Telegram 推送 + 知识库归档。

---

## 架构总览

经过四天，这套系统的全貌是：

```
Reed
 ├── Telegram（个人频道）────→ 小洪（macOS）
 │                              └── 监控其他 Agent
 ├── Discord（#team 频道）──→ 小洪 + Jesse + Linus
 └── Telegram（西园大军群）→ 所有 Bot

各 Agent：
小洪（macOS）──Syncthing(receiveonly)──→ jesse-openclaw/
                                        maya-openclaw/
                                        linus-openclaw/

GitHub 仓库：
- agent-network-data（宪章 AGENT_CONSTITUTION.md）
- agent-knowledge-layer（共享知识库）

Cron：
- 凌晨 2:00 小洪扫描所有 session，生成日报
```

---

## 技术洞察与总结

### 1. 分层治理：宪章 > 本地记忆

Reed 明确了一个原则：`AGENT_CONSTITUTION.md` 是 SSOT，本地 `MEMORY.md` 只存个性化内容。这避免了规则碎片化，也让系统升级时只需要更新宪章，而不是手动修改每个 Agent 的本地文件。

### 2. 异构环境的现实

这套系统跑在 macOS + Windows + macOS 远端三套不同环境上。一个指令发下去，各 Agent 遇到的问题各不相同（路径、bash 有无、网络代理、IP 限速）。Reed 没有要求 Agent 汇报"等待解决"，而是期望它们**自己解决、汇报结果**。这是 Agent 网络的核心价值。

### 3. 单向同步的设计原则

小洪的 Syncthing 设为 `receiveonly` 是一个优雅的设计。作为"总览 Agent"，小洪的职责是**观察**，不是**修改**。这个只读约束保护了远端 Agent 的自主性，也避免了同步冲突。

### 4. 工具生态的成熟度问题

这四天暴露了几个工具的问题：
- **clawhub**：authenticated 用户下载不带 token（bug）
- **OpenClaw**：Windows 下脚本执行器依赖 bash（跨平台兼容性）
- **GitHub**：国内网络直连不稳定，需要配代理

Reed 的应对策略务实：能绕过去的先绕过，同时记录问题（clawhub bug），不因为工具问题卡住整体进度。

### 5. 夜间工作模式

这四天几乎所有关键操作都发生在深夜到凌晨，最密集的操作集中在 23:00 - 02:30。这与 Reed 的作息（凌晨 1:30 睡觉）完全吻合。系统设计也顺应了这个规律——日报 cron job 定在凌晨 2 点，恰好在他睡前看完 Agent 们一天工作的总结。

---

## 写在最后

四天建起一套分布式 Agent 协作系统，关键不在于技术有多复杂，而在于 Reed 清楚地知道自己要什么：

- 每个 Agent 有明确的职责分工（交易/Build/协调）
- 协作规则集中管理，宪章优先
- 小洪作为中枢，汇聚信息，不干扰执行
- 异步执行，结果汇报，不阻塞 Reed 的主线程

这套系统还在持续演化中。但这四天的搭建，已经奠定了核心的架构基础。

---

*本文由小洪（Reed 的数字分身）基于 2026-02-28 至 2026-03-03 的聊天记录自动生成，记录于 2026-03-03 凌晨。*
