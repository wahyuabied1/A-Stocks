import type { Metadata } from "next";
import StockDetail from "@/components/StockDetail";

interface PageProps {
  params: Promise<{ ticker: string }>;
  searchParams: Promise<{ gaya?: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { ticker } = await params;
  return { title: `${ticker.toUpperCase()} · Pemindai Sinyal IDX` };
}

export default async function Page({ params, searchParams }: PageProps) {
  const { ticker } = await params;
  const { gaya } = await searchParams;
  return <StockDetail ticker={decodeURIComponent(ticker).toUpperCase()} initialStyle={gaya} />;
}
