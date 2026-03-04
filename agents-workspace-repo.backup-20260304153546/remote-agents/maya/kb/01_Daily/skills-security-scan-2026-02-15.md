今晚结论摘要（<=10行）
- 扫描 skills 数：92（high=1 / medium=7 / low=84）
- ⚠️ 发现 HIGH 风险：需要尽快人工复核相关 skill（重点看 eval/提权/SSH 相关命中）
- 说明：本次为静态审计/grep 抽样；命中不等于恶意，但建议对新增/近期变更的 skill 做人工代码审阅
- 报告已写入：/home/ubuntu/.openclaw/kb/01_Daily/skills-security-scan-2026-02-15.md

---

# Nightly Skills Security Scan (2026-02-15)

扫描范围：
- /home/ubuntu/.openclaw/workspace/skills
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills
- /home/ubuntu/.openclaw/skills

## 1password

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/1password
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/1password/SKILL.md:4:homepage: https://developer.1password.com/docs/cli/get-started/
```

## apple-notes

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/apple-notes
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/apple-notes/SKILL.md:4:homepage: https://github.com/antoniorodr/memo
```

## apple-reminders

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/apple-reminders
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/apple-reminders/SKILL.md:4:homepage: https://github.com/steipete/remindctl
```

## bear-notes

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/bear-notes
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：读取环境变量/密钥线索
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/bear-notes/SKILL.md:40:2. Save it: `echo "YOUR_TOKEN" > ~/.config/grizzly/token`
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/bear-notes/SKILL.md:90:2. Environment variables (`GRIZZLY_TOKEN_FILE`, `GRIZZLY_CALLBACK_URL`, `GRIZZLY_TIMEOUT`)
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/bear-notes/SKILL.md:98:callback_url = "http://127.0.0.1:42123/success"
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/bear-notes/SKILL.md:4:homepage: https://bear.app
```

## blogwatcher

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/blogwatcher
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/blogwatcher/SKILL.md:4:homepage: https://github.com/Hyaxia/blogwatcher
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/blogwatcher/SKILL.md:39:- Add a blog: `blogwatcher add "My Blog" https://example.com`
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/blogwatcher/SKILL.md:54:    URL: https://xkcd.com
```

## blucli

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/blucli
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/blucli/SKILL.md:4:homepage: https://blucli.sh
```

## bluebubbles

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/bluebubbles
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中：无

## camsnap

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/camsnap
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/camsnap/SKILL.md:4:homepage: https://camsnap.ai
```

## canvas

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/canvas
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：网络请求/下载(curl/wget/fetch/axios)
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/canvas/SKILL.md:161:3. Test URL directly: `curl http://<hostname>:18793/__openclaw__/canvas/<file>.html`
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/canvas/SKILL.md:43:http://<tailscale-hostname>:18793/__openclaw__/canvas/<file>.html
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/canvas/SKILL.md:114:- **loopback**: `http://127.0.0.1:18793/__openclaw__/canvas/<file>.html`
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/canvas/SKILL.md:115:- **lan/tailnet/auto**: `http://<hostname>:18793/__openclaw__/canvas/<file>.html`
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/canvas/SKILL.md:140:canvas action:present node:mac-63599bc4-b54d-4392-9048-b97abd58343a target:http://peters-mac-studio-1.sheep-coho.ts.net:18793/__openclaw__/canvas/snake.html
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/canvas/SKILL.md:161:3. Test URL directly: `curl http://<hostname>:18793/__openclaw__/canvas/<file>.html`
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/canvas/SKILL.md:186:http://<host>:18793/__openclaw__/canvas/index.html  → ~/clawd/canvas/index.html
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/canvas/SKILL.md:187:http://<host>:18793/__openclaw__/canvas/games/snake.html → ~/clawd/canvas/games/snake.html
```

## clawhub

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/clawhub
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/clawhub/SKILL.md:75:- Default registry: https://clawhub.com (override with CLAWHUB_REGISTRY or --registry)
```

## coding-agent

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/coding-agent
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/coding-agent/SKILL.md:129:git clone https://github.com/user/repo.git $REVIEW_DIR
```

## discord

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/discord
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/discord/SKILL.md:16:- For fetchMessage: `guildId`, `channelId`, `messageId`, or a `messageLink` like `https://discord.com/channels/<guildId>/<channelId>/<messageId>`.
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/discord/SKILL.md:19:- For media: `mediaUrl` with `file:///path` for local files or `https://...` for remote.
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/discord/SKILL.md:26:**Note:** `fetchMessage` accepts message IDs or full links like `https://discord.com/channels/<guildId>/<channelId>/<messageId>`.
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/discord/SKILL.md:168:  "messageLink": "https://discord.com/channels/999/123/456"
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/discord/SKILL.md:194:- `mediaUrl` supports local files (`file:///path/to/file`) and remote URLs (`https://...`)
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/discord/SKILL.md:480:  "activityUrl": "https://twitch.tv/example"
```

## eightctl

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/eightctl
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/eightctl/SKILL.md:4:homepage: https://eightctl.sh
```

## food-order

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/food-order
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/food-order/SKILL.md:4:homepage: https://ordercli.sh
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/food-order/SKILL.md:22:- Login (no password, preferred): `ordercli foodora session chrome --url https://www.foodora.at/ --profile "Default"`
```

## gemini

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/gemini
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/gemini/SKILL.md:4:homepage: https://ai.google.dev/
```

## gifgrep

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/gifgrep
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/gifgrep/SKILL.md:4:homepage: https://gifgrep.com
```

## github

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/github
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中：无

## gog

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/gog
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/gog/SKILL.md:4:homepage: https://gogcli.sh
```

## goplaces

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/goplaces
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：读取环境变量/密钥线索
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/goplaces/SKILL.md:43:- Pagination: `goplaces search "pizza" --page-token "NEXT_PAGE_TOKEN"`
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/goplaces/SKILL.md:4:homepage: https://github.com/steipete/goplaces
```

## healthcheck

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/healthcheck
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中：无

## himalaya

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/himalaya
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/himalaya/SKILL.md:4:homepage: https://github.com/pimalaya/himalaya
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/himalaya/references/configuration.md:157:backend.auth.auth-url = "https://provider.com/oauth/authorize"
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/himalaya/references/configuration.md:158:backend.auth.token-url = "https://provider.com/oauth/token"
```

## imsg

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/imsg
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/imsg/SKILL.md:4:homepage: https://imsg.to
```

## local-places

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:20 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：网络请求/下载(curl/wget/fetch/axios)
- 脚本文件(节选)：
  - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/src/local_places/schemas.py
  - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/src/local_places/google_places.py
  - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/src/local_places/main.py
  - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/src/local_places/__init__.py
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SKILL.md:35:1. **Check server:** `curl http://127.0.0.1:8000/ping`
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SKILL.md:40:curl -X POST http://127.0.0.1:8000/locations/resolve \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SKILL.md:48:curl -X POST http://127.0.0.1:8000/places/search \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SKILL.md:61:curl http://127.0.0.1:8000/places/{place_id}
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SERVER_README.md:59:curl -X POST http://127.0.0.1:8000/places/search \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SERVER_README.md:81:curl -X POST http://127.0.0.1:8000/locations/resolve \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SKILL.md:35:1. **Check server:** `curl http://127.0.0.1:8000/ping`
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SKILL.md:40:curl -X POST http://127.0.0.1:8000/locations/resolve \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SKILL.md:48:curl -X POST http://127.0.0.1:8000/places/search \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SKILL.md:61:curl http://127.0.0.1:8000/places/{place_id}
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/src/local_places/main.py:20:    servers=[{"url": os.getenv("OPENAPI_SERVER_URL", "http://maxims-macbook-air:8000")}],
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SERVER_README.md:21:Open the API docs at http://127.0.0.1:8000/docs.
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SERVER_README.md:59:curl -X POST http://127.0.0.1:8000/places/search \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SERVER_README.md:81:curl -X POST http://127.0.0.1:8000/locations/resolve \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SKILL.md:4:homepage: https://github.com/Hyaxia/local_places
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/src/local_places/google_places.py:22:    "GOOGLE_PLACES_BASE_URL", "https://places.googleapis.com/v1"
```

## mcporter

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/mcporter
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/mcporter/SKILL.md:4:homepage: http://mcporter.dev
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/mcporter/SKILL.md:39:- Full URL: `mcporter call https://api.example.com/mcp.fetch url:https://example.com`
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/mcporter/SKILL.md:40:- Stdio: `mcporter call --stdio "bun run ./server.ts" scrape url=https://example.com`
```

## model-usage

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/model-usage
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:20 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 脚本文件(节选)：
  - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/model-usage/scripts/model_usage.py
- 高风险关键字命中：无

## nano-banana-pro

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/nano-banana-pro
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:20 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 可执行文件(节选)：
  - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/nano-banana-pro/scripts/generate_image.py
- 脚本文件(节选)：
  - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/nano-banana-pro/scripts/generate_image.py
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/nano-banana-pro/SKILL.md:4:homepage: https://ai.google.dev/
```

## nano-pdf

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/nano-pdf
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/nano-pdf/SKILL.md:4:homepage: https://pypi.org/project/nano-pdf/
```

## notion

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：网络请求/下载(curl/wget/fetch/axios)
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:35:curl -X GET "https://api.notion.com/v1/..." \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:48:curl -X POST "https://api.notion.com/v1/search" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:58:curl "https://api.notion.com/v1/pages/{page_id}" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:66:curl "https://api.notion.com/v1/blocks/{page_id}/children" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:74:curl -X POST "https://api.notion.com/v1/pages" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:90:curl -X POST "https://api.notion.com/v1/data_sources/{data_source_id}/query" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:103:curl -X POST "https://api.notion.com/v1/data_sources" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:121:curl -X PATCH "https://api.notion.com/v1/pages/{page_id}" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:131:curl -X PATCH "https://api.notion.com/v1/blocks/{page_id}/children" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:4:homepage: https://developers.notion.com
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:18:1. Create an integration at https://notion.so/my-integrations
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:35:curl -X GET "https://api.notion.com/v1/..." \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:48:curl -X POST "https://api.notion.com/v1/search" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:58:curl "https://api.notion.com/v1/pages/{page_id}" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:66:curl "https://api.notion.com/v1/blocks/{page_id}/children" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:74:curl -X POST "https://api.notion.com/v1/pages" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:90:curl -X POST "https://api.notion.com/v1/data_sources/{data_source_id}/query" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:103:curl -X POST "https://api.notion.com/v1/data_sources" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:121:curl -X PATCH "https://api.notion.com/v1/pages/{page_id}" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:131:curl -X PATCH "https://api.notion.com/v1/blocks/{page_id}/children" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:153:- **URL:** `{"url": "https://..."}`
```

## obsidian

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/obsidian
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/obsidian/SKILL.md:4:homepage: https://help.obsidian.md
```

## openai-image-gen

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-image-gen
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:20 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：读取环境变量/密钥线索
- 脚本文件(节选)：
  - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-image-gen/scripts/gen.py
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-image-gen/SKILL.md:10:        "requires": { "bins": ["python3"], "env": ["OPENAI_API_KEY"] },
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-image-gen/SKILL.md:11:        "primaryEnv": "OPENAI_API_KEY",
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-image-gen/scripts/gen.py:176:    api_key = (os.environ.get("OPENAI_API_KEY") or "").strip()
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-image-gen/scripts/gen.py:178:        print("Missing OPENAI_API_KEY", file=sys.stderr)
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-image-gen/SKILL.md:4:homepage: https://platform.openai.com/docs/api-reference/images
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-image-gen/scripts/gen.py:87:    url = "https://api.openai.com/v1/images/generations"
```

## openai-whisper

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper/SKILL.md:4:homepage: https://openai.com/research/whisper
```

## openai-whisper-api

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:20 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：网络请求/下载(curl/wget/fetch/axios) 读取环境变量/密钥线索
- 脚本文件(节选)：
  - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/scripts/transcribe.sh
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/scripts/transcribe.sh:75:curl -sS https://api.openai.com/v1/audio/transcriptions \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/SKILL.md:10:        "requires": { "bins": ["curl"], "env": ["OPENAI_API_KEY"] },
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/SKILL.md:11:        "primaryEnv": "OPENAI_API_KEY",
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/SKILL.md:42:Set `OPENAI_API_KEY`, or configure it in `~/.openclaw/openclaw.json`:
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/scripts/transcribe.sh:59:if [[ "${OPENAI_API_KEY:-}" == "" ]]; then
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/scripts/transcribe.sh:60:  echo "Missing OPENAI_API_KEY" >&2
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/scripts/transcribe.sh:76:  -H "Authorization: Bearer $OPENAI_API_KEY" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/SKILL.md:4:homepage: https://platform.openai.com/docs/guides/speech-to-text
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/scripts/transcribe.sh:75:curl -sS https://api.openai.com/v1/audio/transcriptions \
```

## openhue

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openhue
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openhue/SKILL.md:4:homepage: https://www.openhue.io/cli
```

## oracle

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/oracle
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：读取环境变量/密钥线索
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/oracle/SKILL.md:86:- Auto-pick: `api` when `OPENAI_API_KEY` is set; otherwise `browser`.
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/oracle/SKILL.md:4:homepage: https://askoracle.dev
```

## ordercli

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/ordercli
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：读取环境变量/密钥线索
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/ordercli/SKILL.md:71:- Requires `DELIVEROO_BEARER_TOKEN` (optional `DELIVEROO_COOKIE`).
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/ordercli/SKILL.md:4:homepage: https://ordercli.sh
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/ordercli/SKILL.md:66:- `ordercli foodora session chrome --url https://www.foodora.at/ --profile "Default"`
```

## peekaboo

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/peekaboo
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/peekaboo/SKILL.md:4:homepage: https://peekaboo.boo
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/peekaboo/SKILL.md:154:peekaboo app launch "Safari" --open https://example.com
```

## sag

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sag
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sag/SKILL.md:4:homepage: https://sag.sh
```

## session-logs

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/session-logs
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中：无

## sherpa-onnx-tts

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**medium**
- 理由：执行外部命令(child_process/exec/spawn) 读取环境变量/密钥线索
- 可执行文件(节选)：
  - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts:5:const { spawnSync } = require("node:child_process");
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts:5:const { spawnSync } = require("node:child_process");
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts:157:const child = spawnSync(
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts:19:  const value = explicit || process.env.SHERPA_ONNX_RUNTIME_DIR || "";
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts:24:  const value = explicit || process.env.SHERPA_ONNX_MODEL_DIR || "";
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts:29:  const explicit = (explicitFlag || process.env.SHERPA_ONNX_MODEL_FILE || "").trim();
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts:44:  const explicit = (explicitFlag || process.env.SHERPA_ONNX_TOKENS_FILE || "").trim();
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts:51:  const explicit = (explicitFlag || process.env.SHERPA_ONNX_DATA_DIR || "").trim();
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts:144:const env = { ...process.env };
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts:44:  const explicit = (explicitFlag || process.env.SHERPA_ONNX_TOKENS_FILE || "").trim();
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts:130:    "Model directory is missing required files. Set SHERPA_ONNX_MODEL_FILE, SHERPA_ONNX_TOKENS_FILE, SHERPA_ONNX_DATA_DIR or pass --model-file/--tokens-file/--data-dir.",
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/SKILL.md:17:              "url": "https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.12.23/sherpa-onnx-v1.12.23-osx-universal2-shared.tar.bz2",
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/SKILL.md:28:              "url": "https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.12.23/sherpa-onnx-v1.12.23-linux-x64-shared.tar.bz2",
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/SKILL.md:39:              "url": "https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.12.23/sherpa-onnx-v1.12.23-win-x64-shared.tar.bz2",
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/SKILL.md:49:              "url": "https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-en_US-lessac-high.tar.bz2",
```

## skill-creator

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/skill-creator
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-13 05:55:29 UTC（约 2 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 脚本文件(节选)：
  - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/skill-creator/scripts/quick_validate.py
  - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/skill-creator/scripts/init_skill.py
  - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/skill-creator/license.txt:4:                        http://www.apache.org/licenses/
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/skill-creator/license.txt:196:       http://www.apache.org/licenses/LICENSE-2.0
```

## slack

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/slack
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中：无

## songsee

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/songsee
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/songsee/SKILL.md:4:homepage: https://github.com/steipete/songsee
```

## sonoscli

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sonoscli
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：读取环境变量/密钥线索
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sonoscli/SKILL.md:46:- Spotify Web API search is optional and requires `SPOTIFY_CLIENT_ID/SECRET`.
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sonoscli/SKILL.md:4:homepage: https://sonoscli.sh
```

## spotify-player

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/spotify-player
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/spotify-player/SKILL.md:4:homepage: https://www.spotify.com
```

