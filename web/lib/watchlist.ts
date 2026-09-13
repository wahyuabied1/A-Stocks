import type { SearchResult, WatchlistUpdate } from "./types";

async function postWatchlist(body: object): Promise<WatchlistUpdate> {
  const res = await fetch("/api/watchlist", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await res.json().catch(() => null);
  if (!res.ok) throw new Error(data?.error ?? `HTTP ${res.status}`);
  return data as WatchlistUpdate;
}

export const addToWatchlist = (tickers: string[]) => postWatchlist({ add: tickers });
export const removeFromWatchlist = (tickers: string[]) => postWatchlist({ remove: tickers });

export async function searchStocks(query: string, signal?: AbortSignal): Promise<SearchResult[]> {
  const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`, { signal, cache: "no-store" });
  if (!res.ok) return [];
  return ((await res.json()) as { results: SearchResult[] }).results;
}

/** "bbca, BBRI tlkm.jk" → ["BBCA", "BBRI", "TLKM"] jika seluruh input berupa kode 4 huruf; selain itu null. */
export function parseTickers(input: string): string[] | null {
  const parts = input
    .toUpperCase()
    .split(/[\s,;]+/)
    .map((p) => p.replace(/\.JK$/, ""))
    .filter(Boolean);
  return parts.length > 0 && parts.every((p) => /^[A-Z]{4}$/.test(p)) ? parts : null;
}
