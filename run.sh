#!/usr/bin/env bash
# Jalankan API Python (port 8765) dan dashboard Next.js (port 3000) sekaligus. Ctrl+C menghentikan keduanya.
set -euo pipefail
cd "$(dirname "$0")"

.venv/bin/python -m scanner &
API_PID=$!
trap 'kill "$API_PID" 2>/dev/null || true' EXIT

cd web
npm run dev
