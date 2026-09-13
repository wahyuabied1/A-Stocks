"""Notifikasi Telegram untuk sinyal baru (tiap sinyal dikirim sekali per hari per jenis)."""
import html
import json
import threading
import urllib.error
import urllib.request

from .config import ROOT
from .skill import sr

STATE_PATH = ROOT / ".scanner_state.json"
STATUS_ICON = {"SETUP": "🟢", "WASPADA": "🟠", "PANTAU": "⚪"}
STYLE_LABEL = {"scalper": "SCALPER", "bpjs": "BPJS", "bsjp": "BSJP", "swing": "SWING"}


def format_signal(s):
    e, rp = html.escape, sr.fmt_rp
    lines = [f"{STATUS_ICON.get(s['status'], '')} <b>{e(s['status'])} · {STYLE_LABEL[s['style']]} · {e(s['ticker'])}</b>",
             f"{e(s['title'])} (skor {s['score']})",
             f"Harga {rp(s['price'])} · data {e(s['as_of'])}"]
    p = s.get("plan")
    if p:
        targets = " / ".join(rp(x) for x in p["targets"]) or "-"
        rr = p["rr"] if p["rr"] is not None else "-"
        lines.append(f"Entry {rp(p['entry'][0])}–{rp(p['entry'][1])} · Stop {rp(p['stop'])} · "
                     f"Target {targets} · R:R {rr}")
        if p.get("lots"):
            lines.append(f"Ukuran sesuai batas risikomu: {p['lots']} lot (risiko ±{rp(p['risk_rp'])})")
        lines += ["• " + e(n) for n in p["notes"]]
    if s["reasons"]:
        lines += ["<b>Alasan</b>"] + ["• " + e(r) for r in s["reasons"]]
    if s["warnings"]:
        lines += ["<b>Peringatan</b>"] + ["• " + e(w) for w in s["warnings"][:5]]
    lines.append("<i>Edukasi, bukan rekomendasi. Keputusan &amp; eksekusi order sepenuhnya milikmu.</i>")
    return "\n".join(lines)


class TelegramNotifier:
    def __init__(self, cfg):
        tg = cfg["telegram"]
        self.token = str(tg.get("bot_token") or "").strip()
        self.chat_id = str(tg.get("chat_id") or "").strip()
        self.enabled = bool(tg.get("enabled") and self.token and self.chat_id)
        self.statuses = set(tg.get("statuses") or ["SETUP", "WASPADA"])
        self.last_error = ("Telegram diaktifkan tetapi bot_token/chat_id kosong."
                           if tg.get("enabled") and not self.enabled else None)
        self._lock = threading.Lock()
        self._sent = self._load()

    def _load(self):
        try:
            return json.loads(STATE_PATH.read_text()).get("sent", [])
        except (OSError, ValueError):
            return []

    def notify(self, signals):
        if not self.enabled:
            return
        for s in signals:
            if s["status"] not in self.statuses:
                continue
            with self._lock:
                if s["id"] in self._sent:
                    continue
                self._sent.append(s["id"])
            if self.send(format_signal(s)):
                with self._lock:
                    self._sent = self._sent[-1000:]
                    STATE_PATH.write_text(json.dumps({"sent": self._sent}))
            else:
                with self._lock:
                    self._sent.remove(s["id"])

    def send(self, text):
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{self.token}/sendMessage",
            data=json.dumps({"chat_id": self.chat_id, "text": text, "parse_mode": "HTML",
                             "disable_web_page_preview": True}).encode(),
            headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                ok = bool(json.load(resp).get("ok"))
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            self.last_error = f"Gagal kirim Telegram: {getattr(e, 'reason', e)}"
            return False
        self.last_error = None if ok else "Telegram menolak pesan (cek bot_token/chat_id)."
        return ok

    def send_test(self):
        if not self.enabled:
            return False, self.last_error or "Telegram belum diaktifkan di config.json."
        ok = self.send("✅ Tes pemindai sinyal IDX berhasil. Sinyal SETUP/WASPADA akan dikirim ke chat ini.")
        return ok, self.last_error
