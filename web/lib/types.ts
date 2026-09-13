// Bentuk data dari API Python (scanner/engine.py & sr_levels.py).

export type Style = "scalper" | "bpjs" | "bsjp" | "swing";
export type Status = "SETUP" | "WASPADA" | "PANTAU";

export interface Plan {
  entry: [number, number];
  stop: number;
  targets: number[];
  rr: number | null;
  risk_pct: number;
  reward_pct: number | null;
  lots: number | null;
  risk_rp: number | null;
  notes: string[];
}

export interface Signal {
  id: string;
  ticker: string;
  style: Style;
  kind: string;
  title: string;
  status: Status;
  score: number;
  price: number;
  as_of: string;
  timeframe: string;
  reasons: string[];
  warnings: string[];
  plan: Plan | null;
}

export interface Limits {
  ara: number;
  arb: number;
  ara_pct: number | null;
  arb_pct: number | null;
  label: string;
  acuan: string;
}

export interface ZoneSummary {
  zone: [number, number];
  strength: string;
  dist_pct: number;
}

export interface Summary {
  price: number;
  as_of: string;
  timeframe: string;
  support: ZoneSummary | null;
  resistance: ZoneSummary | null;
  rsi: number | null;
  macd: string | null;
  ma_alignment: string | null;
  volume_ratio: number | null;
  candles: string[];
  limits: Limits;
  warnings: string[];
}

export interface Market {
  date: string;
  time: string;
  weekday: number;
  trading: boolean;
  bsjp_window: boolean;
  phase: string;
  label: string;
}

export interface ScannerState {
  generated_at: string;
  market: Market;
  data_source: string;
  data_note: string;
  disclaimer: string;
  styles: Style[];
  watchlist: string[];
  max_watchlist: number;
  signals: Signal[];
  summaries: Partial<Record<Style, Record<string, Summary>>>;
  errors: Partial<Record<Style, Record<string, string>>>;
  last_scan: Partial<Record<Style, string>>;
  telegram: { enabled: boolean; error: string | null };
}

export interface Bar {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface LinePoint {
  time: string;
  value: number;
}

export interface Zone {
  kind: "support" | "resistance";
  lo: number;
  hi: number;
  mid: number;
  strength: string;
  touches: number;
  dist_pct: number;
  confluence: string[];
}

export interface Divergence {
  type: string;
  from: string;
  to: string;
  bars_ago: number;
}

export interface Cross {
  type: string;
  date: string;
  bars_ago: number;
}

export interface CandleInfo {
  date: string;
  patterns: { name: string; bias: string }[];
  prior_trend_5: string;
  location: string[];
  volume_vs_avg20: number | null;
  bars_ago: number;
}

export interface ChartData {
  ticker: string;
  style: Style;
  timeframe: string;
  as_of: string;
  tick_size: number;
  bars: Bar[];
  lines: Record<string, LinePoint[]>;
  zones: Zone[];
  limits: Limits[];
  fibonacci: {
    direction: string;
    anchor_low: { date: string; price: number };
    anchor_high: { date: string; price: number };
    retracement: Record<string, number>;
    extension: Record<string, number>;
    retracement_now_pct: number;
  } | null;
  rsi: { period: number; value: number; zone: string; value_5_bars_ago: number | null; divergences: Divergence[] } | null;
  macd: {
    setting: string;
    macd: number;
    signal: number;
    histogram: number;
    macd_pct_of_price: number;
    above_signal: boolean;
    above_zero: boolean;
    histogram_trend: string;
    last_signal_cross: Cross | null;
    last_zero_cross: Cross | null;
    divergences: Divergence[];
  } | null;
  moving_averages: {
    levels: Record<string, { value: number; dist_pct: number; slope_5: string | null }>;
    alignment: string;
    crosses: Record<string, Cross | null>;
  } | null;
  volume: {
    avg_volume_20: number;
    avg_volume_50: number;
    last_vs_avg20: number | null;
    ratio_20_vs_50: number | null;
    up_down_volume_ratio_20: number | null;
    obv_20: string;
    price_20: string;
    obv_divergence: boolean;
    spikes_20: { date: string; ratio: number; change_pct: number }[];
  } | null;
  candlestick: CandleInfo[];
  summary: Summary;
  signals: Signal[];
  error: string | null;
}

export interface SearchResult {
  ticker: string;
  name: string;
  type: string;
  in_watchlist: boolean;
}

export interface WatchlistUpdate {
  watchlist: string[];
  added: string[];
  removed: string[];
  rejected: Record<string, string>;
}

/** Respons /api/chart bisa berupa data lengkap atau hanya pesan error (belum dipindai / gagal). */
export type ChartResponse = ChartData | { ticker: string; style: Style; bars: []; error: string };

export function isFullChart(c: ChartResponse | null): c is ChartData {
  return !!c && c.bars.length > 0 && "summary" in c;
}
