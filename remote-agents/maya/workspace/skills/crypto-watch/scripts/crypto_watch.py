#!/usr/bin/env python3
"""crypto-watch: anomaly + opportunity alerts for major coins.

- Reads config from ~/.openclaw/workspace/crypto-watch/watchlist.json
- Fetches 15m candles from Binance public API by default (no key)
  - Fallback to OKX public candles if Binance is blocked (e.g. HTTP 451)
- Maintains runtime state in /tmp/openclaw/crypto-watch-state.json
- If no alerts: prints nothing
- If alerts: prints JSON to stdout:
    {"ts": <epoch>, "alerts": [{"symbol":..., "name":..., "lines":[...], "chart": "/tmp/...png"}, ...]}

Designed to be run periodically (e.g. every 5 minutes) by OpenClaw cron.
"""

from __future__ import annotations

import json
import os
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone

BINANCE_BASE = "https://api.binance.com"
OKX_BASE = "https://www.okx.com"

CONFIG_PATH = os.path.expanduser("~/.openclaw/workspace/crypto-watch/watchlist.json")
STATE_PATH = "/tmp/openclaw/crypto-watch-state.json"
CHART_DIR = "/tmp/openclaw/crypto-watch-charts"


def _http_json(url: str, timeout: int = 10):
    req = urllib.request.Request(url, headers={"User-Agent": "openclaw-crypto-watch/0.4"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw)


def _binance_klines(symbol: str, interval: str = "15m", limit: int = 300):
    # Binance max limit is 1000
    limit = max(10, min(int(limit), 1000))
    qs = urllib.parse.urlencode({"symbol": symbol, "interval": interval, "limit": str(limit)})
    url = f"{BINANCE_BASE}/api/v3/klines?{qs}"
    data = _http_json(url)
    rows = []
    for k in data:
        # [open_time, open, high, low, close, volume, close_time, ...]
        t = float(k[0]) / 1000.0
        o = float(k[1])
        h = float(k[2])
        l = float(k[3])
        c = float(k[4])
        v = float(k[5])
        rows.append((t, o, h, l, c, v))
    return rows


def _okx_candles(inst_id: str, bar: str = "15m", limit: int = 300):
    limit = max(50, min(int(limit), 300))
    qs = urllib.parse.urlencode({"instId": inst_id, "bar": bar, "limit": str(limit)})
    url = f"{OKX_BASE}/api/v5/market/candles?{qs}"
    obj = _http_json(url)
    if str(obj.get("code")) != "0":
        raise RuntimeError(f"OKX error: {obj}")
    data = obj.get("data") or []
    data = list(reversed(data))  # newest-first -> reverse
    rows = []
    for c in data:
        t = float(c[0]) / 1000.0
        o = float(c[1])
        h = float(c[2])
        l = float(c[3])
        cl = float(c[4])
        v = float(c[5])
        rows.append((t, o, h, l, cl, v))
    return rows


def _load_json(path: str, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except Exception:
        return default


def _save_json(path: str, payload):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def _pct(a: float, b: float) -> float:
    if a == 0:
        return 0.0
    return (b - a) / a * 100.0


def _fmt_price(x: float) -> str:
    if x >= 1000:
        return f"{x:,.0f}"
    if x >= 100:
        return f"{x:,.2f}"
    if x >= 1:
        return f"{x:,.4f}"
    return f"{x:,.8f}"


def _make_wide_chart(name: str, rows, limit: int = 300) -> str | None:
    """Generate a wide 15m K-line chart with volume. Returns path or None."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        from matplotlib.patches import Rectangle
    except Exception:
        return None

    if not rows:
        return None

    os.makedirs(CHART_DIR, exist_ok=True)
    rows = rows[-limit:]

    xs = [mdates.date2num(datetime.fromtimestamp(t, tz=timezone.utc)) for t, *_ in rows]
    if len(xs) > 1:
        delta = min(xs[i + 1] - xs[i] for i in range(len(xs) - 1))
        w = delta * 0.65
    else:
        w = 0.02

    fig, (ax, axv) = plt.subplots(
        2,
        1,
        figsize=(16, 6),
        facecolor="#0f141c",
        gridspec_kw={"height_ratios": [4, 1], "hspace": 0.05},
    )
    ax.set_facecolor("#0f141c")
    axv.set_facecolor("#0f141c")

    up = "#22c55e"
    dn = "#ef4444"
    wick = "#9ca3af"

    vols = [r[5] for r in rows]
    maxv = max(vols) if vols else 1

    for i, (_t, o, h, l, c, v) in enumerate(rows):
        x = xs[i]
        color = up if c >= o else dn
        ax.plot([x, x], [l, h], color=wick, linewidth=0.8, alpha=0.9)
        y = min(o, c)
        height = abs(c - o) or 1e-9
        ax.add_patch(Rectangle((x - w / 2, y), w, height, facecolor=color, edgecolor=color, linewidth=0))
        axv.add_patch(Rectangle((x - w / 2, 0), w, v, facecolor=color, edgecolor="none", alpha=0.7))

    axv.set_ylim(0, maxv * 1.15)
    axv.set_yticks([])

    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
    ax.tick_params(axis="x", colors="#cbd5e1", labelsize=8)
    ax.tick_params(axis="y", colors="#cbd5e1", labelsize=9)
    ax.grid(True, color="#334155", alpha=0.25, linewidth=0.6)

    last_close = rows[-1][4]
    start_dt = datetime.fromtimestamp(rows[0][0], tz=timezone.utc)
    end_dt = datetime.fromtimestamp(rows[-1][0], tz=timezone.utc)
    ax.set_title(
        f"{name} 15m (last {len(rows)} bars) close={last_close:,.2f} | {start_dt:%Y-%m-%d %H:%M} → {end_dt:%Y-%m-%d %H:%M} UTC",
        color="#e5e7eb",
        fontsize=11,
        pad=8,
    )

    ax.set_xlim(xs[0] - w, xs[-1] + w)
    axv.set_xlim(xs[0] - w, xs[-1] + w)

    out = os.path.join(CHART_DIR, f"{name.lower()}_15m_{int(time.time())}.png")
    plt.savefig(out, dpi=170, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return out


@dataclass
class Thresholds:
    crash15m: float
    spike15m: float
    crash1h: float
    spike1h: float
    bounce: float
    crash_window_s: int
    cooldown_s: int


def main() -> int:
    cfg = _load_json(CONFIG_PATH, None)
    if not cfg or "symbols" not in cfg:
        return 0

    th_cfg = cfg.get("thresholds", {})
    thresholds = Thresholds(
        crash15m=float(th_cfg.get("crash15mPct", -2.0)),
        spike15m=float(th_cfg.get("spike15mPct", 2.0)),
        crash1h=float(th_cfg.get("crash1hPct", -4.0)),
        spike1h=float(th_cfg.get("spike1hPct", 4.0)),
        bounce=float(th_cfg.get("bounceFromLowPct", 1.8)),
        crash_window_s=int(float(th_cfg.get("crashWindowHours", 6)) * 3600),
        cooldown_s=int(float(th_cfg.get("cooldownMinutes", 60)) * 60),
    )

    bars = int(cfg.get("bars", 300) or 300)
    bars = max(120, min(bars, 300))

    exchange = str(cfg.get("exchange", "binance")).lower().strip() or "binance"

    # intrabar (unfinished 15m candle) shock detection
    intrabar_range_pct = float(th_cfg.get("intrabarRange15mPct", 4.0) or 4.0)
    intrabar_leg_pct = float(th_cfg.get("intrabarLeg15mPct", 2.0) or 2.0)
    intrabar_cooldown_s = int(float(th_cfg.get("intrabarCooldownMinutes", 20) or 20) * 60)

    state = _load_json(STATE_PATH, {"symbols": {}})
    state_syms = state.setdefault("symbols", {})

    now = int(time.time())
    out_alerts = []

    for item in cfg.get("symbols", []):
        sym = str(item.get("symbol", "")).upper().strip()
        name = str(item.get("name", sym)).upper().strip() or sym
        if not sym:
            continue

        sym_state = state_syms.setdefault(sym, {})
        last_alert = sym_state.setdefault("last_alert", {})
        crash_state = sym_state.setdefault("crash", {"active": False, "ts": 0, "low": None})

        # fetch candles
        k15 = None
        if exchange == "binance":
            try:
                k15 = _binance_klines(sym, "15m", bars + 2)
            except Exception:
                # fallback
                try:
                    k15 = _okx_candles(sym.replace("USDT", "-USDT"), "15m", bars + 2)
                except Exception:
                    k15 = None
        else:
            try:
                k15 = _okx_candles(sym.replace("USDT", "-USDT"), "15m", bars + 2)
            except Exception:
                k15 = None

        if not k15 or len(k15) < 60:
            continue

        highs = [x[2] for x in k15]
        lows = [x[3] for x in k15]
        closes = [x[4] for x in k15]
        vols = [x[5] for x in k15]

        # treat last bar as possibly in-progress; last closed = -2
        prev_close = closes[-3]
        last_close = closes[-2]
        cur_low = lows[-1]

        price = last_close
        ch15 = _pct(prev_close, last_close)
        ch1h = _pct(closes[-6], last_close) if len(closes) >= 6 else 0.0

        highs_closed = highs[:-1]
        lows_closed = lows[:-1]
        closes_closed = closes[:-1]
        vols_closed = vols[:-1]

        hi300 = max(highs_closed)
        lo300 = min(lows_closed)

        # volume context
        vol20 = (sum(vols_closed[-20:]) / 20.0) if len(vols_closed) >= 20 else None
        vol_mult = (vols_closed[-1] / vol20) if (vol20 and vol20 > 0) else None

        # z-score of 15m return over last 96 bars (~24h)
        z = None
        if len(closes_closed) >= 100:
            rets = []
            for i in range(-97, -1):
                a = closes_closed[i - 1]
                b = closes_closed[i]
                rets.append(_pct(a, b))
            m = sum(rets) / len(rets)
            var = sum((x - m) ** 2 for x in rets) / max(1, (len(rets) - 1))
            sd = var ** 0.5
            if sd > 1e-9:
                z = (ch15 - m) / sd

        # recent range (default last 50 bars)
        lb = int(th_cfg.get("breakoutLookbackBars", 50) or 50)
        lb = max(20, min(lb, len(highs_closed) - 2))
        hiN = max(highs_closed[-lb - 1 : -1])
        loN = min(lows_closed[-lb - 1 : -1])
        breakoutN = price > hiN
        breakdownN = price < loN

        # crude swing structure (Dow-ish)
        def pivots(vals, kind="high"):
            idxs = []
            for i in range(2, len(vals) - 2):
                if kind == "high":
                    if vals[i] > vals[i - 1] and vals[i] > vals[i - 2] and vals[i] >= vals[i + 1] and vals[i] >= vals[i + 2]:
                        idxs.append(i)
                else:
                    if vals[i] < vals[i - 1] and vals[i] < vals[i - 2] and vals[i] <= vals[i + 1] and vals[i] <= vals[i + 2]:
                        idxs.append(i)
            return idxs

        window = max(60, lb + 20)
        hs = highs_closed[-window:]
        ls = lows_closed[-window:]
        ph = pivots(hs, "high")
        pl = pivots(ls, "low")
        trend = None
        try:
            if len(ph) >= 2 and len(pl) >= 2:
                hh1 = hs[ph[-1]]
                hh0 = hs[ph[-2]]
                ll1 = ls[pl[-1]]
                ll0 = ls[pl[-2]]
                if hh1 > hh0 and ll1 > ll0:
                    trend = "HH/HL"
                elif hh1 < hh0 and ll1 < ll0:
                    trend = "LH/LL"
        except Exception:
            trend = None

        def ctx() -> str:
            bits = []
            if vol_mult is not None:
                bits.append(f"量:{vol_mult:.1f}x")
            bits.append(f"近{lb}区间:{_fmt_price(loN)}~{_fmt_price(hiN)}")
            bits.append(f"大区间:{_fmt_price(lo300)}~{_fmt_price(hi300)}")
            if trend:
                bits.append(f"结构:{trend}")
            if z is not None:
                bits.append(f"z:{z:+.1f}")
            return " · ".join(bits)

        def cooled(key: str, cooldown_s: int | None = None) -> bool:
            ts = int(last_alert.get(key, 0) or 0)
            cd = thresholds.cooldown_s if cooldown_s is None else int(cooldown_s)
            return (now - ts) >= cd

        lines = []

        # Opportunity: breakout/breakdown with volume confirmation
        vol_ok = (vol_mult is None) or (vol_mult >= float(th_cfg.get("breakoutVolMult", 1.5) or 1.5))
        if breakoutN and vol_ok and cooled("breakout"):
            lines.append(f"【突破机会】{name} 15m 上破近{lb}区间 价:{_fmt_price(price)}")
            lines.append(f"  {ctx()}")
            last_alert["breakout"] = now

        if breakdownN and vol_ok and cooled("breakdown"):
            lines.append(f"【跌破警报】{name} 15m 下破近{lb}区间 价:{_fmt_price(price)}")
            lines.append(f"  {ctx()}")
            last_alert["breakdown"] = now

        # Intrabar shock (unfinished 15m candle): capture violent swings that may fade before close.
        cur_open = float(k15[-1][1])
        cur_high = float(k15[-1][2])
        cur_low_live = float(k15[-1][3])
        cur_close = float(k15[-1][4])
        cur_ts = int(k15[-1][0])
        intrabar_range = ((cur_high - cur_low_live) / cur_open * 100.0) if cur_open > 0 else 0.0
        intrabar_up = ((cur_high - cur_open) / cur_open * 100.0) if cur_open > 0 else 0.0
        intrabar_down = ((cur_low_live - cur_open) / cur_open * 100.0) if cur_open > 0 else 0.0
        intrabar_move = _pct(prev_close, cur_close)
        last_intrabar_bar_ts = int(sym_state.get("last_intrabar_bar_ts", 0) or 0)
        intrabar_hit = (intrabar_range >= intrabar_range_pct) and (
            intrabar_up >= intrabar_leg_pct or intrabar_down <= -intrabar_leg_pct
        )
        if intrabar_hit and cooled("intrabar", intrabar_cooldown_s) and cur_ts != last_intrabar_bar_ts:
            lines.append(
                f"【盘中剧震(未收线)】{name} 15m 振幅 {intrabar_range:.2f}% (↑{intrabar_up:+.2f}% / ↓{intrabar_down:.2f}%) 现价:{_fmt_price(cur_close)}"
            )
            lines.append(f"  盘中相对前收:{intrabar_move:+.2f}% · {ctx()}")
            last_alert["intrabar"] = now
            sym_state["last_intrabar_bar_ts"] = cur_ts

        # Crash / Spike
        z_crash = (z is not None and z <= -3.0)
        z_spike = (z is not None and z >= 3.0)

        if (ch15 <= thresholds.crash15m or z_crash) and cooled("crash15m"):
            lines.append(f"【异常急跌】{name} 15m {ch15:.2f}% 价:{_fmt_price(price)}")
            lines.append(f"  {ctx()}")
            last_alert["crash15m"] = now
            crash_state["active"] = True
            crash_state["ts"] = now
            crash_state["low"] = cur_low

        if ch1h <= thresholds.crash1h and cooled("crash1h"):
            lines.append(f"【异常大跌】{name} 1h {ch1h:.2f}% 价:{_fmt_price(price)}")
            lines.append(f"  {ctx()}")
            last_alert["crash1h"] = now
            crash_state["active"] = True
            crash_state["ts"] = now
            crash_state["low"] = cur_low if crash_state.get("low") is None else min(float(crash_state["low"]), cur_low)

        if (ch15 >= thresholds.spike15m or z_spike) and cooled("spike15m"):
            lines.append(f"【异常急拉】{name} 15m +{ch15:.2f}% 价:{_fmt_price(price)}")
            lines.append(f"  {ctx()}")
            last_alert["spike15m"] = now

        if ch1h >= thresholds.spike1h and cooled("spike1h"):
            lines.append(f"【异常大涨】{name} 1h +{ch1h:.2f}% 价:{_fmt_price(price)}")
            lines.append(f"  {ctx()}")
            last_alert["spike1h"] = now

        # update crash low
        if crash_state.get("active"):
            ts0 = int(crash_state.get("ts", 0) or 0)
            if now - ts0 > thresholds.crash_window_s:
                crash_state["active"] = False
            else:
                low = crash_state.get("low")
                crash_state["low"] = cur_low if low is None else min(float(low), cur_low)

        # bounce
        if crash_state.get("active") and crash_state.get("low") is not None and cooled("bounce"):
            low = float(crash_state["low"])
            if low > 0 and price >= low * (1.0 + thresholds.bounce / 100.0):
                rebound = _pct(low, price)
                lines.append(f"【大跌反弹】{name} 从低点反弹 +{rebound:.2f}% 价:{_fmt_price(price)}")
                lines.append(f"  {ctx()}")
                last_alert["bounce"] = now
                crash_state["active"] = False

        if lines:
            chart = _make_wide_chart(name, k15, limit=min(300, bars))
            out_alerts.append({
                "symbol": sym,
                "name": name,
                "lines": lines,
                "chart": chart,
            })

    _save_json(STATE_PATH, state)

    if not out_alerts:
        return 0

    print(json.dumps({"ts": now, "alerts": out_alerts}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
