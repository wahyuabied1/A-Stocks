"use client";

import { useState } from "react";
import { addToWatchlist, removeFromWatchlist } from "@/lib/watchlist";

interface Props {
  ticker: string;
  inWatchlist: boolean;
  onChanged: () => void;
}

export default function WatchlistToggle({ ticker, inWatchlist, onChanged }: Props) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function toggle() {
    setBusy(true);
    setError(null);
    try {
      const r = inWatchlist ? await removeFromWatchlist([ticker]) : await addToWatchlist([ticker]);
      if (r.rejected[ticker]) setError(r.rejected[ticker]);
      onChanged();
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  }

  return (
    <span className="watch-toggle">
      <button type="button" className={inWatchlist ? "" : "primary"} onClick={toggle} disabled={busy}>
        {busy ? "Menyimpan…" : inWatchlist ? "★ Hapus dari watchlist" : "☆ Tambah ke watchlist"}
      </button>
      {error && <span className="neg">{error}</span>}
    </span>
  );
}
