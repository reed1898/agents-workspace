# 从“隧道”到“load”：把本地 Mac 稳定接入 OpenClaw Gateway 的一次踩坑复盘

> 这篇文章写给未来的我：当你需要让云端/服务器上的 **OpenClaw Gateway** 稳定控制 **本地 Mac（Reed‑Mac）** 时，为什么“隧道方案”一开始看似好用、但很容易变脆；以及我后来切到“load（加载式接入）”后，为什么体验更稳、更可复盘。
>
> 注：本文刻意聚焦“连接/可控性”而不是 bot 分发、KB 结构等其他话题。

---

## 0. 需求复述：我到底想实现什么？

我想要的不是“Mac 能上网”，而是：

- **本地 Mac** 作为一个可执行节点（browser/system），能被 **Gateway** 远程调度（跑命令、控制浏览器、抓取受限内容等）。
- 整个链路要满足：
  1) **稳定在线**（断了能自愈）
  2) **可审计**（知道谁在控制、做了什么）
  3) **可回滚**（出问题能快速止血）

换句话说：我需要把本地 Mac 纳入一套“可运营”的 agent 基础设施里。

---

## 1. 两条路：隧道（tunnel） vs 加载式接入（load）

我最终踩出来的经验是：这两条路都能跑起来，但它们的失败模式完全不同。

### 方案 A：隧道（tunnel）
**直觉**：我先打通网络 → Gateway 看到 Mac → 远程控制。

常见形态（不点名具体工具，避免把实现绑死）：
- 通过某种隧道/反向代理，让 Gateway 能访问到本地服务端口
- 或者让本地穿透到公网/内网一个可达地址

**优点**：
- 上手快：只要网络通，立刻能测。
- 对“临时远程”很友好。

**缺点（也是我这次踩到的核心）**：
- **可用≠可控**：网络能通，但链路经常在边缘条件下退化（重连、延迟、端口飘、权限/会话状态不一致）。
- **故障定位成本高**：断了到底是 tunnel、DNS、端口、证书、还是本地进程挂了？很难一眼看穿。
- **缺少统一的“配置真源”**：容易出现“你以为你改的是 A，实际生效的是 B”。

> 经验：隧道方案更像“把一台机器临时暴露出来”，而不是“把这台机器纳入系统”。

### 方案 B：load（加载式接入）
**直觉**：不是先把网络打通再想办法接入，而是反过来——

> 用一个可重复的“加载动作”，把本地节点以标准方式注册/接入 Gateway，然后由 Gateway 统一管理这条链路。

**优点**：
- **更像系统**：连接是一个“可重复的状态机”，不是一次性穿透。
- **可复盘**：哪些配置被加载、何时加载、加载后验证结果是什么，都能写成 SOP。
- **自愈空间更大**：配合 watchdog/launchd 这种机制，能把“断线重连”变成默认行为。

**潜在代价**：
- 初始理解成本更高：要搞清楚“load 到底加载了什么”，以及“谁是配置真源”。

> 经验：load 方案本质是把连接这件事产品化：有入口、有约束、有验证。

---

## 2. 我是怎么判断“隧道方案不行了”的？（症状清单）

当我开始频繁遇到下面任意一条时，就说明它不适合作为长期方案：

- 连接**间歇性失效**：偶发断线，且无法稳定复现。
- 指令执行**卡住/超时**：明明在线，但 `system.run` / browser 控制时延飙升或无响应。
- 需要人工介入才能恢复：必须手动重启 tunnel/重启某个服务。
- “看似通了但实际不可控”：比如能打开页面，但发帖/抓回执这类动作链路不闭环。

### 2.1 这次踩到的“真实症状”（来自 service log 的硬证据）

这次我遇到的并不是抽象的“偶尔不稳”，而是几种很典型、能落到日志证据的失败模式：

- **端口占用 → launchd KeepAlive 疯狂重启**
  - 现象：tunnel 进程因端口被占用启动失败，随后被 launchd 反复拉起，导致系统持续抖动。
  - 关键词证据：`端口占用 + launchd 疯狂重启`

- **节点执行链路直接断掉**
  - 现象：隧道/链路抖动时，Gateway 侧会报 `node disconnected (system.run)`，执行闭环被打断。

- **tunnel 常驻进程（launchd label）**
  - 证据：出现过明确的 label：`ai.reed.openclaw.tunnel`，并且还讨论要确保它 `KeepAlive=true`。

> 注：以上三条来自 Gateway 侧 service log（`/tmp/openclaw/openclaw-2026-02-13.log`）中当日对话与报错信息的汇总；属于“可复盘”的证据源。

---

## 3. 切到 load 之后，我把它当作“工程交付”来做

这一步最关键的不是具体命令，而是我把它拆成了 3 个可验证里程碑：

### M1：加载成功（配置层）
- load 动作能稳定完成
- Gateway 侧能看到节点/能力（caps）

### M2：最小闭环可控（执行层）
- 能执行一条**无副作用**命令（例如：打印版本、列目录）
- 能打开一个页面并截图（browser proxy）

### M3：关键业务闭环（回执层）
- 能完成一个“必须有回执”的动作：
  - 例如发一条推文后，能抓到发布链接/时间
  - 或者发一条测试消息能确认到达

> 经验：没有回执的自动化都是玄学。控制节点也是一样。

---

## 4. 最重要的 5 条规则（我以后会强制遵守）

