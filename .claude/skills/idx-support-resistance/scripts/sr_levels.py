#!/usr/bin/env python3
"""Deteksi support & resistance saham IDX dari data OHLCV (intraday, harian, atau mingguan).

Python murni (tanpa dependensi). Opsional: --ticker memakai yfinance jika terpasang.

Contoh:
    python3 sr_levels.py --csv BBCA.csv
    python3 sr_levels.py --csv BBRI_5m.csv --style bpjs
    python3 sr_levels.py --ticker BBCA --style investor
    python3 sr_levels.py --csv BBCA.csv --json
"""
import argparse
import csv
import json
import math
import sys
from collections import OrderedDict
from datetime import date

# Preset per gaya trading (lihat references/trading-styles/): interval & periode yfinance,
# jumlah bar yang dianalisis, dan lebar fractal swing kiri/kanan.
STYLE_PRESETS = {
    "scalper":    {"interval": "1m",  "period": "5d",  "lookback": 660, "window": 3},
    "bpjs":       {"interval": "5m",  "period": "1mo", "lookback": 330, "window": 3},
    "bsjp":       {"interval": "1d",  "period": "1y",  "lookback": 60,  "window": 3},
    "ara-hunter": {"interval": "1d",  "period": "1y",  "lookback": 60,  "window": 3},
    "swing":      {"interval": "1d",  "period": "2y",  "lookback": 250, "window": 5},
    "position":   {"interval": "1d",  "period": "5y",  "lookback": 500, "window": 10},
    "investor":   {"interval": "1wk", "period": "10y", "lookback": 260, "window": 4},
}
DEFAULTS = {"interval": "1d", "period": "2y", "lookback": 250, "window": 5}
FCA_BOARDS = ("akselerasi", "pemantauan")

# ---------------------------------------------------------------------------
# Aturan BEI (lihat references/idx-rules.md)
# ---------------------------------------------------------------------------

def tick_size(price):
    if price < 200:
        return 1
    if price < 500:
        return 2
    if price < 2000:
        return 5
    if price < 5000:
        return 10
    return 25


def round_tick(price, mode="nearest"):
    def snap(t):
        q = price / t
        if mode == "down":
            return math.floor(q + 1e-9) * t
        if mode == "up":
            return math.ceil(q - 1e-9) * t
        return math.floor(q + 0.5) * t

    t = tick_size(price)
    v = snap(t)
    # Pembulatan bisa melewati batas fraksi; hitung ulang dengan fraksi harga hasil.
    if tick_size(v) != t:
        v = snap(tick_size(v))
    return int(v)


def min_price(board, rule):
    return 1 if board in FCA_BOARDS or rule == "baru" else 50


def auto_rejection(ref, board, arb_pct, rule):
    """Batas harga satu sesi dari harga acuan (close sesi sebelumnya)."""
    minp = min_price(board, rule)
    if ref <= 10 and (board in FCA_BOARDS or rule == "baru"):
        r = int(round(ref))
        return {"ara": r + 1, "arb": max(minp, r - 1), "ara_pct": None, "arb_pct": None}
    if board in FCA_BOARDS:
        up = down = 0.10
    else:
        up = 0.35 if ref <= 200 else 0.25 if ref <= 5000 else 0.20
        down = arb_pct
    return {"ara": round_tick(ref * (1 + up), "down"),
            "arb": max(minp, round_tick(ref * (1 - down), "up")),
            "ara_pct": up, "arb_pct": down}


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

COL_ALIASES = {
    "date": ["date", "datetime", "tanggal", "time", "waktu"],
    "open": ["open", "pembukaan", "buka"],
    "high": ["high", "tertinggi"],
    "low": ["low", "terendah"],
    "close": ["adj close", "adj_close", "adjclose", "close", "penutupan", "tutup", "last"],
    "volume": ["volume", "vol"],
}


def _num(s):
    s = str(s).strip().replace(",", "")
    return float(s) if s not in ("", "null", "None", "nan", "-") else None


def load_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        headers = {h.strip().lower(): h for h in reader.fieldnames}
        cols = {}
        for key, aliases in COL_ALIASES.items():
            for a in aliases:
                if a in headers:
                    cols[key] = headers[a]
                    break
        missing = [k for k in ("date", "high", "low", "close") if k not in cols]
        if missing:
            sys.exit(f"Kolom wajib tidak ditemukan: {missing}. Header: {reader.fieldnames}")
        rows = []
        for r in reader:
            try:
                h, l, c = _num(r[cols["high"]]), _num(r[cols["low"]]), _num(r[cols["close"]])
            except ValueError:
                continue
            if None in (h, l, c) or h <= 0:
                continue
            o = _num(r[cols["open"]]) if "open" in cols else c
            v = _num(r[cols["volume"]]) if "volume" in cols else 0
            rows.append({"date": r[cols["date"]].strip()[:16].replace("T", " "), "open": o or c,
                         "high": h, "low": l, "close": c, "volume": v or 0})
    rows.sort(key=lambda x: x["date"])
    return rows


def load_yfinance(ticker, interval, period):
    try:
        import yfinance as yf
    except ImportError:
        sys.exit("yfinance belum terpasang. Pasang dengan: pip install yfinance  (atau pakai --csv)")
    sym = ticker.upper()
    if not sym.endswith(".JK"):
        sym += ".JK"
    df = yf.Ticker(sym).history(period=period, interval=interval, auto_adjust=True)
    if df.empty:
        sys.exit(f"Data {sym} ({interval}, {period}) kosong.")
    fmt = "%Y-%m-%d" if interval in ("1d", "5d", "1wk", "1mo", "3mo") else "%Y-%m-%d %H:%M"
    return [{"date": idx.strftime(fmt), "open": float(r["Open"]), "high": float(r["High"]),
             "low": float(r["Low"]), "close": float(r["Close"]), "volume": float(r["Volume"])}
            for idx, r in df.iterrows()]


# ---------------------------------------------------------------------------
# Indikator
# ---------------------------------------------------------------------------

def group_sessions(rows):
    groups = OrderedDict()
    for r in rows:
        groups.setdefault(r["date"][:10], []).append(r)
    return groups


