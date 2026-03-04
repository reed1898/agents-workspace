#!/usr/bin/env python3
import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import requests


def rsi14(closes):
    if len(closes) < 15:
        return None
    deltas = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    gains = [max(d, 0) for d in deltas[-14:]]
    losses = [abs(min(d, 0)) for d in deltas[-14:]]
    avg_gain = sum(gains) / 14
    avg_loss = sum(losses) / 14
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def sma(values, n):
    if len(values) < n:
        return None
    return sum(values[-n:]) / n


def calc_scores(pe, rsi, trend):
    quality = 72
    valuation = 50
    momentum = 50

    if pe is not None:
        if pe < 20:
            valuation = 78
        elif pe < 35:
            valuation = 63
        else:
            valuation = 42

    if rsi is not None:
        if 45 <= rsi <= 65:
            momentum += 20
        elif rsi > 75:
            momentum -= 10
        elif rsi < 30:
            momentum -= 5

    if trend == "uptrend":
        momentum += 15
    elif trend == "downtrend":
        momentum -= 15

    total = round(quality * 0.35 + valuation * 0.3 + momentum * 0.35, 1)
    return {
        "quality": max(0, min(100, int(round(quality)))),
        "valuation": max(0, min(100, int(round(valuation)))),
        "momentum": max(0, min(100, int(round(momentum)))),
        "total": total,
    }


def build_conclusion(scores, trend):
    t = scores["total"]
    if t >= 75:
        base = "综合评分高，可列入重点跟踪与分批配置候选。"
    elif t >= 60:
        base = "综合中性偏多，建议结合仓位与风险预算小步试探。"
    else:
        base = "综合偏弱，优先观察等待更优风险收益比。"

    if trend == "uptrend":
        base += " 当前技术趋势偏强。"
    elif trend == "downtrend":
        base += " 当前技术趋势偏弱。"
    return base


def human_text(report):
    val = report.get("valuation", {})
    news = report.get("news", [])
    news_text = "；".join([f"{n.get('time','')} {n.get('title','')}" for n in news[:3]]) if news else "暂无结构化新闻"
    return (
        f"股票：{report['symbol']} ({report['company']})\n"
        f"时间：{report['as_of']}\n"
        f"现价：{report['price']} {report['currency']} ({report['change_percent']}%)\n"
        f"估值：PE={val.get('pe')}, PB={val.get('pb')}, 市值={val.get('market_cap')}\n"
        f"技术面：SMA20={report['technical']['sma20']}, SMA50={report['technical']['sma50']}, "
        f"RSI14={report['technical']['rsi14']}, 趋势={report['technical']['trend']}\n"
        f"新闻/公告：{news_text}\n"
        f"风险：{'；'.join(report['risks'])}\n"
        f"催化：{'；'.join(report['catalysts'])}\n"
        f"评分：质量{report['scores']['quality']} / 估值{report['scores']['valuation']} / "
        f"动量{report['scores']['momentum']} / 总分{report['scores']['total']}\n"
        f"结论：{report['conclusion']}\n"
        f"置信度：{report['confidence']}"
    )


def is_cn_symbol(symbol: str) -> bool:
    s = symbol.strip().upper()
    if s.isdigit() and len(s) == 6:
        return True
    return s.endswith('.SZ') or s.endswith('.SH')


def to_secid(symbol: str) -> str:
    s = symbol.strip().upper().replace('.SZ', '').replace('.SH', '')
    if s.startswith('6'):
        return f"1.{s}"
    return f"0.{s}"


def parse_cn_pe(raw_val):
    if raw_val is None:
        return None
    try:
        v = float(raw_val) / 100
        if abs(v) > 10000:
            return None
        return round(v, 2)
    except Exception:
        return None


def fetch_cn_quote(symbol: str):
    secid = to_secid(symbol)
    fields = "f57,f58,f43,f44,f45,f46,f47,f48,f60,f169,f170,f162,f167,f116,f117"
    url = f"https://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields={fields}"
    data = requests.get(url, timeout=10).json().get("data")
    if not data:
        raise RuntimeError(f"未获取到 {symbol} 实时行情")

    price = (data.get("f43") or 0) / 100
    prev = (data.get("f60") or 0) / 100
    return {
        "symbol": data.get("f57", symbol),
        "company": data.get("f58") or symbol,
        "price": round(price, 2),
        "open": round((data.get("f46") or 0) / 100, 2),
        "high": round((data.get("f44") or 0) / 100, 2),
        "low": round((data.get("f45") or 0) / 100, 2),
        "change_percent": round(((price - prev) / prev * 100), 2) if prev else 0,
        "pe": parse_cn_pe(data.get("f162")),
        "pb": round((data.get("f167") or 0) / 100, 2) if data.get("f167") is not None else None,
        "market_cap": int(data.get("f116")) if data.get("f116") else None,
        "float_market_cap": int(data.get("f117")) if data.get("f117") else None,
    }


