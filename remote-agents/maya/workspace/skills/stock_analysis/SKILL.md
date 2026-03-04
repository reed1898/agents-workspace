---
name: stock_analysis
description: Deep analysis skill for individual stocks. Outputs standardized JSON + human-readable conclusions, suitable for batch calling by portfolio analysis tasks. Supports A-shares, HK stocks, and US stocks.
version: 0.1.0
author: OpenClaw Assistant
tags: [stock, analysis, finance, portfolio, investment]
---

# stock_analysis

Performs in-depth analysis of individual stocks, generating structured JSON reports and human-readable conclusions. Can be batch-called by upstream portfolio analysis tasks.

## Features

- 📊 **Multi-dimensional Analysis**: Valuation, technical indicators, risks, catalysts
- 📈 **Quantitative Scoring**: Quality/Valuation/Momentum scores + composite total
- 🌐 **Multi-market Support**: A-shares, HK stocks, US stocks (depends on data source availability)
- 📄 **Dual Output Formats**: JSON (structured) + TXT (human-readable)
- 🔧 **Offline Mode**: `--sample` flag generates sample reports without network/dependencies

## Installation

### One-click Install

```bash
bash {baseDir}/scripts/install_deps.sh
```

The script will automatically:
- Check Python 3 environment
- Create virtual environment (recommended)
- Install `requests` and other dependencies

### Manual Install

```bash
cd {baseDir}
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
pip install requests
```

### System Dependency Issues

If your system lacks `python3-pip` or you don't have sudo access, the script will suggest fallback options:

```bash
# User-level installation without sudo
pip3 install --user requests
```

## Usage

### Basic Usage

```bash
bash {baseDir}/scripts/analyze_stock.sh AAPL
bash {baseDir}/scripts/analyze_stock.sh 00700      # Tencent HK
bash {baseDir}/scripts/analyze_stock.sh 000001.SZ  # Ping An Bank A-share
```

### Specify Output Directory

```bash
bash {baseDir}/scripts/analyze_stock.sh TSLA --out-dir ~/reports
```

### Offline Sample Mode

When network is unavailable or dependencies are not installed, use `--sample` to generate sample reports:

```bash
bash {baseDir}/scripts/analyze_stock.sh AAPL --sample
```

## Output Files

Each execution generates two files (saved to `outputs/` or specified directory):

| File | Format | Purpose |
|------|--------|---------|
| `{symbol}_{timestamp}.json` | Structured JSON | Programmatic parsing, batch processing |
| `{symbol}_{timestamp}.txt` | Plain text | Human reading, sharing |

## JSON Output Fields

```json
{
  "symbol": "AAPL",
  "company": "Apple Inc.",
  "as_of": "2026-02-11T20:30:00Z",
  "price": 185.42,
  "currency": "USD",
  "change_percent": 1.25,
  "valuation": {
    "pe": 28.5,
    "pb": 45.2,
    "market_cap": "2.8T"
  },
  "technical": {
    "sma20": 182.30,
    "sma50": 178.90,
    "rsi14": 58.3,
    "trend": "uptrend"
  },
  "risks": ["Macro interest rate risk", "Supply chain concentration risk"],
  "catalysts": ["New product launch cycle", "AI feature rollout expectations"],
  "scores": {
    "quality": 72,
    "valuation": 63,
    "momentum": 65,
    "total": 66.8
  },
  "conclusion": "Composite score neutral-to-positive. Consider gradual entry based on position sizing and risk budget. Current technical trend is strong.",
  "confidence": "medium",
  "data_sources": ["yahoo_finance", "calculated"]
}
```

### Scoring Algorithm

| Dimension | Weight | Calculation Logic |
|-----------|--------|-------------------|
| **Quality** | 35% | Based on industry benchmark, quality companies baseline at 72 |
| **Valuation** | 30% | PE<20=78pts, PE<35=63pts, else 42pts |
| **Momentum** | 35% | RSI 45-65 adds points, uptrend adds points, overbought/oversold deducts |
| **Total** | 100% | Weighted average, 0-100 scale |

### Confidence Levels

- `high`: Multiple data sources cross-validated, complete data
- `medium`: Partial data missing or delayed
- `low`: Mainly relies on estimation or sample data

## Data Sources

Current version uses the following data sources (in priority order):

1. **Yahoo Finance** (via `yfinance` or API) - US/HK stocks
2. **East Money/Flush** (planned) - A-share data
3. **Calculated Metrics** - RSI, SMA and other technical indicators computed locally

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `python3: command not found` | Install Python 3.8+ |
| `ModuleNotFoundError: requests` | Run `install_deps.sh` or `pip install requests` |
| Network connection failed | Use `--sample` offline mode, or check proxy settings |
| Empty data returned | Check stock symbol format (e.g., A-shares need `.SZ`/`.SS`) |

## Batch Processing Example

Suitable for portfolio analysis scenarios:

```bash
#!/bin/bash
SYMBOLS=("AAPL" "TSLA" "00700" "000001.SZ")
OUT_DIR="./portfolio_reports"
mkdir -p $OUT_DIR

for sym in "${SYMBOLS[@]}"; do
  echo "Analyzing $sym..."
  bash {baseDir}/scripts/analyze_stock.sh "$sym" --out-dir "$OUT_DIR"
done

# Aggregate all JSON
cat $OUT_DIR/*.json | jq -s '.' > portfolio_summary.json
```

## Upstream References

This skill's analysis framework and field design references:
- https://github.com/ZhuLinsen/daily_stock_analysis

See: `{baseDir}/references/upstream.md`

## Changelog

- **v0.1.0** (2026-02-11): Initial release with basic analysis framework and scoring system

## License

MIT License - Consistent with OpenClaw project
