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