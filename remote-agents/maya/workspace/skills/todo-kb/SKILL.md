---
name: todo-kb
description: 在知识库里管理 Todo（新增、查看、完成、重开、更新、删除），并把任务持久化到 `/home/ubuntu/.openclaw/kb/20_Inbox/`。当用户说“记个待办/加个 todo/看待办/完成第N条/删除待办/更新截止时间”时使用。
---

# Todo KB

用脚本管理 Todo，数据统一存到知识库，便于同步和检索。

## 存储位置

- JSON 数据：`/home/ubuntu/.openclaw/kb/20_Inbox/todo-list.json`
- Markdown 视图：`/home/ubuntu/.openclaw/kb/20_Inbox/todo-list.md`

## 命令

脚本路径：`/home/ubuntu/.openclaw/workspace/skills/todo-kb/scripts/todo_kb.py`

```bash
# 新增
python .../todo_kb.py add "整理 OpenClaw 发布笔记" --tags "openclaw,content" --due "2026-02-25"

# 查看（默认 open）
python .../todo_kb.py list
python .../todo_kb.py list --status all
python .../todo_kb.py list --status done
python .../todo_kb.py list --q "发布"

# 完成 / 重开
python .../todo_kb.py done 3
python .../todo_kb.py reopen 3

# 更新
python .../todo_kb.py update 3 --title "整理 OpenClaw 社区周报" --due "2026-02-26" --tags "openclaw,weekly"

# 删除
python .../todo_kb.py remove 3
```

## 对话工作流

1. 用户让你“加待办” → 用 `add`。
2. 用户让你“看待办” → 用 `list`（默认 open）。
3. 用户让你“完成第 N 条” → 用 `done N`。
4. 用户说“这个重新打开” → 用 `reopen N`。
5. 用户改标题/标签/截止日 → 用 `update N ...`。
6. 用户让你删除 → 用 `remove N`。

执行后在聊天里返回简短确认，并在需要时附当前 open 列表。
