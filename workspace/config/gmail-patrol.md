# Gmail 每日巡检配置

## 巡检时间
- 早: 09:00
- 中: 14:00
- 晚: 21:00
- 周末不休息，频率一样

## 邮箱信息
- Gmail: fishwarter@gmail.com
- 关联 QQ 邮箱: fishwarter@qq.com, 33657434@qq.com, fishwarter@foxmail.com
- 部分邮件会同时发到 Gmail 和 QQ 邮箱（To 里包含多个地址）

## 来源识别规则
- To/CC 里包含 `@qq.com` 或 `@foxmail.com` → 标记为 `📮 QQ邮箱同发`
- 其他 → 标记为 `📧 Gmail`

## 分类与优先级

### 🔴 紧急/重要（置顶，单独列出）
**发件人匹配：**
- 海淀凯文学校（关键词：凯文、KAIWEN、kaiwen）
- FTX Digital / claims@ftx.pwc.com
- 交易所安全提醒（Bitget、Binance、OKX、Coinbase 等的安全/风控/异常登录）
- 银行/金融机构安全告警

**关键词匹配：**
- 安全、security、verification、异常登录、unauthorized
- 理赔、claim、deadline、到期
- 紧急、urgent

### 💳 账单信息（单独列出）
- 各类账单、扣费通知、订阅续费
- 交易确认（Moomoo 等）
- 关键词：账单、bill、invoice、payment、receipt、subscription、扣费、续费

### 🟠 交易相关
- Crypto 交易所通知（非安全类、非账单类）
- 市场动态通知

### 🔵 值得一读（需全文提取摘要，中文总结）
- AI/Agent: AINews, Latent.Space, Portkey
- Crypto/DeFi: Bankless
- 商业/科技: Not Boring, Sourcery
- 开发者: Apple Developer
- 其他有深度的 Newsletter
- **全部处理**，不限数量（后续根据实际情况优化）
- **使用本地 Codex 子任务处理全文摘要**（节省主会话 token）
- **摘要语言：中文**

### 🟢 一般通知
- 产品更新（Prisma 等）
- 平台通知

### ⚪ 可忽略（直接跳过）
- Seeking Alpha（全部）
- 推广广告（Adobe 等）
- 营销邮件
- 证券对账单（SecuritiesDepository / gtht.com / gtjas.com）

## 处理规则
1. 扫描所有未读
2. 分类汇报
3. 🔵 类邮件：通过 Codex 子任务读全文，提取中文摘要
4. 有价值内容收录到知识库 shared/
5. 汇报完成后，全部标为已读

## 汇报格式
```
📧 邮件巡检 | {日期} {早/中/晚}间 | {N}封未读

🔴 紧急
- [{来源}] {发件人}: {主题}
  → {摘要}

💳 账单
- [{来源}] {发件人}: {主题}
  → {金额/明细}

🟠 交易
- [{来源}] {发件人}: {主题}

🔵 推荐阅读
- [{来源}] {发件人}: {主题}
  → {中文全文摘要，2-3句}

🟢 通知
- [{来源}] {简要列出}

⚪ 已跳过: {N}封 ({来源分布})

✅ 已全部标为已读
```

## 技术实现
- 通过 HEARTBEAT.md 触发
- 使用 gws-proxy.sh 脚本（自动检测 QuickQ 代理端口 + token 刷新）
- Gmail API: +triage 扫描，messages.get 读全文，messages.modify 标已读
- Newsletter 全文摘要：spawn Codex 子任务处理，减少主会话 token 消耗
