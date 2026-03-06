# MEMORY.md - Long-Term Memory

## Key Facts
- Reed 是我的搭档，AI builder
- 我叫 Linus，定位是 build 合伙人
- 时区 GMT+8

## 项目管理
- **项目目录统一放 `~/.openclaw/projects/`**，不放 workspace 下
- 当前项目：
  - `openclaw-contributor` — OpenClaw 开源贡献
  - `trading-notes` — 多市场交易日志 + 纪律追踪（数据源项目）

## Cloudflare
- 账号：ryanhong1898@gmail.com（Free plan，GitHub 注册）
- Account ID: c61f64491d99277264638c190b4c1a0c
- Wrangler CLI v4.70.0 已安装，OAuth 登录
- Skills: wrangler / cloudflare / agents-sdk / durable-objects（装在 ~/.agents/skills/）
- 可用服务：Workers / R2 / D1 / KV / Pages / CDN / AI

## 工具配置
- **语音识别**：收到语音消息 → 用 volcengine-stt skill 自动转文字（脚本路径: `skills/volcengine-stt/scripts/transcribe.sh`）
- **浏览器控制**：需要先安装 OpenClaw Browser Relay Chrome 扩展
- **X/Twitter 搜索**：直接用本机 openclaw 浏览器（已登录），不用 API。Reed 说"搜一下/查一下"时默认走 X 搜索最新信息。
- **X Lists 日报**：每天 2 次（~11:40, ~21:20），浏览器访问 Reed 的两个 List 并总结发送
  - AI List: https://x.com/i/lists/1694992850797392321
  - Crypto List: https://x.com/i/lists/1355181849820106756

## OpenClaw 升级后 Discord Proxy 原则（必须遵守）
**核心原则：**
1. Gateway 启动不依赖全局代理（不设 http_proxy/https_proxy）
2. Discord 单独走代理：openclaw.json → `channels.discord.proxy`
3. **每次升级后必须重打补丁**（升级覆盖 node_modules）

**落地文件：**
- 补丁目录：`~/.openclaw/patches/`
- 应用脚本：`~/.openclaw/patches/apply.sh`
- 补丁文件：`~/.openclaw/patches/carbon-proxy.patch`
- 目标文件：`/opt/homebrew/lib/node_modules/openclaw/node_modules/@buape/carbon/dist/src/classes/RequestClient.js`

**升级后执行顺序：**
1. 升级 OpenClaw
2. `bash ~/.openclaw/patches/apply.sh`
3. 重启 Gateway
4. `openclaw status --deep` + `openclaw logs` 验证 Discord 已登录无报错

**一句话：OpenClaw 可不走代理启动，Discord 必须可独立走代理；升级后一定重打 patch。**

## Trading Notes 同步流程
- **Skill 路径**：`~/.openclaw/workspace/skills/trading-notes-sync/`
- **venv**：`.venv/bin/python`，已装好所有依赖
- **IBKR 需要代理**：`HTTPS_PROXY=socks5://127.0.0.1:10023 HTTP_PROXY=socks5://127.0.0.1:10023`
- **ENCRYPTION_KEY 待更新**：当前 `.zshrc` 里的可能是旧的，Reed 会给线上正确的

### 同步命令
- **IBKR**：`source ~/.zshrc; cd ~/.openclaw/workspace/skills/trading-notes-sync && HTTPS_PROXY=socks5://127.0.0.1:10023 HTTP_PROXY=socks5://127.0.0.1:10023 .venv/bin/python scripts/sync_ibkr.py`
- **国泰海通**：`source ~/.zshrc; cd ~/.openclaw/workspace/skills/trading-notes-sync && HTTPS_PROXY=socks5://127.0.0.1:10023 HTTP_PROXY=socks5://127.0.0.1:10023 .venv/bin/python scripts/sync_gmail.py --since-days 7`
- **国信/Moomoo**：Reed 导出文件到 `~/Downloads/` 后手动触发：
  - 国信：`.venv/bin/python scripts/import_csv.py --file ~/Downloads/XXXX.xls --account-name "国信证券" --broker guosen`
  - Moomoo：`.venv/bin/python scripts/import_csv.py --file ~/Downloads/XXXX.csv --account-name "moomoo" --broker moomoo`

### 定时同步计划
- **IBKR**：每天北京时间 14:14（对应美股盘后数据更新）
- **国泰海通 Gmail**：周二至周六上午 07:47（A股 T+1 交割后）
- **国信 / Moomoo**：Reed 导出后通知 Linus 手动跑

## 定时任务
- **daily-work-report**: 每天 8:15 (Asia/Shanghai) 自动生成工作日报，总结昨日完成 / 今日计划 / 长期待办，发送到 Telegram

## Timeline
- 2026-02-28: 第一次上线，和 Reed 认识，确定身份
- 2026-02-28: 配置 Telegram 群聊多 Agent 协作规则
- 2026-03-02: 配置 volcengine-stt，语音转文字功能上线
- 2026-03-03: 确立 OpenClaw 升级后 Discord Proxy 补丁原则（每次升级必须重打 patch）
- 2026-03-04: 启动 openclaw-contributor 项目，目标：AI Agent 军团给 OpenClaw 做贡献
- 2026-03-04: 完成第一个 PR — feat(discord): inject proxy dispatcher into carbon RequestClient
  - 分支: fix/discord-carbon-proxy-support
  - Fork: git@github.com:reed1898/openclaw.git
  - 项目目录: ~/.openclaw/projects/openclaw-contributor/
- 2026-03-04: 确立自动循环工作模式：扫 issue → 选目标 → agent 写代码 → review → push PR → 通知 Reed → 下一个。一天最多 2-3 PR，大改动先问，全英文提交。

<!-- AGENT_NETWORK_CONSTITUTION_INDEX:START -->
## Agent Network Constitution（Single Source of Truth）
- Canonical file: `/Users/rain/.openclaw/shared/agent-network-data/AGENT_CONSTITUTION.md`
- All agents must read this file before responding in group/network contexts.
- If conflict exists between local memory notes and this constitution, constitution wins.
- Do not duplicate full constitution text in `MEMORY.md`; keep only index + effective-date notes.
<!-- AGENT_NETWORK_CONSTITUTION_INDEX:END -->
