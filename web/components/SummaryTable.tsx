import Link from "next/link";
import { pct, rp } from "@/lib/format";
import type { ScannerState, Style, ZoneSummary } from "@/lib/types";

function ZoneCell({ zone }: { zone: ZoneSummary | null }) {
  if (!zone) return <>-</>;
  return (
    <>
      {rp(zone.zone[0])}–{rp(zone.zone[1])}{" "}
      <span className="meta">
        ({pct(zone.dist_pct)}, {zone.strength})
      </span>
    </>
  );
}

export default function SummaryTable({ state, style }: { state: ScannerState; style: Style }) {
  const rows = state.summaries[style] ?? {};
  const tickers = state.watchlist.filter((t) => rows[t]);

  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Kode</th>
            <th>Harga</th>
            <th>Data</th>
            <th>Support terdekat</th>
            <th>Resistance terdekat</th>
            <th>RSI</th>
            <th>MACD</th>
            <th>Susunan MA</th>
            <th>Vol</th>
            <th>Candle</th>
            <th>ARA / ARB</th>
          </tr>
        </thead>
        <tbody>
          {tickers.length === 0 && (
            <tr>
              <td colSpan={11} className="meta">Belum ada data untuk gaya ini.</td>
            </tr>
          )}
          {tickers.map((t) => {
            const r = rows[t];
            return (
              <tr key={t}>
                <td>
                  <Link href={`/saham/${t}?gaya=${style}`}><b>{t}</b></Link>
                </td>
                <td className="num">{rp(r.price)}</td>
                <td className="meta">{r.as_of}</td>
                <td><ZoneCell zone={r.support} /></td>
                <td><ZoneCell zone={r.resistance} /></td>
                <td className={`num ${r.rsi == null ? "" : r.rsi > 70 ? "neg" : r.rsi < 30 ? "pos" : ""}`}>{r.rsi ?? "-"}</td>
                <td>{r.macd ?? "-"}</td>
                <td>{r.ma_alignment ?? "-"}</td>
                <td className="num">{r.volume_ratio == null ? "-" : `${r.volume_ratio}x`}</td>
                <td>{r.candles.join(", ") || "-"}</td>
                <td className="num">{rp(r.limits.ara)} / {rp(r.limits.arb)}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
