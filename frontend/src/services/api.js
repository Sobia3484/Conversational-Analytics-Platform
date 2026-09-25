import axios from "axios";

const api = axios.create({
  baseURL: "/api",
  headers: { "Content-Type": "application/json" },
  timeout: 30000,
});

export async function askAnalytics(question) {
  const response = await api.post("/query", { question });
  return response.data;
}

// Phase 17 — single fast call for the whole Dashboard page, bypassing the
// AI entirely (no Groq calls, so it can't fail from AI-side issues and
// costs nothing to load).
export async function getDashboard({ startDate, endDate, recentLimit } = {}) {
  const params = {};
  if (startDate) params.start_date = startDate;
  if (endDate) params.end_date = endDate;
  if (recentLimit) params.recent_limit = recentLimit;
  const response = await api.get("/dashboard", { params });
  return response.data;
}