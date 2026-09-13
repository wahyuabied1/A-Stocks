"""Loop pemindaian: ambil data → analisis skill → aturan sinyal → simpan state & kirim notifikasi."""
import re
import threading
import time
from datetime import datetime

from .config import save_watchlist
from .data import STYLE_DATA
from .market import WIB, session_status
from .signals import RULES, sort_signals
from .skill import sr

INTRADAY_STYLES = ("scalper", "bpjs")
MAX_WATCHLIST = 50  # batasi agar tidak kena pembatasan akses Yahoo Finance
TICKER_RE = re.compile(r"[A-Z]{4}")
OFF_HOURS_REFRESH = 900
DISCLAIMER = ("Sinyal bersifat edukasi berdasarkan aturan teknikal, bukan rekomendasi beli/jual. "
              "Aplikasi tidak mengeksekusi order; keputusan dan transaksi sepenuhnya milikmu.")


def summarize(res):
    def zone(z):
        return None if not z else {"zone": [z["zone_lo"], z["zone_hi"]], "strength": z["strength"],
                                   "dist_pct": z["dist_pct"]}

    rsi, macd = res["rsi"] or {}, res["macd"] or {}
    return {
        "price": res["last_close"],
        "as_of": res["as_of"],
        "timeframe": res["timeframe"],
        "support": zone(res["supports"][0] if res["supports"] else None),
        "resistance": zone(res["resistances"][0] if res["resistances"] else None),
        "rsi": rsi.get("value"),
        "macd": (f"{'>' if macd['above_signal'] else '<'} signal, {'>' if macd['above_zero'] else '<'} 0"
                 if macd else None),
        "ma_alignment": (res["moving_average_analysis"] or {}).get("alignment"),
        "volume_ratio": (res["volume"] or {}).get("last_vs_avg20"),
        "candles": [p["name"] for c in res["candlestick"] if c["bars_ago"] <= 1 for p in c["patterns"]],
        "limits": res["auto_rejection"][-1],
        "warnings": res["warnings"],
    }


CHART_BARS = {"scalper": 240, "bpjs": 330, "bsjp": 120, "swing": 250}


def build_chart(rows, res, style):
    """Data untuk chart candlestick: bar terakhir, garis MA/VWAP, zona S/R, dan hasil indikator."""
    n = CHART_BARS[style]
    bars = rows[-n:]
    closes = [r["close"] for r in rows]

    def series(values):
        return [{"time": b["date"], "value": round(v, 2)} for b, v in zip(bars, values[-n:]) if v is not None]

    lines = {"MA20": series(sr.sma_series(closes, 20)), "MA50": series(sr.sma_series(closes, 50))}
    if res["timeframe"] == "intraday":
        vwap, day, pv, vol = [], None, 0.0, 0.0
        for r in rows:  # VWAP berjalan, direset tiap sesi
            if r["date"][:10] != day:
                day, pv, vol = r["date"][:10], 0.0, 0.0
            pv += (r["high"] + r["low"] + r["close"]) / 3 * r["volume"]
            vol += r["volume"]
            vwap.append(pv / vol if vol else None)
        lines["VWAP"] = series(vwap)

    def zones(items, kind):
        return [{"kind": kind, "lo": z["zone_lo"], "hi": z["zone_hi"], "mid": z["mid"], "strength": z["strength"],
                 "touches": z["touches"], "dist_pct": z["dist_pct"], "confluence": z["confluence"]} for z in items]

    return {
        "style": style,
        "timeframe": res["timeframe"],
        "as_of": res["as_of"],
        "tick_size": res["tick_size"],
        "bars": bars,
        "lines": lines,
        "zones": zones(res["supports"], "support") + zones(res["resistances"], "resistance"),
        "limits": res["auto_rejection"],
        "fibonacci": res["fibonacci"],
        "rsi": res["rsi"],
        "macd": res["macd"],
        "moving_averages": res["moving_average_analysis"],
        "volume": res["volume"],
        "candlestick": res["candlestick"],
        "summary": summarize(res),
    }


