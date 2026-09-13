"use client";

import { useEffect, useRef, useState } from "react";
import {
  CandlestickSeries,
  ColorType,
  CrosshairMode,
  HistogramSeries,
  LineSeries,
  LineStyle,
  createChart,
  createSeriesMarkers,
  type AutoscaleInfo,
  type LineWidth,
  type LogicalRange,
  type SeriesMarker,
  type Time,
  type UTCTimestamp,
} from "lightweight-charts";
import type { ChartData, LinePoint, Signal } from "@/lib/types";

export interface Layers {
  plan: boolean;
  zones: boolean;
  ma: boolean;
  vwap: boolean;
  limits: boolean;
  candles: boolean;
}

interface Props {
  data: ChartData;
  signal: Signal | null;
  layers: Layers;
}

/** "YYYY-MM-DD" → business day; "YYYY-MM-DD HH:MM" (WIB) → timestamp yang ditampilkan apa adanya. */
function toTime(date: string): Time {
  if (date.length <= 10) return date as Time;
  const [d, t] = date.split(" ");
  const [y, m, day] = d.split("-").map(Number);
  const [hh, mm] = t.split(":").map(Number);
  return (Date.UTC(y, m - 1, day, hh, mm) / 1000) as UTCTimestamp;
}

function cssVar(name: string): string {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

export default function CandleChart({ data, signal, layers }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const viewRef = useRef<{ key: string; range: LogicalRange | null } | null>(null);
  const [themeVersion, setThemeVersion] = useState(0);

  useEffect(() => {
    const mq = window.matchMedia("(prefers-color-scheme: dark)");
    const onChange = () => setThemeVersion((v) => v + 1);
    mq.addEventListener("change", onChange);
    return () => mq.removeEventListener("change", onChange);
  }, []);

  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;

    const color = {
      bg: cssVar("--panel"),
      text: cssVar("--muted"),
      grid: cssVar("--line"),
      up: cssVar("--up"),
      down: cssVar("--down"),
      support: cssVar("--green"),
      resistance: cssVar("--red"),
      entry: cssVar("--accent"),
      stop: cssVar("--red"),
      target: cssVar("--green"),
      ma20: cssVar("--ma20"),
      ma50: cssVar("--ma50"),
      vwap: cssVar("--vwap"),
    };
    const intraday = data.timeframe === "intraday";
    const key = `${data.ticker}|${data.style}`;

    const chart = createChart(el, {
      autoSize: true,
      layout: { background: { type: ColorType.Solid, color: color.bg }, textColor: color.text },
      grid: { vertLines: { color: color.grid }, horzLines: { color: color.grid } },
      rightPriceScale: { borderColor: color.grid },
      timeScale: { borderColor: color.grid, timeVisible: intraday, secondsVisible: false, rightOffset: 8 },
      crosshair: { mode: CrosshairMode.Normal },
      localization: { priceFormatter: (p: number) => Math.round(p).toLocaleString("id-ID") },
    });

    // Candle + volume
    const candles = chart.addSeries(CandlestickSeries, {
      upColor: color.up,
      downColor: color.down,
      wickUpColor: color.up,
      wickDownColor: color.down,
      borderVisible: false,
      priceFormat: { type: "price", precision: 0, minMove: 1 },
    });
    candles.setData(data.bars.map((b) => ({ time: toTime(b.date), open: b.open, high: b.high, low: b.low, close: b.close })));
    candles.priceScale().applyOptions({ scaleMargins: { top: 0.08, bottom: 0.25 } });

    const volume = chart.addSeries(HistogramSeries, {
      priceFormat: { type: "volume" },
      priceScaleId: "volume",
      lastValueVisible: false,
      priceLineVisible: false,
    });
    volume.priceScale().applyOptions({ scaleMargins: { top: 0.8, bottom: 0 } });
    volume.setData(
      data.bars.map((b) => ({ time: toTime(b.date), value: b.volume, color: `${b.close >= b.open ? color.up : color.down}55` })),
    );

    // Garis MA / VWAP
    const addLine = (points: LinePoint[] | undefined, lineColor: string, title: string) => {
      if (!points?.length) return;
      const s = chart.addSeries(LineSeries, {
        color: lineColor,
        lineWidth: 1,
        title,
        priceLineVisible: false,
        lastValueVisible: false,
        crosshairMarkerVisible: false,
      });
      s.setData(points.map((p) => ({ time: toTime(p.time), value: p.value })));
    };
    if (layers.ma) {
      addLine(data.lines.MA20, color.ma20, "MA20");
      addLine(data.lines.MA50, color.ma50, "MA50");
    }
    if (layers.vwap) addLine(data.lines.VWAP, color.vwap, "VWAP");

    // Garis harga horizontal
    const priceLine = (price: number, lineColor: string, title: string, style: LineStyle, width: LineWidth, axisLabel = true) =>
      candles.createPriceLine({ price, color: lineColor, lineWidth: width, lineStyle: style, axisLabelVisible: axisLabel, title });

    if (layers.zones) {
      const supports = data.zones.filter((z) => z.kind === "support");
      const resistances = data.zones.filter((z) => z.kind === "resistance");
      supports.forEach((z, i) => {
        priceLine(z.hi, color.support, `S${i + 1}`, LineStyle.Dotted, 1);
        if (z.lo !== z.hi) priceLine(z.lo, color.support, "", LineStyle.Dotted, 1, false);
      });
      resistances.forEach((z, i) => {
        priceLine(z.lo, color.resistance, `R${i + 1}`, LineStyle.Dotted, 1);
        if (z.lo !== z.hi) priceLine(z.hi, color.resistance, "", LineStyle.Dotted, 1, false);
      });
    }
    if (layers.limits && data.limits[0]) {
      priceLine(data.limits[0].ara, color.text, "ARA", LineStyle.LargeDashed, 1);
      priceLine(data.limits[0].arb, color.text, "ARB", LineStyle.LargeDashed, 1);
    }

    const planPrices: number[] = [];
    const plan = layers.plan ? signal?.plan : null;
    if (plan) {
      priceLine(plan.entry[1], color.entry, "Entry", LineStyle.Dashed, 2);
      if (plan.entry[0] !== plan.entry[1]) priceLine(plan.entry[0], color.entry, "Entry", LineStyle.Dashed, 2);
      priceLine(plan.stop, color.stop, "Stop loss", LineStyle.Solid, 2);
      plan.targets.forEach((t, i) => priceLine(t, color.target, `Target ${i + 1}`, LineStyle.Solid, 2));
      planPrices.push(plan.entry[0], plan.entry[1], plan.stop, ...plan.targets);
    }
    // Pastikan entry/stop/target tetap terlihat walau di luar rentang harga yang tampil.
    if (planPrices.length) {
      candles.applyOptions({
        autoscaleInfoProvider: (original: () => AutoscaleInfo | null) => {
          const base = original();
          if (!base?.priceRange) return base;
          return {
            ...base,
            priceRange: {
              minValue: Math.min(base.priceRange.minValue, ...planPrices),
              maxValue: Math.max(base.priceRange.maxValue, ...planPrices),
            },
          };
        },
      });
    }

    // Penanda pola candle & sinyal
    if (layers.candles) {
      const markers: (SeriesMarker<Time> & { sortKey: string })[] = [];
      for (const info of data.candlestick) {
        const bull = info.patterns.some((p) => p.bias.startsWith("bullish"));
        const bear = info.patterns.some((p) => p.bias.startsWith("bearish"));
        const up = bull && !bear;
        const down = bear && !bull;
        markers.push({
          sortKey: info.date,
          time: toTime(info.date),
          position: down ? "aboveBar" : "belowBar",
          shape: up ? "arrowUp" : down ? "arrowDown" : "circle",
          color: up ? color.up : down ? color.down : color.text,
          text: info.patterns.slice(0, 2).map((p) => p.name).join(", "),
        });
      }
      markers.sort((a, b) => a.sortKey.localeCompare(b.sortKey));
      createSeriesMarkers(candles, markers.map(({ sortKey: _sortKey, ...m }) => m));
    }

    // Pertahankan zoom saat data diperbarui; default tampilkan ±120 bar terakhir.
    const saved = viewRef.current;
    if (saved && saved.key === key && saved.range) {
      chart.timeScale().setVisibleLogicalRange(saved.range);
    } else {
      const n = data.bars.length;
      chart.timeScale().setVisibleLogicalRange({ from: Math.max(0, n - 120), to: n + 8 });
    }

    return () => {
      viewRef.current = { key, range: chart.timeScale().getVisibleLogicalRange() };
      chart.remove();
    };
  }, [data, signal, layers, themeVersion]);

  return <div ref={containerRef} className="chart-box" />;
}
