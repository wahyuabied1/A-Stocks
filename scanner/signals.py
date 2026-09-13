"""Aturan sinyal per gaya trading (scalper, BPJS, BSJP, swing).

Setiap aturan membaca hasil `sr_levels.analyze` (zona support/resistance, candlestick, RSI, MACD,
moving average, volume) lalu mengembalikan sinyal berisi alasan, peringatan, dan rencana skenario
(entry/stop/target). Ambang di sini adalah heuristik dari references/ skill idx-support-resistance,
bukan rekomendasi investasi.
"""
import math
from datetime import date

from .skill import sr

STATUS_ORDER = {"SETUP": 0, "WASPADA": 1, "PANTAU": 2}

BULLISH_CANDLES = ("hammer", "inverted hammer", "bullish engulfing", "morning star", "piercing line",
                   "bullish harami", "three white soldiers", "marubozu bullish", "sempat ARB lalu pulih")
BEARISH_CANDLES = ("shooting star", "hanging man", "bearish engulfing", "evening star", "dark cloud cover",
                   "bearish harami", "three black crows", "marubozu bearish", "sempat ARA lalu turun")

fmt = sr.fmt_rp


# ---------------------------------------------------------------------------
# Utilitas
# ---------------------------------------------------------------------------

def _zone(z):
    return f"{fmt(z['zone_lo'])}–{fmt(z['zone_hi'])}"


def _candles(res, max_bars_ago):
    return [p["name"] for c in res["candlestick"] if c["bars_ago"] <= max_bars_ago for p in c["patterns"]]


def _matching(names, prefixes):
    return [n for n in names if n.startswith(prefixes)]


def _illiquid(res):
    return any(w.startswith("Likuiditas rendah") for w in res["warnings"])


def _recent_divergence(res, word, max_bars_ago=10):
    divs = (res["rsi"] or {}).get("divergences", []) + (res["macd"] or {}).get("divergences", [])
    return any(word in d["type"] and d["bars_ago"] <= max_bars_ago for d in divs)


def _add_ticks(price, n):
    for _ in range(n):
        price += sr.tick_size(price)
    return price


def _fib_targets(res):
    fib = res["fibonacci"]
    return list(fib["extension"].values()) if fib and fib["direction"] == "naik" else []


def _intraday_live(res, market, cfg):
    return cfg.get("ignore_market_hours") or (market["trading"] and res["as_of"][:10] == market["date"])