def fetch_cn_daily_closes(symbol: str, lmt: int = 120):
    secid = to_secid(symbol)
    params = {
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "klt": "101",
        "fqt": "1",
        "secid": secid,
        "lmt": str(lmt),
        "end": "20500101",
    }
    url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
    data = requests.get(url, params=params, timeout=10).json().get("data")
    if not data or not data.get("klines"):
        raise RuntimeError(f"未获取到 {symbol} 日线数据")

    closes = []
    for line in data["klines"]:
        # date,open,close,high,low,...
        parts = line.split(",")
        if len(parts) >= 3:
            closes.append(float(parts[2]))
    return closes


def fetch_cn_announcements(symbol: str, limit: int = 5):
    s = symbol.strip().upper().replace('.SZ', '').replace('.SH', '')
    market = 'SZ' if s.startswith(('0', '3')) else 'SH'
    params = {
        "sr": "-1",
        "page_size": str(limit),
        "page_index": "1",
        "ann_type": "A",
        "client_source": "web",
        "stock_list": f"{s}"
    }
    url = "https://np-anotice-stock.eastmoney.com/api/security/ann"
    data = requests.get(url, params=params, timeout=10).json().get("data", {})
    res = []
    for item in data.get("list", [])[:limit]:
        title = item.get("title", "")
        ts = item.get("display_time", "")
        art_code = item.get("art_code", "")
        link = f"https://data.eastmoney.com/notices/detail/{market}{s}/{art_code}.html"
        if title:
            res.append({"time": ts, "title": title, "link": link})
    return res


def sample_report(symbol):
    closes = [
        186.2, 187.1, 186.4, 188.2, 189.0, 188.6, 189.9, 190.5, 191.2, 191.0,
        192.1, 193.2, 192.8, 193.9, 194.4, 194.9, 195.4, 195.0, 196.2, 196.8,
        197.5, 198.1, 197.2, 198.9, 199.4, 200.0, 199.5, 200.8, 201.1, 201.5,
        202.0, 202.6, 203.2, 202.9, 203.8, 204.1, 203.7, 204.5, 205.0, 205.7,
        206.1, 206.4, 205.9, 206.8, 207.2, 207.9, 208.3, 208.0, 208.7, 209.4,
        210.1, 209.7, 210.5, 211.0, 211.4, 212.1, 212.8, 213.2, 213.7, 214.1,
    ]
    price = closes[-1]
    prev = closes[-2]
    change_percent = round((price - prev) / prev * 100, 2)
    sma20_v = sma(closes, 20)
    sma50_v = sma(closes, 50)
    rsi_v = rsi14(closes)

    trend = "sideways"
    if sma20_v and sma50_v:
        if price > sma20_v > sma50_v:
            trend = "uptrend"
        elif price < sma20_v < sma50_v:
            trend = "downtrend"

    pe = 29.4
    mcap = 3.2e12
    scores = calc_scores(pe, rsi_v, trend)

    return {
        "symbol": symbol.upper(),
        "company": "Sample Corp (Offline)",
        "as_of": datetime.now(timezone.utc).isoformat(),
        "price": round(price, 2),
        "currency": "USD",
        "change_percent": change_percent,
        "valuation": {"pe": pe, "market_cap": int(mcap)},
        "technical": {
            "sma20": round(sma20_v, 2) if sma20_v else None,
            "sma50": round(sma50_v, 2) if sma50_v else None,
            "rsi14": round(rsi_v, 2) if rsi_v else None,
            "trend": trend,
        },
        "risks": [
            "宏观流动性收紧导致估值压缩",
            "财报不及预期引发回撤",
            "行业竞争加剧影响利润率",
        ],
        "catalysts": [
            "新产品周期带来收入增长",
            "回购/分红提升股东回报",
            "指引上修触发盈利预期抬升",
        ],
        "scores": scores,
        "conclusion": build_conclusion(scores, trend),
        "confidence": "medium (sample)",
        "data_sources": ["offline_sample_dataset"],
    }


