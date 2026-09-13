import { rp } from "@/lib/format";
import type { Plan } from "@/lib/types";

export default function PlanGrid({ plan }: { plan: Plan }) {
  return (
    <>
      <div className="plan">
        <div>
          <span>Entry</span>
          <b>{plan.entry[0] === plan.entry[1] ? rp(plan.entry[0]) : `${rp(plan.entry[0])}–${rp(plan.entry[1])}`}</b>
        </div>
        <div>
          <span>Stop loss</span>
          <b className="neg">{rp(plan.stop)}</b>
        </div>
        <div>
          <span>Target</span>
          <b className="pos">{plan.targets.map((t) => rp(t)).join(" / ") || "-"}</b>
        </div>
        <div>
          <span>R:R (setelah biaya)</span>
          <b>{plan.rr ?? "-"}</b>
        </div>
        <div>
          <span>Risiko / potensi</span>
          <b>
            −{plan.risk_pct}% / {plan.reward_pct == null ? "-" : `+${plan.reward_pct}%`}
          </b>
        </div>
        <div>
          <span>Lot (batas risikomu)</span>
          <b>{plan.lots ?? "-"}</b>
        </div>
      </div>
      {plan.notes.length > 0 && (
        <div className="notes">
          {plan.notes.map((n) => (
            <div key={n}>{n}</div>
          ))}
        </div>
      )}
    </>
  );
}
