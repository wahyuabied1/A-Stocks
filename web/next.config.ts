import path from "node:path";
import type { NextConfig } from "next";

// Semua request /api/* diteruskan ke API Python (python -m scanner).
const SCANNER_API = process.env.SCANNER_API ?? "http://127.0.0.1:8765";

const nextConfig: NextConfig = {
  // Root eksplisit agar Turbopack tidak memakai package-lock.json lain di folder induk.
  turbopack: { root: path.resolve(__dirname) },
  async rewrites() {
    return [{ source: "/api/:path*", destination: `${SCANNER_API}/api/:path*` }];
  },
};

export default nextConfig;
