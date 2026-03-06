# 卡尔的AI沃茨

> **Author**: 卡尔的AI沃茨
> **Source**: https://x.com/aiwarts/status/2028841164418494872
> **Date**: 2026-03-04 15:02
> **Replies**: 11 · **Retweets**: 82 · **Likes**: 358 · **Views**: 0

---

## TLDR

这条内容信息量很大，我先给你一个精炼版解读（适合转发/收藏）：

这条推文核心是在讲：**把 OpenClaw 从“能用”升级到“好用”，优先做“联网搜索能力栈”而不是花哨功能。**

- 先替换默认搜索：`Brave/Perplexity` → `Tavily + Multi Search Engine`
- 用 `x-reader + Agent Reach` 补齐难解析平台（X/公众号/某书/Reddit/GitHub 等）
- 用 `BrowserWing` 做可复用浏览器操作回放（比单纯 Playwright 更“技能化”）
- 有 Gemini 账号再加：`ModSearch + Gemini Deep Research`
- 用 `find-skills + Clawhub` 让系统自动找技能
- 用 `ClawFeed` 做被动情报订阅源
- 用 `Free Ride` 做 OpenRouter 免费模型兜底，防止长任务中断

如果你愿意，我可以继续把这段整理成你可直接发的版本（比如：  
1）更像教程的「安装顺序清单」  
2）更像评测的「组件对比表」  
3）更像推文的「短句爆款版」）。

---

## Original Content

高级OpenClaw第一步！先用12个Skills把联网搜索做到极致

OpenClaw从中级到高级第一步不是做龙虾分身，先把联网搜索做到极致，把X，某站，某书，播客，公众号，Reddit啥的全都解析明白，再把Deep Research装上，再加上主动订阅的信息源和OpenRouter免费兜底的大模型，这应该是目前云上OpenClaw在不方便文件互传的情况下的最佳搭配方案。

一键安装的命令我整理到最后了。

OpenClaw目前内置的联网搜索是Brave和Perplexity，一个要绑卡一个要付费。

所以我们直接先换成Tavily和Multi Search Engine v2.0.1，

- Tavily每月1000次免费调用，不用绑卡。好处就是它本身就是专门给Agent做的搜索API，返回的内容处理过了。

- Multi Search Engine集成了17 个搜索引擎（8个中文+9个全球），不需要API，安装的时候把搜索规则记下就行

但总有些难啃的链接，公众号，某书，某X的不好解析，这段时间我还装了Agent Reach和x-reader，

它们覆盖的平台是有重复的，为了安全性会在本地安装一个docker虚拟机来模拟操作，

- x-reader能覆盖yt，某站，X，公众号，tg，rss，播客，某书
- Agent Reach在x-reader的基础上多了某抖，Reddit，Github，优先用Cookie登陆不需要扫码，但我还是建议用小号。

还有一类是需要浏览器自动化的，
比方说点击确定，滑动页面，一般来说是用Playwright，

但我发现了更好用的，
BrowserWing可以记录浏览器的操作做成Skills，下次再用就可以精确重放了。

如果有一个gemini账号，还可以安ModSearch和Gemini Deep Reserach，

- ModSearch把gemini cli做成了联网搜索，Google的信息搜索本来就很强，不是反代，没有风险。
- Gemini Deep Reserach就相当于把Gemini的Deep Research能力搬到OpenClaw里面了，还是Gemini 3.1 Pro驱动的。

还有三个比较特别的，
find-skills，Clawhub和ClawFeed
find-skills和Clawhub都是让OpenClaw遇到问题主动找合适的Skills的。

把ClawFeed放在这里因为它相当于是一个被动更新的信息源，可以订阅X，RSS，HackerNews，Reddit和GitHub Trending，4个小时更新一次。

最后加个Free Ride，
很多朋友虽然已经开始用API了，但没有做额度管理，如果当时在跑一个很长的任务的话，因为速率限制直接就废了。Free Ride相当于调用了OpenRouter上的免费模型，它自动就按照质量排名了，这样的话我们不需要担心openclaw半夜停了。

（1/2）
