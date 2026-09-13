"""CLI pemindai sinyal IDX.

    python -m scanner                  jalankan dashboard + pemindaian berkala
    python -m scanner --sekali         pindai sekali dan cetak ke terminal
    python -m scanner --gaya swing,bsjp
    python -m scanner --tes-telegram   kirim pesan uji ke Telegram
    python -m scanner --abaikan-jam    abaikan jam bursa (untuk uji dengan data lama)
"""
import argparse
import sys

from .config import CONFIG_PATH, STYLES, load_config
from .data import make_source
from .engine import DISCLAIMER, Scanner
from .notify import TelegramNotifier
from .signals import sort_signals
from .skill import sr

STYLE_LABEL = {"scalper": "Scalper", "bpjs": "BPJS", "bsjp": "BSJP", "swing": "Swing"}


def print_report(style, signals, errors, total):
    fmt = sr.fmt_rp
    print(f"\n=== {STYLE_LABEL[style]} — {total} saham ===")
    if not signals:
        print("  (tidak ada sinyal)")
    for s in sort_signals(signals):
        print(f"  [{s['status']} {s['score']}] {s['ticker']} — {s['title']} @ {fmt(s['price'])} ({s['as_of']})")
        p = s["plan"]
        if p:
            targets = " / ".join(fmt(x) for x in p["targets"]) or "-"
            lots = f" | {p['lots']} lot" if p["lots"] else ""
            print(f"     Entry {fmt(p['entry'][0])}–{fmt(p['entry'][1])} | Stop {fmt(p['stop'])} | "
                  f"Target {targets} | R:R {p['rr']}{lots}")
        for r in s["reasons"]:
            print(f"     + {r}")
        for w in s["warnings"]:
            print(f"     ! {w}")
    for ticker, err in errors.items():
        print(f"  x {ticker}: {err}")


def main():
    ap = argparse.ArgumentParser(prog="python -m scanner",
                                 description="Pemindai sinyal saham IDX (edukasi, tanpa eksekusi order)")
    ap.add_argument("--config", help=f"path config (default {CONFIG_PATH.name})")
    ap.add_argument("--sekali", action="store_true", help="pindai sekali lalu cetak ke terminal")
    ap.add_argument("--gaya", help=f"gaya dipisah koma: {','.join(STYLES)}")
    ap.add_argument("--abaikan-jam", action="store_true", help="abaikan jam bursa (untuk pengujian)")
    ap.add_argument("--tes-telegram", action="store_true", help="kirim pesan uji ke Telegram")
    ap.add_argument("--port", type=int, help="port dashboard")
    args = ap.parse_args()

    try:
        cfg, created = load_config(args.config)
    except ValueError as e:
        sys.exit(str(e))
    if created:
        print(f"{CONFIG_PATH.name} dibuat dari contoh. Isi watchlist kamu di file itu.")
    if args.gaya:
        styles = [s.strip().lower() for s in args.gaya.split(",") if s.strip()]
        bad = [s for s in styles if s not in STYLES]
        if bad:
            sys.exit(f"Gaya tidak dikenal: {bad}. Pilihan: {', '.join(STYLES)}")
        cfg["styles"] = styles
    if args.abaikan_jam:
        cfg["ignore_market_hours"] = True
    if args.port:
        cfg["dashboard"]["port"] = args.port
    if not cfg["watchlist"] and args.sekali:
        sys.exit("Watchlist kosong. Isi 'watchlist' di config.json atau tambahkan lewat dashboard.")

    notifier = TelegramNotifier(cfg)
    if args.tes_telegram:
        ok, err = notifier.send_test()
        sys.exit(0 if ok else f"Tes Telegram gagal: {err}")

    try:
        source = make_source(cfg)
    except RuntimeError as e:
        sys.exit(str(e))
    scanner = Scanner(cfg, source, notifier)

    if args.sekali:
        print(DISCLAIMER)
        print(source.delay_note)
        for style in cfg["styles"]:
            signals, errors = scanner.scan_style(style)
            print_report(style, signals, errors, len(cfg["watchlist"]))
        if notifier.last_error:
            print(f"\nTelegram: {notifier.last_error}")
        return

    from .server import serve
    serve(scanner, cfg)


if __name__ == "__main__":
    main()
