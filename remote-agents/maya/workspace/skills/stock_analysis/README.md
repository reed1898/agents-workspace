# stock_analysis

基于 `ZhuLinsen/daily_stock_analysis` 思路封装的单股深度分析 skill。

## 目录说明

- `SKILL.md`：ClawHub 技能说明与调用方式
- `scripts/analyze_stock.sh`：统一入口（推荐上层任务调用）
- `scripts/stock_analyzer.py`：核心分析逻辑（在线 + sample 降级）
- `scripts/install_deps.sh`：依赖检测与安装指引
- `references/upstream.md`：与上游仓库对齐说明
- `PRE_RELEASE_CHECKLIST.md`：发布前检查清单

## 快速试跑（离线）

```bash
bash scripts/analyze_stock.sh AAPL --sample
```

产物默认输出到：`skills/stock_analysis/outputs/`
