# Heinrich

> **Author**: Heinrich
> **Source**: https://x.com/arscontexta/status/2013045749580259680
> **Date**: 2026-02-16 00:52
> **Replies**: 79 · **Retweets**: 246 · **Likes**: 2494 · **Views**: 1200164

---

## TLDR

**TLDR** — Heinrich分享了他如何使用Claude Code和Markdown文件构建一个基于AI的思考操作系统，强调知识库与代码库的相似性，并介绍了他的“Vault”系统，一个用于组织和导航知识的框架。

**Key Points**
- **AI作为思考伙伴**：Claude Code帮助提取关键概念，连接已有知识，并构建动态的思维表示。
- **Vault系统**：通过Markdown文件链接构建知识库，每个文件都是独立且可组合的“知识块”。
- **知识库与代码库的相似性**：两者都是文本文件集合，有结构和模式，并受益于能够导航和操作的代理。
- **哲学与结构**：每个Vault需要根据自己的目的和哲学来构建，类似于代码库的设计。
- **深度与广度**：Heinrich强调深度比广度更重要，质量比速度更重要。
- **文件结构**：Heinrich提供了一个详细的文件结构示例，包括捕获区、思考区、参考资料、创作区等。
- **链接的重要性**：Heinrich建议将链接融入句子中，而不是作为脚注，使链接成为思考的一部分。
- **AI的运作**：Claude通过扫描结构、索引和主题页面来导航，并记录导航中的发现。
- **人类角色**：从创作者转变为编辑和 curator，指导系统进行笔记，并做出判断。

**Process / Steps**
- 创建一个Vault，包括子文件夹以匹配你的目的。
- 编写Claude.md文件来解释你的系统。
- 使用Claude来操作Vault，捕获内容并寻找联系。
- 定期审查和编辑系统输出，确保质量。

**Fact Check**
- **AI作为思考伙伴**：**部分可验证**。AI可以辅助思考，但其效果取决于系统的设计和用户的使用。
- **Vault系统**：**可验证**。Markdown文件和链接结构是可验证的。
- **知识库与代码库的相似性**：**可验证**。两者都是文本文件集合，有结构和模式。
- **哲学与结构**：**意见**。这取决于个人的观点和目的。
- **深度与广度**：**意见**。这取决于个人的目标和价值观。
- **文件结构**：**可验证**。文件结构是可验证的。
- **链接的重要性**：**可验证**。链接在Markdown文件中的使用是可验证的。
- **AI的运作**：**部分可验证**。AI的运作方式取决于系统的设计和数据。
- **人类角色**：**意见**。人类角色的变化取决于个人的观点。

Credibility: 7/10 — 虽然Heinrich的方法和观点是可验证的，但它们也包含个人意见和哲学观点。

---

## Original Content

Heinrich@arscontextaobsidian + claude code 101ive spent the last year building an operating system for thinking with ai. claude code runs my obsidian vaultsit extracts the key concepts, connects them to what you already figured out, and builds a living representation of your thinkingi find myself only working in the vault nowthe markdown files know everything ive discovered, nicely structured and with automatic situational context injection for in-context learningi use a vault index that helps the agent decide what notes to pull in, same pattern as how claude code decides which skills to load(if you think about it, every note is basically a skill in some sense... highly curated knowledge that gets injected when relevant)the deeper thing is that a vault encodes how you think, not just what you thought about. the methodology becomes part of the system

its all just markdown files, you own it completely. this is ai as thinking partner, not as a writing assistantknowledge = code?i realized: knowledge bases and codebases have a lot in commontheyre both folders of text files with relationships between them, they both have conventions and patterns, and they both benefit from agents that can navigate and operate themvibe coding changed how we write software by letting ai handle implementation while you focus on direction, and the same shift applies to knowledge workyou dont take notes anymore. you operate a system that takes noteswhat is a vault?a vault is a folder of markdown files that link to each other:markdown
my-vault/
├── 00_inbox/           # capture zone, zero friction
├── 01_thinking/        # your notes and synthesis
│   └── notes/          # individual thinking notes
├── 02_reference/       # external knowledge
│   ├── tools/          # tool documentation
│   ├── approaches/     # methods and patterns
│   └── sources/        # external knowledge
├── 03_creating/        # content in progress
│   └── drafts/
├── 04_published/       # finished work archive
├── 05_archive/         # inactive content
├── 06_system/          # templates and scripts
├── CLAUDE.md           # teaches the ai your system
└── attachments/        # images and files
files connect using [[wiki links]] which build a network of ideaswhen you write [[quality is the hard part]] in one note, it creates a clickable link to another note with that titlethe agent can follow these links to jump between related ideas, discovering connections you forgot existedhow to write good noteshow you write those links mattersmost people put references at the bottom like footnotes. instead, weave links into your sentencesdont write "this relates to quality, see: quality-note". write "because [[quality is the hard part]] we need to focus on curation"the link becomes part of your thought, and the agent can follow your reasoning by following the linksalso write notes that stand alone and are composableif someone lands on a note from a link, they shouldnt need to read five other notes first to understand itthink of notes like lego blockseach one is complete on its own, but they connect to build bigger structureswhen your notes work this way, the network itself becomes valuablethe thing is, ai doesnt automatically understand your philosophy. you have to teach itwatching an ai completely disrespect my philosophies taught me this the hard waywhen you need to teach claude how you think, you realize how much implicit knowledge you carry around. suddenly you have to textualize everythingmy claudemd is around 2000 lines now because i keep refining what works and what doesntevery vault needs its own philosophyheres what most guides get wrong. they give you a system and say follow this but every vault serves a different purpose and needs different principlessame as codebases reallyyou wouldnt use the same folder structure for a cli tool and a web appi run multiple vaults. one is for thinking about ai and knowledge management, which is the example ill shareanother is for work, which tracks projects and clients with completely different rules. the philosophy changes based on purposesame underlying pattern, different rules. the pattern is:markdown files with links that any ai can reada CLAUDE.md file that teaches the agent your specific systemstructure that lets the agent orient quicklyconventions written as instructions so the ai stays consistentwhat goes in those instructions depends entirely on your purposewhat this could bea work vault might emphasize:capture first, structure laterproject folders with meetings and outputsclient context for ai consumptiona research vault might emphasize:source tracking and citationsliterature notesclaim verificationa creative vault might emphasize:idea capture and incubationdraft progressionreference organizationthe thinking vault examplethe vault im sharing focuses on developing understanding. the philosophy comes from the claude md file:i can feel the difference when the vault is well maintained versus full of noise. depth matters more than breadthhere is a snippet from the claude md to emphasize on this:markdowndepth over breadth. quality over speed. tokens are free.

