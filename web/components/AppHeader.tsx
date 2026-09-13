"use client";

import Link from "next/link";
import { useState } from "react";
import { STYLE_LABEL } from "@/lib/format";
import type { ScannerState, Style } from "@/lib/types";

interface Props {
  state: ScannerState | null;
  error: string | null;
  onRefresh: () => void;
}

export default function AppHeader({ state, error, onRefresh }: Props) {
  const [scanning, setScanning] = useState(false);
  const market = state?.market;
  const apiDown = !!error && !state;

  async function scan() {
    setScanning(true);
    try {
      await fetch("/api/scan", { method: "POST" });
    } catch {
      // API tidak terhubung; status ditampilkan di pill.
    }
    setTimeout(() => {
      onRefresh();
      setScanning(false);
    }, 5000);
  }

  const scans = state
    ? Object.entries(state.last_scan)
        .map(([style, time]) => `${STYLE_LABEL[style as Style]} ${time?.slice(11) ?? "-"}`)
        .join(" · ")
    : "";

  return (
    <header className="app-header">
      <Link href="/" className="brand">Pemindai Sinyal IDX</Link>
      <span className={`pill ${apiDown ? "bad" : market?.trading ? "live" : ""}`}>
        {apiDown ? "API Python tidak terhubung" : market ? `${market.label} · ${market.time} WIB` : "Memuat…"}
      </span>
      {state && (
        <span className={`pill ${state.telegram.enabled ? "live" : ""}`} title={state.telegram.error ?? ""}>
          {state.telegram.enabled ? "Telegram aktif" : "Telegram nonaktif"}
        </span>
      )}
      {scans && <span className="meta">Pindai terakhir: {scans}</span>}
      <button type="button" className="primary" onClick={scan} disabled={scanning || apiDown}>
        {scanning ? "Memindai…" : "Pindai sekarang"}
      </button>
    </header>
  );
}