def _plan(entry_lo, entry_hi, stop, targets, cfg, notes=()):
    buy, sell = cfg["fees"]["buy_pct"] / 100, cfg["fees"]["sell_pct"] / 100
    entry_lo, entry_hi = min(entry_lo, entry_hi), max(entry_lo, entry_hi)
    cost = entry_hi * (1 + buy)  # asumsi terburuk: terisi di batas atas zona entry
    risk = cost - stop * (1 - sell)
    targets = sorted({int(x) for x in targets if x and x > entry_hi})[:2]
    reward = targets[0] * (1 - sell) - cost if targets else None
    budget = cfg["risk"].get("risk_per_trade_rp")
    lots = int(budget // (risk * 100)) if budget and risk > 0 else None
    return {
        "entry": [int(entry_lo), int(entry_hi)],
        "stop": int(stop),
        "targets": targets,
        "rr": round(reward / risk, 2) if reward is not None and risk > 0 else None,
        "risk_pct": round(risk / cost * 100, 2),
        "reward_pct": round(reward / cost * 100, 2) if reward is not None else None,
        "lots": lots,
        "risk_rp": round(lots * risk * 100) if lots else None,
        "notes": list(notes),
    }


def _status(score, plan, cfg, warnings, style):
    min_rr = cfg["risk"]["min_reward_risk"]
    if isinstance(min_rr, dict):
        min_rr = min_rr.get(style, 1.5)
    if plan and not plan["targets"]:
        warnings.append("Tidak ada target di atas harga entry — tentukan target sendiri")
        return "PANTAU"
    if plan and plan["rr"] is not None and plan["rr"] < min_rr:
        warnings.append(f"R:R setelah biaya hanya {plan['rr']} (< {min_rr}) — setup kurang layak")
        return "PANTAU"
    return "SETUP" if score >= 60 else "PANTAU"


def _signal(ticker, style, kind, title, status, score, res, reasons, warnings, plan=None):
    return {
        "id": f"{ticker}|{style}|{kind}|{res['as_of'][:10]}",
        "ticker": ticker,
        "style": style,
        "kind": kind,
        "title": title,
        "status": status,
        "score": max(0, min(100, round(score))),
        "price": res["last_close"],
        "as_of": res["as_of"],
        "timeframe": res["timeframe"],
        "reasons": reasons,
        "warnings": list(dict.fromkeys(warnings)),
        "plan": plan,
    }


def sort_signals(signals):
    return sorted(signals, key=lambda s: (STATUS_ORDER[s["status"]], -s["score"], s["ticker"]))


# ---------------------------------------------------------------------------
# Swing (data harian)
# ---------------------------------------------------------------------------

def swing_signals(ticker, rows, res, cfg, market):
    out = []
    price, t = res["last_close"], res["tick_size"]
    atr = res["atr14"] or t
    prev_close = rows[-2]["close"]
    low2 = min(rows[-1]["low"], rows[-2]["low"])
    sups, ress = res["supports"], res["resistances"]
    rsi, macd = res["rsi"] or {}, res["macd"] or {}
    alignment = (res["moving_average_analysis"] or {}).get("alignment", "")
    vr = (res["volume"] or {}).get("last_vs_avg20") or 0
    candles = _candles(res, 1)
    bull, bear = _matching(candles, BULLISH_CANDLES), _matching(candles, BEARISH_CANDLES)
    penalty = 15 if _illiquid(res) else 0

    # 1. Breakout resistance: close menembus zona yang kemarin masih di atas/di dalam.
    broken = next((z for z in sups if prev_close <= z["zone_hi"] < price), None)
    if broken:
        reasons = [f"Close {fmt(price)} menembus zona {_zone(broken)} ({broken['strength']}, "
                   f"{broken['touches']} sentuhan)"]
        warnings = list(res["warnings"])
        score = 40 - penalty
        if vr >= 1.5:
            score += 20
            reasons.append(f"Volume {vr}x rata-rata 20 hari mengonfirmasi breakout")
        else:
            warnings.append(f"Volume hanya {vr}x rata-rata 20 hari — breakout belum terkonfirmasi volume")
        if macd.get("above_zero"):
            score += 10
            reasons.append("MACD di atas garis nol")
        rv = rsi.get("value")
        if rv is not None and 50 <= rv <= 75:
            score += 10
            reasons.append(f"RSI {rv} (momentum positif, belum jenuh)")
        elif rv is not None and rv > 75:
            warnings.append(f"RSI {rv} sudah tinggi — rawan pullback; skenario retest lebih aman")
        if bull:
            score += 10
            reasons.append("Candle: " + ", ".join(bull))
        if bear:
            score -= 10
            warnings.append("Candle pelemahan: " + ", ".join(bear))
        if alignment.startswith("bullish"):
            score += 10
            reasons.append("Susunan MA bullish (MA20 > MA50 > MA200)")
        entry_lo = broken["zone_hi"]
        entry_hi = max(entry_lo, sr.round_tick(min(price, broken["zone_hi"] + 0.5 * atr), "down"))
        stop = sr.round_tick(broken["zone_lo"] - t, "down")
        targets = ([z["zone_lo"] for z in ress] or _fib_targets(res)
                   or [sr.round_tick(entry_hi + 2 * (entry_hi - stop), "up")])
        notes = ["Skenario retest: tunggu harga kembali ke zona breakout dan bertahan di atasnya."]
        if price - broken["zone_hi"] > atr:
            notes.append("Harga sudah >1 ATR di atas zona breakout — hindari mengejar harga.")
        plan = _plan(entry_lo, entry_hi, stop, targets, cfg, notes)
        out.append(_signal(ticker, "swing", "breakout", "Breakout resistance",
                           _status(score, plan, cfg, warnings, "swing"), score, res, reasons, warnings, plan))

    # 2. Buy on Weakness: harga menguji support terdekat dan close tidak jebol
    #    (dilewati jika bar yang sama baru saja menembus support di atasnya).
    lost = next((z for z in ress if prev_close >= z["zone_lo"] > price), None)
    s1 = sups[0] if sups else None
    if s1 and not broken and not lost and s1["zone_lo"] - atr <= low2 <= s1["zone_hi"] + 0.5 * atr \
            and price >= s1["zone_lo"]:
        reasons = [f"Harga menguji support {_zone(s1)} ({s1['strength']}, {s1['touches']} sentuhan)"]
        if low2 < s1["zone_lo"]:
            reasons.append(f"Sempat menembus bawah zona ({fmt(low2)}) lalu close kembali di atasnya (false break)")
        warnings = list(res["warnings"])
        score = 35 - penalty
        if s1["strength"] == "Kuat":
            score += 10
        if s1["confluence"]:
            score += 5
            reasons.append("Konfluensi: " + ", ".join(s1["confluence"][:4]))
        if bull:
            score += 20
            reasons.append("Candle pembalikan: " + ", ".join(bull))
        else:
            warnings.append("Belum ada candle pembalikan — tunggu konfirmasi")
        if bear:
            score -= 10
            warnings.append("Candle pelemahan: " + ", ".join(bear))
        if rsi.get("value") is not None and rsi["value"] < 45:
            score += 5
            reasons.append(f"RSI {rsi['value']} (sudah terkoreksi)")
        if _recent_divergence(res, "bullish"):
            score += 10
            reasons.append("Bullish divergence RSI/MACD dalam 10 bar terakhir")
        if macd.get("histogram_trend") == "negatif dan mengecil":
            score += 5
            reasons.append("Histogram MACD negatif tapi mengecil (tekanan jual melemah)")
        cross = macd.get("last_signal_cross")
        if cross and cross["type"] == "naik" and cross["bars_ago"] <= 3:
            score += 10
            reasons.append(f"MACD baru memotong signal ke atas ({cross['bars_ago']} bar lalu)")
        if alignment.startswith("bearish"):
            score -= 10
            warnings.append("Tren besar masih turun (MA20 < MA50 < MA200) — pantulan melawan tren")
        if vr >= 1.2 and price > prev_close:
            score += 5
            reasons.append(f"Pantulan dengan volume {vr}x rata-rata")
        stop = sr.round_tick(min(s1["zone_lo"], low2) - max(t, 0.25 * atr), "down")
        targets = [z["zone_lo"] for z in ress] or _fib_targets(res)
        plan = _plan(s1["zone_lo"], s1["zone_hi"], stop, targets, cfg,
                     ["Antre di dalam zona support; batal jika close harian di bawah stop."])
        out.append(_signal(ticker, "swing", "bow", "Buy on Weakness di support",
                           _status(score, plan, cfg, warnings, "swing"), score, res, reasons, warnings, plan))

    # 3. Waspada: close jatuh di bawah support yang kemarin masih bertahan.
    if lost:
        reasons = [f"Close {fmt(price)} jatuh di bawah support {_zone(lost)} ({lost['strength']})"]
        score = 50
        if vr >= 1.5:
            score += 20
            reasons.append(f"Breakdown dengan volume {vr}x rata-rata")
        if macd and not macd.get("above_zero"):
            reasons.append("MACD di bawah garis nol")
        warnings = list(res["warnings"]) + [
            "Support yang tembus berpotensi menjadi resistance. Jika memegang posisi, tinjau kembali "
            "stop loss yang sudah kamu tetapkan."]
        out.append(_signal(ticker, "swing", "breakdown", "Breakdown support", "WASPADA",
                           score, res, reasons, warnings))

    # 4. Waspada: mendekati resistance dengan tanda pelemahan.
    r1 = ress[0] if ress else None
    if r1 and not lost and r1["zone_lo"] - price <= 0.5 * atr:
        signs = []
        if bear:
            signs.append("candle " + ", ".join(bear))
        if rsi.get("value") is not None and rsi["value"] > 70:
            signs.append(f"RSI {rsi['value']} (overbought)")
        if _recent_divergence(res, "bearish"):
            signs.append("bearish divergence RSI/MACD")
        if signs:
            reasons = [f"Harga {fmt(price)} dekat resistance {_zone(r1)} ({r1['strength']})",
                       "Tanda pelemahan: " + "; ".join(signs)]
            out.append(_signal(ticker, "swing", "near_resistance", "Mendekati resistance, momentum melemah",
                               "WASPADA", 45 + 10 * len(signs), res, reasons,
                               list(res["warnings"]) + ["Ruang naik terbatas sebelum resistance tertembus."]))
    return out


# ---------------------------------------------------------------------------
# BSJP (data harian, dievaluasi menjelang penutupan)
# ---------------------------------------------------------------------------

def bsjp_signals(ticker, rows, res, cfg, market):
    bar, prev = rows[-1], rows[-2]
    h, l, c = bar["high"], bar["low"], bar["close"]
    t = res["tick_size"]
    chg = c / prev["close"] - 1
    pos = (c - l) / (h - l) if h > l else 1.0
    if chg <= 0 or pos < 0.6:
        return []

    ignore_hours = cfg.get("ignore_market_hours")
    is_today = ignore_hours or bar["date"][:10] == market["date"]
    in_session = market["phase"] in ("sesi1", "istirahat", "sesi2")
    vr = (res["volume"] or {}).get("last_vs_avg20") or 0
    vr_need = 1.2 if is_today and in_session else 1.5

    reasons = [f"Naik {chg * 100:+.2f}% dan close di {pos * 100:.0f}% rentang harian (dekat high)"]
    warnings = list(res["warnings"])
    score = 30 - (15 if _illiquid(res) else 0)
    if pos >= 0.8:
        score += 10
    if vr >= vr_need:
        score += 20
        reasons.append(f"Volume {vr}x rata-rata 20 hari" + (" (volume hari berjalan)" if in_session else ""))
    else:
        warnings.append(f"Volume {vr}x rata-rata — belum menunjukkan minat beli besar")
    ma20 = ((res["moving_average_analysis"] or {}).get("levels") or {}).get("MA20")
    if ma20 and ma20["dist_pct"] > 0:
        score += 10
        reasons.append(f"Di atas MA20 ({fmt(ma20['value'])})")
    else:
        score -= 5
        warnings.append("Di bawah MA20 — melawan tren pendek")
    rv = (res["rsi"] or {}).get("value")
    if rv is not None and rv >= 80:
        score -= 15
        warnings.append(f"RSI {rv} sangat tinggi — rawan profit taking pagi hari")
    today = _candles(res, 0)
    bull, bear = _matching(today, BULLISH_CANDLES), _matching(today, BEARISH_CANDLES)
    if bear:
        score -= 20
        warnings.append("Candle hari ini menunjukkan penolakan: " + ", ".join(bear))
    if bull:
        score += 5
        reasons.append("Candle: " + ", ".join(bull))
    if any(n.startswith("candle ARA") for n in today):
        score -= 10
        warnings.append("Sudah ARA hari ini — risiko tidak kebagian antrean dan berbalik besok (lihat ara-hunter.md)")

    ara_next = res["auto_rejection"][-1]["ara"]
    ress, sups = res["resistances"], res["supports"]
    r1 = ress[0] if ress else None
    if r1:
        room = (r1["zone_lo"] / c - 1) * 100
        if room < 1.5:
            score -= 15
            warnings.append(f"Resistance terdekat {_zone(r1)} hanya {room:.1f}% di atas — ruang gap up sempit")
        else:
            score += 10
            reasons.append(f"Ruang ke resistance terdekat {room:.1f}% ({_zone(r1)})")

    entry_lo, entry_hi = sr.round_tick(c - 2 * t, "down"), sr.round_tick(c)
    # Invalidasi BSJP: kembali ke bawah tengah rentang hari ini atau turun ±3% dari close, mana yang
    # lebih dekat. Low harian sering terlalu jauh untuk posisi yang hanya menginap satu malam.
    stops = [sr.round_tick(l - t, "down"), sr.round_tick((h + l) / 2, "down"), sr.round_tick(c * 0.97, "down")]
    if sups and sups[0]["zone_lo"] < entry_lo:
        stops.append(sr.round_tick(sups[0]["zone_lo"] - t, "down"))
    stop = max((s for s in stops if s < entry_lo), default=sr.round_tick(entry_lo - t, "down"))
    t1 = min(x for x in (sr.round_tick(c * 1.03, "down"), r1["zone_lo"] if r1 else None, ara_next) if x)
    t2 = min(r1["mid"] if r1 and r1["mid"] > t1 else sr.round_tick(c * 1.05, "down"), ara_next)
    notes = ["Rencana keluar: pre-opening 08.45–09.00 atau 09.00–10.00 besok.",
             "Stop: di bawah tengah rentang hari ini atau −3% dari close (mana yang lebih dekat).",
             f"Batas ARA besok {fmt(ara_next)}.",
             "Cek kalender ex-date dividen sebelum menginapkan posisi."]
    if date.fromisoformat(bar["date"][:10]).weekday() == 4:
        notes.append("Hari Jumat: posisi menginap 2 malam + akhir pekan (risiko berita lebih besar).")
    plan = _plan(entry_lo, entry_hi, stop, [t1, t2], cfg, notes)

    status = _status(score, plan, cfg, warnings, "bsjp")
    if not is_today:
        warnings.append(f"Bar terakhir {bar['date']} bukan data hari ini — pratinjau saja.")
        status = "PANTAU" if status == "SETUP" else status
    elif status == "SETUP" and not (market["bsjp_window"] or ignore_hours):
        warnings.append("Di luar jendela BSJP (14.30–16.00 WIB) — cek ulang menjelang penutupan.")
        status = "PANTAU"
    return [_signal(ticker, "bsjp", "bsjp", "Kandidat BSJP", status, score, res, reasons, warnings, plan)]


# ---------------------------------------------------------------------------
# BPJS / intraday (data 5 menit)
# ---------------------------------------------------------------------------

def bpjs_signals(ticker, rows, res, cfg, market):
    if not _intraday_live(res, market, cfg):
        return []
    out = []
    sl = res["session_levels"]
    vw, orb, prev_s = sl.get("vwap_sesi_terakhir"), sl.get("opening_range_30m"), sl.get("sesi_sebelumnya")
    bar, pbar = rows[-1], rows[-2]
    c, t = bar["close"], res["tick_size"]
    atr = res["atr14"] or t
    rsi, macd = res["rsi"] or {}, res["macd"] or {}
    alignment = (res["moving_average_analysis"] or {}).get("alignment", "")
    vr = (res["volume"] or {}).get("last_vs_avg20") or 0
    bull = _matching(_candles(res, 0), BULLISH_CANDLES)
    penalty = 15 if _illiquid(res) else 0
    ress = res["resistances"]
    closing_note = "Tutup posisi sebelum 15.49 WIB — BPJS tidak menginap."

    # 1. Pullback ke VWAP yang bertahan.
    if vw and bar["low"] <= vw + max(t, 0.1 * atr) and c > vw:
        above = sum(1 for r in rows[-7:-1] if r["close"] > vw)
        if above >= 4:
            reasons = [f"Pullback ke VWAP {fmt(vw)} lalu close di atasnya",
                       f"{above} dari 6 bar sebelumnya di atas VWAP"]
            warnings = list(res["warnings"])
            score = 40 - penalty
            if macd.get("above_zero"):
                score += 10
                reasons.append("MACD 5 menit di atas garis nol")
            if rsi.get("value") is not None and 40 <= rsi["value"] <= 70:
                score += 10
                reasons.append(f"RSI {rsi['value']}")
            if bull:
                score += 15
                reasons.append("Candle: " + ", ".join(bull))
            if alignment.startswith("bullish"):
                score += 10
                reasons.append("Susunan MA 5 menit bullish")
            stop = sr.round_tick(min(bar["low"], vw) - max(2 * t, 0.3 * atr), "down")
            targets = [z["zone_lo"] for z in ress]
            if prev_s:
                targets.append(sr.round_tick(prev_s["high"], "down"))
            plan = _plan(sr.round_tick(vw), sr.round_tick(c), stop, targets, cfg, [closing_note])
            out.append(_signal(ticker, "bpjs", "vwap_pullback", "Pullback VWAP bertahan",
                               _status(score, plan, cfg, warnings, "bpjs"), score, res, reasons, warnings, plan))

    # 2. Breakout opening range (setelah 09.30).
    if orb and bar["date"][11:16] >= "09:30" and pbar["close"] <= orb["high"] < c:
        reasons = [f"Menembus high opening range {fmt(orb['high'])}"]
        warnings = list(res["warnings"])
        score = 40 - penalty
        if vr >= 1.5:
            score += 20
            reasons.append(f"Volume {vr}x rata-rata 20 bar")
        else:
            warnings.append(f"Volume hanya {vr}x — breakout rawan gagal")
        if macd.get("above_zero"):
            score += 10
            reasons.append("MACD 5 menit di atas garis nol")
        if rsi.get("value") is not None and rsi["value"] > 75:
            warnings.append(f"RSI {rsi['value']} sudah tinggi")
        else:
            score += 5
        stop = sr.round_tick((orb["high"] + orb["low"]) / 2, "down")
        entry_lo, entry_hi = sr.round_tick(orb["high"], "up"), sr.round_tick(c)
        targets = [z["zone_lo"] for z in ress] + [sr.round_tick(entry_hi + 1.5 * (entry_hi - stop), "up")]
        plan = _plan(entry_lo, entry_hi, stop, targets, cfg,
                     ["Stop di tengah opening range.", closing_note])
        out.append(_signal(ticker, "bpjs", "orb_breakout", "Breakout opening range",
                           _status(score, plan, cfg, warnings, "bpjs"), score, res, reasons, warnings, plan))

    # 3. Waspada: jatuh ke bawah VWAP dengan volume.
    if vw and c < vw <= pbar["close"] and vr >= 1.5:
        out.append(_signal(ticker, "bpjs", "lose_vwap", "Jatuh ke bawah VWAP dengan volume", "WASPADA", 55, res,
                           [f"Close {fmt(c)} di bawah VWAP {fmt(vw)} dengan volume {vr}x rata-rata"],
                           list(res["warnings"]) + ["Penjual mengambil alih sesi — hati-hati dengan posisi intraday."]))
    return out


# ---------------------------------------------------------------------------
# Scalper (data 1 menit) — selalu PANTAU karena data tertunda
# ---------------------------------------------------------------------------

def scalper_signals(ticker, rows, res, cfg, market):
    if not _intraday_live(res, market, cfg):
        return []
    out = []
    bar, pbar = rows[-1], rows[-2]
    c, t = bar["close"], res["tick_size"]
    fee_rt = cfg["fees"]["buy_pct"] + cfg["fees"]["sell_pct"]
    tick_pct = t / c * 100
    be_ticks = math.ceil(fee_rt / tick_pct)
    warnings = ["Data tertunda ±10–15 menit: sinyal scalper hanya untuk observasi/latihan, bukan untuk eksekusi."]
    warnings += res["warnings"]
    if be_ticks >= 2:
        warnings.append(f"1 tick = {tick_pct:.2f}% — butuh ≥{be_ticks} tick hanya untuk menutup biaya ±{fee_rt}%")
    vr = (res["volume"] or {}).get("last_vs_avg20") or 0
    bull = _matching(_candles(res, 0), BULLISH_CANDLES)
    penalty = 15 if _illiquid(res) else 0
    target = _add_ticks(c, be_ticks + 2)

    s1 = res["supports"][0] if res["supports"] else None
    if s1 and s1["zone_lo"] - t <= bar["low"] <= s1["zone_hi"] + t and c >= s1["zone_lo"] and (bull or vr >= 2):
        reasons = [f"Memantul di support intraday {_zone(s1)}"]
        score = 35 - penalty - (10 if be_ticks >= 3 else 0)
        if bull:
            score += 15
            reasons.append("Candle 1 menit: " + ", ".join(bull))
        if vr >= 2:
            score += 15
            reasons.append(f"Volume {vr}x rata-rata 20 bar")
        if s1["strength"] == "Kuat":
            score += 10
        plan = _plan(sr.round_tick(c - t, "down"), sr.round_tick(c), sr.round_tick(s1["zone_lo"] - t, "down"),
                     [target], cfg, [f"Target {be_ticks + 2} tick (impas biaya ±{be_ticks} tick)."])
        out.append(_signal(ticker, "scalper", "support_bounce", "Pantulan support intraday", "PANTAU",
                           score, res, reasons, list(warnings), plan))

    prev_s = res["session_levels"].get("sesi_sebelumnya")
    if prev_s and pbar["close"] <= prev_s["high"] < c and vr >= 2:
        reasons = [f"Menembus high sesi sebelumnya {fmt(prev_s['high'])}", f"Volume {vr}x rata-rata 20 bar"]
        plan = _plan(sr.round_tick(prev_s["high"], "up"), sr.round_tick(c), sr.round_tick(prev_s["high"] - 2 * t, "down"),
                     [target], cfg, [f"Target {be_ticks + 2} tick."])
        out.append(_signal(ticker, "scalper", "prev_high_break", "Tembus high sesi sebelumnya", "PANTAU",
                           50 - penalty, res, reasons, list(warnings), plan))
    return out


RULES = {"swing": swing_signals, "bsjp": bsjp_signals, "bpjs": bpjs_signals, "scalper": scalper_signals}