def online_report(symbol):
    if is_cn_symbol(symbol):
        q = fetch_cn_quote(symbol)
        closes = fetch_cn_daily_closes(symbol)
        if len(closes) < 55:
            raise RuntimeError(f"{symbol} 日线数据不足，至少需要 55 个交易日。")

        price = q["price"]
        sma20_v = sma(closes, 20)
        sma50_v = sma(closes, 50)
        rsi_v = rsi14(closes)

        trend = "sideways"
        if sma20_v and sma50_v:
            if price > sma20_v > sma50_v:
                trend = "uptrend"
            elif price < sma20_v < sma50_v:
                trend = "downtrend"

        pe = q.get("pe")
        scores = calc_scores(pe if isinstance(pe, (int, float)) else None, rsi_v, trend)

        notices = fetch_cn_announcements(symbol, limit=5)
        notice_titles = [n["title"] for n in notices[:3]]

        risks = ["成长风格回撤时弹性较高，波动风险偏大", "若跌破关键支撑位需防守仓位"]
        if pe is not None and pe < 0:
            risks.append("当前PE为负，盈利稳定性需持续跟踪")
        if trend == "downtrend":
            risks.append("技术趋势偏弱，反弹失败风险较高")

        catalysts = ["若公告出现订单/业绩超预期，可能触发估值修复", "资金回流并放量突破关键位可增强上行延续"]
        if notice_titles:
            catalysts.append(f"近期公告关注：{notice_titles[0][:28]}")

        return {
            "symbol": q["symbol"],
            "company": q["company"],
            "as_of": datetime.now(timezone.utc).isoformat(),
            "price": round(price, 2),
            "currency": "CNY",
            "change_percent": q["change_percent"],
            "valuation": {
                "pe": pe,
                "pb": q.get("pb"),
                "market_cap": q.get("market_cap"),
                "float_market_cap": q.get("float_market_cap"),
            },
            "technical": {
                "sma20": round(sma20_v, 2) if sma20_v else None,
                "sma50": round(sma50_v, 2) if sma50_v else None,
                "rsi14": round(rsi_v, 2) if rsi_v else None,
                "trend": trend,
            },
            "news": notices,
            "risks": risks,
            "catalysts": catalysts,
            "scores": scores,
            "conclusion": build_conclusion(scores, trend),
            "confidence": "medium",
            "data_sources": ["eastmoney_quote", "eastmoney_kline", "eastmoney_announcements"],
        }

    try:
        import yfinance as yf
    except Exception:
        raise RuntimeError(
            "缺少 yfinance。请先运行 scripts/install_deps.sh 安装依赖，或使用 --sample 离线模式。"
        )

    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="6mo", interval="1d")
    if hist.empty:
        raise RuntimeError(f"未获取到 {symbol} 历史数据，请检查代码或网络。")

    closes = [float(x) for x in hist["Close"].dropna().tolist()]
    if len(closes) < 55:
        raise RuntimeError(f"{symbol} 历史数据不足，至少需要 55 个交易日。")

    info = ticker.info or {}
    company = info.get("shortName") or info.get("longName") or symbol.upper()
    currency = info.get("currency", "USD")
    pe = info.get("trailingPE")
    mcap = info.get("marketCap")

    price = closes[-1]
    prev = closes[-2]
    change_percent = round((price - prev) / prev * 100, 2)
    sma20_v = sma(closes, 20)
    sma50_v = sma(closes, 50)
    rsi_v = rsi14(closes)

    trend = "sideways"
    if sma20_v and sma50_v:
        if price > sma20_v > sma50_v:
            trend = "uptrend"
        elif price < sma20_v < sma50_v:
            trend = "downtrend"

    scores = calc_scores(pe if isinstance(pe, (int, float)) else None, rsi_v, trend)

    risks = ["宏观波动影响风险偏好", "估值高位回撤风险"]
    if pe and pe > 35:
        risks.append("高PE对业绩兑现要求较高")

    catalysts = ["财报超预期", "行业景气度上行"]
    if trend == "uptrend":
        catalysts.append("技术面维持多头结构")

    return {
        "symbol": symbol.upper(),
        "company": company,
        "as_of": datetime.now(timezone.utc).isoformat(),
        "price": round(price, 2),
        "currency": currency,
        "change_percent": change_percent,
        "valuation": {
            "pe": round(pe, 2) if isinstance(pe, (int, float)) and not math.isnan(pe) else None,
            "market_cap": int(mcap) if isinstance(mcap, (int, float)) else None,
        },
        "technical": {
            "sma20": round(sma20_v, 2) if sma20_v else None,
            "sma50": round(sma50_v, 2) if sma50_v else None,
            "rsi14": round(rsi_v, 2) if rsi_v else None,
            "trend": trend,
        },
        "news": [],
        "risks": risks,
        "catalysts": catalysts,
        "scores": scores,
        "conclusion": build_conclusion(scores, trend),
        "confidence": "medium",
        "data_sources": ["yfinance"],
    }


def main():
    parser = argparse.ArgumentParser(description="Single stock deep analysis")
    parser.add_argument("symbol", help="股票代码，例如 AAPL / TSLA / 600519.SS")
    parser.add_argument("--out-dir", default=str(Path(__file__).resolve().parents[1] / "outputs"))
    parser.add_argument("--sample", action="store_true", help="使用离线样例数据")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    report = sample_report(args.symbol) if args.sample else online_report(args.symbol)

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    stem = f"{args.symbol.upper()}_{ts}"
    json_path = out_dir / f"{stem}.json"
    txt_path = out_dir / f"{stem}.txt"

    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    txt_path.write_text(human_text(report) + "\n", encoding="utf-8")

    print(json.dumps({"json": str(json_path), "txt": str(txt_path), "symbol": report["symbol"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