def detect_timeframe(rows, sessions):
    if len(sessions) < len(rows):
        return "intraday"
    try:
        span = (date.fromisoformat(rows[-1]["date"][:10]) - date.fromisoformat(rows[0]["date"][:10])).days
    except ValueError:
        return "harian"
    gap = span / max(1, len(rows) - 1)
    return "bulanan" if gap >= 20 else "mingguan" if gap >= 4 else "harian"


def session_hlc(bars):
    return {"date": bars[0]["date"][:10], "open": bars[0]["open"], "high": max(b["high"] for b in bars),
            "low": min(b["low"] for b in bars), "close": bars[-1]["close"]}


def vwap(bars):
    v = sum(b["volume"] for b in bars)
    return sum((b["high"] + b["low"] + b["close"]) / 3 * b["volume"] for b in bars) / v if v else None


def sma(values, n):
    return sum(values[-n:]) / n if len(values) >= n else None


def atr(rows, n=14):
    trs = []
    for i in range(1, len(rows)):
        h, l, pc = rows[i]["high"], rows[i]["low"], rows[i - 1]["close"]
        trs.append(max(h - l, abs(h - pc), abs(l - pc)))
    return sum(trs[-n:]) / min(n, len(trs)) if trs else 0


def find_swings(rows, w):
    swings = []
    for i in range(w, len(rows) - w):
        seg = rows[i - w:i + w + 1]
        if rows[i]["high"] >= max(r["high"] for r in seg):
            swings.append(("high", i, rows[i]["high"]))
        if rows[i]["low"] <= min(r["low"] for r in seg):
            swings.append(("low", i, rows[i]["low"]))
    return swings


def cluster_levels(swings, rows, tol, avg_vol):
    pts = sorted(swings, key=lambda s: s[2])
    clusters = []
    for s in pts:
        # Batasi lebar cluster agar tidak "merambat" menjadi zona yang terlalu lebar.
        if clusters and abs(s[2] - clusters[-1]["mean"]) <= tol and s[2] - clusters[-1]["points"][0][2] <= tol * 2:
            c = clusters[-1]
            c["points"].append(s)
            c["mean"] = sum(p[2] for p in c["points"]) / len(c["points"])
        else:
            clusters.append({"points": [s], "mean": s[2]})

    n = len(rows)
    out = []
    for c in clusters:
        idxs = [p[1] for p in c["points"]]
        prices = [p[2] for p in c["points"]]
        touches = len(c["points"])
        last_idx = max(idxs)
        recency = 1 - (n - 1 - last_idx) / n
        vol_ratio = (sum(rows[i]["volume"] for i in idxs) / touches / avg_vol) if avg_vol else 1
        kinds = {p[0] for p in c["points"]}
        score = level_score(touches, recency, vol_ratio, len(kinds) == 2)
        out.append({
            "level": c["mean"], "lo": min(prices), "hi": max(prices), "touches": touches,
            "last_touch": rows[last_idx]["date"], "recency": round(recency, 2),
            "vol_ratio": round(vol_ratio, 2), "role_reversal": len(kinds) == 2,
            "score": round(score, 2),
        })
    return out


def level_score(touches, recency, vol_ratio, role_reversal):
    return round(touches * 2 + recency * 3 + min(vol_ratio, 3) + (1.5 if role_reversal else 0), 2)


def build_zones(levels, t, tol):
    """Bulatkan zona ke fraksi harga lalu gabungkan zona yang tumpang tindih."""
    for lv in levels:
        lv["zone_lo"] = max(1, round_tick(lv["lo"] - t, "down"))
        lv["zone_hi"] = round_tick(lv["hi"] + t, "up")
    merged = []
    for lv in sorted(levels, key=lambda x: x["zone_lo"]):
        m = merged[-1] if merged else None
        if m and lv["zone_lo"] <= m["zone_hi"] and max(m["zone_hi"], lv["zone_hi"]) - m["zone_lo"] <= tol * 3 + 2 * t:
            w = m["touches"] + lv["touches"]
            m["level"] = (m["level"] * m["touches"] + lv["level"] * lv["touches"]) / w
            m["vol_ratio"] = round((m["vol_ratio"] * m["touches"] + lv["vol_ratio"] * lv["touches"]) / w, 2)
            m["lo"], m["hi"] = min(m["lo"], lv["lo"]), max(m["hi"], lv["hi"])
            m["zone_hi"] = max(m["zone_hi"], lv["zone_hi"])
            m["touches"] = w
            m["last_touch"] = max(m["last_touch"], lv["last_touch"])
            m["recency"] = max(m["recency"], lv["recency"])
            m["role_reversal"] = m["role_reversal"] or lv["role_reversal"]
            m["score"] = level_score(w, m["recency"], m["vol_ratio"], m["role_reversal"])
        else:
            merged.append(dict(lv))
    return merged


