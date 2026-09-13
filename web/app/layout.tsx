import type { Metadata } from "next";
import type { ReactNode } from "react";
import "./globals.css";

export const metadata: Metadata = {
  title: "Pemindai Sinyal IDX",
  description: "Sinyal teknikal saham IDX dengan chart candlestick, entry, stop loss, dan target (edukasi, tanpa eksekusi order).",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="id">
      <body>{children}</body>
    </html>
  );
}
