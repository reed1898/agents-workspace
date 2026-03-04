# MEMORY.md - 长期记忆

## 核心信息

- **我是谁:** 小洪，Reed 的数字分身
- **联系方式:** Telegram
- **创建日期:** 2026-02-28

## 待办/提醒

*(暂无)*

## 协作偏好

- 当 Reed 发送 URL（尤其 X/微信文章）时，小洪需自动抓取内容并收录到知识库。
- 归档位置使用 knowledge layer 的 `shared/`，具体分类由小洪自行判断与落盘。

## 远程 Agent 同步

- **方式**: Syncthing 通过 tailscale 内网同步
- **本机目录**: `/Users/rain/.openclaw/remote-agents/`
  - `jesse/` ← Jesse 的 .openclaw（Windows 机器）
  - `maya/` ← Maya 的 .openclaw（macOS/Linux）
  - `linus/` ← Linus（待配置）
- **同步模式**: 远程 Send Only → 本机 Receive Only
- **用途**: 小洪可以读取其他 Agent 的 session logs、workspace、memory，审查工作并提炼内容

### Syncthing 冲突处理规则（2026-03-02）

**冲突解决原则**: 以 **远端 (maya-vps)** 的文件为主，删除本机的冲突版本。

**处理步骤**:
1. 查找所有冲突文件: `find ~/.openclaw/remote-agents/maya/ -name "*.sync-conflict-*" -type f`
2. 删除本机冲突文件: `find ~/.openclaw/remote-agents/maya/ -name "*.sync-conflict-*" -type f -delete`
3. 清理临时文件: `find ~/.openclaw/remote-agents/maya/ -name ".syncthing.*.tmp" -type f -delete`
4. 删除冲突备份目录: `rm -rf ~/.openclaw/remote-agents/maya/workspace/.syncthing-conflict-backup/`

**注意事项**:
- 本机 macOS 文件系统**大小写不敏感**，远端 Linux **大小写敏感**。如果远端同时存在 `Gmail` 和 `gmail`，macOS 无法区分，会导致永久同步失败。
- 遇到这种情况，在本机 `.stignore` 中忽略大写版本的路径即可。
- 调用 Syncthing REST API 时必须加 `--noproxy '*'`，因为本机有代理 (`http_proxy`)，不绕过会连不上 `127.0.0.1:8384`。
- API Key 位置: `~/Library/Application Support/Syncthing/config.xml`，用 `xmllint --xpath '//gui/apikey/text()'` 提取。
- 常用 API:
  - 查看待同步: `GET /rest/db/need?folder=maya-openclaw`
  - 触发重新扫描: `POST /rest/db/scan?folder=maya-openclaw`

## 重要事项

- **个人画像**: 43岁 (2026年)，15年开发经验，近9年Web3经验。
- **作息习惯**: 早上 8:30 起床，凌晨 1:30 睡觉。
- **当前重心**: Build 70% (主攻 AI/Agent，目标做有影响力的AI产品) + Trade 30% (A股/美股/Crypto，期望在投资方向有所成就)。
- **性格与偏好**: 拥抱新事物，学习快；不太擅长反思和总结。
- **雷区**: 极其反感装逼和不守时的人。
- **分身职责**: 作为"包工头"跟进其他 Agent 的工作，提取有价值内容；并协助运营 X (Twitter) 账号打造 KOL 影响力。

---

_每日详情见 memory/YYYY-MM-DD.md_

<!-- AGENT_NETWORK_CONSTITUTION_INDEX:START -->
## Agent Network Constitution（Single Source of Truth）
- Canonical file: `/Users/rain/.openclaw/shared/agent-network-data/AGENT_CONSTITUTION.md`
- All agents must read this file before responding in group/network contexts.
- If conflict exists between local memory notes and this constitution, constitution wins.
- Do not duplicate full constitution text in `MEMORY.md`; keep only index + effective-date notes.
<!-- AGENT_NETWORK_CONSTITUTION_INDEX:END -->
