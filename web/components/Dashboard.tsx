"use client";

import { useMemo, useState } from "react";
import { STYLE_LABEL } from "@/lib/format";
import type { ScannerState, Status, Style } from "@/lib/types";
import { usePolling } from "@/lib/usePolling";
import AppHeader from "./AppHeader";
import FilterGroup from "./FilterGroup";
import Notice from "./Notice";
import SignalCard from "./SignalCard";
import SummaryTable from "./SummaryTable";
import WatchlistManager from "./WatchlistManager";

const STATUSES: readonly (Status | "semua")[] = ["semua", "SETUP", "WASPADA", "PANTAU"];

export default function Dashboard() {
  const { data: state, error, reload } = usePolling<ScannerState>("/api/state", 15000);
  const [styleFilter, setStyleFilter] = useState<Style | "semua">("semua");
  const [statusFilter, setStatusFilter] = useState<Status | "semua">("semua");
  const [summaryStyle, setSummaryStyle] = useState<Style | null>(null);

  const styles = state?.styles ?? [];
  const activeSummary: Style | undefined =
    summaryStyle && styles.includes(summaryStyle) ? summaryStyle : styles.includes("swing") ? "swing" : styles[0];

  const signals = useMemo(
    () =>
      (state?.signals ?? []).filter(
        (s) => (styleFilter === "semua" || s.style === styleFilter) && (statusFilter === "semua" || s.status === statusFilter),
      ),
    [state, styleFilter, statusFilter],
  );

  const errors = state
    ? Object.entries(state.errors).flatMap(([style, byTicker]) =>
        Object.entries(byTicker ?? {}).map(([ticker, msg]) => `${STYLE_LABEL[style as Style]} · ${ticker}: ${msg}`),
      )
    : [];

  return (
    <>
      <AppHeader state={state} error={error} onRefresh={reload} />
      <main className="container">
        <Notice state={state} error={error} />

        {state && (
          <>
            <WatchlistManager state={state} onChanged={reload} />

            <h2>Sinyal</h2>
            <FilterGroup
              ariaLabel="Filter gaya"
              items={["semua", ...styles] as const}
              value={styleFilter}
              label={(v) => (v === "semua" ? "Semua gaya" : STYLE_LABEL[v])}
              onChange={setStyleFilter}
            />
            <FilterGroup
              ariaLabel="Filter status"
              items={STATUSES}
              value={statusFilter}
              label={(v) => (v === "semua" ? "Semua status" : v)}
              onChange={setStatusFilter}
            />
            {signals.length === 0 ? (
              <div className="empty">
                {state.watchlist.length === 0
                  ? "Belum ada saham di watchlist. Tambahkan saham di atas untuk mulai memindai."
                  : "Tidak ada sinyal untuk filter ini. Pemindaian berjalan otomatis; sinyal intraday hanya muncul saat sesi perdagangan. Klik kode saham di watchlist atau tabel untuk melihat chart."}
              </div>
            ) : (
              <div className="grid">
                {signals.map((s) => (
                  <SignalCard key={s.id} signal={s} />
                ))}
              </div>
            )}

            <h2>Ringkasan watchlist</h2>
            {activeSummary && (
              <>
                <FilterGroup
                  ariaLabel="Pilih gaya ringkasan"
                  items={styles}
                  value={activeSummary}
                  label={(v) => STYLE_LABEL[v]}
                  onChange={setSummaryStyle}
                />
                <SummaryTable state={state} style={activeSummary} />
              </>
            )}

            {errors.length > 0 && (
              <details>
                <summary>Error pemindaian ({errors.length})</summary>
                <ul>
                  {errors.map((e) => (
                    <li key={e}>{e}</li>
                  ))}
                </ul>
              </details>
            )}
            <footer>
              Sumber data: {state.data_source} · diperbarui {state.generated_at} WIB · data dimuat ulang tiap 15 detik
            </footer>
          </>
        )}
      </main>
    </>
  );
}
