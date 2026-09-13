import type { Style } from "./types";

export const STYLES: Style[] = ["scalper", "bpjs", "bsjp", "swing"];

export const STYLE_LABEL: Record<Style, string> = {
  scalper: "Scalper",
  bpjs: "BPJS",
  bsjp: "BSJP",
  swing: "Swing",
};

export function isStyle(value: unknown): value is Style {
  return typeof value === "string" && (STYLES as string[]).includes(value);
}

export function rp(value?: number | null): string {
  return value == null ? "-" : "Rp" + Math.round(value).toLocaleString("id-ID");
}

export function pct(value?: number | null): string {
  return value == null ? "-" : `${value > 0 ? "+" : ""}${value.toFixed(2)}%`;
}