def volume_profile(rows, bin_size, top=5):
    lo = min(r["low"] for r in rows)
    bins = {}
    for r in rows:
        if r["volume"] <= 0:
            continue
        a, b = int((r["low"] - lo) // bin_size), int((r["high"] - lo) // bin_size)
        share = r["volume"] / (b - a + 1)
        for k in range(a, b + 1):
            bins[k] = bins.get(k, 0) + share
    total = sum(bins.values()) or 1
    ranked = sorted(bins.items(), key=lambda kv: kv[1], reverse=True)[:top]
    return [{"lo": round_tick(lo + k * bin_size, "down"), "hi": round_tick(lo + (k + 1) * bin_size, "up"),
             "pct_volume": round(v / total * 100, 1)} for k, v in ranked]


def classic_pivots(bar):
    h, l, c = bar["high"], bar["low"], bar["close"]
    p = (h + l + c) / 3
    raw = {"R2": p + (h - l), "R1": 2 * p - l, "P": p, "S1": 2 * p - h, "S2": p - (h - l)}
    return {k: round_tick(max(v, 1)) for k, v in raw.items()}


def rsi_series(closes, n=14):
    """RSI Wilder; elemen ke-i sejajar dengan closes[i] (None sebelum data cukup)."""
    if len(closes) <= n:
        return [None] * len(closes)
    diffs = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    ag = sum(max(d, 0) for d in diffs[:n]) / n
    al = sum(max(-d, 0) for d in diffs[:n]) / n

    def value():
        if al == 0:
            return 50.0 if ag == 0 else 100.0
        return 100 - 100 / (1 + ag / al)

    out = [None] * n + [value()]
    for d in diffs[n:]:
        ag = (ag * (n - 1) + max(d, 0)) / n
        al = (al * (n - 1) + max(-d, 0)) / n
        out.append(value())
    return out


def momentum_divergence(data, vals, swings):
    """Bandingkan dua swing low dan dua swing high terakhir antara harga dan indikator (RSI/MACD)."""
    rsi_vals = vals
    found = []
    for kind in ("low", "high"):
        pts = [s for s in swings if s[0] == kind and rsi_vals[s[1]] is not None][-2:]
        if len(pts) < 2:
            continue
        (_, i1, p1), (_, i2, p2) = pts
        r1, r2 = rsi_vals[i1], rsi_vals[i2]
        label = None
        if kind == "low":
            if p2 < p1 and r2 > r1:
                label = "bullish divergence (regular) — potensi pembalikan naik"
            elif p2 > p1 and r2 < r1:
                label = "hidden bullish divergence — potensi kelanjutan tren naik"
        else:
            if p2 > p1 and r2 < r1:
                label = "bearish divergence (regular) — potensi pembalikan turun"
            elif p2 < p1 and r2 > r1:
                label = "hidden bearish divergence — potensi kelanjutan tren turun"
        if label:
            found.append({"type": label, "from": data[i1]["date"], "to": data[i2]["date"],
                          "price": [p1, p2], "rsi": [round(r1, 1), round(r2, 1)],
                          "bars_ago": len(data) - 1 - i2})
    return found


def volume_analysis(data, n=20):
    vols = [r["volume"] for r in data]
    if not any(vols) or len(data) < 3:
        return None
    up_vol = down_vol = 0
    spikes = []
    for i in range(max(1, len(data) - n), len(data)):
        prior = vols[max(0, i - n):i]
        avg_i = sum(prior) / len(prior)
        chg = data[i]["close"] / data[i - 1]["close"] - 1
        if chg > 0:
            up_vol += vols[i]
        elif chg < 0:
            down_vol += vols[i]
        if avg_i and vols[i] >= 2 * avg_i:
            spikes.append({"date": data[i]["date"], "ratio": round(vols[i] / avg_i, 1),
                           "change_pct": round(chg * 100, 2)})
    obv = [0]
    for i in range(1, len(data)):
        d = data[i]["close"] - data[i - 1]["close"]
        obv.append(obv[-1] + (vols[i] if d > 0 else -vols[i] if d < 0 else 0))
    k = min(n, len(data) - 1)
    obv_up = obv[-1] > obv[-1 - k]
    price_up = data[-1]["close"] > data[-1 - k]["close"]
    avg20 = sum(vols[-n:]) / min(n, len(vols))
    avg50 = sum(vols[-50:]) / min(50, len(vols))
    return {
        "avg_volume_20": round(avg20),
        "avg_volume_50": round(avg50),
        "last_vs_avg20": round(vols[-1] / avg20, 2) if avg20 else None,
        "ratio_20_vs_50": round(avg20 / avg50, 2) if avg50 else None,
        "up_down_volume_ratio_20": round(up_vol / down_vol, 2) if down_vol else None,
        "obv_20": "naik" if obv_up else "turun",
        "price_20": "naik" if price_up else "turun",
        "obv_divergence": obv_up != price_up,
        "spikes_20": spikes[-5:],
    }


def sma_series(values, n):
    out, total = [None] * len(values), 0.0
    for i, v in enumerate(values):
        total += v
        if i >= n:
            total -= values[i - n]
        if i >= n - 1:
            out[i] = total / n
    return out


def ema_series(values, n):
    """EMA dengan seed SMA n bar pertama; elemen ke-i sejajar values[i]."""
    if len(values) < n:
        return [None] * len(values)
    k = 2 / (n + 1)
    out = [None] * (n - 1) + [sum(values[:n]) / n]
    for v in values[n:]:
        out.append(v * k + out[-1] * (1 - k))
    return out


def last_cross(a, b, dates, window):
    """Persilangan terakhir seri a terhadap b dalam `window` bar terakhir: 'naik' = a memotong b ke atas."""
    n = len(a)
    for i in range(n - 1, max(1, n - window) - 1, -1):
        if None in (a[i], b[i], a[i - 1], b[i - 1]):
            break
        prev, cur = a[i - 1] - b[i - 1], a[i] - b[i]
        if prev <= 0 < cur or prev >= 0 > cur:
            return {"type": "naik" if cur > 0 else "turun", "date": dates[i], "bars_ago": n - 1 - i}
    return None


def ma_analysis(rows, window):
    closes = [r["close"] for r in rows]
    dates = [r["date"] for r in rows]
    price = closes[-1]
    series = {f"MA{n}": sma_series(closes, n) for n in (5, 10, 20, 50, 100, 200)}
    series["EMA20"] = ema_series(closes, 20)
    levels = {}
    for name, s in series.items():
        if s[-1] is None:
            continue
        prev = s[-6] if len(s) >= 6 else None
        levels[name] = {
            "value": round_tick(max(1, s[-1])),
            "dist_pct": round((price / s[-1] - 1) * 100, 2),
            "slope_5": None if prev is None else "naik" if s[-1] > prev else "turun" if s[-1] < prev else "datar",
        }
    trio = [series[k][-1] for k in ("MA20", "MA50", "MA200")]
    if None in trio:
        alignment = "data kurang untuk MA200"
    elif trio[0] > trio[1] > trio[2]:
        alignment = "bullish (MA20 > MA50 > MA200)"
    elif trio[0] < trio[1] < trio[2]:
        alignment = "bearish (MA20 < MA50 < MA200)"
    else:
        alignment = "campuran (transisi/sideways)"
    crosses = {}
    for fast, slow, up, down in (("MA50", "MA200", "golden cross", "death cross"),
                                 ("MA20", "MA50", "MA20 memotong MA50 ke atas", "MA20 memotong MA50 ke bawah")):
        c = last_cross(series[fast], series[slow], dates, window)
        if c:
            c["type"] = up if c["type"] == "naik" else down
        crosses[f"{fast}/{slow}"] = c
    return {"levels": levels, "alignment": alignment, "crosses": crosses}


def macd_analysis(rows, data, swings, fast=12, slow=26, signal=9):
    closes = [r["close"] for r in rows]
    dates = [r["date"] for r in rows]
    ef, es = ema_series(closes, fast), ema_series(closes, slow)
    line = [a - b if a is not None and b is not None else None for a, b in zip(ef, es)]
    start = next((i for i, v in enumerate(line) if v is not None), None)
    if start is None or len(closes) - start < signal + 2:
        return None
    sig = [None] * start + ema_series(line[start:], signal)
    hist = [m - s if m is not None and s is not None else None for m, s in zip(line, sig)]
    window = len(data)
    return {
        "setting": f"{fast},{slow},{signal}",
        "macd": round(line[-1], 2),
        "signal": round(sig[-1], 2),
        "histogram": round(hist[-1], 2),
        "macd_pct_of_price": round(line[-1] / closes[-1] * 100, 2),
        "above_signal": line[-1] > sig[-1],
        "above_zero": line[-1] > 0,
        "histogram_trend": ("positif" if hist[-1] > 0 else "negatif") + (
            " dan membesar" if abs(hist[-1]) > abs(hist[-2]) else " dan mengecil"),
        "last_signal_cross": last_cross(line, sig, dates, window),
        "last_zero_cross": last_cross(line, [0.0] * len(line), dates, window),
        "divergences": momentum_divergence(data, line[-len(data):], swings),
    }


def candle_patterns(data, zones, tol, tf, board, arb_pct, rule, last_n=3):
    """Deteksi pola candlestick pada `last_n` bar terakhir beserta lokasi terhadap zona S/R dan volume.

    Ambang bentuk candle adalah heuristik; definisinya ada di references/indicators/candlestick.md.
    """
    def parts(b):
        o, h, l, c = b["open"], b["high"], b["low"], b["close"]
        return o, h, l, c, abs(c - o), h - l, h - max(o, c), min(o, c) - l

    def bull(b):
        return b["close"] > b["open"]

    def bear(b):
        return b["close"] < b["open"]

    out = []
    for i in range(max(3, len(data) - last_n), len(data)):
        b, p1, p2 = data[i], data[i - 1], data[i - 2]
        o, h, l, c, body, rng, upper, lower = parts(b)
        if rng <= 0 and tf != "harian":
            continue
        o1, h1, l1, c1, body1, rng1, _, _ = parts(p1)
        o2, _, _, c2, body2, rng2, _, _ = parts(p2)
        prior = data[max(0, i - 6):i]
        trend = ("naik" if prior[-1]["close"] > prior[0]["close"]
                 else "turun" if prior[-1]["close"] < prior[0]["close"] else "datar")
        found = []

        if rng > 0:
            short_shadow = lambda s: s <= max(body * 0.5, rng * 0.1)
            if body <= rng * 0.1:
                found.append(("doji", "netral — keraguan"))
            if lower >= 2 * body and lower >= rng * 0.6 and short_shadow(upper):
                found.append(("hanging man", "bearish") if trend == "naik" else ("hammer", "bullish"))
            if upper >= 2 * body and upper >= rng * 0.6 and short_shadow(lower):
                found.append(("inverted hammer", "bullish") if trend == "turun" else ("shooting star", "bearish"))
            if body >= rng * 0.9:
                found.append(("marubozu bullish", "bullish") if c > o else ("marubozu bearish", "bearish"))
        if bear(p1) and bull(b) and o <= c1 and c >= o1 and body > body1:
            found.append(("bullish engulfing", "bullish"))
        if bull(p1) and bear(b) and o >= c1 and c <= o1 and body > body1:
            found.append(("bearish engulfing", "bearish"))
        if rng1 > 0 and body1 >= rng1 * 0.6 and body < body1 * 0.5 \
                and max(o, c) <= max(o1, c1) and min(o, c) >= min(o1, c1):
            if bear(p1):
                found.append(("bullish harami", "bullish — butuh konfirmasi"))
            elif bull(p1):
                found.append(("bearish harami", "bearish — butuh konfirmasi"))
        mid1 = (o1 + c1) / 2
        if bear(p1) and bull(b) and o <= c1 and mid1 < c < o1:
            found.append(("piercing line", "bullish"))
        if bull(p1) and bear(b) and o >= c1 and o1 < c < mid1:
            found.append(("dark cloud cover", "bearish"))
        if rng2 > 0 and body2 >= rng2 * 0.5 and body1 <= body2 * 0.3:
            # Candle tengah ("bintang") harus berada di bawah/atas close candle pertama.
            if bear(p2) and bull(b) and (o1 + c1) / 2 <= c2 and c > (o2 + c2) / 2:
                found.append(("morning star", "bullish"))
            if bull(p2) and bear(b) and (o1 + c1) / 2 >= c2 and c < (o2 + c2) / 2:
                found.append(("evening star", "bearish"))
        three = [p2, p1, b]
        if all(bull(x) and x["high"] - x["close"] <= (x["close"] - x["open"]) * 0.3 for x in three) \
                and c2 < c1 < c and o2 <= o1 <= c2 and o1 <= o <= c1:
            found.append(("three white soldiers", "bullish"))
        if all(bear(x) and x["close"] - x["low"] <= (x["open"] - x["close"]) * 0.3 for x in three) \
                and c2 > c1 > c and c2 <= o1 <= o2 and c1 <= o <= o1:
            found.append(("three black crows", "bearish"))
        # Gap sungguhan: celah antara range bar ini dan bar sebelumnya yang tidak tertutup di bar ini.
        if tf != "intraday" and l > h1:
            found.append((f"gap up {(l / h1 - 1) * 100:.1f}% (belum tertutup)", "bullish"))
        if tf != "intraday" and h < l1:
            found.append((f"gap down {(h / l1 - 1) * 100:.1f}% (belum tertutup)", "bearish"))
        if tf == "harian":
            lim = auto_rejection(c1, board, arb_pct, rule)
            if c >= lim["ara"]:
                found.append(("candle ARA (close di batas atas)", "bullish — cek antrean & risiko gorengan"))
            elif h >= lim["ara"]:
                found.append(("sempat ARA lalu turun (ekor atas)", "bearish — antrean ARA gagal bertahan"))
            if c <= lim["arb"]:
                found.append(("candle ARB (close di batas bawah)", "bearish — cek antrean jual"))
            elif l <= lim["arb"]:
                found.append(("sempat ARB lalu pulih (ekor bawah)", "bullish — ada pembeli di batas bawah"))
        if not found:
            continue

        location = []
        for z in zones:
            lo, hi = z["zone_lo"] - tol * 0.5, z["zone_hi"] + tol * 0.5
            if lo <= l <= hi or lo <= h <= hi or (l <= lo and h >= hi):
                role = "support" if z["mid"] <= c else "resistance"
                location.append(f"menguji {role} {fmt_rp(z['zone_lo'])}–{fmt_rp(z['zone_hi'])}")
        prior_vol = [x["volume"] for x in data[max(0, i - 20):i]]
        avg = sum(prior_vol) / len(prior_vol) if prior_vol else 0
        out.append({
            "date": b["date"],
            "patterns": [{"name": n, "bias": s} for n, s in found],
            "prior_trend_5": trend,
            "location": location[:2] or ["tidak di dekat zona S/R terdeteksi"],
            "volume_vs_avg20": round(b["volume"] / avg, 2) if avg else None,
            "bars_ago": len(data) - 1 - i,
        })
    return out


FIB_RETRACEMENT = [0.236, 0.382, 0.5, 0.618, 0.786]
FIB_EXTENSION = [1.272, 1.618]


def fibonacci(data, price):
    """Fibonacci dari high tertinggi & low terendah lookback; arah = ekstrem mana yang lebih akhir."""
    hi_i = max(range(len(data)), key=lambda i: data[i]["high"])
    lo_i = min(range(len(data)), key=lambda i: data[i]["low"])
    hi, lo = data[hi_i]["high"], data[lo_i]["low"]
    rng = hi - lo
    if rng <= 0:
        return None
    up = lo_i < hi_i
    pct = lambda r: f"{r * 100:.1f}%".replace(".0%", "%")
    return {
        "direction": "naik" if up else "turun",
        "anchor_low": {"date": data[lo_i]["date"], "price": lo},
        "anchor_high": {"date": data[hi_i]["date"], "price": hi},
        "retracement": {pct(r): round_tick(max(1, hi - rng * r if up else lo + rng * r)) for r in FIB_RETRACEMENT},
        "extension": {pct(e): round_tick(max(1, lo + rng * e if up else hi - rng * e)) for e in FIB_EXTENSION},
        "retracement_now_pct": round(((hi - price) if up else (price - lo)) / rng * 100, 1),
    }


PSYCH = [50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000]


def strength_label(score, best):
    r = score / best if best else 0
    return "Kuat" if r >= 0.66 else "Sedang" if r >= 0.4 else "Lemah"


def fmt_rp(x):
    return "-" if x is None else f"Rp{x:,.0f}".replace(",", ".")


def fmt_num(x):
    return f"{x:,.0f}".replace(",", ".")


def fmt_pct(p):
    return "nominal Rp1" if p is None else f"{p:.0%}"


# ---------------------------------------------------------------------------
# Analisis utama
# ---------------------------------------------------------------------------

def analyze(rows, lookback, window, board, arb_pct, rule, max_levels, style):
    if len(rows) < window * 2 + 20:
        sys.exit(f"Data terlalu sedikit ({len(rows)} bar). Minimal ~{window * 2 + 20} bar.")
    sessions = group_sessions(rows)
    keys = list(sessions)
    tf = detect_timeframe(rows, sessions)
    intraday = tf == "intraday"

    closes_all = [r["close"] for r in rows]
    data = rows[-lookback:]
    last = data[-1]
    price = last["close"]
    vols = [r["volume"] for r in data]
    avg_vol20 = sum(vols[-20:]) / min(20, len(vols))
    avg_vol = sum(vols) / len(vols)
    a = atr(data)
    t = tick_size(price)
    tol = max(a * 0.5, t * (2 if intraday else 3), price * (0.002 if intraday else 0.01))

    # --- Peringatan data ---------------------------------------------------
    warnings = []
    session_values = [sum(b["close"] * b["volume"] for b in bars) for bars in sessions.values()][-20:]
    avg_value = sum(session_values) / len(session_values)
    avg_value /= {"mingguan": 5, "bulanan": 21}.get(tf, 1)
    if 0 < avg_value < 1e9:
        warnings.append(f"Likuiditas rendah: rata-rata nilai transaksi ~Rp{avg_value / 1e6:,.0f} juta/hari; "
                        "level kurang andal.".replace(",", "."))
    zero_vol = sum(1 for v in vols if v == 0)
    if zero_vol > len(vols) * 0.05:
        warnings.append(f"{zero_vol} bar bervolume nol (kemungkinan suspensi/tidak aktif).")
    if not any(v > 0 for v in vols):
        warnings.append("Tidak ada data volume; skor volume & volume profile diabaikan.")
    if tf in ("harian", "intraday"):
        start = data[0]["date"][:10]
        sess_keys = [k for k in keys if k >= start]
        for prev_k, k in zip(sess_keys, sess_keys[1:]):
            chg = sessions[k][-1]["close"] / sessions[prev_k][-1]["close"] - 1
            if abs(chg) > 0.40:
                warnings.append(f"Perubahan {chg:+.0%} pada {k} melebihi batas ARA/ARB normal — "
                                "cek aksi korporasi / harga belum adjusted.")
    if rule == "lama" and board not in FCA_BOARDS and min(r["low"] for r in data) < 50:
        warnings.append("Ada harga di bawah Rp50: kemungkinan saham di papan full call auction atau aturan "
                        "harga minimum Rp1 sudah berlaku — pertimbangkan --board pemantauan / --price-rule baru.")

    # --- Batas ARA/ARB -----------------------------------------------------
    limits = [dict(auto_rejection(price, board, arb_pct, rule),
                   label="Sesi berikutnya", acuan=f"close {last['date']}")]
    if intraday and len(keys) >= 2:
        prev_close = sessions[keys[-2]][-1]["close"]
        limits.insert(0, dict(auto_rejection(prev_close, board, arb_pct, rule),
                              label=f"Sesi {keys[-1]}", acuan=f"close {keys[-2]}"))
    active = limits[0]

    # --- Level sesi (intraday) --------------------------------------------
    session_levels = {}
    if intraday:
        cur_bars = sessions[keys[-1]]
        cur = session_hlc(cur_bars)
        prev = session_hlc(sessions[keys[-2]]) if len(keys) >= 2 else None
        orb = [b for b in cur_bars if len(b["date"]) >= 16 and b["date"][11:16] < "09:30"]
        vw = vwap(cur_bars)
        session_levels = {
            "sesi_terakhir": cur,
            "sesi_sebelumnya": prev,
            "opening_range_30m": ({"high": max(b["high"] for b in orb), "low": min(b["low"] for b in orb)}
                                  if orb else None),
            "vwap_sesi_terakhir": round_tick(vw) if vw else None,
        }
        pivots = {f"sesi berikutnya (dari {cur['date']})": classic_pivots(cur)}
        if prev:
            pivots[f"sesi {cur['date']} (dari {prev['date']})"] = classic_pivots(prev)
    else:
        pivots = {f"bar berikutnya (dari {last['date']})": classic_pivots(last)}

    # --- Swing levels ------------------------------------------------------
    swings = find_swings(data, window)
    levels = build_zones(cluster_levels(swings, data, tol, avg_vol), t, tol)

    ma = {f"MA{n}": (round_tick(sma(closes_all, n)) if sma(closes_all, n) else None) for n in (20, 50, 200)}
    hvn = volume_profile(data, tol) if any(v > 0 for v in vols) else []

    # --- Indikator pendukung (references/indicators/) ----------------------
    rsi_vals = rsi_series(closes_all)[-len(data):]
    rsi_info = None
    if rsi_vals[-1] is not None:
        now = rsi_vals[-1]
        before = rsi_vals[-6] if len(rsi_vals) >= 6 else None
        zone = ("overbought (>70)" if now > 70 else "oversold (<30)" if now < 30
                else "momentum positif (50–70)" if now >= 50 else "momentum negatif (30–50)")
        rsi_info = {"period": 14, "value": round(now, 1), "zone": zone,
                    "value_5_bars_ago": round(before, 1) if before is not None else None,
                    "divergences": momentum_divergence(data, rsi_vals, swings)}
    ma_info = ma_analysis(rows, len(data))
    macd_info = macd_analysis(rows, data, swings)
    volume_info = volume_analysis(data)
    fib = fibonacci(data, price)

    refs = [(f"angka bulat {fmt_rp(p)}", p) for p in PSYCH]
    if fib:
        refs += [(f"Fib {k}", v) for k, v in fib["retracement"].items()]
    refs += [(k, v) for k, v in ma.items() if v is not None]
    if intraday:
        if session_levels["sesi_sebelumnya"]:
            refs += [("high sesi sebelumnya", session_levels["sesi_sebelumnya"]["high"]),
                     ("low sesi sebelumnya", session_levels["sesi_sebelumnya"]["low"])]
        if session_levels["vwap_sesi_terakhir"]:
            refs.append(("VWAP", session_levels["vwap_sesi_terakhir"]))

    def classify(cands):
        sup, res = [], []
        for lv in cands:
            zl, zh = lv["zone_lo"], lv["zone_hi"]
            lv.update(mid=round_tick(lv["level"]), dist_pct=round((lv["level"] / price - 1) * 100, 2))
            lv["confluence"] = [name for name, v in refs if zl - tol * 0.5 <= v <= zh + tol * 0.5]
            if any(zl <= h["hi"] and h["lo"] <= zh for h in hvn):
                lv["confluence"].append("HVN")
            if zh < price:
                sup.append(lv)
            elif zl > price:
                res.append(lv)
            else:
                (sup if lv["level"] <= price else res).append(lv)
                lv["note"] = "harga sedang berada di dalam zona"
        return sup, res

    supports, resistances = classify(levels)
    # Fractal butuh `window` bar di kedua sisi, jadi saat harga di ujung rentang lookback satu sisi
    # bisa kosong. Cari sisi yang kosong itu di data yang lebih panjang.
    ext = rows[-max(lookback * 4, 250):]
    if (not supports or not resistances) and len(ext) > len(data):
        ext_sup, ext_res = classify(build_zones(cluster_levels(find_swings(ext, window), ext, tol, avg_vol), t, tol))
        for lv in ext_sup + ext_res:
            lv["note"] = "; ".join(filter(None, [lv.get("note"), f"dari data lebih panjang ({len(ext)} bar)"]))
        supports = supports or ext_sup
        resistances = resistances or ext_res

    for lv in resistances:
        if lv["zone_lo"] > active["ara"]:
            lv["confluence"].append(f"di atas ARA {active['label'].lower()} (tak tercapai dalam sesi itu)")
    for lv in supports:
        if lv["zone_hi"] < active["arb"]:
            lv["confluence"].append(f"di bawah ARB {active['label'].lower()} (tak tercapai dalam sesi itu)")

    supports.sort(key=lambda x: -x["level"])
    resistances.sort(key=lambda x: x["level"])
    candidates = supports + resistances
    best = max([l["score"] for l in candidates] or [1])
    for lv in candidates:
        lv["strength"] = strength_label(lv["score"], best)
    candles = candle_patterns(data, candidates, tol, tf, board, arb_pct, rule)

    return {
        "style": style,
        "timeframe": tf,
        "as_of": last["date"],
        "bars_used": len(data),
        "period": f"{data[0]['date']} s/d {last['date']}",
        "board": board,
        "price_rule": rule,
        "last_close": int(price) if price == int(price) else round(price, 2),
        "tick_size": t,
        "atr14": round(a, 1),
        "zone_tolerance": round(tol, 1),
        "auto_rejection": limits,
        "auto_rejection_note": "ARB papan reguler memakai --arb-pct (default 15%, SK Kep-00003/BEI/04-2025); "
                               "verifikasi aturan BEI terkini.",
        "moving_averages": ma,
        "last_volume_vs_avg20": round(last["volume"] / avg_vol20, 2) if avg_vol20 else None,
        "session_levels": session_levels,
        "supports": supports[:max_levels],
        "resistances": resistances[:max_levels],
        "volume_profile_hvn": hvn,
        "candlestick": candles,
        "moving_average_analysis": ma_info,
        "macd": macd_info,
        "rsi": rsi_info,
        "volume": volume_info,
        "fibonacci": fib,
        "classic_pivots": pivots,
        "warnings": warnings,
    }


def to_markdown(res):
    L = []
    style = f" — gaya {res['style']}" if res["style"] else ""
    L.append(f"# Hasil S/R{style} (data {res['timeframe']} {res['period']}, {res['bars_used']} bar)")
    L.append(f"Harga terakhir: {fmt_rp(res['last_close'])} | Fraksi: {fmt_rp(res['tick_size'])} | "
             f"ATR14: {res['atr14']} | Toleransi zona: {res['zone_tolerance']}")
    for lim in res["auto_rejection"]:
        L.append(f"Batas {lim['label']} (acuan {lim['acuan']}): ARA {fmt_rp(lim['ara'])} (+{fmt_pct(lim['ara_pct'])}) | "
                 f"ARB {fmt_rp(lim['arb'])} (-{fmt_pct(lim['arb_pct'])})")
    L.append(f"_{res['auto_rejection_note']}_")
    ma_note = " (dihitung per bar intraday)" if res["timeframe"] == "intraday" else ""
    L.append("MA" + ma_note + ": " + " | ".join(f"{k} {fmt_rp(v)}" for k, v in res["moving_averages"].items()))
    L.append(f"Volume bar terakhir vs rata-rata 20 bar: {res['last_volume_vs_avg20']}x")

    sl = res["session_levels"]
    if sl:
        L.append("\n## Level sesi (intraday)")
        cur, prev = sl["sesi_terakhir"], sl["sesi_sebelumnya"]
        L.append(f"- Sesi {cur['date']}: open {fmt_rp(cur['open'])}, high {fmt_rp(cur['high'])}, "
                 f"low {fmt_rp(cur['low'])}, last {fmt_rp(cur['close'])}")
        if prev:
            L.append(f"- Sesi sebelumnya {prev['date']}: high {fmt_rp(prev['high'])}, low {fmt_rp(prev['low'])}, "
                     f"close {fmt_rp(prev['close'])}")
        if sl["opening_range_30m"]:
            o = sl["opening_range_30m"]
            L.append(f"- Opening range 09.00–09.30: {fmt_rp(o['low'])} – {fmt_rp(o['high'])}")
        L.append(f"- VWAP sesi terakhir: {fmt_rp(sl['vwap_sesi_terakhir'])}")

    def table(title, items):
        L.append(f"\n## {title}")
        if not items:
            L.append("(tidak ada swing level terdeteksi di sisi ini — gunakan ARA/ARB, pivot, angka bulat)")
            return
        L.append("| Zona | Mid | Jarak | Touches | Terakhir | Vol ratio | Skor | Kekuatan | Konfluensi |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for lv in items:
            conf = ", ".join(lv["confluence"] + (["role reversal"] if lv["role_reversal"] else [])
                             + ([lv["note"]] if lv.get("note") else [])) or "-"
            L.append(f"| {fmt_rp(lv['zone_lo'])}–{fmt_rp(lv['zone_hi'])} | {fmt_rp(lv['mid'])} | "
                     f"{lv['dist_pct']:+.2f}% | {lv['touches']} | {lv['last_touch']} | {lv['vol_ratio']} | "
                     f"{lv['score']} | {lv['strength']} | {conf} |")

    table("Resistance (terdekat dulu)", res["resistances"])
    table("Support (terdekat dulu)", res["supports"])

    L.append("\n## Candlestick (3 bar terakhir)")
    for x in res["candlestick"]:
        names = ", ".join(f"{p['name']} ({p['bias']})" for p in x["patterns"])
        vol = f"volume {x['volume_vs_avg20']}x rata-rata 20" if x["volume_vs_avg20"] is not None else "volume -"
        L.append(f"- {x['date']}: {names} | tren 5 bar sebelumnya {x['prior_trend_5']} | "
                 f"{'; '.join(x['location'])} | {vol}")
    if not res["candlestick"]:
        L.append("- Tidak ada pola candlestick yang terdeteksi.")

    mi = res["moving_average_analysis"]
    if mi and mi["levels"]:
        L.append("\n## Moving average (nilai | harga vs MA | slope 5 bar)")
        L.append(f"Susunan: {mi['alignment']}")
        L.append(" | ".join(f"{k} {fmt_rp(v['value'])} ({v['dist_pct']:+.2f}%, {v['slope_5'] or '-'})"
                            for k, v in mi["levels"].items()))
        for k, c in mi["crosses"].items():
            L.append(f"- {k}: " + (f"{c['type']} pada {c['date']} ({c['bars_ago']} bar lalu)" if c
                                   else f"tidak ada persilangan dalam {res['bars_used']} bar terakhir"))

    mc = res["macd"]
    if mc:
        L.append(f"\n## MACD ({mc['setting']})")
        L.append(f"MACD {mc['macd']} | signal {mc['signal']} | histogram {mc['histogram']} ({mc['histogram_trend']}) | "
                 f"MACD = {mc['macd_pct_of_price']}% dari harga")
        L.append(f"Posisi: MACD {'di atas' if mc['above_signal'] else 'di bawah'} signal, "
                 f"{'di atas' if mc['above_zero'] else 'di bawah'} garis nol")
        for label, key in (("crossover signal", "last_signal_cross"), ("crossover garis nol", "last_zero_cross")):
            c = mc[key]
            L.append(f"- Terakhir {label}: " + (
                f"ke {'atas' if c['type'] == 'naik' else 'bawah'} pada {c['date']} ({c['bars_ago']} bar lalu)"
                if c else "tidak ada dalam rentang lookback"))
        for d in mc["divergences"]:
            L.append(f"- {d['type']}: {d['from']} → {d['to']} ({d['bars_ago']} bar lalu)")
        if not mc["divergences"]:
            L.append("- Tidak ada divergence MACD pada dua swing low/high terakhir.")

    ri = res["rsi"]
    if ri:
        L.append(f"\n## Momentum — RSI({ri['period']})")
        L.append(f"RSI terakhir: {ri['value']} — {ri['zone']}; 5 bar lalu: {ri['value_5_bars_ago']}")
        for d in ri["divergences"]:
            L.append(f"- {d['type']}: {d['from']} → {d['to']} (harga {fmt_rp(d['price'][0])} → "
                     f"{fmt_rp(d['price'][1])}, RSI {d['rsi'][0]} → {d['rsi'][1]}, {d['bars_ago']} bar lalu)")
        if not ri["divergences"]:
            L.append("- Tidak ada divergence pada dua swing low/high terakhir.")

    vo = res["volume"]
    if vo:
        L.append("\n## Volume (satuan mengikuti sumber data; yfinance = lembar, 1 lot = 100 lembar)")
        L.append(f"Rata-rata 20 bar: {fmt_num(vo['avg_volume_20'])} | 50 bar: {fmt_num(vo['avg_volume_50'])} | "
                 f"rasio 20/50: {vo['ratio_20_vs_50']}x | bar terakhir vs rata-rata 20: {vo['last_vs_avg20']}x")
        L.append(f"Rasio volume naik/turun (20 bar): {vo['up_down_volume_ratio_20']} | "
                 f"OBV 20 bar {vo['obv_20']}, harga {vo['price_20']} → "
                 + ("divergence OBV (volume tidak mengonfirmasi harga)" if vo["obv_divergence"] else "searah"))
        for s in vo["spikes_20"]:
            L.append(f"- Volume spike {s['date']}: {s['ratio']}x rata-rata, harga {s['change_pct']:+.2f}%")
        if not vo["spikes_20"]:
            L.append("- Tidak ada volume spike (≥2× rata-rata) dalam 20 bar terakhir.")

    fb = res["fibonacci"]
    if fb:
        L.append(f"\n## Fibonacci (kaki {fb['direction']}: low {fmt_rp(fb['anchor_low']['price'])} "
                 f"@ {fb['anchor_low']['date']}, high {fmt_rp(fb['anchor_high']['price'])} @ {fb['anchor_high']['date']})")
        L.append("Retracement: " + " | ".join(f"{k} {fmt_rp(v)}" for k, v in fb["retracement"].items()))
        L.append("Extension: " + " | ".join(f"{k} {fmt_rp(v)}" for k, v in fb["extension"].items()))
        L.append(f"Harga saat ini di retracement {fb['retracement_now_pct']}% dari kaki tersebut.")

    if res["volume_profile_hvn"]:
        L.append("\n## Volume profile — High Volume Nodes")
        for h in res["volume_profile_hvn"]:
            L.append(f"- {fmt_rp(h['lo'])}–{fmt_rp(h['hi'])}: {h['pct_volume']}% volume")
    L.append("\n## Pivot klasik")
    for label, pv in res["classic_pivots"].items():
        L.append(f"- Untuk {label}: " + " | ".join(f"{k} {fmt_rp(v)}" for k, v in pv.items()))
    if res["warnings"]:
        L.append("\n## Peringatan")
        L.extend(f"- {w}" for w in res["warnings"])
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Deteksi support & resistance saham IDX")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--csv", help="File CSV OHLCV (Date/Datetime,Open,High,Low,Close,Volume)")
    src.add_argument("--ticker", help="Kode saham, contoh BBCA (butuh yfinance)")
    ap.add_argument("--style", choices=sorted(STYLE_PRESETS),
                    help="Preset gaya trading: atur interval, periode, lookback, dan window")
    ap.add_argument("--interval", help="Interval yfinance, contoh 1m, 5m, 1d, 1wk")
    ap.add_argument("--period", help="Periode yfinance, contoh 5d, 1mo, 2y, 10y")
    ap.add_argument("--lookback", type=int, help="Jumlah bar yang dianalisis")
    ap.add_argument("--window", type=int, help="Lebar fractal swing kiri/kanan")
    ap.add_argument("--board", default="utama",
                    choices=["utama", "pengembangan", "ekonomi-baru", "akselerasi", "pemantauan"])
    ap.add_argument("--arb-pct", type=float, default=0.15,
                    help="Batas ARB papan reguler (default 0.15, SK Kep-00003/BEI/04-2025)")
    ap.add_argument("--price-rule", choices=["lama", "baru"], default="lama",
                    help="lama: harga minimum Rp50; baru: minimum Rp1, ARA/ARB nominal Rp1 untuk harga Rp1-10")
    ap.add_argument("--max-levels", type=int, default=3)
    ap.add_argument("--json", action="store_true", help="Output JSON")
    args = ap.parse_args()

    preset = STYLE_PRESETS.get(args.style, {})
    cfg = {k: getattr(args, k) if getattr(args, k) is not None else preset.get(k, v) for k, v in DEFAULTS.items()}
    rows = load_csv(args.csv) if args.csv else load_yfinance(args.ticker, cfg["interval"], cfg["period"])
    board = args.board if args.board in FCA_BOARDS else "utama"
    res = analyze(rows, cfg["lookback"], cfg["window"], board, args.arb_pct, args.price_rule,
                  args.max_levels, args.style)
    print(json.dumps(res, indent=2, ensure_ascii=False) if args.json else to_markdown(res))


if __name__ == "__main__":
    main()
