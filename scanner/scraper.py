"""Scraper harga saham BEI (IDX) real-time dari Google Finance dengan fallback ke Yahoo Finance."""
import logging
import re
import threading
import time
from datetime import datetime
import zoneinfo

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger("scanner.scraper")
WIB = zoneinfo.ZoneInfo("Asia/Jakarta")

# Cache in-memory (ticker -> (timestamp, data)) dengan TTL 20 detik agar selaras dengan polling 30 detik
_CACHE = {}
_LOCK = threading.Lock()
CACHE_TTL = 20  # detik

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
}


def _clean_price_text(text: str) -> float | None:
    """Mengubah string harga (misal: 'Rp105', 'Rp 10.450', '105.00') menjadi float."""
    if not text:
        return None
    # Hapus mata uang dan spasi
    cleaned = re.sub(r"[^\d,\.]", "", text.strip())
    if not cleaned:
        return None

    # Deteksi format ribuan dan desimal Indonesia (10.450,00) vs format standar (10,450.00 / 105)
    if "," in cleaned and "." in cleaned:
        if cleaned.rfind(",") > cleaned.rfind("."):
            # Format Indonesia: titik = ribuan, koma = desimal
            cleaned = cleaned.replace(".", "").replace(",", ".")
        else:
            # Format US: koma = ribuan, titik = desimal
            cleaned = cleaned.replace(",", "")
    elif "," in cleaned:
        # Hanya koma, periksa apakah desimal atau ribuan
        parts = cleaned.split(",")
        if len(parts) == 2 and len(parts[1]) <= 2:
            cleaned = cleaned.replace(",", ".")
        else:
            cleaned = cleaned.replace(",", "")
    elif "." in cleaned:
        # Jika ada titik, periksa apakah format ribuan IDR (misal 9.450) atau desimal (misal 94.5)
        parts = cleaned.split(".")
        if len(parts) == 2 and len(parts[1]) == 3 and int(parts[0]) > 0:
            # Kemungkinan besar ribuan tanpa desimal (misal saham BBCA 9.850)
            cleaned = cleaned.replace(".", "")

    try:
        val = float(cleaned)
        return val if val > 0 else None
    except ValueError:
        return None


def _scrape_google_finance(ticker: str) -> tuple[float | None, str | None]:
    """Mengambil harga terkini dari Google Finance."""
    url = f"https://www.google.com/finance/quote/{ticker}:IDX"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=8)
        if resp.status_code != 200:
            return None, f"Google Finance HTTP {resp.status_code}"

        soup = BeautifulSoup(resp.text, "html.parser")
        # Class elemen harga Google Finance
        price_el = soup.find("div", class_="YMlKec fxKbKc")
        if not price_el:
            # Coba selektor alternatif
            price_el = soup.select_one("[data-last-price]") or soup.select_one(".YMlKec")

        if price_el:
            price = _clean_price_text(price_el.get_text())
            if price:
                return price, None

        return None, "Elemen harga tidak ditemukan di halaman Google Finance"
    except Exception as e:
        return None, str(e)


def _scrape_yahoo_finance(ticker: str) -> tuple[float | None, str | None]:
    """Fallback cepat ke yfinance jika Google Finance gagal."""
    try:
        import yfinance as yf
        t = yf.Ticker(f"{ticker}.JK")
        # Coba fast_info terlebih dahulu (lebih cepat)
        price = getattr(t.fast_info, "last_price", None)
        if price and price > 0:
            return float(price), None
        
        # Coba info reguler jika fast_info kosong
        info = t.info or {}
        price = info.get("currentPrice") or info.get("regularMarketPrice")
        if price and price > 0:
            return float(price), None

        return None, "Harga yfinance kosong atau saham tidak aktif"
    except Exception as e:
        return None, str(e)


def scrape_realtime_price(ticker: str) -> dict:
    """Mengambil harga saham terkini dengan proteksi cache dan fallback."""
    clean_ticker = ticker.strip().upper().removesuffix(".JK")
    now_dt = datetime.now(WIB)
    as_of_str = now_dt.strftime("%H:%M:%S WIB")

    # Cek cache
    with _LOCK:
        if clean_ticker in _CACHE:
            cached_time, cached_data = _CACHE[clean_ticker]
            if time.time() - cached_time < CACHE_TTL:
                return cached_data

    # 1. Coba Google Finance (Prioritas utama)
    price, err = _scrape_google_finance(clean_ticker)
    source = "googlefinance"

    # 2. Fallback ke Yahoo Finance jika Google Finance gagal
    if price is None:
        logger.warning("Google Finance gagal untuk %s (%s), mencoba fallback ke yfinance", clean_ticker, err)
        yf_price, yf_err = _scrape_yahoo_finance(clean_ticker)
        if yf_price is not None:
            price = yf_price
            source = "yfinance"
            err = None
        else:
            err = f"Google: {err}; Yahoo: {yf_err}"

    success = price is not None
    result = {
        "ticker": clean_ticker,
        "price": round(price, 2) if price else None,
        "source": source if success else None,
        "as_of": as_of_str,
        "success": success,
        "error": err,
    }

    # Simpan ke cache jika sukses
    if success:
        with _LOCK:
            _CACHE[clean_ticker] = (time.time(), result)

    return result
