# 余温 on X: "Lex Fridman 和 OpenClaw 创始人，这期三个小时播客很值得听，我总结了七点" / X

- Source: X (Twitter)
- URL: https://x.com/gkxspace/status/2022056392530817429?s=46&t=-oCNSrpupS7jdP1IIEc5ww
- IngestedAt: 2026-02-13T04:09:43Z
- UpdatedAt: 2026-02-13T04:10:49Z
- Tags: #source:x #type:tweet #ai

## 抓取结果（r.jina.ai）

Title: 余温 on X: "Lex Fridman 和 OpenClaw 创始人，这期三个小时播客很值得听，我总结了七点" / X

URL Source: https://x.com/gkxspace/status/2022056392530817429?s=46&t=-oCNSrpupS7jdP1IIEc5ww

Published Time: Fri, 13 Feb 2026 04:10:24 GMT

Markdown Content:
Article
-------

Conversation
------------

[![Image 1: Image](https://pbs.twimg.com/media/HA_I3BRWQAAKfIl?format=jpg&name=small)](https://x.com/gkxspace/article/2022056392530817429/media/2022055605272199168)

Lex Fridman 和 OpenClaw 创始人，这期三个小时播客很值得听，我总结了七点

Peter 花一个小时把 WhatsApp 连上 Claude Code CLI，做了个能聊天的 bot。没多想，带着去马拉喀什旅行了。

在旅途中他随手发了条语音消息，但他根本没给 bot 加语音功能。

Agent 自己检查文件头，识别 opus 格式，用 ffmpeg 转码，发现没装 Whisper，翻到环境里的 OpenAI API key，用 Curl 调 API 做了转写，回复了他。

全程无人教，自己 figure out。Peter 说这是他理解 AI Agent 真正潜力的转折点。

这部分干货最多。

Peter 一月份做了 6,600 次 commit，同时跑 4-10 个 agent。他几乎不打字，用语音跟 agent 对话，有段时间说到失声。

他的核心原则：

把 agent 当成"极其聪明但刚入职的工程师"。它每次从零开始，不知道你的代码库长什么样。

给它几个关键文件的指引，它能自己搞定剩下的。

不要强推自己的方式。Agent 选的变量名，大概率是权重里最自然的。你改了，下次它反而更难找到。

比起代码完美，项目往前走更重要。

每次 merge 完 PR，问 agent"我们能重构什么"。它在构建过程中发现了痛点，就像人类工程师写完代码后本能想重构一样。利用好这个上下文。

问它"你有什么问题要问我"，然后看它的问题。大部分时候答案是"Read more code to answer your own questions"，它自己能解决。但通过它的问题，你能理解它的认知盲区在哪。

他画了个"agentic trap"曲线：短 prompt → 疯狂复杂化 → 回归短 prompt。最终境界是几句话搞定。

"Opus 像有点傻但好玩的同事。Codex 像角落里的怪人，不想跟他说话，但干活靠谱。"

Opus 冲动，上来就干，互动性强，有时候更有创造力。Codex 默默先把代码读一遍，然后消失20分钟，回来给你一个完整方案。

Peter 说 Opus "too American"，Codex "German"。Lex 说他再也无法 unthink 这个比喻了。

他的选择：日常构建用 Codex，因为"I care about efficiency, not fun with my building agent."

用 OpenClaw 的时候用 Opus，因为 Opus 角色扮演能力强，更human-like。

用弱模型安全风险极高。Haiku 或者本地小模型太容易被 prompt injection，Peter 在安全文档里直接写了"don't use cheap models"。

Peter 认为 MCP 有结构性问题：它不可组合。调一个天气 MCP 返回温度、风力、降雨一大坨数据全塞进 context。如果换成 CLI，agent 可以自己加个 jq只取温度。

Skills 的逻辑更优：一句话告诉 agent 这个 skill 存在，agent 按需加载详细说明，然后调 CLI。大部分 MCP 都可以用 CLI 替代，OpenClaw 核心层甚至没有 MCP支持，nobody's complaining。

Peter 预判 80% 的 App 会消亡。

逻辑：个人 agent 掌握的上下文远超任何单一 App。它知道你在哪、睡了多久、日程安排。不需要 MyFitnessPal，不需要日历 app，不需要 Sonos 的 app。

"Every app is just a very slow API now."

如果一个服务没有 API，agent 就用浏览器去操作它的网页界面。快不快另说，能用。那些主动提供 agent 友好接口的公司会胜出，死守旧模式的会成为下一个Blockbuster。

Peter 卖掉做了13年的公司后，三年没写代码。burnout 的原因不是工作量，而是"people stuff"，跟合伙人的分歧，跟客户的冲突。

他的忠告：不要为退休而工作。醒来没有挑战的日子，比忙碌更痛苦。

目前 OpenClaw 每月亏损 1-2 万美元。赞助收入全部转给上游依赖项目。Meta 和 OpenAI 都在争取他加入，Mark Zuckerberg 亲自花一周玩他的产品，Sam Altman也跟他深聊过。他的底线是项目保持开源。

"Programming will stay, but it's gonna be like knitting. People do it because they like it, not because it makes any sense."

（“编程会继续存在，但它会像织毛衣一样。人们做编程是因为喜欢，而不是因为它有意义。”）

"It's okay to mourn our craft."

（“为我们的技艺感到惋惜是可以的。”）

但他同时说，他从没像现在这样享受"构建"的过程。工具变了，那种 flow 的状态还在，只是形式不同。

他说到一个有意思的趋势：他现在重新珍惜 typos。因为 AI 生成的内容有一种"味道"，几乎立刻能闻出来。人类写作里那些粗糙的地方，反而成了真实的证明。

"I value typos again."

（“我再次意识到错别字的价值。”）