this is not about efficiency. this is about excellence. when you pick a task, you are committing to understanding it completely and leaving behind work that future agents can build on.how claude finds thingswhen claude starts a session it needs to understand what exists without reading every filethats impossible with thousands of notes. so my system has layers that let the agent orient quickly:json"hooks": {
    "SessionStart": [{
        "hooks": [{
            "type": "command",
            "command": "tree -L 3 -a -I '.git|.obsidian' --noreport"
        }]
    }]
}claude sees the folder structure. a hook automatically shows what folders and files exist at session startan index file that lists every note with a one sentence description. claude can scan 50 notes in seconds without opening themtopic pages (MOCs) that link to related notes these act like tables of contents for each subjectthey also contain notes that claude leaves for itself about what it learned while traversing the graph, leaving breadcrumbs for future sessionsthe ai starts broad, narrows to whats relevant, then follows links to build understandingcore principlesthese are the rules that work for my thinking vault. other vault types might need different ones:can this note be linked from elsewhere and still make sense? if linking to it forces you to explain three other things first, split it up. thats composabilityi stopped naming notes like topics and started naming them like claims. instead of "thoughts on ai slop" you write "quality is the hard part". when you link to it, the title becomes part of your sentence naturally (this also forces claude to think differently when building sentences, which i believe is beneficial because it requires understanding)insight that individual notes matter less than their relationships. a note with many incoming links is more valuable than an isolated note because every link creates a new reading path. the network is the knowledgehow the agent operatesevery task starts with orientation. claude scans the structure, checks the index for relevant notes, reads the topic page before making changesit follows links to build understanding and makes no changes without contextwhen claude discovers something useful about navigating a topic, it records that in the topic pagefuture sessions read those notes and learn from past navigation. this is how the vault remembers how to think through itselfsometimes two notes interact in interesting ways. claude creates a new note capturing the insight that emerges from combining themevery new capture triggers a search for related notes. claude adds links with contextfolder architecturemarkdownvault/
├── 00_inbox/           # capture zone
├── 01_thinking/        # your notes and topic pages
│   ├── knowledge-work.md    # example topic page
│   └── notes/               # individual notes
├── 02_reference/       # stuff from others
├── 03_creating/        # drafts in progress
├── 04_published/       # finished work
├── 05_archive/         # old stuff
└── 06_system/          # templates and configthis structure works for a personal thinking vault. a work vault might have projects and clientsthe point isnt the specific folders but that folder location tells you what something ismarkdown is the system. tools like obsidian are just windows into it. the vault could survive any app disappearingeverything is plain text that any editor can read and any ai can process. you own your data completelyhow to startcreate a folder with subfolders that match your purpose. think about what you actually need to organizewrite a claude md that explains your system. start simple and evolve it as you learn what workslet claude operate. capture something and ask claude to find connections. let it navigate and discover relationships and suggest where things belongALWAYS review what it produces and edit for qualityyoure not taking notes anymore but directing a system that takes notes. your job becomes judgment, which means deciding what mattersthe human role evolves from writer to editor and from creator to curatortldrvibe coding changed how we write software. vibe note taking changes how we thinka vault is just markdown files that link to each otherllms have no memory, so vaults give them oneclaude md teaches the ai how your system worksevery vault needs its own philosophy based on purposewhat stays constant: markdown, links, ai operates while you provide judgmentif you want to see how this evolves, follow along. im open sourcing my notes soonheinrich8:28 AM · Jan 19, 2026·1.2M ViewsRelevantView quotes