1) **单一真源（SSOT）**：连接配置只认一个地方（不要到处散落）。
2) **变更只用 patch，不用覆盖**：尤其是路由/bindings 类配置，覆盖一次就可能“看似能跑、实际串台”。
3) **每次变更都要冒烟测试**：
   - 节点在线
   - 跑一条只读命令
   - 完成一次回执闭环
4) **把自愈变成默认**：用 launchd/watchdog 保证“断了自动拉起”。
5) **对外动作必须可暂停**：任何可能影响外部世界的操作（发帖/发消息/执行脚本）都要能一键停。

---

## 5. 一份可直接复制的验证清单（Checklist）

- [ ] Gateway 侧能看到 Reed‑Mac 节点在线
- [ ] 能执行：`whoami` / `uname -a` 这类无副作用命令
- [ ] 能打开浏览器到一个固定 URL 并截图
- [ ] 能完成一次“回执动作”（比如发一条测试消息并确认收到）
- [ ] 断网/睡眠后能自动恢复（至少 1 次）

---

## 6. 可复现 SOP：Mac（Reed‑Mac）通过 OpenClaw Node 接入 VPS Gateway

下面这份是“照抄就能跑”的版本（敏感 token 已打码）。核心分两条链路：

- **优先：Tailscale 直连 VPS Gateway**（最稳，少一层 ssh）
- **兜底：SSH 本地端口转发（tunnel）**（在直连不可用时启用）

### 6.1 前置条件（VPS / Gateway 侧）

1) VPS 上 Gateway 正常运行（例：18789）：
- `openclaw gateway status`

2) **重要约束**：如果 VPS Gateway 配置为 `bind=127.0.0.1`（loopback-only），那么：
- 远端 Mac **无法直接连** `54.x.x.x:18789`
- 必须要么走 **Tailscale**（让 18789 在 tailnet 可达），要么走 **SSH 端口转发**（把 VPS 的 127.0.0.1:18789 映射到 Mac 的本地端口）

> 这也是 tunnel 一开始出现的根因：loopback gateway 本来就“不对公网开放”。

### 6.2 Mac 侧：启动 tunnel（SSH 本地端口转发）

脚本（来自 `/Users/rain/bin/openclaw-tunnel.sh`）：

```bash
PORT=18790
REMOTE_HOST="54.169.134.15"   # VPS 公网 IP
REMOTE_USER="ubuntu"
REMOTE_PORT=18789              # VPS 上的 gateway 端口（loopback only）

ssh -N \
  -L ${PORT}:127.0.0.1:${REMOTE_PORT} \
  ${REMOTE_USER}@${REMOTE_HOST} \
  -o ExitOnForwardFailure=yes \
  -o BatchMode=yes \
  -o ServerAliveInterval=15 \
  -o ServerAliveCountMax=2
```

**Launchd**：
- label：`ai.reed.openclaw.tunnel`
- `KeepAlive=true`（如果你要它长期稳定在线，这是必须的）

**已知坑（本次踩到）**：
- 本地 `18790` 如果被占用，会触发 **launchd KeepAlive 疯狂重启**（你今天遇到的就是这个）。

### 6.3 Mac 侧：启动 OpenClaw Node（把 Mac 注册成 Reed‑Mac 节点）

最小命令（来自 `/Users/rain/bin/openclaw-node.sh`，token 已打码）：

```bash
export OPENCLAW_GATEWAY_TOKEN=***REDACTED***
openclaw node run --host 127.0.0.1 --port 18790 --display-name "Reed-Mac"
```

它的含义很直白：
- `--host/--port` 指向“Gateway 的可达地址”
  - tunnel 模式下：就是 **Mac 本地的 127.0.0.1:18790**（转发到 VPS 的 127.0.0.1:18789）
- `--display-name` 让 Gateway 侧以 `Reed-Mac` 显示

### 6.4 推荐的“自动选择”策略：优先 Tailscale，失败再 kickstart tunnel

这段来自 `/Users/rain/bin/openclaw-node-wait.sh` 的设计思路：

1) **优先路径：Tailscale 直连**（不需要 ssh tunnel）
- `PRIMARY_HOST=100.126.19.85`（VPS 的 tailnet IP）
- `PRIMARY_PORT=18789`

2) 如果直连失败：
- `launchctl kickstart -k gui/<uid>/ai.reed.openclaw.tunnel`
- 等待本地 18790 可用后，再 `node run --host 127.0.0.1 --port 18790`

这套策略的好处：
- tailscale 通的时候，链路最短、最稳
- tailscale 掉了，tunnel 自动顶上（但 tunnel 自己也要修到不抖）

### 6.5 冒烟测试（每次变更都要跑）

在 VPS（Gateway）侧：
- `openclaw status` / `nodes status` 应看到 `Reed-Mac connected=true`

最小无副作用执行：
- `nodes.run node=Reed-Mac command=["whoami"]`

浏览器能力验证（如启用 browser caps）：
- 打开固定 URL + 截图（确保 browser proxy 不只是“看起来在线”）

### 6.6 回滚 / 止血

- 先停 node：卸载/停止 `ai.reed.openclaw.node`（或对应 node plist）
- 再停 tunnel：卸载/停止 `ai.reed.openclaw.tunnel`
- 不要动 Gateway 主配置的情况下，Mac 会自然从 nodes 列表里离线

---

## 结语：为什么这件事值得写下来？

当你开始用 agent 做“长期生产系统”时，连接方式不再是网络问题，而是工程问题：

> **你是在管理一条可运营的控制链路。**

隧道能救急，load 才能长期。
