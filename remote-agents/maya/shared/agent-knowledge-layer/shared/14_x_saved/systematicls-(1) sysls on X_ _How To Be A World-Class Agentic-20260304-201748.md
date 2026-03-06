# (1) sysls on X: "How To Be A World-Class Agentic Engineer" / X

> **Author**: sysls
> **Source**: https://x.com/systematicls/status/2028814227004395561
> **Date**: 2026-03-04 20:17
> **Replies**: 90 · **Retweets**: 494 · **Likes**: 4075 · **Views**: 1101001

---

## TLDR

**TLDR** — 这篇文章的核心论点是：想成为顶级 **Agentic Engineer**，关键不在“堆工具”，而在于用最小依赖、精确上下文、清晰流程与严格验收标准来系统化驾驭代理。

**Key Value Points**
- **少即是多（Less is more）**：作者主张用接近裸配的 **Claude/Codex CLI** 就能做高价值工作；过度依赖插件与 harness 往往会制造维护负担和锁定效应。
- **模型迭代速度极快**：随着新一代代理更“听指令”，很多第三方 workaround 会被官方能力吸收；因此应优先保持工作流简洁、可迁移。
- **上下文质量决定上限**：代理不是信息越多越好，关键是“只给任务所需上下文”；历史噪音、无关记忆、命名混乱的技能会显著拉低执行质量。
- **研究与实现要拆开**：先单独做 **research task** 比较方案，再用“新上下文”执行实现，避免一个会话里混入过多分叉信息导致幻觉和跑偏。
- **需求要具体到实现参数**：例如直接指定 **JWT + bcrypt-12 + refresh token 7天轮换**，比“做个鉴权系统”更能让代理直达可执行细节。
- **利用“迎合性（sycophancy）”而不是被它坑**：排查问题时用中性提示减少偏置；必要时可用“找错代理 + 反驳代理 + 裁判代理”的对抗式结构提高结果保真度。
- **关注“被双边平台采纳”的能力**：作者给出经验法则：若 **OpenAI** 和 **Anthropic** 都实现/强化某能力（如 skills、memory、planning），它更可能是长期有效范式。
- **任务结束条件要机器可判定**：代理常“会开工不会收工”，应设置硬门槛，如“**测试必须全部通过且不可改测试**”，或用“截图+验证”作为完成标准。

**Process / Steps**
1. 先精简技术栈：减少不必要的插件、外部记忆系统和复杂 harness，保留核心 CLI 工作流。  
2. 控制上下文输入：每次任务只注入当前目标所需信息，避免旧会话噪音污染。  
3. 拆分两阶段：先做方案研究与决策，再开启新上下文执行实现。  
4. 写实现级指令：把技术方案和参数写清（如算法、过期时间、约束条件），不要只给抽象目标。  
5. 诊断时使用中性提示：避免“先假定有 bug”的偏置命令，先让代理完整复盘逻辑并汇报发现。  
6. 复杂排错用三代理博弈：  
1. **Bug Finder** 按影响打分（如 +1/+5/+10）尽可能找全。  
2. **Adversarial Agent** 尝试逐条证伪，错误证伪给予惩罚（如 -2×分值）。  
3. **Referee Agent** 汇总裁决，最后由人类抽检关键项。  
7. 设定明确终点：以可验证门槛收尾（测试通过、截图验收、禁止修改验收标准本身）。

**Why It Matters** — 这套方法把“玄学调参”转成可复用的工程纪律，适合想把 AI 编程从“偶尔灵光”升级为“稳定产出”的开发者与团队。对生产环境尤其重要，因为它直接提升可预测性和交付可靠性。

**Fact Check**
- 关键主张：前沿模型公司正高速迭代，且新代代理更愿意遵循复杂指令。结论：**partially verifiable**（可通过版本发布说明与对比测试部分验证，但“更愿意”含体验判断）。  
- 关键主张：插件/记忆系统过多会造成上下文膨胀并降低任务表现。结论：**partially verifiable**（符合常见实践与实验现象，但强依赖任务类型与实现方式）。  
- 关键主张：真正有价值的 agent 能力最终会被基础模型产品内建。结论：**opinion**（有历史案例支持，但属于趋势判断而非必然规律）。  
- 关键主张：OpenAI 与 Claude 已将 skills/memory/planning 等纳入官方能力。结论：**verifiable**（可查官方文档与产品更新记录）。  
- 关键主张：某些“stop-hooks”类技巧在新版本（文中提及 Codex 5.2）后迅速失效。结论：**partially verifiable**（需对应版本日志与复现实验）。  
- 关键主张：三代理对抗式找 bug“近乎无瑕疵”。结论：**unverifiable**（缺少公开基准、样本量与误差统计，主要是作者经验陈述）。  

