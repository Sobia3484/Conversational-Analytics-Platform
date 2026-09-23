import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Phase 15/16 — Frontend build config.
// The dev server proxies /api/* to the FastAPI backend (Phase 9-14),
// so the frontend can call relative paths like "/api/query" without
// hardcoding a host — see src/services/api.js.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
