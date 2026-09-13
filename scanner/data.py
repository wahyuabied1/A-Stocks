"""Sumber data harga. Tambah kelas baru di sini untuk memakai feed real-time berlisensi."""
import logging
import threading
import time
from pathlib import Path

from .config import ROOT
from .skill import sr

# Interval & periode data per gaya, selaras dengan STYLE_PRESETS di sr_levels.py.
STYLE_DATA = {
    "scalper": ("1m", "5d"),
    "bpjs": ("5m", "1mo"),
    "bsjp": ("1d", "1y"),
    "swing": ("1d", "2y"),
}


class YFinanceSource:
    name = "yfinance"
    delay_note = ("Data yfinance untuk saham BEI tertunda ±10–15 menit dan bisa tidak lengkap. "
                  "Selalu cek harga & antrean terkini di aplikasi sekuritas.")

    def __init__(self):
        try:
            import yfinance
        except ImportError as e:
            raise RuntimeError("yfinance belum terpasang. Jalankan: .venv/bin/pip install -r requirements.txt") from e
        # yfinance mencetak error panjang untuk kode yang tidak ada; kegagalan sudah ditangani di sini.
        logging.getLogger("yfinance").setLevel(logging.CRITICAL)
        self._yf = yfinance
        self._cache = {}
        self._lock = threading.Lock()

    def fetch(self, ticker, interval, period, ttl):
        key = (ticker, interval, period)
        with self._lock:
            hit = self._cache.get(key)
            if hit and time.time() - hit[0] < ttl:
                return hit[1]
        df = self._yf.Ticker(f"{ticker}.JK").history(period=period, interval=interval, auto_adjust=True)
        if df is None or df.empty:
            raise ValueError(f"data {interval} kosong (kode salah, saham disuspensi, atau yfinance bermasalah)")
        daily = interval in ("1d", "5d", "1wk", "1mo")
        rows = []
        for idx, r in df.iterrows():
            o, h, l, c = (float(r[k]) for k in ("Open", "High", "Low", "Close"))
            if any(v != v for v in (o, h, l, c)) or h <= 0:  # lewati bar NaN
                continue
            if getattr(idx, "tzinfo", None) is not None:
                idx = idx.tz_convert("Asia/Jakarta")
            vol = float(r["Volume"]) if r["Volume"] == r["Volume"] else 0.0
            rows.append({"date": idx.strftime("%Y-%m-%d" if daily else "%Y-%m-%d %H:%M"),
                         "open": o, "high": h, "low": l, "close": c, "volume": vol})
        with self._lock:
            self._cache[key] = (time.time(), rows)
        return rows

    def exists(self, ticker):
        try:
            df = self._yf.Ticker(f"{ticker}.JK").history(period="5d", interval="1d")
        except Exception:
            return False
        return df is not None and not df.empty

    def search(self, query, limit=10):
        """Cari saham BEI (.JK) berdasarkan kode atau nama lewat pencarian Yahoo Finance."""
        results = {}
        for q in (query, f"{query}.JK"):
            try:
                quotes = self._yf.Search(q, max_results=20, news_count=0).quotes
            except Exception:
                continue
            for item in quotes:
                symbol = str(item.get("symbol", ""))
                if symbol.endswith(".JK") and len(symbol) == 7 and symbol[:4] not in results:
                    results[symbol[:4]] = {"ticker": symbol[:4],
                                           "name": item.get("longname") or item.get("shortname") or "",
                                           "type": item.get("quoteType", "")}
            if results:
                break
        return list(results.values())[:limit]


class CsvSource:
    """File CSV lokal: <csv_dir>/<KODE>_<interval>.csv, misalnya BBCA_1d.csv atau BBCA_5m.csv."""
    name = "csv"
    delay_note = "Data dari file CSV lokal — tidak ter-update otomatis."

    def __init__(self, csv_dir):
        self.dir = Path(csv_dir)

    def fetch(self, ticker, interval, period, ttl):
        path = self.dir / f"{ticker}_{interval}.csv"
        if not path.exists():
            raise FileNotFoundError(f"file {path} tidak ditemukan")
        return sr.load_csv(str(path))

    def exists(self, ticker):
        return any(self.dir.glob(f"{ticker}_*.csv"))

    def search(self, query, limit=10):
        q = query.strip().upper()
        tickers = sorted({p.name.split("_")[0] for p in self.dir.glob("*_*.csv")})
        return [{"ticker": t, "name": "", "type": "CSV"} for t in tickers if q in t][:limit]


def make_source(cfg):
    if cfg["data_source"] == "csv":
        base = Path(cfg["csv_dir"])
        return CsvSource(base if base.is_absolute() else ROOT / base)
    return YFinanceSource()
