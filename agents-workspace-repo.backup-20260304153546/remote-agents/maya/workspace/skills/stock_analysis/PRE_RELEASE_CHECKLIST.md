# stock_analysis 发布前检查（最简）

## 1) 安装

```bash
cd skills/stock_analysis
bash scripts/install_deps.sh
```

若提示缺 `python3-pip` / `python3-venv`：

```bash
sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv git
```

无 sudo 降级：

```bash
python3 -m ensurepip --upgrade
python3 -m pip install --user yfinance pandas numpy
```

## 2) 配置

当前最小版无密钥依赖（yfinance 公共数据）。

## 3) 试跑

离线：
```bash
bash scripts/analyze_stock.sh AAPL --sample
```

在线：
```bash
bash scripts/analyze_stock.sh AAPL
```

预期：在 `outputs/` 下生成 `.json` + `.txt` 文件。

## 4) 已知限制

- 技术指标与评分规则是轻量版，不构成投资建议。
- 在线模式依赖网络与 yfinance 可用性。
- A 股/港股 symbol 需按 yfinance 规则填写（如 `600519.SS`, `0700.HK`）。
