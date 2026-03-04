# KB 自动化规则

## 1) 自动入库
所有报告类输出应同时：
- 发送到 Telegram
- 写入 `kb/` 对应目录

## 2) 自动 Git 同步
由定时任务执行：
- 检查 `kb` 仓库是否有变更
- 若有变更：`git add -A && git commit && git push origin main`
- 若无变更：不提交

## 3) 命名与结构
- Crypto：`01_Daily/crypto/YYYY-MM/crypto-YYYY-MM-DD-HHMM.md`
- A股：`01_Daily/ashare/YYYY-MM/ashare-YYYY-MM-DD-HHMM.md`
- 美股：`01_Daily/us/YYYY-MM/us-YYYY-MM-DD-HHMM.md`
- AI：`01_Daily/ai/YYYY-MM/ai-YYYY-MM-DD-HHMM.md`
