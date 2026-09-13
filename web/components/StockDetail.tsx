"use client";

import dynamic from "next/dynamic";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { STYLE_LABEL, isStyle, pct, rp } from "@/lib/format";
import { isFullChart, type ChartData, type ChartResponse, type ScannerState, type Style } from "@/lib/types";
import { usePolling } from "@/lib/usePolling";
import AppHeader from "./AppHeader";
import type { Layers } from "./CandleChart";
import FilterGroup from "./FilterGroup";
import PlanGrid from "./PlanGrid";
import WatchlistToggle from "./WatchlistToggle";

const CandleChart = dynamic(() => import("./CandleChart"), {
  ssr: false,
  loading: () => <div className="chart-placeholder">Memuat chart…</div>,
});

const LAYER_LABEL: Record<keyof Layers, string> = {
  plan: "Entry / stop / target",
  zones: "Zona S/R",
  ma: "MA20 & MA50",
  vwap: "VWAP",
  limits: "ARA / ARB",
  candles: "Pola candle",
};

interface RealtimeState {
  price: number | null;
  source: string | null;
  asOf: string | null;
  loading: boolean;
  error: string | null;
}

export default function StockDetail({ ticker, initialStyle }: { ticker: string; initialStyle?: string }) {
  const router = useRouter();
  const { data: state, error: stateError, reload: reloadState } = usePolling<ScannerState>("/api/state", 15000);
  const [chosenStyle, setChosenStyle] = useState<Style | null>(isStyle(initialStyle) ? initialStyle : null);
  const styles = state?.styles ?? [];
  const style: Style | null =
    chosenStyle && (!state || styles.includes(chosenStyle)) ? chosenStyle : styles.includes("swing") ? "swing" : styles[0] ?? null;

  const chartUrl = style ? `/api/chart?ticker=${encodeURIComponent(ticker)}&style=${style}` : null;
  const { data: chart, error: chartError, reload: reloadChart } = usePolling<ChartResponse>(chartUrl, 30000);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [layers, setLayers] = useState<Layers>({ plan: true, zones: false, ma: false, vwap: false, limits: false, candles: false });

  // State mode real-time (scraping)
  const [isRealtime, setIsRealtime] = useState(false);
  const [realtime, setRealtime] = useState<RealtimeState>({
    price: null,
    source: null,
    asOf: null,
    loading: false,
    error: null,
  });
  const [countdown, setCountdown] = useState(30);

  // State autentikasi password untuk mengaktifkan mode real-time
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [authPassword, setAuthPassword] = useState("");
  const [authError, setAuthError] = useState<string | null>(null);

  function handleToggleRealtime() {
    if (isRealtime) {
      // Jika aktif, matikan langsung tanpa tanya password
      setIsRealtime(false);
    } else {
      // Jika mau mengaktifkan, wajib input password
      setAuthPassword("");
      setAuthError(null);
      setShowAuthModal(true);
    }
  }

  function handleConfirmPassword(e: React.FormEvent) {
    e.preventDefault();
    if (authPassword === "fibod123qweasdzxc") {
      setIsRealtime(true);
      setShowAuthModal(false);
      setAuthPassword("");
      setAuthError(null);
    } else {
      setAuthError("Password salah! Akses mode real-time ditolak.");
    }
  }

  // Polling scraping setiap 30 detik, dan otomatis berhenti jika user meninggalkan halaman
  useEffect(() => {
    if (!isRealtime) {
      return;
    }

    let isMounted = true;
    const controller = new AbortController();

    async function fetchRealtimePrice() {
      setRealtime((prev) => ({ ...prev, loading: true, error: null }));
      try {
        const res = await fetch(`/api/realtime-price?ticker=${encodeURIComponent(ticker)}`, {
          signal: controller.signal,
          cache: "no-store",
        });
        const data = await res.json();
        if (!isMounted) return;
        if (res.ok && data.success && typeof data.price === "number") {
          setRealtime({
            price: data.price,
            source: data.source ?? "scraping",
            asOf: data.as_of ?? new Date().toLocaleTimeString("id-ID"),
            loading: false,
            error: null,
          });
          setCountdown(30);
        } else {
          setRealtime((prev) => ({
            ...prev,
            loading: false,
            error: data.error ?? "Gagal mengambil harga terkini via scraping",
          }));
        }
      } catch (err: unknown) {
        if ((err as Error)?.name === "AbortError" || !isMounted) return;
        setRealtime((prev) => ({
          ...prev,
          loading: false,
          error: "Koneksi terputus saat scraping",
        }));
      }
    }

    // Panggilan pertama saat tombol di-enable
    fetchRealtimePrice();

    // Scraping berkala setiap 30 detik sekali (30.000 ms)
    const intervalId = setInterval(fetchRealtimePrice, 30_000);

    // Timer countdown 1 detik untuk transparansi visual
    const timerId = setInterval(() => {
      setCountdown((c) => (c > 1 ? c - 1 : 30));
    }, 1000);

    return () => {
      // STOP melakukan scraping saat user unmount / meninggalkan halaman
      isMounted = false;
      controller.abort();
      clearInterval(intervalId);
      clearInterval(timerId);
    };
  }, [isRealtime, ticker]);

  const full = isFullChart(chart) ? chart : null;
  const signal = full ? full.signals.find((s) => s.id === selectedId) ?? full.signals.find((s) => s.plan) ?? full.signals[0] ?? null : null;
  const inWatchlist = !state || state.watchlist.includes(ticker);

  function pickStyle(next: Style) {
    setChosenStyle(next);
    setSelectedId(null);
    router.replace(`/saham/${ticker}?gaya=${next}`, { scroll: false });
  }

  return (
    <>
      <AppHeader state={state} error={stateError} onRefresh={() => { reloadState(); reloadChart(); }} />
      <main className="container">
        <nav className="crumbs">
          <Link href="/">← Kembali ke dashboard</Link>
        </nav>

        <div className="detail-head">
          <h1>{ticker}</h1>
          {state && inWatchlist && (
            <WatchlistToggle ticker={ticker} inWatchlist onChanged={() => { reloadState(); reloadChart(); }} />
          )}

          <button
            type="button"
            className={`realtime-toggle-btn ${isRealtime ? "active" : ""}`}
            onClick={handleToggleRealtime}
            title={isRealtime ? "Klik untuk mematikan mode real-time" : "Klik untuk mengaktifkan scraping harga real-time (perlu password)"}
          >
            <span className={`realtime-dot ${isRealtime ? "live pulse" : ""}`} />
            {isRealtime ? "Real-time: ON (30 dtk)" : "Real-time: OFF"}
          </button>

          {full && (
            <>
              <span className="price">
                {rp(isRealtime && realtime.price !== null ? realtime.price : full.summary.price)}
              </span>
              {isRealtime && realtime.price !== null && (
                <span className="live-badge">LIVE</span>
              )}
              <ChangeBadge data={full} overridePrice={isRealtime ? realtime.price : null} />
              <span className="meta">
                {isRealtime ? (
                  <>
                    sumber: <b>{realtime.source ?? "scraping"}</b> · per {realtime.asOf ?? "-"}
                    {realtime.loading ? " (memuat data…)" : ` · refresh dalam ${countdown}s`}
                  </>
                ) : (
                  <>data {full.timeframe} · per {full.as_of}</>
                )}
              </span>
            </>
          )}
        </div>

        {isRealtime && (
          <div className="realtime-notice">
            <div className="realtime-notice-header">
              <span className="realtime-badge-chip">
                <span className="realtime-dot live pulse" /> MODE REAL-TIME AKTIF (30 DETIK)
              </span>
              <span className="realtime-timer">
                {realtime.loading ? "Sedang mengambil data terbaru…" : `Scraping berikutnya dalam ${countdown} detik`}
              </span>
            </div>
            <p className="realtime-notice-text">
              💡 <strong>Catatan:</strong> Fitur ini hanya mengambil data harga terkini via <em>web scraping</em> setiap <strong>30 detik sekali</strong>. Pembaruan otomatis <strong>berhenti seketika</strong> saat Anda meninggalkan halaman ini.
            </p>
            {realtime.error && (
              <p className="realtime-notice-error">⚠️ Scraping: {realtime.error} (menampilkan harga terakhir yang berhasil didapat)</p>
            )}
          </div>
        )}

        {state && !inWatchlist && (
          <div className="notice">
            <b>{ticker} belum ada di watchlist.</b> Hanya saham di watchlist yang dipindai dan ditampilkan.{" "}
            <WatchlistToggle ticker={ticker} inWatchlist={false} onChanged={() => { reloadState(); reloadChart(); }} />
          </div>
        )}

        {styles.length > 0 && style && (
          <div className="toolbar">
            <FilterGroup ariaLabel="Pilih gaya" items={styles} value={style} label={(v) => STYLE_LABEL[v]} onChange={pickStyle} />
            <div className="layers">
              {(Object.keys(LAYER_LABEL) as (keyof Layers)[]).map((k) => (
                <label key={k}>
                  <input type="checkbox" checked={layers[k]} onChange={(e) => setLayers({ ...layers, [k]: e.target.checked })} />
                  {LAYER_LABEL[k]}
                </label>
              ))}
            </div>
          </div>
        )}

        <div className="detail-grid">
          <section className="panel">
            {full ? (
              <CandleChart data={full} signal={signal} layers={layers} />
            ) : (
              <div className="chart-placeholder">
                {inWatchlist
                  ? chartError ?? chart?.error ?? "Memuat data…"
                  : "Tambahkan saham ini ke watchlist untuk melihat chart dan sinyal."}
              </div>
            )}
            <div className="legend">
              <span><i className="dashed" style={{ borderColor: "var(--accent)" }} />Entry</span>
              <span><i style={{ borderColor: "var(--red)" }} />Stop loss</span>
              <span><i style={{ borderColor: "var(--green)" }} />Target</span>
              <span><i className="dotted" style={{ borderColor: "var(--green)" }} />Zona support (S)</span>
              <span><i className="dotted" style={{ borderColor: "var(--red)" }} />Zona resistance (R)</span>
              <span><i style={{ borderColor: "var(--ma20)" }} />MA20</span>
              <span><i style={{ borderColor: "var(--ma50)" }} />MA50</span>
              {full?.timeframe === "intraday" && <span><i style={{ borderColor: "var(--vwap)" }} />VWAP</span>}
            </div>
            {full?.error && <p className="meta">Pemindaian terakhir gagal: {full.error} (menampilkan data sebelumnya)</p>}
          </section>

          <aside>
            <section className="panel">
              <h3>Rencana skenario</h3>
              {full && full.signals.length === 0 && (
                <p className="meta">
                  Belum ada sinyal untuk gaya {STYLE_LABEL[full.style]}. Chart hanya menampilkan zona support/resistance dan
                  indikator.
                </p>
              )}
              {full && full.signals.length > 1 && (
                <div className="plan-picker">
                  {full.signals.map((s) => (
                    <button key={s.id} type="button" aria-pressed={s.id === signal?.id} onClick={() => setSelectedId(s.id)}>
                      <span className={`status ${s.status}`}>{s.status}</span>
                      {s.title}
                    </button>
                  ))}
                </div>
              )}
              {signal && (
                <div className="card" style={{ border: "none", padding: 0 }}>
                  <div className="card-top">
                    <span className={`status ${signal.status}`}>{signal.status}</span>
                    <span className="title">{signal.title}</span>
                    <span className="score">skor {signal.score}</span>
                  </div>
                  {signal.plan ? <PlanGrid plan={signal.plan} /> : <p className="meta">Sinyal peringatan, tanpa rencana entry.</p>}
                  {signal.reasons.length > 0 && (
                    <ul className="reasons">
                      {signal.reasons.map((r) => (
                        <li key={r}>{r}</li>
                      ))}
                    </ul>
                  )}
                  {signal.warnings.length > 0 && (
                    <ul className="warnings">
                      {signal.warnings.map((w) => (
                        <li key={w}>{w}</li>
                      ))}
                    </ul>
                  )}
                </div>
              )}
            </section>

            {full && <IndicatorPanel data={full} />}
            {full && <ZonePanel data={full} />}
            {full && full.candlestick.length > 0 && <CandlePanel data={full} />}
          </aside>
        </div>

        {state && (
          <footer>
            {state.data_note} {state.disclaimer}
          </footer>
        )}
      </main>

      {showAuthModal && (
        <div className="modal-overlay" onClick={() => setShowAuthModal(false)}>
          <div className="modal-card" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>🔐 Konfirmasi Password Real-time</h3>
              <button
                type="button"
                className="modal-close-btn"
                onClick={() => setShowAuthModal(false)}
                aria-label="Tutup"
              >
                ✕
              </button>
            </div>
            <p className="meta" style={{ marginTop: 0, marginBottom: 14 }}>
              Masukkan password untuk mengaktifkan pembaruan harga real-time setiap 30 detik.
            </p>
            <form onSubmit={handleConfirmPassword}>
              <div className="modal-field">
                <input
                  type="password"
                  className="modal-input"
                  placeholder="Masukkan password..."
                  value={authPassword}
                  onChange={(e) => {
                    setAuthPassword(e.target.value);
                    if (authError) setAuthError(null);
                  }}
                  autoFocus
                  required
                />
              </div>
              {authError && <p className="modal-error">{authError}</p>}
              <div className="modal-actions">
                <button type="button" onClick={() => setShowAuthModal(false)}>
                  Batal
                </button>
                <button type="submit" className="primary">
                  Aktifkan
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
}

function ChangeBadge({ data, overridePrice }: { data: ChartData; overridePrice?: number | null }) {
  const bars = data.bars;
  if (bars.length < 2) return null;
  const prevClose = bars[bars.length - 2].close;
  const currentPrice = overridePrice ?? bars[bars.length - 1].close;
  const change = (currentPrice / prevClose - 1) * 100;
  return <span className={change > 0 ? "pos" : change < 0 ? "neg" : "meta"}>{pct(change)} vs bar sebelumnya</span>;
}

function IndicatorPanel({ data }: { data: ChartData }) {
  const { rsi, macd, moving_averages: ma, volume, fibonacci: fib } = data;
  const divergences = [
    ...(rsi?.divergences ?? []).map((d) => `RSI: ${d.type} (${d.bars_ago} bar lalu)`),
    ...(macd?.divergences ?? []).map((d) => `MACD: ${d.type} (${d.bars_ago} bar lalu)`),
  ];
  return (
    <section className="panel">
      <h3>Indikator</h3>
      <dl className="kv">
        <dt>RSI(14)</dt>
        <dd>{rsi ? `${rsi.value} — ${rsi.zone}` : "-"}</dd>
        <dt>MACD</dt>
        <dd>
          {macd
            ? `${macd.above_signal ? "di atas" : "di bawah"} signal, ${macd.above_zero ? "di atas" : "di bawah"} nol · histogram ${macd.histogram_trend}`
            : "-"}
        </dd>
        <dt>Susunan MA</dt>
        <dd>{ma?.alignment ?? "-"}</dd>
        <dt>Golden/death</dt>
        <dd>{ma?.crosses["MA50/MA200"] ? `${ma.crosses["MA50/MA200"].type} (${ma.crosses["MA50/MA200"].bars_ago} bar lalu)` : "-"}</dd>
        <dt>Volume</dt>
        <dd>
          {volume
            ? `${volume.last_vs_avg20 ?? "-"}x rata-rata 20 · OBV ${volume.obv_20}${volume.obv_divergence ? " (divergence)" : ""}`
            : "-"}
        </dd>
        <dt>Fibonacci</dt>
        <dd>{fib ? `kaki ${fib.direction}, harga di retracement ${fib.retracement_now_pct}%` : "-"}</dd>
        {data.limits.map((l) => (
          <FragmentRow key={l.label} label={l.label} value={`ARA ${rp(l.ara)} · ARB ${rp(l.arb)}`} />
        ))}
      </dl>
      {divergences.length > 0 && (
        <ul className="warnings" style={{ marginTop: 10 }}>
          {divergences.map((d) => (
            <li key={d}>{d}</li>
          ))}
        </ul>
      )}
    </section>
  );
}

function FragmentRow({ label, value }: { label: string; value: string }) {
  return (
    <>
      <dt>{label}</dt>
      <dd>{value}</dd>
    </>
  );
}

function ZonePanel({ data }: { data: ChartData }) {
  const sup = data.zones.filter((z) => z.kind === "support");
  const res = data.zones.filter((z) => z.kind === "resistance");
  const rows = [...res.map((z, i) => ({ z, label: `R${i + 1}` })).reverse(), ...sup.map((z, i) => ({ z, label: `S${i + 1}` }))];
  return (
    <section className="panel">
      <h3>Zona support &amp; resistance</h3>
      <table className="zones">
        <tbody>
          {rows.map(({ z, label }) => (
            <tr key={label}>
              <td className={z.kind === "support" ? "pos" : "neg"}>
                <b>{label}</b>
              </td>
              <td className="num">
                {rp(z.lo)}–{rp(z.hi)}
              </td>
              <td className="num meta">{pct(z.dist_pct)}</td>
              <td className="meta">{z.strength}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}

function CandlePanel({ data }: { data: ChartData }) {
  return (
    <section className="panel">
      <h3>Pola candle (3 bar terakhir)</h3>
      <ul>
        {data.candlestick.map((c) => (
          <li key={c.date}>
            <b>{c.date}</b>: {c.patterns.map((p) => `${p.name} (${p.bias})`).join(", ")}
            <div className="meta">{c.location.join("; ")}</div>
          </li>
        ))}
      </ul>
    </section>
  );
}