class Scanner:
    def __init__(self, cfg, source, notifier):
        self.cfg, self.source, self.notifier = cfg, source, notifier
        self.board = cfg["board"] if cfg["board"] in sr.FCA_BOARDS else "utama"
        self._lock = threading.Lock()
        self._watchlist_lock = threading.Lock()
        self._wake = threading.Event()
        self.signals, self.summaries, self.errors, self.last_scan, self.charts = {}, {}, {}, {}, {}
        self.next_due = {s: 0.0 for s in cfg["styles"]}

    def scan_style(self, style):
        market = session_status()
        interval, period = STYLE_DATA[style]
        preset = sr.STYLE_PRESETS[style]
        ttl = max(30, self.cfg["refresh_seconds"].get(style, 300) - 5)
        signals, summaries, errors, charts = [], {}, {}, {}
        for ticker in self.cfg["watchlist"]:
            try:
                rows = self.source.fetch(ticker, interval, period, ttl)
                need = preset["window"] * 2 + 30
                if len(rows) < need:
                    raise ValueError(f"data terlalu sedikit ({len(rows)} bar, perlu ≥{need})")
                res = sr.analyze(rows, preset["lookback"], preset["window"], self.board,
                                 self.cfg["arb_pct"], self.cfg["price_rule"], 3, style)
                summaries[ticker] = summarize(res)
                charts[ticker] = build_chart(rows, res, style)
                signals += RULES[style](ticker, rows, res, self.cfg, market)
            except SystemExit as e:  # sr_levels memakai sys.exit untuk data tidak valid
                errors[ticker] = str(e)
            except Exception as e:  # satu saham gagal tidak boleh menghentikan pemindaian
                errors[ticker] = f"{type(e).__name__}: {e}"
        # Watchlist bisa berubah saat pemindaian berjalan: simpan hanya saham yang masih ada.
        current = set(self.cfg["watchlist"])
        signals = [s for s in signals if s["ticker"] in current]
        errors = {t: e for t, e in errors.items() if t in current}
        with self._lock:
            self.signals[style] = signals
            self.summaries[style] = {t: v for t, v in summaries.items() if t in current}
            self.charts[style] = {t: v for t, v in charts.items() if t in current}
            self.errors[style] = errors
            self.last_scan[style] = datetime.now(WIB).strftime("%Y-%m-%d %H:%M:%S")
        self.notifier.notify(signals)
        return signals, errors

    def run_forever(self, stop_event):
        while not stop_event.is_set():
            for style in self.cfg["styles"]:
                if time.time() < self.next_due[style]:
                    continue
                self.scan_style(style)
                every = self.cfg["refresh_seconds"].get(style, 300)
                if style in INTRADAY_STYLES and not session_status()["trading"] \
                        and not self.cfg.get("ignore_market_hours"):
                    every = max(every, OFF_HOURS_REFRESH)
                self.next_due[style] = time.time() + every
            self._wake.wait(5)
            self._wake.clear()

    def request_scan(self):
        for style in self.next_due:
            self.next_due[style] = 0.0
        self._wake.set()

    def update_watchlist(self, add=(), remove=(), replace=None):
        """Tambah/hapus/ganti watchlist, simpan ke config.json, lalu pindai saham baru."""
        with self._watchlist_lock:
            current = list(self.cfg["watchlist"])
            new = [] if replace is not None else list(current)
            rejected = {}
            for raw in (replace if replace is not None else add):
                ticker = str(raw).strip().upper().removesuffix(".JK")
                if not ticker or ticker in new:
                    continue
                if not TICKER_RE.fullmatch(ticker):
                    rejected[ticker] = "Kode saham harus 4 huruf, contoh BBCA."
                elif len(new) >= MAX_WATCHLIST:
                    rejected[ticker] = f"Watchlist maksimal {MAX_WATCHLIST} saham."
                elif ticker not in current and not self.source.exists(ticker):
                    rejected[ticker] = "Kode tidak ditemukan di sumber data (cek ejaan, atau saham disuspensi/delisting)."
                else:
                    new.append(ticker)
            drop = {str(r).strip().upper().removesuffix(".JK") for r in remove}
            new = [t for t in new if t not in drop]
            added = [t for t in new if t not in current]
            removed = [t for t in current if t not in new]

            if new != current:
                save_watchlist(self.cfg["_config_path"], new)
                self.cfg["watchlist"] = new
                keep = set(new)
                with self._lock:
                    for store in (self.summaries, self.charts, self.errors):
                        for style in store:
                            store[style] = {t: v for t, v in store[style].items() if t in keep}
                    for style in self.signals:
                        self.signals[style] = [s for s in self.signals[style] if s["ticker"] in keep]
                if added:
                    self.request_scan()
            return {"watchlist": new, "added": added, "removed": removed, "rejected": rejected}

    def chart(self, ticker, style):
        """Data chart + sinyal satu saham; None jika saham/gaya tidak ada di konfigurasi."""
        if ticker not in self.cfg["watchlist"] or style not in self.cfg["styles"]:
            return None
        with self._lock:
            data = self.charts.get(style, {}).get(ticker)
            error = self.errors.get(style, {}).get(ticker)
            signals = [s for s in self.signals.get(style, []) if s["ticker"] == ticker]
        if data is None:
            return {"ticker": ticker, "style": style, "bars": [],
                    "error": error or "Belum dipindai — tunggu beberapa detik."}
        return {**data, "ticker": ticker, "signals": sort_signals(signals), "error": error}

    def snapshot(self):
        with self._lock:
            return {
                "generated_at": datetime.now(WIB).strftime("%Y-%m-%d %H:%M:%S"),
                "market": session_status(),
                "data_source": self.source.name,
                "data_note": self.source.delay_note,
                "disclaimer": DISCLAIMER,
                "styles": self.cfg["styles"],
                "watchlist": self.cfg["watchlist"],
                "max_watchlist": MAX_WATCHLIST,
                "signals": sort_signals([s for sigs in self.signals.values() for s in sigs]),
                "summaries": self.summaries,
                "errors": self.errors,
                "last_scan": self.last_scan,
                "telegram": {"enabled": self.notifier.enabled, "error": self.notifier.last_error},
            }