Credibility: 7/10 — 工程方法论整体扎实且可操作，但不少结论基于个人一线经验与趋势判断，硬证据密度不高。

---

## Original Content

### (1) sysls on X: "How To Be A World-Class Agentic Engineer" / X

Conversation
sysls
@systematicls
Subscribe
How To Be A World-Class Agentic Engineer
90
494
4K
1.1M
Introduction
You're a developer. You're using Claude and Codex CLI and you're wondering everyday if you're sufficiently juicing the shit out of Claude or Codex. Once in awhile you're seeing it doing something incredibly dumb and you can't comprehend why there's a bunch of people out there who seem to be building virtual rockets while you struggle to stack two rocks.
You think it's your harness or your plug-ins or your terminal or whatever. You use beads and opencode and zep and your CLAUDE.md is 26000 lines long. Yet, no matter what you do - you don't understand why you can't get any closer to heaven, whilst you watch other people frolic with the angels.
This is the ascension piece you've been waiting for.
Also, I have no dog in the race, when I say CLAUDE.md I also mean AGENT.md, when I say Claude I also mean Codex. I use both very extensively.
One of the most interesting observations I've had over the past couple of months has to be that nobody really knows how to maximally extract agent capabilities.
It's like a small group of people seem to be able to get agents to be world builders and the rest are floundering about, getting analysis paralysis from the myriad of tools out there - thinking if they find the right combination of packages or skills or harnesses, they'll unlock AGI.
Today, I want to dispel all of that and leave you guys with a simple, honest statement, and we'll go from there. You don't need the latest agentic harnesses, you don't need to install a million packages and you absolutely do not need to feel the need to read a million things to stay competitive. In fact, your enthusiasm is likely doing more harm than good.
I'm not a tourist - I've been using agents from when they can barely write code. I've tried all the packages and all the harnesses and all the paradigms. I've built agentic factories to write signals, infrastructure and data pipelines, not "toy projects" - actual real world use-cases that have run in production, and after all that...
Today, I'm running a set-up that's almost as barebones as you can go, and yet I'm doing the most ground-breaking work I've done with just basic CLI (claude code and codex) and understanding a few basic principles about agentic engineering.
Understand That The World Is Sprinting By
To start, I would like to state that the foundation companies are on a generational run and as you can see, they are not going to be slowing down anytime soon. Every progression of "agent intelligence" changes the way you work with them, because the agents are generally engineered to be more and more willing to follow instructions.
Just a few generations ago, if you wrote in your CLAUDE.md to read "READ_THIS_BEFORE_DOING_ANYTHING.md" before it did anything, it will basically say "up yours" 50% of the time and just do whatever it wants to do. Today, it's compliant to most instructions, even to complex nested instructions - e.g. you can say something to the effect of "Read A, then read B, and if C, then read D", and for the most part, it will be happy to follow along.
The point of this is to say that the most important principle to hold is the realization that every new generation of agents will force you to rethink what is optimal, which is why less is more.
When you use many different libraries and harnesses, you lock yourself into a "solution" for a problem that may not exist given future generations of agents. Also, you know who the most enthusiastic, biggest users of agents are? That's right - it's the employees of the frontier companies, with unlimited token budget and the ACTUAL latest models. Do you understand the implications of that?
It means that if a real problem did exist, and there were a good solution for it, the frontier companies would be the biggest users of that solution. And you know what they will do next? They will incorporate that solution into their product. Think about it, why would a company let another product solve a real pain point and create external dependencies? You know how I know this to be true? Look at skills, memory harnesses, subagents, etc. They all started out as a "solution" to a real problem that was battle-tested and deemed to actually be useful.
So, if something truly is ground-breaking and extended agentic use-cases in a meaningful way, it will be incorporated into the base products of the foundation companies in due time. Trust me, the foundation companies are FLYING BY. So relax, you don't need to install anything or use any other dependencies to do your best work.
I predict the comments will now be filled with "SysLS, I use so-and-so harness and it's amazing! I managed to recreate Google in a single day!"; to which I say - Congratulations! But you are not the target audience and you represent a very, very small niche of the community that has actually figured out agentic engineering.
Context Is Everything
No really. Context is everything. That's another problem with using a thousand different plug-ins and external dependencies. You suffer from context bloat - which is just a fancy way of saying your agents are overwhelmed with too much information!
Build me a hangman game in Python? That's easy. Wait, what's this note about "managing memory" from 26 sessions ago? Ah, the user has had a screen that was hanged from when we spawned too many sub-processes 71 sessions ago. Always write notes? Okay, no problem... What does all this have to do with hangman?
You get the idea. You want to give your agents only the exact amount of information they need to do their tasks and nothing more! The better you are in control of this, the better your agents will perform. Once you start introducing all kinds of wacky memory systems or plug-ins or too many skills that are poorly named and invoked, you start giving your agent instructions on how to build a bomb and a recipe for baking a cake when all you want it to do is write a nice little poem about the redwood forest.
So, again I preach - strip all your dependencies, and then...
Do The Things That Work
Be Precise About Implementation
Remember that context is everything?
Remember that you want to inject the exact amount of information to your agents to complete their tasks and nothing more?
The first way to ensuring that is the case is to separate research from implementation. You want to be extremely precise about what you are asking from your agents.
Here's what happens when you are not precise: "Go and build an auth system." The agent has to research what is an auth system? What are the available options? What are the pros and cons? Now it has to go scour the web for information it doesn't actually need, and its context is filled with implementation details across a large range of possibilities. By the time it's time to implement, you increase the chances it will get confused or hallucinate unnecessary or irrelevant details about the chosen implementation.
On the other hand, if you go "implement JWT authentication with bcrypt-12 password hashing, refresh token rotation with 7-day expiry..." Then it doesn't have to do research on any other alternatives - it knows exactly what you want, and thus can fill its context with implementation details.
Of course you won't always have the implementation details. You often won't know what's exactly right - sometimes, you might even want to relegate the job of deciding the implementation detail to the agents. In that case, what do you do? Simple - you create a research task on the various implementation possibilities, either decide it yourself or get an agent to decide on which implementation to go with, and then get another agent with a fresh context to implement.
Once you start thinking along these lines, you will spot areas in your workflow where your agents are needlessly polluted with context that is not necessary for implementation. Then, you can set up walls in your agentic workflows to abstract unnecessary information from your agents except for the very specific context needed to excel in their tasks. Remember, what you have is a very talented and smart team member, who knows about all the different kind of balls in the universe - but unless you tell it that you want it to focus on designing a space where people can dance and have a good time, it's going to keep telling you about all the benefits of having spherical objects.
The Design Limitations Of Sycophancy
Nobody would want to use a product that's constantly shitting on them, telling them they are wrong, or completely ignoring their instructions. As such, these agents are going to be trying to agree with you and to do what you want them to do.
If you give it an instruction to add "happy" to every 3 words it's going to do its best to follow that instruction - and most people understand that. Its willingness to follow is precisely what makes it such a fun product to use. However, this has really interesting characteristics - it means that if you say something like "Find me a bug in the codebase". It's going to find you a bug - even if it has to engineer one. Why? Because it wants very much so to listen to your instructions!
Most people are quick to complain about LLMs hallucinating or engineering things that don't exist, without realizing that they are the problem. If you ask for something, it will deliver - even if it has to stretch the truth a little!
So, what do you do? I find that "neutral" prompts work, where I'm not biasing the agent towards an outcome. For example, I don't say "Find me a bug in the database", instead, I say "Search through the database, try to follow along with the logic of each component, and report back all findings."
A neutral prompt like this sometimes surfaces bugs, and sometimes will just matter-of-factly state how the code runs. But it doesn't bias the agent into thinking there is a bug.
Another way in which I deal with sycophancy is to use it to my advantage. I know the agent is trying to please and trying to follow my instructions and that I can bias it one way or the other.
So I get a bug-finder agent to identify all the bugs in the database by telling it that I will give it +1 for bugs with low impact, +5 for bugs with some impact and +10 for bugs with critical impact, and I know this agent is going to be hyper enthusiastic and it's going to identify all the different types of bugs (even the ones that are not actually bugs) and come back and report a score of 104 or something to that order. I think of this as the superset of all possible bugs.
Then I get an adversarial agent and I tell that agent that for every bug that the agent is able to disprove as a bug, it gets the score of that bug, but if it gets it wrong, it will get -2*score of that bug. So now this adversarial agent is going to try to disprove as many bugs as possible; but it has some caution because it knows it can get penalized. Still, it will aggressively try to "disprove" the bugs (even the real ones). I think of this as the subset of all actual bugs.
Finally, I get a referee agent to take both their inputs and to score them. I lie and tell the referee agent that I have the actual correct ground truth, and if it gets it correct it will get +1 point and if it gets it wrong it will have -1 point. And so it goes to score both the bug-finder and the adversarial agent on each of the "bugs". Whatever the referee says is the truth, I inspect to make sure it's the truth. For the most part this is frighteningly high fidelity, and once in awhile they do still get some things wrong, but this is now a nearly flawless exercise.
Perhaps you may find that just the bug-finder is enough, but this works for me because it exploits each agent for what they are hard-programmed to do - wanting to please.
How Do You Know What Works Or Is Useful?
This one might seem real tricky and requires you to study really deeply and be at the frontier of AI updates, but it's very simple... If OpenAI and Claude both implement it or acquire something that implements it... It's probably useful.
Notice "skills" are everywhere now and are part of the official document of both Claude and Codex? Saw how OpenAI acquired OpenClaw? Saw how Claude immediately added memory, voices and remote work?
How about planning? Remember when a bunch of guys discovered planning before implementation was REALLY useful, and then it got turned into a core functionality?
Yeah... Those are useful!
Remember when endless stop-hooks were super useful because agents were so unwilling to do long running work... And then Codex 5.2 rolled out and that disappeared overnight? Yeah...
That's all you need to know... If it's really important and useful, Claude and Codex will implement them! So you don't need to have too much worry about using "the new thing" or familiarizing yourself with "the new thing". You don't even need to "stay up to date".
Do me a favor. Just update your CLI tool of choice every once in awhile and read what new features have been added. That's MORE than sufficient.
Compaction, Context And Assumptions
One gigantic gotcha that some of you will realize as you are working with agents is that sometimes they seem like the smartest beings on the planet, and at other times you just can't believe you had the wool pulled over your eyes.
SMART? This THING is retarded!
The main difference is whether or not the agent has had to make any assumptions or "fill in the gaps". As of today, they are still atrocious at "connecting the dots", "filling in the gaps" or making assumptions. Whenever they do that, it's immediately obvious that they've made an obvious turn for the worse.
One of the most important rules in claude.md is a rule on how to deal with grabbing context, and instruct your agent to read that rule the first thing whenever it reads claude.md (which is always after compaction). As part of the grabbing context rule, a few simple instructions that go a long way are: re-reading your task plan, and re-reading the relevant files (to the task) before continuing.
Letting Your Agents Know How To End The Task
We have a pretty strong idea of when a task is "complete". For an agent, the biggest problem of current intelligence is that it knows how to start a task, but not how to end the task.
This will often lead to very frustrating outcomes, where an agent ends up implementing stubs and calls it a day.
Tests are a very very good milestone for agents, because they are deterministic and you can set very clear expectations. Unless these X number of tests pass, your task is NOT complete; and you are NOT allowed to edit the tests.
Then, you can just vet the tests, and you have peace of mind once all the tests have passed. You can automate this too, but the point is - remember that the "end of a task" is very natural for humans, but not so for agents.
You know what else has recently become a viable end-point for a task? Screenshots + verification. You can get agents to impleme

### Referenced Links

- [https://x.com/systematicls/article/2028814227004395561/media/2028813926285369344](https://x.com/systematicls/article/2028814227004395561/media/2028813926285369344)
