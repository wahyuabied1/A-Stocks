import Link from "next/link";
import { STYLE_LABEL, rp } from "@/lib/format";
import type { Signal } from "@/lib/types";
import PlanGrid from "./PlanGrid";

export default function SignalCard({ signal: s }: { signal: Signal }) {
  const href = `/saham/${s.ticker}?gaya=${s.style}`;
  return (
    <article className="card">
      <div className="card-top">
        <Link href={href} className="ticker">{s.ticker}</Link>
        <span className="pill">{STYLE_LABEL[s.style]}</span>
        <span className={`status ${s.status}`}>{s.status}</span>
        <span className="score">skor {s.score}</span>
      </div>
      <div className="title">{s.title}</div>
      <div className="meta">
        Harga {rp(s.price)} · data {s.as_of}
      </div>
      {s.plan && <PlanGrid plan={s.plan} />}
      {s.reasons.length > 0 && (
        <ul className="reasons">
          {s.reasons.map((r) => (
            <li key={r}>{r}</li>
          ))}
        </ul>
      )}
      {s.warnings.length > 0 && (
        <ul className="warnings">
          {s.warnings.map((w) => (
            <li key={w}>{w}</li>
          ))}
        </ul>
      )}
      <Link href={href} className="chart-link">Lihat chart candlestick &amp; rencana →</Link>
    </article>
  );
}