## summarize

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/summarize
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：读取环境变量/密钥线索
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/summarize/SKILL.md:60:- OpenAI: `OPENAI_API_KEY`
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/summarize/SKILL.md:74:- `--youtube auto` (Apify fallback if `APIFY_API_TOKEN` set)
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/summarize/SKILL.md:87:- `APIFY_API_TOKEN` for YouTube fallback
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/summarize/SKILL.md:4:homepage: https://summarize.sh
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/summarize/SKILL.md:41:summarize "https://example.com" --model google/gemini-3-flash-preview
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/summarize/SKILL.md:43:summarize "https://youtu.be/dQw4w9WgXcQ" --youtube auto
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/summarize/SKILL.md:51:summarize "https://youtu.be/dQw4w9WgXcQ" --youtube auto --extract-only
```

## things-mac

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/things-mac
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：读取环境变量/密钥线索
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/things-mac/SKILL.md:35:- Optional: set `THINGS_AUTH_TOKEN` to avoid passing `--auth-token` for update ops.
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/things-mac/SKILL.md:69:- Auth: set `THINGS_AUTH_TOKEN` or pass `--auth-token <TOKEN>`
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/things-mac/SKILL.md:70:- Title: `things update --id <UUID> --auth-token <TOKEN> "New title"`
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/things-mac/SKILL.md:71:- Notes replace: `things update --id <UUID> --auth-token <TOKEN> --notes "New notes"`
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/things-mac/SKILL.md:72:- Notes append/prepend: `things update --id <UUID> --auth-token <TOKEN> --append-notes "..."` / `--prepend-notes "..."`
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/things-mac/SKILL.md:73:- Move lists: `things update --id <UUID> --auth-token <TOKEN> --list "Travel" --heading "Before"`
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/things-mac/SKILL.md:74:- Tags replace/add: `things update --id <UUID> --auth-token <TOKEN> --tags "a,b"` / `things update --id <UUID> --auth-token <TOKEN> --add-tags "a,b"`
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/things-mac/SKILL.md:75:- Complete/cancel (soft-delete-ish): `things update --id <UUID> --auth-token <TOKEN> --completed` / `--canceled`
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/things-mac/SKILL.md:76:- Safe preview: `things --dry-run update --id <UUID> --auth-token <TOKEN> --completed`
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/things-mac/SKILL.md:4:homepage: https://github.com/ossianhempel/things3-cli
```

## tmux

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/tmux
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:20 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 可执行文件(节选)：
  - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/tmux/scripts/find-sessions.sh
  - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/tmux/scripts/wait-for-text.sh
- 脚本文件(节选)：
  - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/tmux/scripts/find-sessions.sh
  - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/tmux/scripts/wait-for-text.sh
- 高风险关键字命中：无

## trello

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：网络请求/下载(curl/wget/fetch/axios) 读取环境变量/密钥线索
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:28:All commands use curl to hit the Trello REST API.
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:33:curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id}'
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:39:curl -s "https://api.trello.com/1/boards/{boardId}/lists?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id}'
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:45:curl -s "https://api.trello.com/1/lists/{listId}/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id, desc}'
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:51:curl -s -X POST "https://api.trello.com/1/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:60:curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:67:curl -s -X POST "https://api.trello.com/1/cards/{cardId}/actions/comments?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:74:curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:88:curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=name,id" | jq
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:91:curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | select(.name | contains("Work"))'
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:94:curl -s "https://api.trello.com/1/boards/{boardId}/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, list: .idList}'
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:8:      { "emoji": "📋", "requires": { "bins": ["jq"], "env": ["TRELLO_API_KEY", "TRELLO_TOKEN"] } },
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:23:   export TRELLO_TOKEN="your-token"
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:33:curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id}'
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:39:curl -s "https://api.trello.com/1/boards/{boardId}/lists?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id}'
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:45:curl -s "https://api.trello.com/1/lists/{listId}/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id, desc}'
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:51:curl -s -X POST "https://api.trello.com/1/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:60:curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:67:curl -s -X POST "https://api.trello.com/1/cards/{cardId}/actions/comments?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:74:curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:88:curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=name,id" | jq
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:91:curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | select(.name | contains("Work"))'
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:94:curl -s "https://api.trello.com/1/boards/{boardId}/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, list: .idList}'
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:4:homepage: https://developer.atlassian.com/cloud/trello/rest/
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:18:1. Get your API key: https://trello.com/app-key
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:33:curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id}'
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:39:curl -s "https://api.trello.com/1/boards/{boardId}/lists?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id}'
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:45:curl -s "https://api.trello.com/1/lists/{listId}/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id, desc}'
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:51:curl -s -X POST "https://api.trello.com/1/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:60:curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:67:curl -s -X POST "https://api.trello.com/1/cards/{cardId}/actions/comments?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:74:curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:88:curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=name,id" | jq
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:91:curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | select(.name | contains("Work"))'
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:94:curl -s "https://api.trello.com/1/boards/{boardId}/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, list: .idList}'
```

## video-frames

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/video-frames
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:20 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 脚本文件(节选)：
  - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/video-frames/scripts/frame.sh
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/video-frames/SKILL.md:4:homepage: https://ffmpeg.org
```

## voice-call

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/voice-call
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中：无

## wacli

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/wacli
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/wacli/SKILL.md:4:homepage: https://wacli.sh
```

## weather

- 路径：/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/weather
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-07 10:10:19 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：网络请求/下载(curl/wget/fetch/axios)
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/weather/SKILL.md:17:curl -s "wttr.in/London?format=3"
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/weather/SKILL.md:24:curl -s "wttr.in/London?format=%l:+%c+%t+%h+%w"
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/weather/SKILL.md:31:curl -s "wttr.in/London?T"
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/weather/SKILL.md:42:- PNG: `curl -s "wttr.in/Berlin.png" -o /tmp/weather.png`
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/weather/SKILL.md:49:curl -s "https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true"
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/weather/SKILL.md:4:homepage: https://wttr.in/:help
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/weather/SKILL.md:49:curl -s "https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true"
/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/weather/SKILL.md:54:Docs: https://open-meteo.com/en/docs
```

## clawra-selfie

- 路径：/home/ubuntu/.openclaw/skills/clawra-selfie
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-11 17:10:45 UTC（约 3 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**medium**
- 理由：执行外部命令(child_process/exec/spawn) 网络请求/下载(curl/wget/fetch/axios) 读取环境变量/密钥线索
- 可执行文件(节选)：
  - /home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.sh
