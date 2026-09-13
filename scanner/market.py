"""Status sesi perdagangan BEI (WIB). Hari libur bursa nasional tidak dideteksi."""
from datetime import datetime, time as dtime
from zoneinfo import ZoneInfo

WIB = ZoneInfo("Asia/Jakarta")


def session_status(now=None):
    now = now or datetime.now(WIB)
    t, wd = now.time(), now.weekday()
    base = {"date": now.strftime("%Y-%m-%d"), "time": now.strftime("%H:%M:%S"), "weekday": wd,
            "trading": False, "bsjp_window": False}
    if wd >= 5:
        return {**base, "phase": "libur", "label": "Pasar tutup (akhir pekan)"}

    friday = wd == 4
    s1_end = dtime(11, 30) if friday else dtime(12, 0)
    s2_start = dtime(14, 0) if friday else dtime(13, 30)
    phases = [
        (dtime(8, 45), dtime(9, 0), "pre-opening", "Pre-opening (call auction)", False),
        (dtime(9, 0), s1_end, "sesi1", "Sesi 1", True),
        (s1_end, s2_start, "istirahat", "Istirahat siang", False),
        (s2_start, dtime(15, 50), "sesi2", "Sesi 2", True),
        (dtime(15, 50), dtime(16, 0), "pre-closing", "Pre-closing (call auction)", False),
    ]
    for start, end, phase, label, trading in phases:
        if start <= t < end:
            return {**base, "phase": phase, "label": label, "trading": trading,
                    "bsjp_window": dtime(14, 30) <= t < dtime(16, 0)}
    if t < dtime(8, 45):
        return {**base, "phase": "pra-pasar", "label": "Sebelum pasar buka"}
    return {**base, "phase": "tutup", "label": "Pasar sudah tutup"}
