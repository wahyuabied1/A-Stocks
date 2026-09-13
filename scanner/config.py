"""Memuat config.json (dibuat dari config.example.json saat pertama kali dijalankan)."""
import copy
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config.json"
EXAMPLE_PATH = Path(__file__).resolve().parent / "config.example.json"
STYLES = ("scalper", "bpjs", "bsjp", "swing")

DEFAULTS = {
    "watchlist": [],
    "styles": list(STYLES),
    "data_source": "yfinance",
    "csv_dir": "data",
    "refresh_seconds": {"scalper": 60, "bpjs": 120, "bsjp": 300, "swing": 900},
    "board": "utama",
    "arb_pct": 0.15,
    "price_rule": "lama",
    "fees": {"buy_pct": 0.15, "sell_pct": 0.25},
    "risk": {"risk_per_trade_rp": None,
             "min_reward_risk": {"swing": 1.5, "bpjs": 1.2, "bsjp": 1.0, "scalper": 1.0}},
    "telegram": {"enabled": False, "bot_token": "", "chat_id": "", "statuses": ["SETUP", "WASPADA"]},
    "dashboard": {"host": "127.0.0.1", "port": 8765},
    "ignore_market_hours": False,
}


def _merge(base, override):
    out = copy.deepcopy(base)
    for k, v in override.items():
        if k.startswith("_"):
            continue
        out[k] = _merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out


def load_config(path=None):
    """Kembalikan (config, dibuat_baru)."""
    path = Path(path) if path else CONFIG_PATH
    created = False
    if not path.exists():
        shutil.copy(EXAMPLE_PATH, path)
        created = True
    with open(path, encoding="utf-8") as f:
        cfg = _merge(DEFAULTS, json.load(f))
    cfg["watchlist"] = list(dict.fromkeys(
        t.strip().upper().removesuffix(".JK") for t in cfg["watchlist"] if str(t).strip()))
    unknown = [s for s in cfg["styles"] if s not in STYLES]
    if unknown:
        raise ValueError(f"Gaya tidak dikenal di config: {unknown}. Pilihan: {', '.join(STYLES)}")
    cfg["_config_path"] = str(path)
    return cfg, created


def save_watchlist(path, tickers):
    """Tulis ulang hanya kunci `watchlist` di config.json (kunci lain & catatan tetap)."""
    path = Path(path)
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw["watchlist"] = list(tickers)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(raw, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)
