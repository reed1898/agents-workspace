# Issue #001: Discord channel proxy 配置不生效

## 问题描述
OpenClaw 的 `channels.discord.proxy` 配置对 **Gateway WebSocket** 和 **REST API（自有代码）** 生效，但对 `@buape/carbon` 库的 `RequestClient` 不生效。Carbon 是 Discord bot 框架，它的 `RequestClient.js` 直接调用 `fetch()` 时不会走 proxy。

## 源码分析

### OpenClaw 自己的代码已支持 proxy ✅
在 `subagent-registry-CkqrXKq4.js` 中：
- **Gateway WebSocket proxy** (line ~57252): 读取 `discordConfig.proxy`，创建 `ProxyAgent` 用于 WebSocket 连接
- **REST fetch proxy** (line ~58212): `resolveDiscordRestFetch(proxyUrl, runtime)` 创建带 proxy dispatcher 的 fetch wrapper
- 这两部分都能正确从 `channels.discord.proxy` 读取代理配置

### @buape/carbon 不支持 proxy ❌
`@buape/carbon/dist/src/classes/RequestClient.js` 的 `fetch()` 调用没有 `dispatcher` 参数，所以：
- Discord REST API 的一部分请求（通过 carbon 库发出的）不走代理
- 需要手动 patch 注入 `ProxyAgent`

## 当前 workaround
Reed 的 patch (`~/.openclaw/patches/carbon-proxy.patch`) 做了：
1. 在 `RequestClient.js` 顶部读取 `~/.openclaw/openclaw.json`
2. 提取 `channels.discord.proxy` 配置
3. 创建 `ProxyAgent`
4. 在 `fetch()` 调用时注入 `dispatcher`

## 修复方案

### 方案 A：在 OpenClaw 侧传入 proxy fetch（推荐）
OpenClaw 已经有 `resolveDiscordRestFetch()` 创建了 proxy fetch。问题是 carbon 的 `RequestClient` 没有接收外部 fetch 的接口。

**需要看 carbon 源码是否支持自定义 fetch**——如果 carbon 的构造函数或 options 支持传入自定义 fetcher，OpenClaw 可以在初始化 carbon client 时传入 proxy-aware fetch。

### 方案 B：向 @buape/carbon 提 PR
给 carbon 加一个 `fetchImpl` 或 `dispatcher` 配置项，让上层框架可以注入代理。

### 方案 C：向 OpenClaw 提 PR
在 OpenClaw 的 discord channel 初始化代码中，monkey-patch carbon 的 RequestClient 来注入 proxy dispatcher。这样升级后不需要手动 patch。

## 深入分析

### Carbon Client 初始化链路
```
OpenClaw: new Client({ token, requestOptions, ... })
  → Carbon Client: this.rest = new RequestClient(token, options.requestOptions)
    → RequestClient.executeRequest() → fetch(url, { method, headers, body, signal })  ← 没有 dispatcher!
```

### RequestClientOptions 不支持自定义 fetch
Carbon 的 `RequestClientOptions` 只有：`tokenHeader`, `baseUrl`, `apiVersion`, `userAgent`, `timeout`, `queueRequests`, `maxQueueSize`
**没有** `fetch` / `fetchImpl` / `dispatcher` 选项。

### OpenClaw 初始化 Carbon Client 的位置
`subagent-registry-CkqrXKq4.js` line ~58509:
```js
const client = new Client({
  baseUrl: "http://localhost",
  deploySecret: "a",
  clientId: applicationId,
  publicKey: "a",
  token,
  autoDeploy: false,
  eventQueue: { listenerTimeout: 12e4, ...discordCfg.eventQueue }
}, { commands, listeners, components, modals }, clientPlugins);
```

### OpenClaw 自己的 proxy-aware fetch 已存在
`resolveDiscordRestFetch(rawDiscordCfg.proxy, runtime)` (line ~58316) 创建了带 ProxyAgent 的 fetch wrapper，但只用于 OpenClaw 自己的 REST 调用（如 media download），**没有传给 carbon Client**。

## 修复方案：方案 2 — 在 OpenClaw 侧 monkey-patch

### 改动点
在 `new Client(...)` 之后、使用 `client.rest` 之前，注入 proxy dispatcher：

```js
// After creating the carbon client
if (discordRestFetch !== fetch) {
  // Override carbon's RequestClient.executeRequest to use proxy
  const originalExecuteRequest = client.rest.executeRequest.bind(client.rest);
  // ... or simpler: directly replace client.rest with a patched version
}
```

### 最简方案
由于 `client.rest` 是 public 属性，可以在创建后直接替换 fetch 行为。最干净的做法是：

**在 OpenClaw 的 Discord provider 代码中，创建 Client 后，wrap `client.rest` 的 `executeRequest` 方法，在 fetch 调用时注入 dispatcher。**

或者更简单：**直接给 carbon 提 PR，给 `RequestClientOptions` ���一个 `fetchImpl` 或 `dispatcher` 选项**，然后 OpenClaw 侧只需要传入即可。

### 推荐组合打法
1. **短期**：给 OpenClaw 提 PR，在初始化 carbon client 后 monkey-patch `client.rest`
2. **中期**：给 @buape/carbon 提 PR，加 `dispatcher`/`fetchImpl` 支持
3. carbon PR 合并后 OpenClaw 升级 carbon 依赖，移除 monkey-patch
