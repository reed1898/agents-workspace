# HEARTBEAT.md

## Heartbeat Tasks

### 1) Syncthing 同步有效性检测（每 4 小时做一次）
- 读取 API key：`xmllint --xpath 'string(//gui/apikey)' "$HOME/Library/Application Support/Syncthing/config.xml"`
- 调用 `http://127.0.0.1:8384/rest/system/connections`：检查远程设备是否在线
- 调用 `http://127.0.0.1:8384/rest/db/need?folder=<folderId>`：检查 `jesse-openclaw`、`maya-openclaw`、`linus-openclaw` 是否有积压
- 调用 `http://127.0.0.1:8384/rest/db/status?folder=<folderId>`：检查 `state` 是否为 `idle`

### 2) 判定标准
- 正常：
  - 远程设备连接正常（预期设备在线）
  - 三个 folder 的 `state=idle` 且 `need` 无积压
- 异常（任一命中即异常）：
  - API 不可达 / key 读取失败
  - 设备离线（持续出现）
  - folder 长时间非 `idle` 或 `need` 持续积压

### 3) 异常时通知
- 立即给 Reed 发告警消息（不要等下一次）
- 告警内容必须包含：
  - 异常类型（连接/API/积压）
  - 受影响的设备或 folder
  - 检测时间（Asia/Shanghai）
  - 建议动作（如重启 tailscale/syncthing、触发 scan）

### 4) 执行频率与静默策略
- heartbeat 仍按系统频率（30 分钟）触发
- 仅当距离上次 Syncthing 检测已超过 4 小时才执行本检测
- 正常时不主动打扰，回复 `HEARTBEAT_OK`
