# web-change-watcher (OpenClaw skill MVP)

一个极小可交付的“网页变更监控”组件：定时抓取 URL，把内容做轻量归一化后存盘；当页面发生变化时输出 diff。

> 付费方向（后续）：
> - 多 URL 监控 + 变更规则（CSS selector / 关键词 / 阈值）
> - 去噪（广告/时间戳/随机 token）
> - OpenClaw cron 一键部署 + Telegram/Email 通知
> - 团队共享 dashboard / 变更历史

## 安装/运行

```bash
cd /home/ubuntu/.openclaw/projects/web-change-watcher
npm install

# 直接运行（第一次会创建 baseline，退出码 1）
node ./src/oc-webwatch.js https://example.com --dir ./.state

# 以“文本模式”做变更检测（更接近“可见内容”，更抗噪）
node ./src/oc-webwatch.js https://example.com --dir ./.state --mode text

# 第二次运行（一般是 UNCHANGED，退出码 0）
node ./src/oc-webwatch.js https://example.com --dir ./.state

# 作为 bin（npm 会在 node_modules/.bin 下放 oc-webwatch）
./node_modules/.bin/oc-webwatch https://example.com --dir ./.state

# 机器可读输出（用于 OpenClaw workflow/cron 的后续接入）
./node_modules/.bin/oc-webwatch https://example.com --dir ./.state --mode text --out json

# 只监控页面的一部分（CSS selector）
# 例如只看页面标题，显著降低“广告/时间戳/随机推荐位”的噪声
./node_modules/.bin/oc-webwatch https://example.com --dir ./.state --mode text --selector 'h1'
```

## 自测

```bash
npm test
# 预期输出：SELFTEST_OK
```

## Exit Code 语义

- `0`：未变化
- `1`：首次创建基线（baseline）
- `2`：检测到变化（同时尝试输出 `diff -u`）
- `3`：错误

## 目录结构

- `src/oc-webwatch.js`：核心可执行脚本
- `.state/`：运行时产生的快照与 hash（可 gitignore）
