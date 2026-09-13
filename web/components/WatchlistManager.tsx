"use client";

import Link from "next/link";
import { useEffect, useState, type FormEvent } from "react";
import type { ScannerState, SearchResult, WatchlistUpdate } from "@/lib/types";
import { addToWatchlist, parseTickers, removeFromWatchlist, searchStocks } from "@/lib/watchlist";

interface Props {
  state: ScannerState;
  onChanged: () => void;
}

export default function WatchlistManager({ state, onChanged }: Props) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [searching, setSearching] = useState(false);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState<{ kind: "ok" | "error"; text: string } | null>(null);

  // Pencarian (debounce 350 ms). Input berupa daftar kode tidak perlu dicari.
  useEffect(() => {
    const q = query.trim();
    if (q.length < 2 || (parseTickers(q)?.length ?? 0) > 1) {
      setResults([]);
      return;
    }
    const ctrl = new AbortController();
    const id = setTimeout(async () => {
      setSearching(true);
      try {
        setResults(await searchStocks(q, ctrl.signal));
      } catch {
        // dibatalkan karena input berubah
      } finally {
        setSearching(false);
      }
    }, 350);
    return () => {
      clearTimeout(id);
      ctrl.abort();
    };
  }, [query]);

  async function run(action: () => Promise<WatchlistUpdate>) {
    setBusy(true);
    setMessage(null);
    try {
      const r = await action();
      const rejected = Object.entries(r.rejected).map(([t, why]) => `${t}: ${why}`);
      const done = [
        r.added.length ? `Ditambahkan: ${r.added.join(", ")} (sedang dipindai).` : "",
        r.removed.length ? `Dihapus: ${r.removed.join(", ")}.` : "",
      ].filter(Boolean);
      if (rejected.length) setMessage({ kind: "error", text: [...done, ...rejected].join(" ") });
      else if (done.length) setMessage({ kind: "ok", text: done.join(" ") });
      if (r.added.length && !rejected.length) {
        setQuery("");
        setResults([]);
      }
      onChanged();
    } catch (e) {
      setMessage({ kind: "error", text: e instanceof Error ? e.message : String(e) });
    } finally {
      setBusy(false);
    }
  }

  function submit(e: FormEvent) {
    e.preventDefault();
    const tickers = parseTickers(query) ?? (results[0] ? [results[0].ticker] : null);
    if (!tickers) {
      setMessage({ kind: "error", text: "Ketik kode saham 4 huruf (contoh BBCA) atau pilih dari hasil pencarian." });
      return;
    }
    run(() => addToWatchlist(tickers));
  }

  const errorByTicker: Record<string, string> = {};
  for (const byTicker of Object.values(state.errors)) {
    for (const [t, msg] of Object.entries(byTicker ?? {})) errorByTicker[t] ??= msg;
  }
  const scanned = new Set(Object.values(state.summaries).flatMap((s) => Object.keys(s ?? {})));
  const signalCount: Record<string, number> = {};
  for (const s of state.signals) signalCount[s.ticker] = (signalCount[s.ticker] ?? 0) + 1;
  const full = state.watchlist.length >= state.max_watchlist;

  return (
    <section className="panel watchlist">
      <div className="watchlist-head">
        <h3>Watchlist saya</h3>
        <span className="meta">
          {state.watchlist.length}/{state.max_watchlist} saham · hanya saham di watchlist yang dipindai dan ditampilkan
        </span>
      </div>

      <form className="search" onSubmit={submit}>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={full ? "Watchlist penuh — hapus saham dulu" : "Cari kode atau nama saham, atau ketik beberapa kode: BBCA, BBRI, TLKM"}
          aria-label="Cari saham untuk ditambahkan ke watchlist"
          autoComplete="off"
          disabled={full}
        />
        <button type="submit" className="primary" disabled={busy || full || !query.trim()}>
          {busy ? "Menyimpan…" : "Tambah"}
        </button>
        {(results.length > 0 || searching) && (
          <ul className="search-results">
            {searching && results.length === 0 && <li className="meta">Mencari…</li>}
            {results.map((r) => {
              const inList = state.watchlist.includes(r.ticker);
              return (
                <li key={r.ticker}>
                  <span>
                    <b>{r.ticker}</b> <span className="meta">{r.name}</span>
                  </span>
                  {inList ? (
                    <span className="meta">✓ Sudah di watchlist</span>
                  ) : (
                    <button type="button" disabled={busy || full} onClick={() => run(() => addToWatchlist([r.ticker]))}>
                      + Tambah
                    </button>
                  )}
                </li>
              );
            })}
          </ul>
        )}
      </form>

      {message && <p className={`message ${message.kind}`}>{message.text}</p>}

      {state.watchlist.length === 0 ? (
        <p className="empty">Watchlist masih kosong. Cari dan tambahkan saham di atas untuk mulai memindai.</p>
      ) : (
        <ul className="chips">
          {state.watchlist.map((t) => {
            const error = errorByTicker[t];
            const pending = !scanned.has(t) && !error;
            return (
              <li key={t} className={`chip ${error ? "has-error" : ""}`} title={error ?? (pending ? "Sedang dipindai…" : "")}>
                <Link href={`/saham/${t}`}>{t}</Link>
                {signalCount[t] ? <span className="chip-badge">{signalCount[t]} sinyal</span> : null}
                {pending && <span className="meta">memindai…</span>}
                {error && <span className="chip-err">error</span>}
                <button type="button" aria-label={`Hapus ${t} dari watchlist`} disabled={busy} onClick={() => run(() => removeFromWatchlist([t]))}>
                  ×
                </button>
              </li>
            );
          })}
        </ul>
      )}
    </section>
  );
}
