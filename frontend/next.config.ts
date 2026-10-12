import type { NextConfig } from "next";

// The Python engine binds to loopback only; the browser talks to it through this same origin.
const ENGINE_URL = process.env.TAXCOPILOT_ENGINE_URL ?? "http://127.0.0.1:8000";

const nextConfig: NextConfig = {
  cacheComponents: true,
  partialPrefetching: true,
  poweredByHeader: false,
  devIndicators: false,
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
  async rewrites() {
    return [{ source: "/api/:path*", destination: `${ENGINE_URL}/api/:path*` }];
  },
};

export default nextConfig;
