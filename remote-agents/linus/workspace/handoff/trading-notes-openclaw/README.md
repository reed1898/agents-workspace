# Trading Notes Sync — Agent 交接包

## 概述
这个包可以让另一台机器上的 OpenClaw Agent 直接上手管理 trading-notes 的多市场交易同步。

## 包含内容

```
handoff/trading-notes-openclaw/
├── README.md                 ← 你正在看的文件
├── skill/                    ← trading-notes-sync skill（完整复制）
│   ├── SKILL.md
│   └── scripts/
│       ├── _common.py
│       ├── setup.sh
│       ├── sync_binance.py
│       ├── sync_gmail.py
│       ├── sync_ibkr.py
│       ├── sync_all.py
│       ├── import_csv.py
│       └── show_positions.py
├── memory-context.md         ← 关键记忆和上下文（Agent 直接读）
└── env-template.sh           ← 环境变量模板（需填入真实值）
```

## 部署步骤

### 1. 准备项目代码
```bash
# 克隆 trading-notes 项目（脚本依赖 backend service 层）
git clone <your-trading-notes-repo> ~/.openclaw/projects/trading-notes
```

### 2. 安装 Skill
```bash
# 复制 skill 目录
cp -r skill/ ~/.openclaw/workspace/skills/trading-notes-sync/

# 安装依赖
cd ~/.openclaw/workspace/skills/trading-notes-sync
bash scripts/setup.sh
```

### 3. 配置环境变量
```bash
# 编辑 env-template.sh 填入真实值，然后：
source env-template.sh
# 或者把变量加到 ~/.zshrc / ~/.bashrc
```

### 4. 把 memory-context.md 内容合并到新 Agent 的 MEMORY.md
这样新 Agent 就有了完整的同步流程记忆，不需要你再解释一遍。

### 5. 验证
```bash
cd ~/.openclaw/workspace/skills/trading-notes-sync
.venv/bin/python scripts/show_positions.py --summary
```

## 注意事项
- IBKR 和 Gmail 同步需要能访问境外网络（代理或直连）
- Gmail OAuth refresh token 如果过期，需在 trading-notes Web UI 重新授权
- 国信/Moomoo 是手动导出文件再导入，不走 API
- 所有 API 密钥存储在数据库里（加密），脚本通过 ENCRYPTION_KEY 解密
