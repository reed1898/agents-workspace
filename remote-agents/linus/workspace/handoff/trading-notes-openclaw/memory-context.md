## MEMORY Context: trading-notes-sync

- **Skill 路径**: `~/.openclaw/workspace/skills/trading-notes-sync/`
- **��赖项目**: `~/.openclaw/projects/trading-notes` (必须先 clone)
- **venv**: Skill 目录下的 `.venv/bin/python`，已装好所有依赖
- **IBKR 需要代理**: `HTTPS_PROXY=socks5://127.0.0.1:10023`
- **ENCRYPTION_KEY/SECRET_KEY**: 必须在环境变量中正确设置，用于解密数据库中的 API 凭证。

### 同步命令
- **IBKR**: `cd <skill_dir> && <proxy> .venv/bin/python scripts/sync_ibkr.py`
- **国泰海通 (Gmail)**: `cd <skill_dir> && <proxy> .venv/bin/python scripts/sync_gmail.py --since-days 7`
- **国信/Moomoo**: 手动导出文件到 `~/Downloads/` 后触发：
  - 国信: `.venv/bin/python scripts/import_csv.py --file ~/Downloads/XXXX.xls --account-name "国信证券" --broker guosen`
  - Moomoo: `.venv/bin/python scripts/import_csv.py --file ~/Downloads/XXXX.csv --account-name "moomoo" --broker moomoo`

### 关键问题 & 解决方案
- **问题**: `Fernet Key Error` / 解密失败
  - **原因**: `TRADING_NOTES_ENCRYPTION_KEY` 不正确或未加载。
  - **解决**: 确保 `~/.zshrc` 或 `.env` 中的 key 是最新的，并已 `source`。

- **问题**: `Gmail OAuth failed: ... refresh token may have expired`
  - **原因**: Google 的授权已过期（通常几个月或更久）。这和 `ENCRYPTION_KEY` 无关。
  - **解决**: 访问 `trading-notes` Web UI，找到对应的 `trade_accounts`，点击 "Re-authorize" 重新走一遍 Google 登录流程。

- **问题**: Python 报错 `SyntaxError: invalid syntax` (尤其在 `str | None` 这种地方)
  - **原因**: Python 版本低于 3.10。
  - **解决**: 确保 `python3` 指向 3.10+ 版本。脚本 `_common.py` 已加入 `from __future__ import annotations` 尝试兼容，但不能保证 100% 解决。