- 脚本文件(节选)：
  - /home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.ts
  - /home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.sh
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/skills/clawra-selfie/SKILL.md:240:import { exec } from "child_process";
/home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.ts:16:import { exec } from "child_process";
/home/ubuntu/.openclaw/skills/clawra-selfie/SKILL.md:107:curl -X POST "https://fal.run/xai/grok-imagine-image/edit" \
/home/ubuntu/.openclaw/skills/clawra-selfie/SKILL.md:142:curl -X POST "http://localhost:18789/message" \
/home/ubuntu/.openclaw/skills/clawra-selfie/SKILL.md:209:RESPONSE=$(curl -s -X POST "https://fal.run/xai/grok-imagine-image/edit" \
/home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.sh:82:RESPONSE=$(curl -s -X POST "https://fal.run/xai/grok-imagine-image" \
/home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.sh:137:    curl -s -X POST "$GATEWAY_URL/message" \
/home/ubuntu/.openclaw/skills/clawra-selfie/SKILL.md:283:    credentials: process.env.FAL_KEY!
/home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.ts:99:  const falKey = process.env.FAL_KEY;
/home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.ts:162:    process.env.OPENCLAW_GATEWAY_URL || "http://localhost:18789";
/home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.ts:163:  const gatewayToken = process.env.OPENCLAW_GATEWAY_TOKEN;
/home/ubuntu/.openclaw/skills/clawra-selfie/SKILL.md:33:OPENCLAW_GATEWAY_TOKEN=your_token  # From: openclaw doctor --generate-gateway-token
/home/ubuntu/.openclaw/skills/clawra-selfie/SKILL.md:143:  -H "Authorization: Bearer $OPENCLAW_GATEWAY_TOKEN" \
/home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.ts:13: *   OPENCLAW_GATEWAY_TOKEN - Gateway auth token (optional)
/home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.ts:163:  const gatewayToken = process.env.OPENCLAW_GATEWAY_TOKEN;
/home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.sh:130:    GATEWAY_TOKEN="${OPENCLAW_GATEWAY_TOKEN:-}"
/home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.sh:133:    if [ -n "$GATEWAY_TOKEN" ]; then
/home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.sh:134:        HEADERS="$HEADERS -H \"Authorization: Bearer $GATEWAY_TOKEN\""
/home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.sh:139:        ${GATEWAY_TOKEN:+-H "Authorization: Bearer $GATEWAY_TOKEN"} \
/home/ubuntu/.openclaw/skills/clawra-selfie/SKILL.md:142:curl -X POST "http://localhost:18789/message" \
/home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.ts:12: *   OPENCLAW_GATEWAY_URL - OpenClaw gateway URL (default: http://localhost:18789)
/home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.ts:162:    process.env.OPENCLAW_GATEWAY_URL || "http://localhost:18789";
/home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.sh:129:    GATEWAY_URL="${OPENCLAW_GATEWAY_URL:-http://localhost:18789}"
/home/ubuntu/.openclaw/skills/clawra-selfie/SKILL.md:16:https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png
/home/ubuntu/.openclaw/skills/clawra-selfie/SKILL.md:32:FAL_KEY=your_fal_api_key          # Get from https://fal.ai/dashboard/keys
/home/ubuntu/.openclaw/skills/clawra-selfie/SKILL.md:93:REFERENCE_IMAGE="https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png"
/home/ubuntu/.openclaw/skills/clawra-selfie/SKILL.md:107:curl -X POST "https://fal.run/xai/grok-imagine-image/edit" \
/home/ubuntu/.openclaw/skills/clawra-selfie/SKILL.md:118:      "url": "https://v3b.fal.media/files/...",
/home/ubuntu/.openclaw/skills/clawra-selfie/SKILL.md:166:REFERENCE_IMAGE="https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png"
/home/ubuntu/.openclaw/skills/clawra-selfie/SKILL.md:209:RESPONSE=$(curl -s -X POST "https://fal.run/xai/grok-imagine-image/edit" \
/home/ubuntu/.openclaw/skills/clawra-selfie/SKILL.md:245:const REFERENCE_IMAGE = "https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png";
/home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.ts:103:      "FAL_KEY environment variable not set. Get your key from https://fal.ai/dashboard/keys"
/home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.ts:124:  const response = await fetch("https://fal.run/xai/grok-imagine-image", {
/home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.sh:36:    echo "Get your API key from: https://fal.ai/dashboard/keys"
/home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.sh:82:RESPONSE=$(curl -s -X POST "https://fal.run/xai/grok-imagine-image" \
```

## find-skills

- 路径：/home/ubuntu/.openclaw/skills/find-skills
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-12 15:56:02 UTC（约 3 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/skills/find-skills/SKILL.md:32:**Browse skills at:** https://skills.sh/
/home/ubuntu/.openclaw/skills/find-skills/SKILL.md:64:└ https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
/home/ubuntu/.openclaw/skills/find-skills/SKILL.md:84:Learn more: https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
/home/ubuntu/.openclaw/skills/find-skills/.clawhub/origin.json:3:  "registry": "https://clawhub.ai",
```

## knowledge-base-collector

- 路径：/home/ubuntu/.openclaw/skills/knowledge-base-collector
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-13 07:08:13 UTC（约 2 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 脚本文件(节选)：
  - /home/ubuntu/.openclaw/skills/knowledge-base-collector/scripts/tagger.py
  - /home/ubuntu/.openclaw/skills/knowledge-base-collector/scripts/weekly_digest.py
  - /home/ubuntu/.openclaw/skills/knowledge-base-collector/scripts/wechat_backlog.py
  - /home/ubuntu/.openclaw/skills/knowledge-base-collector/scripts/ingest_url.py
  - /home/ubuntu/.openclaw/skills/knowledge-base-collector/scripts/search_kb.py
  - /home/ubuntu/.openclaw/skills/knowledge-base-collector/scripts/ingest_image.py
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/skills/knowledge-base-collector/scripts/ingest_url.py:63:    url = url.replace("http://", "https://")
/home/ubuntu/.openclaw/skills/knowledge-base-collector/scripts/ingest_url.py:63:    url = url.replace("http://", "https://")
/home/ubuntu/.openclaw/skills/knowledge-base-collector/scripts/ingest_url.py:65:    url = url.replace("https://twitter.com/", "https://x.com/")
/home/ubuntu/.openclaw/skills/knowledge-base-collector/scripts/ingest_url.py:99:    rurl = "https://r.jina.ai/" + url
```

## Gmail

- 路径：/home/ubuntu/.openclaw/workspace/skills/Gmail
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-03 08:35:43 UTC（约 12 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：网络请求/下载(curl/wget/fetch/axios) 读取环境变量/密钥线索
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:19:curl -s -X GET 'https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages?maxResults=10' \
/home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:58:curl -s -X GET 'https://ctrl.maton.ai/connections?app=google-mail&status=ACTIVE' \
/home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:65:curl -s -X POST 'https://ctrl.maton.ai/connections' \
/home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:74:curl -s -X GET 'https://ctrl.maton.ai/connections/{connection_id}' \
/home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:95:curl -s -X DELETE 'https://ctrl.maton.ai/connections/{connection_id}' \
/home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:223:      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
/home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:19:curl -s -X GET 'https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages?maxResults=10' \
/home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:26:https://gateway.maton.ai/google-mail/gmail/v1/users/me/{endpoint}
/home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:47:1. Sign in at [maton.ai](https://maton.ai)
/home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:48:2. Go to [maton.ai/settings](https://maton.ai/settings)
/home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:53:Manage your Google OAuth connections at `https://ctrl.maton.ai`.
/home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:58:curl -s -X GET 'https://ctrl.maton.ai/connections?app=google-mail&status=ACTIVE' \
/home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:65:curl -s -X POST 'https://ctrl.maton.ai/connections' \
/home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:74:curl -s -X GET 'https://ctrl.maton.ai/connections/{connection_id}' \
/home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:84:    "url": "https://connect.maton.ai/?session_token=...",
/home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:95:curl -s -X DELETE 'https://ctrl.maton.ai/connections/{connection_id}' \
/home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:220:  'https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages?maxResults=10',
/home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:236:    'https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages',
/home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:259:- [Gmail API Overview](https://developers.google.com/gmail/api/reference/rest)
/home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:260:- [List Messages](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/list)
/home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:261:- [Get Message](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/get)
/home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:262:- [Send Message](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/send)
/home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:263:- [List Threads](https://developers.google.com/gmail/api/reference/rest/v1/users.threads/list)
/home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:264:- [List Labels](https://developers.google.com/gmail/api/reference/rest/v1/users.labels/list)
/home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:265:- [Create Draft](https://developers.google.com/gmail/api/reference/rest/v1/users.drafts/create)
/home/ubuntu/.openclaw/workspace/skills/Gmail/.clawhub/origin.json:3:  "registry": "https://clawhub.ai",
```

## YouTube

- 路径：/home/ubuntu/.openclaw/workspace/skills/YouTube
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-06 15:37:07 UTC（约 9 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/YouTube/SKILL.md:36:1. Go to [Google Cloud Console](https://console.cloud.google.com)
/home/ubuntu/.openclaw/workspace/skills/YouTube/SKILL.md:79:git clone https://github.com/ZubeidHendricks/youtube-mcp-server
/home/ubuntu/.openclaw/workspace/skills/YouTube/SKILL.md:131:  "https://youtube.com/watch?v=Z-FRe5AKmCU"
/home/ubuntu/.openclaw/workspace/skills/YouTube/SKILL.md:139:  "https://youtube.com/watch?v=VIDEO_ID" 2>&1 | grep -A1000 "WEBVTT"
/home/ubuntu/.openclaw/workspace/skills/YouTube/SKILL.md:167:  "https://youtube.com/watch?v=VIDEO_ID"
/home/ubuntu/.openclaw/workspace/skills/YouTube/SKILL.md:215:git clone https://github.com/ZubeidHendricks/youtube-mcp-server
/home/ubuntu/.openclaw/workspace/skills/YouTube/SKILL.md:273:  "https://youtube.com/watch?v=Z-FRe5AKmCU"
/home/ubuntu/.openclaw/workspace/skills/YouTube/README.md:3:YouTube research and transcription skill for [Clawdbot](https://clawdbot.com).
/home/ubuntu/.openclaw/workspace/skills/YouTube/README.md:21:Get a YouTube API key from [Google Cloud Console](https://console.cloud.google.com):
/home/ubuntu/.openclaw/workspace/skills/YouTube/README.md:47:"Get the transcript for this video: https://youtube.com/watch?v=Z-FRe5AKmCU"
/home/ubuntu/.openclaw/workspace/skills/YouTube/README.md:55:This skill uses the [youtube-mcp-server](https://github.com/ZubeidHendricks/youtube-mcp-server) by Zubeid Hendricks for YouTube Data API integration.
/home/ubuntu/.openclaw/workspace/skills/YouTube/.clawhub/origin.json:3:  "registry": "https://clawhub.ai",
```

## Gmail.disabled-20260208-062106

- 路径：/home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-06 15:37:07 UTC（约 9 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：网络请求/下载(curl/wget/fetch/axios) 读取环境变量/密钥线索
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:19:curl -s -X GET 'https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages?maxResults=10' \
/home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:58:curl -s -X GET 'https://ctrl.maton.ai/connections?app=google-mail&status=ACTIVE' \
/home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:65:curl -s -X POST 'https://ctrl.maton.ai/connections' \
/home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:74:curl -s -X GET 'https://ctrl.maton.ai/connections/{connection_id}' \
/home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:95:curl -s -X DELETE 'https://ctrl.maton.ai/connections/{connection_id}' \
/home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:223:      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
/home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:19:curl -s -X GET 'https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages?maxResults=10' \
/home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:26:https://gateway.maton.ai/google-mail/gmail/v1/users/me/{endpoint}
/home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:47:1. Sign in at [maton.ai](https://maton.ai)
/home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:48:2. Go to [maton.ai/settings](https://maton.ai/settings)
/home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:53:Manage your Google OAuth connections at `https://ctrl.maton.ai`.
/home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:58:curl -s -X GET 'https://ctrl.maton.ai/connections?app=google-mail&status=ACTIVE' \
/home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:65:curl -s -X POST 'https://ctrl.maton.ai/connections' \
/home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:74:curl -s -X GET 'https://ctrl.maton.ai/connections/{connection_id}' \
/home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:84:    "url": "https://connect.maton.ai/?session_token=...",
/home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:95:curl -s -X DELETE 'https://ctrl.maton.ai/connections/{connection_id}' \
/home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:220:  'https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages?maxResults=10',
/home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:236:    'https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages',
/home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:259:- [Gmail API Overview](https://developers.google.com/gmail/api/reference/rest)
/home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:260:- [List Messages](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/list)
/home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:261:- [Get Message](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/get)
/home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:262:- [Send Message](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/send)
/home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:263:- [List Threads](https://developers.google.com/gmail/api/reference/rest/v1/users.threads/list)
/home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:264:- [List Labels](https://developers.google.com/gmail/api/reference/rest/v1/users.labels/list)
/home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:265:- [Create Draft](https://developers.google.com/gmail/api/reference/rest/v1/users.drafts/create)
/home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/.clawhub/origin.json:3:  "registry": "https://clawhub.ai",
```

## claw-roam.disabled-20260208-081734

- 路径：/home/ubuntu/.openclaw/workspace/skills/_disabled/claw-roam.disabled-20260208-081734
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-08 03:43:57 UTC（约 7 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 可执行文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/_disabled/claw-roam.disabled-20260208-081734/scripts/claw-roam.sh
- 脚本文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/_disabled/claw-roam.disabled-20260208-081734/scripts/claw-roam.sh
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/_disabled/claw-roam.disabled-20260208-081734/.clawhub/origin.json:3:  "registry": "https://clawhub.ai",
```

## a-stock-analysis

- 路径：/home/ubuntu/.openclaw/workspace/skills/a-stock-analysis
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-10 02:52:52 UTC（约 5 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 脚本文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/a-stock-analysis/scripts/portfolio.py
  - /home/ubuntu/.openclaw/workspace/skills/a-stock-analysis/scripts/analyze.py
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/a-stock-analysis/scripts/analyze.py:78:        url = f"https://hq.sinajs.cn/list={codes_str}"
/home/ubuntu/.openclaw/workspace/skills/a-stock-analysis/scripts/analyze.py:81:            "Referer": "https://finance.sina.com.cn",
/home/ubuntu/.openclaw/workspace/skills/a-stock-analysis/scripts/analyze.py:178:    url = f"https://quotes.sina.cn/cn/api/jsonp_v2.php/var%20_{symbol}=/CN_MarketDataService.getKLineData?symbol={symbol}&scale=1&ma=no&datalen={count}"
/home/ubuntu/.openclaw/workspace/skills/a-stock-analysis/scripts/analyze.py:182:            "Referer": "https://finance.sina.com.cn",
/home/ubuntu/.openclaw/workspace/skills/a-stock-analysis/.clawhub/origin.json:3:  "registry": "https://clawhub.ai",
```

## avatarkit

- 路径：/home/ubuntu/.openclaw/workspace/skills/avatarkit
- SKILL.md：yes
- package.json：/home/ubuntu/.openclaw/workspace/skills/avatarkit/package.json (name=openclaw-avatarkit version=0.1.0)
- 最近文件修改：2026-02-11 07:35:00 UTC（约 4 天前）
- 版本库：git:main@5a17ff7
- git status：clean
- 风险等级：**low**
- 理由：网络请求/下载(curl/wget/fetch/axios)
- 脚本文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/avatarkit/example.ts
  - /home/ubuntu/.openclaw/workspace/skills/avatarkit/src/image.ts
  - /home/ubuntu/.openclaw/workspace/skills/avatarkit/src/SKILL.ts
  - /home/ubuntu/.openclaw/workspace/skills/avatarkit/src/avatar.ts
  - /home/ubuntu/.openclaw/workspace/skills/avatarkit/src/memory.ts
  - /home/ubuntu/.openclaw/workspace/skills/avatarkit/src/natural.ts
  - /home/ubuntu/.openclaw/workspace/skills/avatarkit/src/api.ts
  - /home/ubuntu/.openclaw/workspace/skills/avatarkit/src/voice.ts
  - /home/ubuntu/.openclaw/workspace/skills/avatarkit/src/types.ts
  - /home/ubuntu/.openclaw/workspace/skills/avatarkit/src/index.ts
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/avatarkit/README.md:92:           "baseUrl": "http://localhost:3000/v1"
/home/ubuntu/.openclaw/workspace/skills/avatarkit/DEVELOPMENT.md:37:| **自建后端** | 部署自己的 API 服务 | `baseUrl: "https://your-api.com/v1"` |
/home/ubuntu/.openclaw/workspace/skills/avatarkit/DEVELOPMENT.md:39:| **官方云服务** | 即将推出 | `baseUrl: "https://api.avatarkit.com/v1"` |
/home/ubuntu/.openclaw/workspace/skills/avatarkit/SKILL.md:6:**Homepage:** https://github.com/rain1898/avatarkit
/home/ubuntu/.openclaw/workspace/skills/avatarkit/SKILL.md:45:openclaw skill install https://github.com/rain1898/avatarkit/raw/main/SKILL.md
/home/ubuntu/.openclaw/workspace/skills/avatarkit/SKILL.md:53:git clone https://github.com/rain1898/avatarkit.git avatarkit
/home/ubuntu/.openclaw/workspace/skills/avatarkit/SKILL.md:80:详见 [backend/README.md](https://github.com/rain1898/avatarkit/blob/main/backend/README.md)
/home/ubuntu/.openclaw/workspace/skills/avatarkit/SKILL.md:118:        "baseUrl": "https://your-backend.com/v1",
/home/ubuntu/.openclaw/workspace/skills/avatarkit/SKILL.md:196:  baseUrl: 'https://your-backend.com/v1',
/home/ubuntu/.openclaw/workspace/skills/avatarkit/SKILL.md:273:- GitHub: https://github.com/rain1898/avatarkit
/home/ubuntu/.openclaw/workspace/skills/avatarkit/SKILL.md:274:- Issues: https://github.com/rain1898/avatarkit/issues
/home/ubuntu/.openclaw/workspace/skills/avatarkit/SKILL.md:275:- 文档: https://github.com/rain1898/avatarkit/blob/main/README.md
/home/ubuntu/.openclaw/workspace/skills/avatarkit/index.html:7:    <link rel="preconnect" href="https://fonts.googleapis.com">
/home/ubuntu/.openclaw/workspace/skills/avatarkit/index.html:8:    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
/home/ubuntu/.openclaw/workspace/skills/avatarkit/index.html:9:    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
/home/ubuntu/.openclaw/workspace/skills/avatarkit/index.html:384:                <a href="https://github.com/reed1898/avatarkit" target="_blank">GitHub</a>
/home/ubuntu/.openclaw/workspace/skills/avatarkit/index.html:412:            <a href="https://github.com/reed1898/avatarkit" class="btn btn-secondary" target="_blank">
/home/ubuntu/.openclaw/workspace/skills/avatarkit/index.html:476:                openclaw skill install https://github.com/reed1898/avatarkit/raw/main/SKILL.md
/home/ubuntu/.openclaw/workspace/skills/avatarkit/index.html:484:            <a href="https://github.com/reed1898" target="_blank">@reed1898</a> 
/home/ubuntu/.openclaw/workspace/skills/avatarkit/index.html:488:            🦞 <a href="https://openclaw.ai" target="_blank">OpenClaw</a> · 
/home/ubuntu/.openclaw/workspace/skills/avatarkit/index.html:489:            <a href="https://github.com/reed1898/avatarkit" target="_blank">GitHub</a>
/home/ubuntu/.openclaw/workspace/skills/avatarkit/README.md:3:[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
/home/ubuntu/.openclaw/workspace/skills/avatarkit/README.md:4:[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue.svg)](https://www.typescriptlang.org/)
/home/ubuntu/.openclaw/workspace/skills/avatarkit/README.md:5:[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-green.svg)](https://openclaw.io)
/home/ubuntu/.openclaw/workspace/skills/avatarkit/README.md:39:openclaw skill install https://github.com/reed1898/avatarkit/raw/main/SKILL.md
/home/ubuntu/.openclaw/workspace/skills/avatarkit/README.md:46:git clone https://github.com/reed1898/avatarkit.git
/home/ubuntu/.openclaw/workspace/skills/avatarkit/README.md:66:        "baseUrl": "https://api.avatarkit.com/v1"
/home/ubuntu/.openclaw/workspace/skills/avatarkit/README.md:134:        "baseUrl": "https://your-backend.com/v1",
/home/ubuntu/.openclaw/workspace/skills/avatarkit/README.md:177:  baseUrl: 'https://your-backend.com/v1',
/home/ubuntu/.openclaw/workspace/skills/avatarkit/src/SKILL.ts:112:  homepage: 'https://avatarkit.com',
/home/ubuntu/.openclaw/workspace/skills/avatarkit/src/SKILL.ts:113:  repository: 'https://github.com/avatarkit/avatarkit-skill',
/home/ubuntu/.openclaw/workspace/skills/avatarkit/src/SKILL.ts:189:    baseUrl: 'https://api.avatarkit.com',
/home/ubuntu/.openclaw/workspace/skills/avatarkit/src/api.ts:44:      baseUrl: 'https://api.avatarkit.com/v1',
/home/ubuntu/.openclaw/workspace/skills/avatarkit/src/index.ts:48:   * 默认: https://api.avatarkit.com/v1
/home/ubuntu/.openclaw/workspace/skills/avatarkit/src/index.ts:87:        baseUrl: config.baseUrl || 'https://api.avatarkit.com/v1',
/home/ubuntu/.openclaw/workspace/skills/avatarkit/vercel.json:2:  "$schema": "https://openapi.vercel.sh/vercel.json",
/home/ubuntu/.openclaw/workspace/skills/avatarkit/backend/package.json:17:    "axios": "^1.6.0",
/home/ubuntu/.openclaw/workspace/skills/avatarkit/package.json:23:    "axios": "^1.6.0"
/home/ubuntu/.openclaw/workspace/skills/avatarkit/src/api.ts:6:import axios, { AxiosInstance, AxiosResponse } from 'axios';
/home/ubuntu/.openclaw/workspace/skills/avatarkit/src/api.ts:50:    this.client = axios.create({
/home/ubuntu/.openclaw/workspace/skills/avatarkit/src/api.ts:205:    const response = await axios.post(endpoint, {
/home/ubuntu/.openclaw/workspace/skills/avatarkit/src/api.ts:232:    const response = await axios.post(endpoint, {
```

## browse

- 路径：/home/ubuntu/.openclaw/workspace/skills/browse
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-06 15:37:07 UTC（约 9 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：网络请求/下载(curl/wget/fetch/axios) 读取环境变量/密钥线索
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/browse/SKILL.md:157:curl -X POST http://127.0.0.1:14113/v1/functions/my-automation/invoke \
/home/ubuntu/.openclaw/workspace/skills/browse/SKILL.md:188:curl -X POST https://api.browserbase.com/v1/functions/<function-id>/invoke \
/home/ubuntu/.openclaw/workspace/skills/browse/skills/create/SKILL.md:130:curl -X POST http://127.0.0.1:14113/v1/functions/my-automation/invoke \
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:119:curl -X POST http://127.0.0.1:14113/v1/functions/my-function/invoke \
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:151:curl -X POST "https://api.browserbase.com/v1/functions/FUNCTION_ID/invoke" \
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:159:curl "https://api.browserbase.com/v1/functions/invocations/INVOCATION_ID" \
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:174:        'x-bb-api-key': process.env.BROWSERBASE_API_KEY!,
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:187:      { headers: { 'x-bb-api-key': process.env.BROWSERBASE_API_KEY! } }
/home/ubuntu/.openclaw/workspace/skills/browse/SKILL.md:153:Server runs at `http://127.0.0.1:14113`
/home/ubuntu/.openclaw/workspace/skills/browse/SKILL.md:157:curl -X POST http://127.0.0.1:14113/v1/functions/my-automation/invoke \
/home/ubuntu/.openclaw/workspace/skills/browse/skills/create/SKILL.md:130:curl -X POST http://127.0.0.1:14113/v1/functions/my-automation/invoke \
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:114:Server runs at `http://127.0.0.1:14113`
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:119:curl -X POST http://127.0.0.1:14113/v1/functions/my-function/invoke \
/home/ubuntu/.openclaw/workspace/skills/browse/SKILL.md:4:homepage: https://browserbase.com
/home/ubuntu/.openclaw/workspace/skills/browse/SKILL.md:25:stagehand fn auth login   # If needed - get credentials from https://browserbase.com/settings
/home/ubuntu/.openclaw/workspace/skills/browse/SKILL.md:36:stagehand goto https://example.com
/home/ubuntu/.openclaw/workspace/skills/browse/SKILL.md:118:  await page.goto("https://example.com");
/home/ubuntu/.openclaw/workspace/skills/browse/SKILL.md:159:  -d '{"params": {"url": "https://example.com"}}'
/home/ubuntu/.openclaw/workspace/skills/browse/SKILL.md:188:curl -X POST https://api.browserbase.com/v1/functions/<function-id>/invoke \
/home/ubuntu/.openclaw/workspace/skills/browse/SKILL.md:207:  await page.goto("https://news.ycombinator.com");
/home/ubuntu/.openclaw/workspace/skills/browse/SKILL.md:270:  await page.goto("https://example.com/login");
/home/ubuntu/.openclaw/workspace/skills/browse/skills/fix/SKILL.md:178:> stagehand goto https://example.com/product/123
/home/ubuntu/.openclaw/workspace/skills/browse/skills/fix/SKILL.md:194:> stagehand fn invoke price-monitor --local -p '{"productUrl": "https://example.com/product/123"}'
/home/ubuntu/.openclaw/workspace/skills/browse/skills/browser-automation/SKILL.md:43:stagehand --ws $BROWSERBASE_CONNECT_URL open https://example.com
/home/ubuntu/.openclaw/workspace/skills/browse/skills/browser-automation/SKILL.md:62:stagehand --ws $BROWSERBASE_CONNECT_URL open https://example.com
/home/ubuntu/.openclaw/workspace/skills/browse/skills/browser-automation/SKILL.md:68:# RootWebArea "Example" url="https://example.com"
/home/ubuntu/.openclaw/workspace/skills/browse/skills/browser-automation/SKILL.md:195:stagehand --ws $BROWSERBASE_CONNECT_URL newpage https://example.com
/home/ubuntu/.openclaw/workspace/skills/browse/skills/browser-automation/SKILL.md:260:stagehand --ws $BROWSERBASE_CONNECT_URL open https://example.com
/home/ubuntu/.openclaw/workspace/skills/browse/skills/browser-automation/SKILL.md:281:stagehand --ws $BROWSERBASE_CONNECT_URL open https://slow-site.com
/home/ubuntu/.openclaw/workspace/skills/browse/skills/browser-automation/SKILL.md:289:stagehand --ws $BROWSERBASE_CONNECT_URL open https://example.com
/home/ubuntu/.openclaw/workspace/skills/browse/skills/browser-automation/SKILL.md:292:stagehand open https://example.com
/home/ubuntu/.openclaw/workspace/skills/browse/skills/browser-automation/SKILL.md:299:stagehand --ws $BROWSERBASE_CONNECT_URL open https://example.com/login
/home/ubuntu/.openclaw/workspace/skills/browse/skills/browser-automation/SKILL.md:313:stagehand --ws $BROWSERBASE_CONNECT_URL open https://example.com
/home/ubuntu/.openclaw/workspace/skills/browse/skills/browser-automation/SKILL.md:327:stagehand --ws $BROWSERBASE_CONNECT_URL open https://example.com
/home/ubuntu/.openclaw/workspace/skills/browse/skills/create/SKILL.md:34:stagehand goto https://example.com
/home/ubuntu/.openclaw/workspace/skills/browse/skills/create/SKILL.md:110:  await page.goto("https://example.com");
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:22:Get API key and Project ID from: https://browserbase.com/settings
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:94:  await page.goto(params.url || "https://example.com");
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:121:  -d '{"params": {"url": "https://news.ycombinator.com"}}'
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:151:curl -X POST "https://api.browserbase.com/v1/functions/FUNCTION_ID/invoke" \
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:154:  -d '{"params": {"url": "https://example.com"}}'
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:159:curl "https://api.browserbase.com/v1/functions/invocations/INVOCATION_ID" \
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:169:    `https://api.browserbase.com/v1/functions/${functionId}/invoke`,
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:186:      `https://api.browserbase.com/v1/functions/invocations/${invocationId}`,
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:225:  await page.goto("https://example.com/login");
/home/ubuntu/.openclaw/workspace/skills/browse/.clawhub/origin.json:3:  "registry": "https://clawhub.ai",
```

## auth

- 路径：/home/ubuntu/.openclaw/workspace/skills/browse/skills/auth
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-06 15:37:07 UTC（约 9 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中：无

## browser-automation

- 路径：/home/ubuntu/.openclaw/workspace/skills/browse/skills/browser-automation
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-06 15:37:07 UTC（约 9 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/browse/skills/browser-automation/SKILL.md:43:stagehand --ws $BROWSERBASE_CONNECT_URL open https://example.com
/home/ubuntu/.openclaw/workspace/skills/browse/skills/browser-automation/SKILL.md:62:stagehand --ws $BROWSERBASE_CONNECT_URL open https://example.com
/home/ubuntu/.openclaw/workspace/skills/browse/skills/browser-automation/SKILL.md:68:# RootWebArea "Example" url="https://example.com"
/home/ubuntu/.openclaw/workspace/skills/browse/skills/browser-automation/SKILL.md:195:stagehand --ws $BROWSERBASE_CONNECT_URL newpage https://example.com
/home/ubuntu/.openclaw/workspace/skills/browse/skills/browser-automation/SKILL.md:260:stagehand --ws $BROWSERBASE_CONNECT_URL open https://example.com
/home/ubuntu/.openclaw/workspace/skills/browse/skills/browser-automation/SKILL.md:281:stagehand --ws $BROWSERBASE_CONNECT_URL open https://slow-site.com
/home/ubuntu/.openclaw/workspace/skills/browse/skills/browser-automation/SKILL.md:289:stagehand --ws $BROWSERBASE_CONNECT_URL open https://example.com
/home/ubuntu/.openclaw/workspace/skills/browse/skills/browser-automation/SKILL.md:292:stagehand open https://example.com
/home/ubuntu/.openclaw/workspace/skills/browse/skills/browser-automation/SKILL.md:299:stagehand --ws $BROWSERBASE_CONNECT_URL open https://example.com/login
/home/ubuntu/.openclaw/workspace/skills/browse/skills/browser-automation/SKILL.md:313:stagehand --ws $BROWSERBASE_CONNECT_URL open https://example.com
/home/ubuntu/.openclaw/workspace/skills/browse/skills/browser-automation/SKILL.md:327:stagehand --ws $BROWSERBASE_CONNECT_URL open https://example.com
```

## create

- 路径：/home/ubuntu/.openclaw/workspace/skills/browse/skills/create
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-06 15:37:07 UTC（约 9 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：网络请求/下载(curl/wget/fetch/axios)
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/browse/skills/create/SKILL.md:130:curl -X POST http://127.0.0.1:14113/v1/functions/my-automation/invoke \
/home/ubuntu/.openclaw/workspace/skills/browse/skills/create/SKILL.md:130:curl -X POST http://127.0.0.1:14113/v1/functions/my-automation/invoke \
/home/ubuntu/.openclaw/workspace/skills/browse/skills/create/SKILL.md:34:stagehand goto https://example.com
/home/ubuntu/.openclaw/workspace/skills/browse/skills/create/SKILL.md:110:  await page.goto("https://example.com");
```

## fix

- 路径：/home/ubuntu/.openclaw/workspace/skills/browse/skills/fix
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-06 15:37:07 UTC（约 9 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/browse/skills/fix/SKILL.md:178:> stagehand goto https://example.com/product/123
/home/ubuntu/.openclaw/workspace/skills/browse/skills/fix/SKILL.md:194:> stagehand fn invoke price-monitor --local -p '{"productUrl": "https://example.com/product/123"}'
```

## functions

- 路径：/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-06 15:37:07 UTC（约 9 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：网络请求/下载(curl/wget/fetch/axios) 读取环境变量/密钥线索
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:119:curl -X POST http://127.0.0.1:14113/v1/functions/my-function/invoke \
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:151:curl -X POST "https://api.browserbase.com/v1/functions/FUNCTION_ID/invoke" \
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:159:curl "https://api.browserbase.com/v1/functions/invocations/INVOCATION_ID" \
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:174:        'x-bb-api-key': process.env.BROWSERBASE_API_KEY!,
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:187:      { headers: { 'x-bb-api-key': process.env.BROWSERBASE_API_KEY! } }
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:114:Server runs at `http://127.0.0.1:14113`
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:119:curl -X POST http://127.0.0.1:14113/v1/functions/my-function/invoke \
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:22:Get API key and Project ID from: https://browserbase.com/settings
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:94:  await page.goto(params.url || "https://example.com");
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:121:  -d '{"params": {"url": "https://news.ycombinator.com"}}'
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:151:curl -X POST "https://api.browserbase.com/v1/functions/FUNCTION_ID/invoke" \
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:154:  -d '{"params": {"url": "https://example.com"}}'
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:159:curl "https://api.browserbase.com/v1/functions/invocations/INVOCATION_ID" \
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:169:    `https://api.browserbase.com/v1/functions/${functionId}/invoke`,
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:186:      `https://api.browserbase.com/v1/functions/invocations/${invocationId}`,
/home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:225:  await page.goto("https://example.com/login");
```

## claw-roam

- 路径：/home/ubuntu/.openclaw/workspace/skills/claw-roam
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-06 17:49:35 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 可执行文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/claw-roam/scripts/claw-roam.sh
- 脚本文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/claw-roam/scripts/claw-roam.sh
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/claw-roam/.clawhub/origin.json:3:  "registry": "https://clawhub.ai",
```

## clawra

- 路径：/home/ubuntu/.openclaw/workspace/skills/clawra
- SKILL.md：yes
- package.json：/home/ubuntu/.openclaw/workspace/skills/clawra/package.json (name=clawra version=1.1.1)
- 最近文件修改：2026-02-11 17:30:58 UTC（约 3 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**medium**
- 理由：执行外部命令(child_process/exec/spawn) 网络请求/下载(curl/wget/fetch/axios) 读取环境变量/密钥线索
- 可执行文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/clawra/bin/cli.js
  - /home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.sh
  - /home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh
- 脚本文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/clawra/bin/cli.js
  - /home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.ts
  - /home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.sh
  - /home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts
  - /home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/clawra/bin/cli.js:12:const { execSync, spawn } = require("child_process");
/home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:240:import { exec } from "child_process";
/home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.ts:16:import { exec } from "child_process";
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:240:import { exec } from "child_process";
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:16:import { exec } from "child_process";
/home/ubuntu/.openclaw/workspace/skills/clawra/bin/cli.js:12:const { execSync, spawn } = require("child_process");
/home/ubuntu/.openclaw/workspace/skills/clawra/bin/cli.js:88:    execSync(`which ${cmd}`, { stdio: "ignore" });
/home/ubuntu/.openclaw/workspace/skills/clawra/bin/cli.js:109:    execSync(cmd, { stdio: "ignore" });
/home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:107:curl -X POST "https://fal.run/xai/grok-imagine-image/edit" \
/home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:142:curl -X POST "http://localhost:18789/message" \
/home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:209:RESPONSE=$(curl -s -X POST "https://fal.run/xai/grok-imagine-image/edit" \
/home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.sh:82:RESPONSE=$(curl -s -X POST "https://fal.run/xai/grok-imagine-image" \
/home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.sh:136:    curl -s -X POST "$GATEWAY_URL/message" \
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:107:curl -X POST "https://fal.run/xai/grok-imagine-image/edit" \
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:142:curl -X POST "http://localhost:18789/message" \
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:209:RESPONSE=$(curl -s -X POST "https://fal.run/xai/grok-imagine-image/edit" \
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh:82:RESPONSE=$(curl -s -X POST "https://fal.run/xai/grok-imagine-image" \
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh:136:    curl -s -X POST "$GATEWAY_URL/message" \
/home/ubuntu/.openclaw/workspace/skills/clawra/.serena/project.yml:11:#   powershell          python              python_jedi         r                   rego
/home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:283:    credentials: process.env.FAL_KEY!
/home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.ts:99:  const falKey = process.env.FAL_KEY;
/home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.ts:162:    process.env.OPENCLAW_GATEWAY_URL || "http://localhost:18789";
/home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.ts:163:  const gatewayToken = process.env.OPENCLAW_GATEWAY_TOKEN;
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:283:    credentials: process.env.FAL_KEY!
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:99:  const falKey = process.env.FAL_KEY;
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:162:    process.env.OPENCLAW_GATEWAY_URL || "http://localhost:18789";
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:163:  const gatewayToken = process.env.OPENCLAW_GATEWAY_TOKEN;
/home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:33:OPENCLAW_GATEWAY_TOKEN=your_token  # From: openclaw doctor --generate-gateway-token
/home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:143:  -H "Authorization: Bearer $OPENCLAW_GATEWAY_TOKEN" \
/home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.ts:13: *   OPENCLAW_GATEWAY_TOKEN - Gateway auth token (optional)
/home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.ts:163:  const gatewayToken = process.env.OPENCLAW_GATEWAY_TOKEN;
/home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.sh:129:    GATEWAY_TOKEN="${OPENCLAW_GATEWAY_TOKEN:-}"
/home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.sh:132:    if [ -n "$GATEWAY_TOKEN" ]; then
/home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.sh:133:        HEADERS="$HEADERS -H \"Authorization: Bearer $GATEWAY_TOKEN\""
/home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.sh:138:        ${GATEWAY_TOKEN:+-H "Authorization: Bearer $GATEWAY_TOKEN"} \
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:33:OPENCLAW_GATEWAY_TOKEN=your_token  # From: openclaw doctor --generate-gateway-token
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:143:  -H "Authorization: Bearer $OPENCLAW_GATEWAY_TOKEN" \
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:13: *   OPENCLAW_GATEWAY_TOKEN - Gateway auth token (optional)
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:163:  const gatewayToken = process.env.OPENCLAW_GATEWAY_TOKEN;
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh:129:    GATEWAY_TOKEN="${OPENCLAW_GATEWAY_TOKEN:-}"
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh:132:    if [ -n "$GATEWAY_TOKEN" ]; then
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh:133:        HEADERS="$HEADERS -H \"Authorization: Bearer $GATEWAY_TOKEN\""
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh:138:        ${GATEWAY_TOKEN:+-H "Authorization: Bearer $GATEWAY_TOKEN"} \
/home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:142:curl -X POST "http://localhost:18789/message" \
/home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.ts:12: *   OPENCLAW_GATEWAY_URL - OpenClaw gateway URL (default: http://localhost:18789)
/home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.ts:162:    process.env.OPENCLAW_GATEWAY_URL || "http://localhost:18789";
/home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.sh:128:    GATEWAY_URL="${OPENCLAW_GATEWAY_URL:-http://localhost:18789}"
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:142:curl -X POST "http://localhost:18789/message" \
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:12: *   OPENCLAW_GATEWAY_URL - OpenClaw gateway URL (default: http://localhost:18789)
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:162:    process.env.OPENCLAW_GATEWAY_URL || "http://localhost:18789";
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh:128:    GATEWAY_URL="${OPENCLAW_GATEWAY_URL:-http://localhost:18789}"
/home/ubuntu/.openclaw/workspace/skills/clawra/bin/cli.js:214:  const FAL_URL = "https://fal.ai/dashboard/keys";
/home/ubuntu/.openclaw/workspace/skills/clawra/bin/cli.js:339:- **Avatar:** https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png
/home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:16:https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png
/home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:32:FAL_KEY=your_fal_api_key          # Get from https://fal.ai/dashboard/keys
/home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:93:REFERENCE_IMAGE="https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png"
/home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:107:curl -X POST "https://fal.run/xai/grok-imagine-image/edit" \
/home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:118:      "url": "https://v3b.fal.media/files/...",
/home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:166:REFERENCE_IMAGE="https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png"
/home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:209:RESPONSE=$(curl -s -X POST "https://fal.run/xai/grok-imagine-image/edit" \
/home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:245:const REFERENCE_IMAGE = "https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png";
/home/ubuntu/.openclaw/workspace/skills/clawra/README.md:2:<img width="300"  alt="image" src="https://github.com/user-attachments/assets/41512c51-e61d-4550-b461-eed06a1b0ec8" />
/home/ubuntu/.openclaw/workspace/skills/clawra/README.md:34:- [OpenClaw](https://github.com/openclaw/openclaw) installed and configured
/home/ubuntu/.openclaw/workspace/skills/clawra/README.md:35:- [fal.ai](https://fal.ai) account (free tier available)
/home/ubuntu/.openclaw/workspace/skills/clawra/README.md:43:Visit [fal.ai/dashboard/keys](https://fal.ai/dashboard/keys) and create an API key.
/home/ubuntu/.openclaw/workspace/skills/clawra/README.md:48:git clone https://github.com/SumeLabs/clawra ~/.openclaw/skills/clawra-selfie
/home/ubuntu/.openclaw/workspace/skills/clawra/README.md:97:https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png
/home/ubuntu/.openclaw/workspace/skills/clawra/.serena/project.yml:16:#   https://github.com/oraios/serena/blob/main/src/solidlsp/ls_config.py
/home/ubuntu/.openclaw/workspace/skills/clawra/.serena/project.yml:24:#   See here for details: https://oraios.github.io/serena/01-about/020_programming-languages.html#language-servers
/home/ubuntu/.openclaw/workspace/skills/clawra/.serena/project.yml:32:# For a list of possible encodings, see https://docs.python.org/3.11/library/codecs.html#standard-encodings
/home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.ts:103:      "FAL_KEY environment variable not set. Get your key from https://fal.ai/dashboard/keys"
/home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.ts:124:  const response = await fetch("https://fal.run/xai/grok-imagine-image", {
/home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.sh:36:    echo "Get your API key from: https://fal.ai/dashboard/keys"
/home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.sh:82:RESPONSE=$(curl -s -X POST "https://fal.run/xai/grok-imagine-image" \
/home/ubuntu/.openclaw/workspace/skills/clawra/package.json:32:    "url": "https://github.com/SumeLabs/clawra"
/home/ubuntu/.openclaw/workspace/skills/clawra/package.json:34:  "homepage": "https://github.com/SumeLabs/clawra#readme",
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:16:https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:32:FAL_KEY=your_fal_api_key          # Get from https://fal.ai/dashboard/keys
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:93:REFERENCE_IMAGE="https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png"
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:107:curl -X POST "https://fal.run/xai/grok-imagine-image/edit" \
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:118:      "url": "https://v3b.fal.media/files/...",
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:166:REFERENCE_IMAGE="https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png"
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:209:RESPONSE=$(curl -s -X POST "https://fal.run/xai/grok-imagine-image/edit" \
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:245:const REFERENCE_IMAGE = "https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png";
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:103:      "FAL_KEY environment variable not set. Get your key from https://fal.ai/dashboard/keys"
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:124:  const response = await fetch("https://fal.run/xai/grok-imagine-image", {
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh:36:    echo "Get your API key from: https://fal.ai/dashboard/keys"
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh:82:RESPONSE=$(curl -s -X POST "https://fal.run/xai/grok-imagine-image" \
```

## skill

- 路径：/home/ubuntu/.openclaw/workspace/skills/clawra/skill
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-11 17:30:58 UTC（约 3 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**medium**
- 理由：执行外部命令(child_process/exec/spawn) 网络请求/下载(curl/wget/fetch/axios) 读取环境变量/密钥线索
- 可执行文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh
- 脚本文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts
  - /home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:240:import { exec } from "child_process";
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:16:import { exec } from "child_process";
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:107:curl -X POST "https://fal.run/xai/grok-imagine-image/edit" \
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:142:curl -X POST "http://localhost:18789/message" \
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:209:RESPONSE=$(curl -s -X POST "https://fal.run/xai/grok-imagine-image/edit" \
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh:82:RESPONSE=$(curl -s -X POST "https://fal.run/xai/grok-imagine-image" \
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh:136:    curl -s -X POST "$GATEWAY_URL/message" \
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:283:    credentials: process.env.FAL_KEY!
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:99:  const falKey = process.env.FAL_KEY;
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:162:    process.env.OPENCLAW_GATEWAY_URL || "http://localhost:18789";
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:163:  const gatewayToken = process.env.OPENCLAW_GATEWAY_TOKEN;
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:33:OPENCLAW_GATEWAY_TOKEN=your_token  # From: openclaw doctor --generate-gateway-token
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:143:  -H "Authorization: Bearer $OPENCLAW_GATEWAY_TOKEN" \
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:13: *   OPENCLAW_GATEWAY_TOKEN - Gateway auth token (optional)
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:163:  const gatewayToken = process.env.OPENCLAW_GATEWAY_TOKEN;
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh:129:    GATEWAY_TOKEN="${OPENCLAW_GATEWAY_TOKEN:-}"
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh:132:    if [ -n "$GATEWAY_TOKEN" ]; then
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh:133:        HEADERS="$HEADERS -H \"Authorization: Bearer $GATEWAY_TOKEN\""
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh:138:        ${GATEWAY_TOKEN:+-H "Authorization: Bearer $GATEWAY_TOKEN"} \
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:142:curl -X POST "http://localhost:18789/message" \
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:12: *   OPENCLAW_GATEWAY_URL - OpenClaw gateway URL (default: http://localhost:18789)
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:162:    process.env.OPENCLAW_GATEWAY_URL || "http://localhost:18789";
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh:128:    GATEWAY_URL="${OPENCLAW_GATEWAY_URL:-http://localhost:18789}"
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:16:https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:32:FAL_KEY=your_fal_api_key          # Get from https://fal.ai/dashboard/keys
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:93:REFERENCE_IMAGE="https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png"
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:107:curl -X POST "https://fal.run/xai/grok-imagine-image/edit" \
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:118:      "url": "https://v3b.fal.media/files/...",
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:166:REFERENCE_IMAGE="https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png"
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:209:RESPONSE=$(curl -s -X POST "https://fal.run/xai/grok-imagine-image/edit" \
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:245:const REFERENCE_IMAGE = "https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png";
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:103:      "FAL_KEY environment variable not set. Get your key from https://fal.ai/dashboard/keys"
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:124:  const response = await fetch("https://fal.run/xai/grok-imagine-image", {
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh:36:    echo "Get your API key from: https://fal.ai/dashboard/keys"
/home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh:82:RESPONSE=$(curl -s -X POST "https://fal.run/xai/grok-imagine-image" \
```

## crypto-price

- 路径：/home/ubuntu/.openclaw/workspace/skills/crypto-price
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-06 15:37:07 UTC（约 9 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：读取环境变量/密钥线索
- 脚本文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/crypto-price/scripts/get_price_chart.py
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/crypto-price/scripts/get_price_chart.py:23:TOKEN_ID_MAP = {
/home/ubuntu/.openclaw/workspace/skills/crypto-price/scripts/get_price_chart.py:837:    token_id = TOKEN_ID_MAP.get(symbol_upper)
/home/ubuntu/.openclaw/workspace/skills/crypto-price/README.md:26:   git clone https://github.com/evgyur/crypto-price.git
/home/ubuntu/.openclaw/workspace/skills/crypto-price/README.md:130:1. **Hyperliquid API** (`https://api.hyperliquid.xyz/info`)
/home/ubuntu/.openclaw/workspace/skills/crypto-price/README.md:134:2. **CoinGecko API** (`https://api.coingecko.com/api/v3/`)
/home/ubuntu/.openclaw/workspace/skills/crypto-price/README.md:183:- [GitHub Repository](https://github.com/evgyur/crypto-price)
/home/ubuntu/.openclaw/workspace/skills/crypto-price/README.md:184:- [ClawdHub](https://clawdhub.com/evgyur/crypto-price)
/home/ubuntu/.openclaw/workspace/skills/crypto-price/README.md:185:- [Clawdbot Documentation](https://docs.clawd.bot)
/home/ubuntu/.openclaw/workspace/skills/crypto-price/scripts/get_price_chart.py:16:COINGECKO_PRICE_URL = "https://api.coingecko.com/api/v3/simple/price?ids={id}&vs_currencies={currency}"
/home/ubuntu/.openclaw/workspace/skills/crypto-price/scripts/get_price_chart.py:17:COINGECKO_OHLC_URL = "https://api.coingecko.com/api/v3/coins/{id}/ohlc?vs_currency={currency}&days=1"
/home/ubuntu/.openclaw/workspace/skills/crypto-price/scripts/get_price_chart.py:18:COINGECKO_SEARCH_URL = "https://api.coingecko.com/api/v3/search?query={query}"
/home/ubuntu/.openclaw/workspace/skills/crypto-price/scripts/get_price_chart.py:19:COINGECKO_MARKET_CHART_URL = "https://api.coingecko.com/api/v3/coins/{id}/market_chart?vs_currency={currency}&days=1"
/home/ubuntu/.openclaw/workspace/skills/crypto-price/scripts/get_price_chart.py:20:COINGECKO_MARKET_CHART_DAYS_URL = "https://api.coingecko.com/api/v3/coins/{id}/market_chart?vs_currency={currency}&days={days}"
/home/ubuntu/.openclaw/workspace/skills/crypto-price/scripts/get_price_chart.py:21:HYPERLIQUID_INFO_URL = "https://api.hyperliquid.xyz/info"
/home/ubuntu/.openclaw/workspace/skills/crypto-price/.clawhub/origin.json:3:  "registry": "https://clawhub.ai",
```

## crypto-watch

- 路径：/home/ubuntu/.openclaw/workspace/skills/crypto-watch
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-08 03:45:04 UTC（约 7 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 可执行文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/crypto-watch/scripts/crypto_watch.py
- 脚本文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/crypto-watch/scripts/crypto_watch.py
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/crypto-watch/references/OKX.md:5:- `GET https://www.okx.com/api/v5/market/candles?instId=<INST>&bar=15m&limit=300`
/home/ubuntu/.openclaw/workspace/skills/crypto-watch/scripts/crypto_watch.py:25:BINANCE_BASE = "https://api.binance.com"
/home/ubuntu/.openclaw/workspace/skills/crypto-watch/scripts/crypto_watch.py:26:OKX_BASE = "https://www.okx.com"
```

## db-readonly

- 路径：/home/ubuntu/.openclaw/workspace/skills/db-readonly
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-09 10:41:27 UTC（约 6 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 可执行文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/db-readonly/scripts/db_readonly.sh
- 脚本文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/db-readonly/scripts/db_readonly.sh
- 高风险关键字命中：无

## deepwiki

- 路径：/home/ubuntu/.openclaw/workspace/skills/deepwiki
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-06 15:37:07 UTC（约 9 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 脚本文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/deepwiki/scripts/deepwiki.js
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/deepwiki/SKILL.md:4:homepage: https://docs.devin.ai/work-with-devin/deepwiki-mcp
/home/ubuntu/.openclaw/workspace/skills/deepwiki/SKILL.md:44:- Base Server: `https://mcp.deepwiki.com/mcp`
/home/ubuntu/.openclaw/workspace/skills/deepwiki/scripts/deepwiki.js:15:const SSE_URL = 'https://mcp.deepwiki.com/sse';
/home/ubuntu/.openclaw/workspace/skills/deepwiki/scripts/deepwiki.js:39:            messageUrl = 'https://mcp.deepwiki.com' + data;
/home/ubuntu/.openclaw/workspace/skills/deepwiki/.clawhub/origin.json:3:  "registry": "https://clawhub.ai",
```

## deepwork-tracker

- 路径：/home/ubuntu/.openclaw/workspace/skills/deepwork-tracker
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-06 15:37:07 UTC（约 9 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/deepwork-tracker/SKILL.md:19:[ -d ~/clawd/deepwork-tracker/.git ] || git clone https://github.com/adunne09/deepwork-tracker.git ~/clawd/deepwork-tracker
/home/ubuntu/.openclaw/workspace/skills/deepwork-tracker/.clawhub/origin.json:3:  "registry": "https://clawhub.ai",
```

## find-skills

- 路径：/home/ubuntu/.openclaw/workspace/skills/find-skills
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-12 15:56:49 UTC（约 3 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/find-skills/SKILL.md:32:**Browse skills at:** https://skills.sh/
/home/ubuntu/.openclaw/workspace/skills/find-skills/SKILL.md:64:└ https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
/home/ubuntu/.openclaw/workspace/skills/find-skills/SKILL.md:84:Learn more: https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
/home/ubuntu/.openclaw/workspace/skills/find-skills/.clawhub/origin.json:3:  "registry": "https://clawhub.ai",
```

## github

- 路径：/home/ubuntu/.openclaw/workspace/skills/github
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-06 15:37:07 UTC（约 9 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/github/.clawhub/origin.json:3:  "registry": "https://clawhub.ai",
```

## gmail-auto-processor

- 路径：/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor
- SKILL.md：yes
- package.json：/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/package.json (name=gmail-auto-processor version=1.0.0)
- 最近文件修改：2026-02-10 05:23:29 UTC（约 5 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：执行外部命令(child_process/exec/spawn)
- 可执行文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/gmail-processor.js
  - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/archive-promotions.sh
- 脚本文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/archive-promotions.js
  - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/gmail-processor.js
  - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/generate-report.js
  - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/archive-promotions.sh
  - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index-anxiety-free.js
  - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/smart-run.js
  - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index-fixed.js
  - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index.js
  - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/task-monitor.js
  - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/batch-process.js
  - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/gmail-quick.js
  - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/test-archive.js
  - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/subagent-run.js
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/archive-promotions.js:1:const { execSync } = require('child_process');
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/gmail-processor.js:7:const { execSync } = require('child_process');
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index-anxiety-free.js:8:const { execSync } = require('child_process');
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/smart-run.js:8:const { execSync } = require('child_process');
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index-fixed.js:8:const { execSync } = require('child_process');
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index.js:10:const { execSync } = require('child_process');
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/task-monitor.js:3:const { execSync } = require('child_process');
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/batch-process.js:8:const { execSync } = require('child_process');
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/gmail-quick.js:6:const { execSync } = require('child_process');
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/test-archive.js:7:const { execSync } = require('child_process');
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/subagent-run.js:8:const { execSync } = require('child_process');
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/archive-promotions.js:1:const { execSync } = require('child_process');
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/archive-promotions.js:9:    const result = execSync('mcporter call --server google-workspace --tool "gmail.search" query="is:unread category:promotions" maxResults=100', { encoding: 'utf8' });
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/archive-promotions.js:21:    execSync(`mcporter call --server google-workspace --tool "gmail.modify" messageId="${msgId}" removeLabelIds='["INBOX","UNREAD"]'`, { encoding: 'utf8', timeout: 10000 });
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/archive-promotions.js:32:    const result = execSync('mcporter call --server google-workspace --tool "gmail.search" query="is:unread" maxResults=1', { encoding: 'utf8' });
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/gmail-processor.js:7:const { execSync } = require('child_process');
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/gmail-processor.js:45:    const result = execSync(cmd, { encoding: 'utf-8', timeout: 30000 });
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index-anxiety-free.js:8:const { execSync } = require('child_process');
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index-anxiety-free.js:47:    const result = execSync(cmd, { encoding: 'utf8', timeout: timeoutMs });
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index-anxiety-free.js:58:    execSync(cmd, { encoding: 'utf8', timeout: 10000 });
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index-anxiety-free.js:69:    execSync(cmd, { encoding: 'utf8', timeout: 10000 });
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/smart-run.js:8:const { execSync } = require('child_process');
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/smart-run.js:17:    const result = execSync(cmd, { encoding: 'utf8', timeout: 10000 });
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/smart-run.js:28:    const result = execSync(cmd, { encoding: 'utf8', timeout: 120000 });
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index-fixed.js:8:const { execSync } = require('child_process');
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index-fixed.js:43:    const result = execSync(cmd, { encoding: 'utf8', timeout: timeoutMs });
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index-fixed.js:55:    execSync(cmd, { encoding: 'utf8', timeout: 10000 });
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index-fixed.js:66:    execSync(cmd, { encoding: 'utf8', timeout: 10000 });
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index.js:10:const { execSync } = require('child_process');
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index.js:64:    const result = execSync(cmd, { encoding: 'utf8', timeout: 30000 });
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index.js:74:    execSync(cmd, { encoding: 'utf8', timeout: 10000 });
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index.js:84:    execSync(cmd, { encoding: 'utf8', timeout: 10000 });
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index.js:95:    execSync(cmd, { encoding: 'utf8', timeout: 10000 });
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/task-monitor.js:3:const { execSync } = require('child_process');
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/batch-process.js:8:const { execSync } = require('child_process');
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/batch-process.js:16:    const result = execSync(cmd, { encoding: 'utf8', timeout: 10000 });
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/batch-process.js:27:    const result = execSync(cmd, { encoding: 'utf8', timeout: 120000 });
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/batch-process.js:84:    execSync('sleep 2');
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/gmail-quick.js:6:const { execSync } = require('child_process');
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/gmail-quick.js:32:    const result = execSync(cmd, { encoding: 'utf-8', timeout: 30000 });
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/test-archive.js:7:const { execSync } = require('child_process');
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/test-archive.js:20:    const result = execSync(cmd, { encoding: 'utf8', timeout: 30000 });
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/test-archive.js:31:    execSync(cmd, { encoding: 'utf8', timeout: 15000 });
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/subagent-run.js:8:const { execSync } = require('child_process');
/home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/subagent-run.js:16:    const result = execSync(cmd, { encoding: 'utf8', timeout: 10000 });
```

## google-workspace-mcp

- 路径：/home/ubuntu/.openclaw/workspace/skills/google-workspace-mcp
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-08 07:52:17 UTC（约 7 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/google-workspace-mcp/.clawhub/origin.json:3:  "registry": "https://clawhub.ai",
```

## imap-smtp-email

- 路径：/home/ubuntu/.openclaw/workspace/skills/imap-smtp-email
- SKILL.md：yes
- package.json：/home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/package.json (name=imap-smtp-email-skill version=1.0.0)
- 最近文件修改：2026-02-06 15:37:07 UTC（约 9 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：读取环境变量/密钥线索
- 脚本文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js
  - /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/imap.js
  - /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/setup.sh
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js:38:    host: process.env.SMTP_HOST,
/home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js:39:    port: parseInt(process.env.SMTP_PORT) || 587,
/home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js:40:    secure: process.env.SMTP_SECURE === 'true', // true for 465, false for other ports
/home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js:42:      user: process.env.SMTP_USER,
/home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js:43:      pass: process.env.SMTP_PASS,
/home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js:46:      rejectUnauthorized: process.env.SMTP_REJECT_UNAUTHORIZED !== 'false',
/home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js:70:    from: options.from || process.env.SMTP_FROM || process.env.SMTP_USER,
/home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js:125:      from: process.env.SMTP_FROM || process.env.SMTP_USER,
/home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js:126:      to: process.env.SMTP_USER, // Send to self
/home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/imap.js:23:const DEFAULT_MAILBOX = process.env.IMAP_MAILBOX || 'INBOX';
/home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/imap.js:50:    user: process.env.IMAP_USER,
/home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/imap.js:51:    password: process.env.IMAP_PASS,
/home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/imap.js:52:    host: process.env.IMAP_HOST || '127.0.0.1',
/home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/imap.js:53:    port: parseInt(process.env.IMAP_PORT) || 1143,
/home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/imap.js:54:    tls: process.env.IMAP_TLS === 'true',
/home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/imap.js:56:      rejectUnauthorized: process.env.IMAP_REJECT_UNAUTHORIZED !== 'false',
/home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/.clawhub/origin.json:3:  "registry": "https://clawhub.ai",
```

## larksuite-wiki

- 路径：/home/ubuntu/.openclaw/workspace/skills/larksuite-wiki
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-06 17:04:37 UTC（约 8 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：读取环境变量/密钥线索
- 可执行文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/larksuite-wiki/larksuite-wiki.py
  - /home/ubuntu/.openclaw/workspace/skills/larksuite-wiki/larksuite-wiki
- 脚本文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/larksuite-wiki/larksuite-wiki.py
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/larksuite-wiki/larksuite-wiki.py:20:        self.app_secret = app_secret or os.getenv("LARK_APP_SECRET") or "xtSodRRMmiU1R4oikynlFbBoEu3T2Wgo"
/home/ubuntu/.openclaw/workspace/skills/larksuite-wiki/larksuite-wiki.py:24:            print("Error: LARK_APP_ID and LARK_APP_SECRET must be set")
/home/ubuntu/.openclaw/workspace/skills/larksuite-wiki/larksuite-wiki.py:25:            print("Run: export LARK_APP_ID='cli_xxx' && export LARK_APP_SECRET='xxx'")
/home/ubuntu/.openclaw/workspace/skills/larksuite-wiki/SKILL.md:11:        "requires": { "env": ["LARK_APP_ID", "LARK_APP_SECRET"] },
/home/ubuntu/.openclaw/workspace/skills/larksuite-wiki/SKILL.md:32:   export LARK_APP_SECRET="xxxxxxxx"
/home/ubuntu/.openclaw/workspace/skills/larksuite-wiki/README.md:20:export LARK_APP_SECRET="xxxxxxxx"
/home/ubuntu/.openclaw/workspace/skills/larksuite-wiki/references/api-reference.md:7:export LARK_APP_SECRET="xtSodRRMmiU1R4oikynlFbBoEu3T2Wgo"
/home/ubuntu/.openclaw/workspace/skills/larksuite-wiki/larksuite-wiki:6:if [ -z "$LARK_APP_ID" ] || [ -z "$LARK_APP_SECRET" ]; then
/home/ubuntu/.openclaw/workspace/skills/larksuite-wiki/larksuite-wiki:10:        LARK_APP_SECRET=$(grep "App Secret" ~/.openclaw/workspace/LOCAL_CONFIG.md | sed 's/.*`\(.*\)`/\1/')
/home/ubuntu/.openclaw/workspace/skills/larksuite-wiki/larksuite-wiki:15:if [ -z "$LARK_APP_ID" ] || [ -z "$LARK_APP_SECRET" ]; then
/home/ubuntu/.openclaw/workspace/skills/larksuite-wiki/larksuite-wiki:16:    echo "Error: LARK_APP_ID and LARK_APP_SECRET not set."
/home/ubuntu/.openclaw/workspace/skills/larksuite-wiki/larksuite-wiki:22:export LARK_APP_SECRET
/home/ubuntu/.openclaw/workspace/skills/larksuite-wiki/larksuite-wiki.py:14:LARK_API_BASE = "https://open.larksuite.com/open-apis"
/home/ubuntu/.openclaw/workspace/skills/larksuite-wiki/SKILL.md:4:homepage: https://open.larksuite.com
/home/ubuntu/.openclaw/workspace/skills/larksuite-wiki/SKILL.md:23:1. Create a Lark/Feishu app at https://open.larksuite.com/console
/home/ubuntu/.openclaw/workspace/skills/larksuite-wiki/SKILL.md:101:# https://xxx.larksuite.com/wiki/TDCZweBJ2iMFO4kI1LAlSE62gnd
/home/ubuntu/.openclaw/workspace/skills/larksuite-wiki/SKILL.md:122:- Lark Open Platform: https://open.larksuite.com/
/home/ubuntu/.openclaw/workspace/skills/larksuite-wiki/SKILL.md:123:- Wiki API: https://open.larksuite.com/document/uAjLw4CM/ukTMukTMukTM/reference/wiki-v1/space/overview
/home/ubuntu/.openclaw/workspace/skills/larksuite-wiki/SKILL.md:124:- Docx API: https://open.larksuite.com/document/uAjLw4CM/ukTMukTMukTM/reference/docx-v1/document/overview
/home/ubuntu/.openclaw/workspace/skills/larksuite-wiki/README.md:18:# Configure credentials (get from https://open.larksuite.com/console)
/home/ubuntu/.openclaw/workspace/skills/larksuite-wiki/README.md:28:1. Create a Lark app at https://open.larksuite.com/console
```

## obsidian-integration

- 路径：/home/ubuntu/.openclaw/workspace/skills/obsidian-integration
- SKILL.md：yes
- package.json：/home/ubuntu/.openclaw/workspace/skills/obsidian-integration/package.json (name=obsidian-integration version=1.0.0)
- 最近文件修改：2026-02-09 08:28:02 UTC（约 6 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：执行外部命令(child_process/exec/spawn)
- 脚本文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/obsidian-integration/index.js
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/obsidian-integration/index.js:3:const { execSync } = require('child_process');
/home/ubuntu/.openclaw/workspace/skills/obsidian-integration/index.js:3:const { execSync } = require('child_process');
```

## reminder

- 路径：/home/ubuntu/.openclaw/workspace/skills/reminder
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-12 17:54:29 UTC（约 2 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 可执行文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/reminder/scripts/reminder-scheduler.sh
- 脚本文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/reminder/scripts/reminder-scheduler.sh
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/reminder/.clawhub/origin.json:3:  "registry": "https://clawhub.ai",
```

## self-reflection

- 路径：/home/ubuntu/.openclaw/workspace/skills/self-reflection
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-06 15:37:07 UTC（约 9 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/self-reflection/SKILL.md:95:Created by [hopyky](https://github.com/hopyky)
/home/ubuntu/.openclaw/workspace/skills/self-reflection/README.md:80:git clone https://github.com/hopyky/self-reflection.git ~/.openclaw/skills/self-reflection
/home/ubuntu/.openclaw/workspace/skills/self-reflection/README.md:288:Created by [hopyky](https://github.com/hopyky)
/home/ubuntu/.openclaw/workspace/skills/self-reflection/README.md:292:Issues and PRs welcome at [github.com/hopyky/self-reflection](https://github.com/hopyky/self-reflection)
/home/ubuntu/.openclaw/workspace/skills/self-reflection/.clawhub/origin.json:3:  "registry": "https://clawhub.ai",
```

## skill-vetter

- 路径：/home/ubuntu/.openclaw/workspace/skills/skill-vetter
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-06 15:37:07 UTC（约 9 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**high**
- 理由：网络请求/下载(curl/wget/fetch/axios) 潜在提权(sudo/setuid) 涉及SSH密钥/authorized_keys
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/skill-vetter/SKILL.md:112:curl -s "https://api.github.com/repos/OWNER/REPO" | jq '{stars: .stargazers_count, forks: .forks_count, updated: .updated_at}'
/home/ubuntu/.openclaw/workspace/skills/skill-vetter/SKILL.md:115:curl -s "https://api.github.com/repos/OWNER/REPO/contents/skills/SKILL_NAME" | jq '.[].name'
/home/ubuntu/.openclaw/workspace/skills/skill-vetter/SKILL.md:118:curl -s "https://raw.githubusercontent.com/OWNER/REPO/main/skills/SKILL_NAME/SKILL.md"
/home/ubuntu/.openclaw/workspace/skills/skill-vetter/SKILL.md:38:• curl/wget to unknown URLs
/home/ubuntu/.openclaw/workspace/skills/skill-vetter/SKILL.md:49:• Requests elevated/sudo permissions
/home/ubuntu/.openclaw/workspace/skills/skill-vetter/SKILL.md:41:• Reads ~/.ssh, ~/.aws, ~/.config without clear reason
/home/ubuntu/.openclaw/workspace/skills/skill-vetter/SKILL.md:112:curl -s "https://api.github.com/repos/OWNER/REPO" | jq '{stars: .stargazers_count, forks: .forks_count, updated: .updated_at}'
/home/ubuntu/.openclaw/workspace/skills/skill-vetter/SKILL.md:115:curl -s "https://api.github.com/repos/OWNER/REPO/contents/skills/SKILL_NAME" | jq '.[].name'
/home/ubuntu/.openclaw/workspace/skills/skill-vetter/SKILL.md:118:curl -s "https://raw.githubusercontent.com/OWNER/REPO/main/skills/SKILL_NAME/SKILL.md"
/home/ubuntu/.openclaw/workspace/skills/skill-vetter/.clawhub/origin.json:3:  "registry": "https://clawhub.ai",
/home/ubuntu/.openclaw/workspace/skills/skill-vetter/SKILL.md:118:curl -s "https://raw.githubusercontent.com/OWNER/REPO/main/skills/SKILL_NAME/SKILL.md"
```

## stock_analysis

- 路径：/home/ubuntu/.openclaw/workspace/skills/stock_analysis
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-13 07:00:53 UTC（约 2 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**medium**
- 理由：网络请求/下载(curl/wget/fetch/axios) 潜在提权(sudo/setuid)
- 可执行文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/stock_analysis/scripts/analyze_stock.sh
  - /home/ubuntu/.openclaw/workspace/skills/stock_analysis/scripts/install_deps.sh
  - /home/ubuntu/.openclaw/workspace/skills/stock_analysis/scripts/stock_analyzer.py
- 脚本文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/stock_analysis/scripts/analyze_stock.sh
  - /home/ubuntu/.openclaw/workspace/skills/stock_analysis/scripts/install_deps.sh
  - /home/ubuntu/.openclaw/workspace/skills/stock_analysis/scripts/stock_analyzer.py
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/scripts/install_deps.sh:36:echo "1) curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/PRE_RELEASE_CHECKLIST.md:13:sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv git
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/PRE_RELEASE_CHECKLIST.md:16:无 sudo 降级：
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/SKILL.md:46:If your system lacks `python3-pip` or you don't have sudo access, the script will suggest fallback options:
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/SKILL.md:49:# User-level installation without sudo
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/scripts/install_deps.sh:23:  echo "sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv git"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/scripts/install_deps.sh:35:echo "\n无法 sudo 时的降级路径（推荐）："
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/SKILL.md:175:- https://github.com/ZhuLinsen/daily_stock_analysis
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/000592.SZ_20260213T005102Z.json:24:      "link": "https://data.eastmoney.com/notices/detail/SZ000592/AN202601301818584297.html"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/000592.SZ_20260213T005102Z.json:29:      "link": "https://data.eastmoney.com/notices/detail/SZ000592/AN202601201818152757.html"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/000592.SZ_20260213T005102Z.json:34:      "link": "https://data.eastmoney.com/notices/detail/SZ000592/AN202601191818114837.html"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/000592.SZ_20260213T005102Z.json:39:      "link": "https://data.eastmoney.com/notices/detail/SZ000592/AN202601121816953303.html"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/000592.SZ_20260213T005102Z.json:44:      "link": "https://data.eastmoney.com/notices/detail/SZ000592/AN202512301811370113.html"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/000547.SZ_20260213T005101Z.json:24:      "link": "https://data.eastmoney.com/notices/detail/SZ000547/AN202602101819860344.html"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/000547.SZ_20260213T005101Z.json:29:      "link": "https://data.eastmoney.com/notices/detail/SZ000547/AN202602101819860343.html"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/000547.SZ_20260213T005101Z.json:34:      "link": "https://data.eastmoney.com/notices/detail/SZ000547/AN202602031819647634.html"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/000547.SZ_20260213T005101Z.json:39:      "link": "https://data.eastmoney.com/notices/detail/SZ000547/AN202601301818587545.html"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/000547.SZ_20260213T005101Z.json:44:      "link": "https://data.eastmoney.com/notices/detail/SZ000547/AN202601271818468013.html"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/002230_20260211T090410Z.json:24:      "link": "https://data.eastmoney.com/notices/detail/SZ002230/AN202601281818505521.html"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/002230_20260211T090410Z.json:29:      "link": "https://data.eastmoney.com/notices/detail/SZ002230/AN202601091816882472.html"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/002230_20260211T090410Z.json:34:      "link": "https://data.eastmoney.com/notices/detail/SZ002230/AN202601091816882481.html"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/002230_20260211T090410Z.json:39:      "link": "https://data.eastmoney.com/notices/detail/SZ002230/AN202601091816882480.html"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/002230_20260211T090410Z.json:44:      "link": "https://data.eastmoney.com/notices/detail/SZ002230/AN202601091816882475.html"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/002291.SZ_20260213T005104Z.json:24:      "link": "https://data.eastmoney.com/notices/detail/SZ002291/AN202602111819880390.html"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/002291.SZ_20260213T005104Z.json:29:      "link": "https://data.eastmoney.com/notices/detail/SZ002291/AN202602111819880391.html"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/002291.SZ_20260213T005104Z.json:34:      "link": "https://data.eastmoney.com/notices/detail/SZ002291/AN202601301818590178.html"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/002291.SZ_20260213T005104Z.json:39:      "link": "https://data.eastmoney.com/notices/detail/SZ002291/AN202601291818544111.html"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/002291.SZ_20260213T005104Z.json:44:      "link": "https://data.eastmoney.com/notices/detail/SZ002291/AN202601261818428882.html"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/300077_20260211T084434Z.json:24:      "link": "https://data.eastmoney.com/notices/detail/SZ300077/AN202602101819859725.html"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/300077_20260211T084434Z.json:29:      "link": "https://data.eastmoney.com/notices/detail/SZ300077/AN202601291818547592.html"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/300077_20260211T084434Z.json:34:      "link": "https://data.eastmoney.com/notices/detail/SZ300077/AN202601271818471511.html"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/300077_20260211T084434Z.json:39:      "link": "https://data.eastmoney.com/notices/detail/SZ300077/AN202601161817861928.html"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/300077_20260211T084434Z.json:44:      "link": "https://data.eastmoney.com/notices/detail/SZ300077/AN202601161817861931.html"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/references/upstream-README-snippet.md:1:来源：`https://github.com/ZhuLinsen/daily_stock_analysis`
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/references/upstream.md:3:上游项目：`https://github.com/ZhuLinsen/daily_stock_analysis.git`
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/scripts/install_deps.sh:36:echo "1) curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/scripts/stock_analyzer.py:132:    url = f"https://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields={fields}"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/scripts/stock_analyzer.py:166:    url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/scripts/stock_analyzer.py:191:    url = "https://np-anotice-stock.eastmoney.com/api/security/ann"
/home/ubuntu/.openclaw/workspace/skills/stock_analysis/scripts/stock_analyzer.py:198:        link = f"https://data.eastmoney.com/notices/detail/{market}{s}/{art_code}.html"
```

## task-status

- 路径：/home/ubuntu/.openclaw/workspace/skills/task-status
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-06 15:37:07 UTC（约 9 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：读取环境变量/密钥线索
- 脚本文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/task-status/scripts/monitor_task.py
  - /home/ubuntu/.openclaw/workspace/skills/task-status/scripts/test_send_status.py
  - /home/ubuntu/.openclaw/workspace/skills/task-status/scripts/send_status_websocket.py
  - /home/ubuntu/.openclaw/workspace/skills/task-status/scripts/send_status_with_logging.py
  - /home/ubuntu/.openclaw/workspace/skills/task-status/scripts/send_status.py
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/task-status/scripts/send_status_websocket.py:48:    gateway_token = os.environ.get("CLAWDBOT_GATEWAY_TOKEN")
/home/ubuntu/.openclaw/workspace/skills/task-status/scripts/send_status_websocket.py:52:        print(f"✗ CLAWDBOT_GATEWAY_TOKEN not found", file=sys.stderr)
/home/ubuntu/.openclaw/workspace/skills/task-status/scripts/send_status_with_logging.py:102:    gateway_token = os.environ.get("CLAWDBOT_GATEWAY_TOKEN")
/home/ubuntu/.openclaw/workspace/skills/task-status/scripts/send_status.py:77:    gateway_token = os.environ.get("CLAWDBOT_GATEWAY_TOKEN")
/home/ubuntu/.openclaw/workspace/skills/task-status/.clawhub/origin.json:3:  "registry": "https://clawhub.ai",
```

## technews

- 路径：/home/ubuntu/.openclaw/workspace/skills/technews
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-06 15:37:07 UTC（约 9 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 脚本文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/technews/scripts/article_fetcher.py
  - /home/ubuntu/.openclaw/workspace/skills/technews/scripts/techmeme_scraper.py
  - /home/ubuntu/.openclaw/workspace/skills/technews/scripts/social_reactions.py
  - /home/ubuntu/.openclaw/workspace/skills/technews/scripts/technews.py
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/technews/README.md:18:git clone https://github.com/yourusername/technews-skill.git
/home/ubuntu/.openclaw/workspace/skills/technews/scripts/techmeme_scraper.py:13:TECHMEME_RSS = "https://www.techmeme.com/feed.xml"
/home/ubuntu/.openclaw/workspace/skills/technews/scripts/social_reactions.py:13:TWITTER_SEARCH = "https://nitter.net/search"
/home/ubuntu/.openclaw/workspace/skills/technews/scripts/social_reactions.py:53:    hn_api = "https://hn.algolia.com/api/v1/search"
/home/ubuntu/.openclaw/workspace/skills/technews/scripts/social_reactions.py:73:                    "hn_url": f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
/home/ubuntu/.openclaw/workspace/skills/technews/.clawhub/origin.json:3:  "registry": "https://clawhub.ai",
```

## trading-journal

- 路径：/home/ubuntu/.openclaw/workspace/skills/trading-journal
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-08 03:43:57 UTC（约 7 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 可执行文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/trading-journal/scripts/trade-log.sh
- 脚本文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/trading-journal/scripts/trade-log.sh
- 高风险关键字命中：无

## ui-ux-pro-max

- 路径：/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-06 15:37:07 UTC（约 9 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**medium**
- 理由：网络请求/下载(curl/wget/fetch/axios) 潜在提权(sudo/setuid) 读取环境变量/密钥线索
- 脚本文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/scripts/design_system.py
  - /home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/scripts/core.py
  - /home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/scripts/__init__.py
  - /home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/scripts/search.py
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/references/upstream-skill-content.md:26:```powershell
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/references/upstream-README.md:304:sudo apt update && sudo apt install python3
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/references/upstream-skill-content.md:22:sudo apt update && sudo apt install python3
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/stacks/nextjs.csv:37:36,Environment,Validate env vars,Check required env vars exist,Validate on startup,Undefined env at runtime,if (!process.env.DATABASE_URL) throw,process.env.DATABASE_URL (might be undefined),High,
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/stacks/nuxtjs.csv:53:52,Environment,Use runtimeConfig for env vars,Access environment variables safely,runtimeConfig in nuxt.config,process.env directly,"runtimeConfig: { apiSecret: '', public: { apiBase: '' } }",process.env.API_SECRET in components,High,https://nuxt.com/docs/guide/going-further/runtime-config
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/stacks/nuxtjs.csv:55:54,Environment,Access public config with useRuntimeConfig,Get public config in components,useRuntimeConfig().public,Direct process.env access,const config = useRuntimeConfig(); config.public.apiBase,process.env.NUXT_PUBLIC_API_BASE,High,https://nuxt.com/docs/api/composables/use-runtime-config
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/data/stacks/nextjs.csv:37:36,Environment,Validate env vars,Check required env vars exist,Validate on startup,Undefined env at runtime,if (!process.env.DATABASE_URL) throw,process.env.DATABASE_URL (might be undefined),High,
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/data/stacks/nuxtjs.csv:53:52,Environment,Use runtimeConfig for env vars,Access environment variables safely,runtimeConfig in nuxt.config,process.env directly,"runtimeConfig: { apiSecret: '', public: { apiBase: '' } }",process.env.API_SECRET in components,High,https://nuxt.com/docs/guide/going-further/runtime-config
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/data/stacks/nuxtjs.csv:55:54,Environment,Access public config with useRuntimeConfig,Get public config in components,useRuntimeConfig().public,Direct process.env access,const config = useRuntimeConfig(); config.public.apiBase,process.env.NUXT_PUBLIC_API_BASE,High,https://nuxt.com/docs/api/composables/use-runtime-config
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/stacks/nextjs.csv:36:35,Environment,Use NEXT_PUBLIC prefix,Client-accessible env vars need prefix,NEXT_PUBLIC_ for client vars,Server vars exposed to client,NEXT_PUBLIC_API_URL,API_SECRET in client code,High,https://nextjs.org/docs/app/building-your-application/configuring/environment-variables
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/stacks/nuxtjs.csv:53:52,Environment,Use runtimeConfig for env vars,Access environment variables safely,runtimeConfig in nuxt.config,process.env directly,"runtimeConfig: { apiSecret: '', public: { apiBase: '' } }",process.env.API_SECRET in components,High,https://nuxt.com/docs/guide/going-further/runtime-config
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/stacks/nuxtjs.csv:54:53,Environment,Use NUXT_ prefix for env override,Override config with environment variables,NUXT_API_SECRET NUXT_PUBLIC_API_BASE,Custom env var names,NUXT_PUBLIC_API_BASE=https://api.example.com,API_BASE=https://api.example.com,High,https://nuxt.com/docs/guide/going-further/runtime-config
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/stacks/astro.csv:23:22,Data,Use environment variables correctly,Import.meta.env for env vars,PUBLIC_ prefix for client vars,Expose secrets to client,import.meta.env.PUBLIC_API_URL,import.meta.env.SECRET in client,High,https://docs.astro.build/en/guides/environment-variables/
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/data/stacks/nextjs.csv:36:35,Environment,Use NEXT_PUBLIC prefix,Client-accessible env vars need prefix,NEXT_PUBLIC_ for client vars,Server vars exposed to client,NEXT_PUBLIC_API_URL,API_SECRET in client code,High,https://nextjs.org/docs/app/building-your-application/configuring/environment-variables
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/data/stacks/nuxtjs.csv:53:52,Environment,Use runtimeConfig for env vars,Access environment variables safely,runtimeConfig in nuxt.config,process.env directly,"runtimeConfig: { apiSecret: '', public: { apiBase: '' } }",process.env.API_SECRET in components,High,https://nuxt.com/docs/guide/going-further/runtime-config
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/data/stacks/nuxtjs.csv:54:53,Environment,Use NUXT_ prefix for env override,Override config with environment variables,NUXT_API_SECRET NUXT_PUBLIC_API_BASE,Custom env var names,NUXT_PUBLIC_API_BASE=https://api.example.com,API_BASE=https://api.example.com,High,https://nuxt.com/docs/guide/going-further/runtime-config
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/data/stacks/astro.csv:23:22,Data,Use environment variables correctly,Import.meta.env for env vars,PUBLIC_ prefix for client vars,Expose secrets to client,import.meta.env.PUBLIC_API_URL,import.meta.env.SECRET in client,High,https://docs.astro.build/en/guides/environment-variables/
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/stacks/astro.csv:50:49,Security,Use HTTPS in production,Secure connections,HTTPS for all production sites,HTTP in production,https://example.com,http://example.com,High,
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/data/stacks/astro.csv:50:49,Security,Use HTTPS in production,Secure connections,HTTPS for all production sites,HTTP in production,https://example.com,http://example.com,High,
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:2:1,Classic Elegant,"Serif + Sans",Playfair Display,Inter,"elegant, luxury, sophisticated, timeless, premium, editorial","Luxury brands, fashion, spa, beauty, editorial, magazines, high-end e-commerce","https://fonts.google.com/share?selection.family=Inter:wght@300;400;500;600;700|Playfair+Display:wght@400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap');","fontFamily: { serif: ['Playfair Display', 'serif'], sans: ['Inter', 'sans-serif'] }","High contrast between elegant heading and clean body. Perfect for luxury/premium."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:3:2,Modern Professional,"Sans + Sans",Poppins,Open Sans,"modern, professional, clean, corporate, friendly, approachable","SaaS, corporate sites, business apps, startups, professional services","https://fonts.google.com/share?selection.family=Open+Sans:wght@300;400;500;600;700|Poppins:wght@400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');","fontFamily: { heading: ['Poppins', 'sans-serif'], body: ['Open Sans', 'sans-serif'] }","Geometric Poppins for headings, humanist Open Sans for readability."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:4:3,Tech Startup,"Sans + Sans",Space Grotesk,DM Sans,"tech, startup, modern, innovative, bold, futuristic","Tech companies, startups, SaaS, developer tools, AI products","https://fonts.google.com/share?selection.family=DM+Sans:wght@400;500;700|Space+Grotesk:wght@400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');","fontFamily: { heading: ['Space Grotesk', 'sans-serif'], body: ['DM Sans', 'sans-serif'] }","Space Grotesk has unique character, DM Sans is highly readable."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:5:4,Editorial Classic,"Serif + Serif",Cormorant Garamond,Libre Baskerville,"editorial, classic, literary, traditional, refined, bookish","Publishing, blogs, news sites, literary magazines, book covers","https://fonts.google.com/share?selection.family=Cormorant+Garamond:wght@400;500;600;700|Libre+Baskerville:wght@400;700","@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Libre+Baskerville:wght@400;700&display=swap');","fontFamily: { heading: ['Cormorant Garamond', 'serif'], body: ['Libre Baskerville', 'serif'] }","All-serif pairing for traditional editorial feel."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:6:5,Minimal Swiss,"Sans + Sans",Inter,Inter,"minimal, clean, swiss, functional, neutral, professional","Dashboards, admin panels, documentation, enterprise apps, design systems","https://fonts.google.com/share?selection.family=Inter:wght@300;400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');","fontFamily: { sans: ['Inter', 'sans-serif'] }","Single font family with weight variations. Ultimate simplicity."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:7:6,Playful Creative,"Display + Sans",Fredoka,Nunito,"playful, friendly, fun, creative, warm, approachable","Children's apps, educational, gaming, creative tools, entertainment","https://fonts.google.com/share?selection.family=Fredoka:wght@400;500;600;700|Nunito:wght@300;400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&family=Nunito:wght@300;400;500;600;700&display=swap');","fontFamily: { heading: ['Fredoka', 'sans-serif'], body: ['Nunito', 'sans-serif'] }","Rounded, friendly fonts perfect for playful UIs."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:8:7,Bold Statement,"Display + Sans",Bebas Neue,Source Sans 3,"bold, impactful, strong, dramatic, modern, headlines","Marketing sites, portfolios, agencies, event pages, sports","https://fonts.google.com/share?selection.family=Bebas+Neue|Source+Sans+3:wght@300;400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Source+Sans+3:wght@300;400;500;600;700&display=swap');","fontFamily: { display: ['Bebas Neue', 'sans-serif'], body: ['Source Sans 3', 'sans-serif'] }","Bebas Neue for large headlines only. All-caps display font."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:9:8,Wellness Calm,"Serif + Sans",Lora,Raleway,"calm, wellness, health, relaxing, natural, organic","Health apps, wellness, spa, meditation, yoga, organic brands","https://fonts.google.com/share?selection.family=Lora:wght@400;500;600;700|Raleway:wght@300;400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&family=Raleway:wght@300;400;500;600;700&display=swap');","fontFamily: { serif: ['Lora', 'serif'], sans: ['Raleway', 'sans-serif'] }","Lora's organic curves with Raleway's elegant simplicity."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:10:9,Developer Mono,"Mono + Sans",JetBrains Mono,IBM Plex Sans,"code, developer, technical, precise, functional, hacker","Developer tools, documentation, code editors, tech blogs, CLI apps","https://fonts.google.com/share?selection.family=IBM+Plex+Sans:wght@300;400;500;600;700|JetBrains+Mono:wght@400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');","fontFamily: { mono: ['JetBrains Mono', 'monospace'], sans: ['IBM Plex Sans', 'sans-serif'] }","JetBrains for code, IBM Plex for UI. Developer-focused."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:11:10,Retro Vintage,"Display + Serif",Abril Fatface,Merriweather,"retro, vintage, nostalgic, dramatic, decorative, bold","Vintage brands, breweries, restaurants, creative portfolios, posters","https://fonts.google.com/share?selection.family=Abril+Fatface|Merriweather:wght@300;400;700","@import url('https://fonts.googleapis.com/css2?family=Abril+Fatface&family=Merriweather:wght@300;400;700&display=swap');","fontFamily: { display: ['Abril Fatface', 'serif'], body: ['Merriweather', 'serif'] }","Abril Fatface for hero headlines only. High-impact vintage feel."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:12:11,Geometric Modern,"Sans + Sans",Outfit,Work Sans,"geometric, modern, clean, balanced, contemporary, versatile","General purpose, portfolios, agencies, modern brands, landing pages","https://fonts.google.com/share?selection.family=Outfit:wght@300;400;500;600;700|Work+Sans:wght@300;400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Work+Sans:wght@300;400;500;600;700&display=swap');","fontFamily: { heading: ['Outfit', 'sans-serif'], body: ['Work Sans', 'sans-serif'] }","Both geometric but Outfit more distinctive for headings."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:13:12,Luxury Serif,"Serif + Sans",Cormorant,Montserrat,"luxury, high-end, fashion, elegant, refined, premium","Fashion brands, luxury e-commerce, jewelry, high-end services","https://fonts.google.com/share?selection.family=Cormorant:wght@400;500;600;700|Montserrat:wght@300;400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=Cormorant:wght@400;500;600;700&family=Montserrat:wght@300;400;500;600;700&display=swap');","fontFamily: { serif: ['Cormorant', 'serif'], sans: ['Montserrat', 'sans-serif'] }","Cormorant's elegance with Montserrat's geometric precision."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:14:13,Friendly SaaS,"Sans + Sans",Plus Jakarta Sans,Plus Jakarta Sans,"friendly, modern, saas, clean, approachable, professional","SaaS products, web apps, dashboards, B2B, productivity tools","https://fonts.google.com/share?selection.family=Plus+Jakarta+Sans:wght@300;400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');","fontFamily: { sans: ['Plus Jakarta Sans', 'sans-serif'] }","Single versatile font. Modern alternative to Inter."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:15:14,News Editorial,"Serif + Sans",Newsreader,Roboto,"news, editorial, journalism, trustworthy, readable, informative","News sites, blogs, magazines, journalism, content-heavy sites","https://fonts.google.com/share?selection.family=Newsreader:wght@400;500;600;700|Roboto:wght@300;400;500;700","@import url('https://fonts.googleapis.com/css2?family=Newsreader:wght@400;500;600;700&family=Roboto:wght@300;400;500;700&display=swap');","fontFamily: { serif: ['Newsreader', 'serif'], sans: ['Roboto', 'sans-serif'] }","Newsreader designed for long-form reading. Roboto for UI."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:16:15,Handwritten Charm,"Script + Sans",Caveat,Quicksand,"handwritten, personal, friendly, casual, warm, charming","Personal blogs, invitations, creative portfolios, lifestyle brands","https://fonts.google.com/share?selection.family=Caveat:wght@400;500;600;700|Quicksand:wght@300;400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400;500;600;700&family=Quicksand:wght@300;400;500;600;700&display=swap');","fontFamily: { script: ['Caveat', 'cursive'], sans: ['Quicksand', 'sans-serif'] }","Use Caveat sparingly for accents. Quicksand for body."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:17:16,Corporate Trust,"Sans + Sans",Lexend,Source Sans 3,"corporate, trustworthy, accessible, readable, professional, clean","Enterprise, government, healthcare, finance, accessibility-focused","https://fonts.google.com/share?selection.family=Lexend:wght@300;400;500;600;700|Source+Sans+3:wght@300;400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&family=Source+Sans+3:wght@300;400;500;600;700&display=swap');","fontFamily: { heading: ['Lexend', 'sans-serif'], body: ['Source Sans 3', 'sans-serif'] }","Lexend designed for readability. Excellent accessibility."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:18:17,Brutalist Raw,"Mono + Mono",Space Mono,Space Mono,"brutalist, raw, technical, monospace, minimal, stark","Brutalist designs, developer portfolios, experimental, tech art","https://fonts.google.com/share?selection.family=Space+Mono:wght@400;700","@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap');","fontFamily: { mono: ['Space Mono', 'monospace'] }","All-mono for raw brutalist aesthetic. Limited weights."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:19:18,Fashion Forward,"Sans + Sans",Syne,Manrope,"fashion, avant-garde, creative, bold, artistic, edgy","Fashion brands, creative agencies, art galleries, design studios","https://fonts.google.com/share?selection.family=Manrope:wght@300;400;500;600;700|Syne:wght@400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700&family=Syne:wght@400;500;600;700&display=swap');","fontFamily: { heading: ['Syne', 'sans-serif'], body: ['Manrope', 'sans-serif'] }","Syne's unique character for headlines. Manrope for readability."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:20:19,Soft Rounded,"Sans + Sans",Varela Round,Nunito Sans,"soft, rounded, friendly, approachable, warm, gentle","Children's products, pet apps, friendly brands, wellness, soft UI","https://fonts.google.com/share?selection.family=Nunito+Sans:wght@300;400;500;600;700|Varela+Round","@import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@300;400;500;600;700&family=Varela+Round&display=swap');","fontFamily: { heading: ['Varela Round', 'sans-serif'], body: ['Nunito Sans', 'sans-serif'] }","Both rounded and friendly. Perfect for soft UI designs."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:21:20,Premium Sans,"Sans + Sans",Satoshi,General Sans,"premium, modern, clean, sophisticated, versatile, balanced","Premium brands, modern agencies, SaaS, portfolios, startups","https://fonts.google.com/share?selection.family=DM+Sans:wght@400;500;700","@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');","fontFamily: { sans: ['DM Sans', 'sans-serif'] }","Note: Satoshi/General Sans on Fontshare. DM Sans as Google alternative."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:22:21,Vietnamese Friendly,"Sans + Sans",Be Vietnam Pro,Noto Sans,"vietnamese, international, readable, clean, multilingual, accessible","Vietnamese sites, multilingual apps, international products","https://fonts.google.com/share?selection.family=Be+Vietnam+Pro:wght@300;400;500;600;700|Noto+Sans:wght@300;400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700&family=Noto+Sans:wght@300;400;500;600;700&display=swap');","fontFamily: { sans: ['Be Vietnam Pro', 'Noto Sans', 'sans-serif'] }","Be Vietnam Pro excellent Vietnamese support. Noto as fallback."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:23:22,Japanese Elegant,"Serif + Sans",Noto Serif JP,Noto Sans JP,"japanese, elegant, traditional, modern, multilingual, readable","Japanese sites, Japanese restaurants, cultural sites, anime/manga","https://fonts.google.com/share?selection.family=Noto+Sans+JP:wght@300;400;500;700|Noto+Serif+JP:wght@400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=Noto+Serif+JP:wght@400;500;600;700&display=swap');","fontFamily: { serif: ['Noto Serif JP', 'serif'], sans: ['Noto Sans JP', 'sans-serif'] }","Noto fonts excellent Japanese support. Traditional + modern feel."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:24:23,Korean Modern,"Sans + Sans",Noto Sans KR,Noto Sans KR,"korean, modern, clean, professional, multilingual, readable","Korean sites, K-beauty, K-pop, Korean businesses, multilingual","https://fonts.google.com/share?selection.family=Noto+Sans+KR:wght@300;400;500;700","@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');","fontFamily: { sans: ['Noto Sans KR', 'sans-serif'] }","Clean Korean typography. Single font with weight variations."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:25:24,Chinese Traditional,"Serif + Sans",Noto Serif TC,Noto Sans TC,"chinese, traditional, elegant, cultural, multilingual, readable","Traditional Chinese sites, cultural content, Taiwan/Hong Kong markets","https://fonts.google.com/share?selection.family=Noto+Sans+TC:wght@300;400;500;700|Noto+Serif+TC:wght@400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&family=Noto+Serif+TC:wght@400;500;600;700&display=swap');","fontFamily: { serif: ['Noto Serif TC', 'serif'], sans: ['Noto Sans TC', 'sans-serif'] }","Traditional Chinese character support. Elegant pairing."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:26:25,Chinese Simplified,"Sans + Sans",Noto Sans SC,Noto Sans SC,"chinese, simplified, modern, professional, multilingual, readable","Simplified Chinese sites, mainland China market, business apps","https://fonts.google.com/share?selection.family=Noto+Sans+SC:wght@300;400;500;700","@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');","fontFamily: { sans: ['Noto Sans SC', 'sans-serif'] }","Simplified Chinese support. Clean modern look."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:27:26,Arabic Elegant,"Serif + Sans",Noto Naskh Arabic,Noto Sans Arabic,"arabic, elegant, traditional, cultural, RTL, readable","Arabic sites, Middle East market, Islamic content, bilingual sites","https://fonts.google.com/share?selection.family=Noto+Naskh+Arabic:wght@400;500;600;700|Noto+Sans+Arabic:wght@300;400;500;700","@import url('https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic:wght@400;500;600;700&family=Noto+Sans+Arabic:wght@300;400;500;700&display=swap');","fontFamily: { serif: ['Noto Naskh Arabic', 'serif'], sans: ['Noto Sans Arabic', 'sans-serif'] }","RTL support. Naskh for traditional, Sans for modern Arabic."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:28:27,Thai Modern,"Sans + Sans",Noto Sans Thai,Noto Sans Thai,"thai, modern, readable, clean, multilingual, accessible","Thai sites, Southeast Asia, tourism, Thai restaurants","https://fonts.google.com/share?selection.family=Noto+Sans+Thai:wght@300;400;500;700","@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@300;400;500;700&display=swap');","fontFamily: { sans: ['Noto Sans Thai', 'sans-serif'] }","Clean Thai typography. Excellent readability."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:29:28,Hebrew Modern,"Sans + Sans",Noto Sans Hebrew,Noto Sans Hebrew,"hebrew, modern, RTL, clean, professional, readable","Hebrew sites, Israeli market, Jewish content, bilingual sites","https://fonts.google.com/share?selection.family=Noto+Sans+Hebrew:wght@300;400;500;700","@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Hebrew:wght@300;400;500;700&display=swap');","fontFamily: { sans: ['Noto Sans Hebrew', 'sans-serif'] }","RTL support. Clean modern Hebrew typography."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:30:29,Legal Professional,"Serif + Sans",EB Garamond,Lato,"legal, professional, traditional, trustworthy, formal, authoritative","Law firms, legal services, contracts, formal documents, government","https://fonts.google.com/share?selection.family=EB+Garamond:wght@400;500;600;700|Lato:wght@300;400;700","@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600;700&family=Lato:wght@300;400;700&display=swap');","fontFamily: { serif: ['EB Garamond', 'serif'], sans: ['Lato', 'sans-serif'] }","EB Garamond for authority. Lato for clean body text."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:31:30,Medical Clean,"Sans + Sans",Figtree,Noto Sans,"medical, clean, accessible, professional, healthcare, trustworthy","Healthcare, medical clinics, pharma, health apps, accessibility","https://fonts.google.com/share?selection.family=Figtree:wght@300;400;500;600;700|Noto+Sans:wght@300;400;500;700","@import url('https://fonts.googleapis.com/css2?family=Figtree:wght@300;400;500;600;700&family=Noto+Sans:wght@300;400;500;700&display=swap');","fontFamily: { heading: ['Figtree', 'sans-serif'], body: ['Noto Sans', 'sans-serif'] }","Clean, accessible fonts for medical contexts."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:32:31,Financial Trust,"Sans + Sans",IBM Plex Sans,IBM Plex Sans,"financial, trustworthy, professional, corporate, banking, serious","Banks, finance, insurance, investment, fintech, enterprise","https://fonts.google.com/share?selection.family=IBM+Plex+Sans:wght@300;400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');","fontFamily: { sans: ['IBM Plex Sans', 'sans-serif'] }","IBM Plex conveys trust and professionalism. Excellent for data."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:33:32,Real Estate Luxury,"Serif + Sans",Cinzel,Josefin Sans,"real estate, luxury, elegant, sophisticated, property, premium","Real estate, luxury properties, architecture, interior design","https://fonts.google.com/share?selection.family=Cinzel:wght@400;500;600;700|Josefin+Sans:wght@300;400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Josefin+Sans:wght@300;400;500;600;700&display=swap');","fontFamily: { serif: ['Cinzel', 'serif'], sans: ['Josefin Sans', 'sans-serif'] }","Cinzel's elegance for headlines. Josefin for modern body."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:34:33,Restaurant Menu,"Serif + Sans",Playfair Display SC,Karla,"restaurant, menu, culinary, elegant, foodie, hospitality","Restaurants, cafes, food blogs, culinary, hospitality","https://fonts.google.com/share?selection.family=Karla:wght@300;400;500;600;700|Playfair+Display+SC:wght@400;700","@import url('https://fonts.googleapis.com/css2?family=Karla:wght@300;400;500;600;700&family=Playfair+Display+SC:wght@400;700&display=swap');","fontFamily: { display: ['Playfair Display SC', 'serif'], sans: ['Karla', 'sans-serif'] }","Small caps Playfair for menu headers. Karla for descriptions."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:35:34,Art Deco,"Display + Sans",Poiret One,Didact Gothic,"art deco, vintage, 1920s, elegant, decorative, gatsby","Vintage events, art deco themes, luxury hotels, classic cocktails","https://fonts.google.com/share?selection.family=Didact+Gothic|Poiret+One","@import url('https://fonts.googleapis.com/css2?family=Didact+Gothic&family=Poiret+One&display=swap');","fontFamily: { display: ['Poiret One', 'sans-serif'], sans: ['Didact Gothic', 'sans-serif'] }","Poiret One for art deco headlines only. Didact for body."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:36:35,Magazine Style,"Serif + Sans",Libre Bodoni,Public Sans,"magazine, editorial, publishing, refined, journalism, print","Magazines, online publications, editorial content, journalism","https://fonts.google.com/share?selection.family=Libre+Bodoni:wght@400;500;600;700|Public+Sans:wght@300;400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=Libre+Bodoni:wght@400;500;600;700&family=Public+Sans:wght@300;400;500;600;700&display=swap');","fontFamily: { serif: ['Libre Bodoni', 'serif'], sans: ['Public Sans', 'sans-serif'] }","Bodoni's editorial elegance. Public Sans for clean UI."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:37:36,Crypto/Web3,"Sans + Sans",Orbitron,Exo 2,"crypto, web3, futuristic, tech, blockchain, digital","Crypto platforms, NFT, blockchain, web3, futuristic tech","https://fonts.google.com/share?selection.family=Exo+2:wght@300;400;500;600;700|Orbitron:wght@400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;500;600;700&family=Orbitron:wght@400;500;600;700&display=swap');","fontFamily: { display: ['Orbitron', 'sans-serif'], body: ['Exo 2', 'sans-serif'] }","Orbitron for futuristic headers. Exo 2 for readable body."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:38:37,Gaming Bold,"Display + Sans",Russo One,Chakra Petch,"gaming, bold, action, esports, competitive, energetic","Gaming, esports, action games, competitive sports, entertainment","https://fonts.google.com/share?selection.family=Chakra+Petch:wght@300;400;500;600;700|Russo+One","@import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@300;400;500;600;700&family=Russo+One&display=swap');","fontFamily: { display: ['Russo One', 'sans-serif'], body: ['Chakra Petch', 'sans-serif'] }","Russo One for impact. Chakra Petch for techy body text."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:39:38,Indie/Craft,"Display + Sans",Amatic SC,Cabin,"indie, craft, handmade, artisan, organic, creative","Craft brands, indie products, artisan, handmade, organic products","https://fonts.google.com/share?selection.family=Amatic+SC:wght@400;700|Cabin:wght@400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=Amatic+SC:wght@400;700&family=Cabin:wght@400;500;600;700&display=swap');","fontFamily: { display: ['Amatic SC', 'sans-serif'], sans: ['Cabin', 'sans-serif'] }","Amatic for handwritten feel. Cabin for readable body."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:40:39,Startup Bold,"Sans + Sans",Clash Display,Satoshi,"startup, bold, modern, innovative, confident, dynamic","Startups, pitch decks, product launches, bold brands","https://fonts.google.com/share?selection.family=Outfit:wght@400;500;600;700|Rubik:wght@300;400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&family=Rubik:wght@300;400;500;600;700&display=swap');","fontFamily: { heading: ['Outfit', 'sans-serif'], body: ['Rubik', 'sans-serif'] }","Note: Clash Display on Fontshare. Outfit as Google alternative."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:41:40,E-commerce Clean,"Sans + Sans",Rubik,Nunito Sans,"ecommerce, clean, shopping, product, retail, conversion","E-commerce, online stores, product pages, retail, shopping","https://fonts.google.com/share?selection.family=Nunito+Sans:wght@300;400;500;600;700|Rubik:wght@300;400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@300;400;500;600;700&family=Rubik:wght@300;400;500;600;700&display=swap');","fontFamily: { heading: ['Rubik', 'sans-serif'], body: ['Nunito Sans', 'sans-serif'] }","Clean readable fonts perfect for product descriptions."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:42:41,Academic/Research,"Serif + Sans",Crimson Pro,Atkinson Hyperlegible,"academic, research, scholarly, accessible, readable, educational","Universities, research papers, academic journals, educational","https://fonts.google.com/share?selection.family=Atkinson+Hyperlegible:wght@400;700|Crimson+Pro:wght@400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Crimson+Pro:wght@400;500;600;700&display=swap');","fontFamily: { serif: ['Crimson Pro', 'serif'], sans: ['Atkinson Hyperlegible', 'sans-serif'] }","Crimson for scholarly headlines. Atkinson for accessibility."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:43:42,Dashboard Data,"Mono + Sans",Fira Code,Fira Sans,"dashboard, data, analytics, code, technical, precise","Dashboards, analytics, data visualization, admin panels","https://fonts.google.com/share?selection.family=Fira+Code:wght@400;500;600;700|Fira+Sans:wght@300;400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Fira+Sans:wght@300;400;500;600;700&display=swap');","fontFamily: { mono: ['Fira Code', 'monospace'], sans: ['Fira Sans', 'sans-serif'] }","Fira family cohesion. Code for data, Sans for labels."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:44:43,Music/Entertainment,"Display + Sans",Righteous,Poppins,"music, entertainment, fun, energetic, bold, performance","Music platforms, entertainment, events, festivals, performers","https://fonts.google.com/share?selection.family=Poppins:wght@300;400;500;600;700|Righteous","@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Righteous&display=swap');","fontFamily: { display: ['Righteous', 'sans-serif'], sans: ['Poppins', 'sans-serif'] }","Righteous for bold entertainment headers. Poppins for body."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:45:44,Minimalist Portfolio,"Sans + Sans",Archivo,Space Grotesk,"minimal, portfolio, designer, creative, clean, artistic","Design portfolios, creative professionals, minimalist brands","https://fonts.google.com/share?selection.family=Archivo:wght@300;400;500;600;700|Space+Grotesk:wght@300;400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=Archivo:wght@300;400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');","fontFamily: { heading: ['Space Grotesk', 'sans-serif'], body: ['Archivo', 'sans-serif'] }","Space Grotesk for distinctive headers. Archivo for clean body."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:46:45,Kids/Education,"Display + Sans",Baloo 2,Comic Neue,"kids, education, playful, friendly, colorful, learning","Children's apps, educational games, kid-friendly content","https://fonts.google.com/share?selection.family=Baloo+2:wght@400;500;600;700|Comic+Neue:wght@300;400;700","@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700&family=Comic+Neue:wght@300;400;700&display=swap');","fontFamily: { display: ['Baloo 2', 'sans-serif'], sans: ['Comic Neue', 'sans-serif'] }","Fun, playful fonts for children. Comic Neue is readable comic style."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:47:46,Wedding/Romance,"Script + Serif",Great Vibes,Cormorant Infant,"wedding, romance, elegant, script, invitation, feminine","Wedding sites, invitations, romantic brands, bridal","https://fonts.google.com/share?selection.family=Cormorant+Infant:wght@300;400;500;600;700|Great+Vibes","@import url('https://fonts.googleapis.com/css2?family=Cormorant+Infant:wght@300;400;500;600;700&family=Great+Vibes&display=swap');","fontFamily: { script: ['Great Vibes', 'cursive'], serif: ['Cormorant Infant', 'serif'] }","Great Vibes for elegant accents. Cormorant for readable text."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:48:47,Science/Tech,"Sans + Sans",Exo,Roboto Mono,"science, technology, research, data, futuristic, precise","Science, research, tech documentation, data-heavy sites","https://fonts.google.com/share?selection.family=Exo:wght@300;400;500;600;700|Roboto+Mono:wght@300;400;500;700","@import url('https://fonts.googleapis.com/css2?family=Exo:wght@300;400;500;600;700&family=Roboto+Mono:wght@300;400;500;700&display=swap');","fontFamily: { sans: ['Exo', 'sans-serif'], mono: ['Roboto Mono', 'monospace'] }","Exo for modern tech feel. Roboto Mono for code/data."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:49:48,Accessibility First,"Sans + Sans",Atkinson Hyperlegible,Atkinson Hyperlegible,"accessible, readable, inclusive, WCAG, dyslexia-friendly, clear","Accessibility-critical sites, government, healthcare, inclusive design","https://fonts.google.com/share?selection.family=Atkinson+Hyperlegible:wght@400;700","@import url('https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&display=swap');","fontFamily: { sans: ['Atkinson Hyperlegible', 'sans-serif'] }","Designed for maximum legibility. Excellent for accessibility."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:50:49,Sports/Fitness,"Sans + Sans",Barlow Condensed,Barlow,"sports, fitness, athletic, energetic, condensed, action","Sports, fitness, gyms, athletic brands, competition","https://fonts.google.com/share?selection.family=Barlow+Condensed:wght@400;500;600;700|Barlow:wght@300;400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;500;600;700&family=Barlow:wght@300;400;500;600;700&display=swap');","fontFamily: { display: ['Barlow Condensed', 'sans-serif'], body: ['Barlow', 'sans-serif'] }","Condensed for impact headlines. Regular Barlow for body."
/home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/typography.csv:51:50,Luxury Minimalist,"Serif + Sans",Bodoni Moda,Jost,"luxury, minimalist, high-end, sophisticated, refined, premium","Luxury minimalist brands, high-end fashion, premium products","https://fonts.google.com/share?selection.family=Bodoni+Moda:wght@400;500;600;700|Jost:wght@300;400;500;600;700","@import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:wght@400;500;600;700&family=Jost:wght@300;400;500;600;700&display=swap');","fontFamily: { serif: ['Bodoni Moda', 'serif'], sans: ['Jost', 'sans-serif'] }","Bodoni's high contrast elegance. Jost for geometric body."
```

## vercel-cli

- 路径：/home/ubuntu/.openclaw/workspace/skills/vercel-cli
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-11 07:23:24 UTC（约 4 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**medium**
- 理由：执行外部命令(child_process/exec/spawn) 读取环境变量/密钥线索
- 可执行文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/vercel-cli/vercel-skill.js
- 脚本文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/vercel-cli/vercel-skill.js
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/vercel-cli/vercel-skill.js:7:const { execSync } = require('child_process');
/home/ubuntu/.openclaw/workspace/skills/vercel-cli/vercel-skill.js:7:const { execSync } = require('child_process');
/home/ubuntu/.openclaw/workspace/skills/vercel-cli/vercel-skill.js:17:    const result = execSync(`vercel ${args}`, {
/home/ubuntu/.openclaw/workspace/skills/vercel-cli/vercel-skill.js:30:    execSync('which vercel', { stdio: 'pipe' });
/home/ubuntu/.openclaw/workspace/skills/vercel-cli/vercel-skill.js:43:      execSync('npm install -g vercel', { stdio: 'inherit' });
/home/ubuntu/.openclaw/workspace/skills/vercel-cli/vercel-skill.js:56:        execSync('vercel login', { stdio: 'inherit' });
/home/ubuntu/.openclaw/workspace/skills/vercel-cli/vercel-skill.js:90:        execSync('vercel logs', { stdio: 'inherit', cwd: projectPath });
/home/ubuntu/.openclaw/workspace/skills/vercel-cli/SKILL.md:28:  - VERCEL_TOKEN: Optional, for non-interactive auth
```

## webapp-testing

- 路径：/home/ubuntu/.openclaw/workspace/skills/webapp-testing
- SKILL.md：yes
- package.json：无
- 最近文件修改：2026-02-06 15:37:07 UTC（约 9 天前）
- 版本库：否（非独立 git 仓库）
- 风险等级：**low**
- 理由：无明显高危特征
- 脚本文件(节选)：
  - /home/ubuntu/.openclaw/workspace/skills/webapp-testing/examples/element_discovery.py
  - /home/ubuntu/.openclaw/workspace/skills/webapp-testing/examples/console_logging.py
  - /home/ubuntu/.openclaw/workspace/skills/webapp-testing/examples/static_html_automation.py
  - /home/ubuntu/.openclaw/workspace/skills/webapp-testing/scripts/with_server.py
- 高风险关键字命中(最多展示若干行)：

```
/home/ubuntu/.openclaw/workspace/skills/webapp-testing/LICENSE.txt:4:                        http://www.apache.org/licenses/
/home/ubuntu/.openclaw/workspace/skills/webapp-testing/LICENSE.txt:196:       http://www.apache.org/licenses/LICENSE-2.0
/home/ubuntu/.openclaw/workspace/skills/webapp-testing/SKILL.md:59:    page.goto('http://localhost:5173') # Server already running and ready
/home/ubuntu/.openclaw/workspace/skills/webapp-testing/examples/element_discovery.py:10:    page.goto('http://localhost:5173')
/home/ubuntu/.openclaw/workspace/skills/webapp-testing/examples/console_logging.py:5:url = 'http://localhost:5173'  # Replace with your URL
/home/ubuntu/.openclaw/workspace/skills/webapp-testing/.clawhub/origin.json:3:  "registry": "https://clawhub.ai",
```

