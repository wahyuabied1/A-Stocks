"""Jembatan ke script skill idx-support-resistance agar logika S/R, indikator, dan aturan BEI tidak diduplikasi."""
import sys
from pathlib import Path

SKILL_SCRIPTS = Path(__file__).resolve().parent.parent / ".claude" / "skills" / "idx-support-resistance" / "scripts"
if not (SKILL_SCRIPTS / "sr_levels.py").exists():
    raise ImportError(f"sr_levels.py tidak ditemukan di {SKILL_SCRIPTS}")
sys.path.insert(0, str(SKILL_SCRIPTS))

import sr_levels as sr  # noqa: E402,F401
