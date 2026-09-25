import { useEffect, useMemo, useState } from "react";
import ChatInput from "./components/ChatInput.jsx";
import ResultRenderer from "./components/ResultRenderer.jsx";
import { askAnalytics, getDashboard } from "./services/api.js";

function formatNumber(value) {
  return Number(value ?? 0).toLocaleString("en-US", { maximumFractionDigits: 0 });
}

function formatMoney(value) {
  return `$${Number(value ?? 0).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

function BrandMark() {
  return (
    <div className="brand-mark" aria-label="AnalyticsPro logo">
      <svg viewBox="0 0 48 48" role="img">
        <path d="M7 37V11h7v26H7Zm13 0V19h7v18h-7Zm13 0V6h7v31h-7Z" fill="currentColor" opacity=".95" />
        <path d="m9 22 9-8 8 4 12-11" fill="none" stroke="currentColor" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" />
        <circle cx="38" cy="7" r="3" fill="currentColor" />
      </svg>
    </div>
  );
}

function SidebarIcon({ type }) {
  const icons = {
    dashboard: "⌂",
    visual: "◔",
    history: "↶",
  };
  return <span className="sidebar-icon" aria-hidden="true">{icons[type]}</span>;
}

function DateRange({ value, customStart, customEnd, onChange, onCustom }) {
  const [open, setOpen] = useState(false);
  const label = value === "all"
    ? "All dates"
    : value === "custom"
      ? `${customStart || "Start"} – ${customEnd || "End"}`
      : `Jan 01, ${value} – Dec 31, ${value}`;

  return (
    <div className="date-picker-wrap">
      <button className="date-range" onClick={() => setOpen((v) => !v)} aria-expanded={open}>
        <span className="calendar-icon">□</span>
        <span>{label}</span>
        <span className="chevron">⌄</span>
      </button>
      {open && (
        <div className="date-popover">
          <strong>Select date range</strong>
          <button className={value === "all" ? "selected" : ""} onClick={() => { onChange("all"); setOpen(false); }}>All dates</button>
          {["2026", "2025", "2024", "2023"].map((year) => (
            <button key={year} className={value === year ? "selected" : ""} onClick={() => { onChange(year); setOpen(false); }}>{year}</button>
          ))}
          <div className="date-custom">
            <span>Custom range</span>
            <input type="date" value={customStart} onChange={(e) => onCustom(e.target.value, customEnd)} />
            <input type="date" value={customEnd} onChange={(e) => onCustom(customStart, e.target.value)} />
            <button className={value === "custom" ? "selected" : "apply-date"} onClick={() => { onChange("custom"); setOpen(false); }}>Apply</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default function App() {
  const [page, setPage] = useState("dashboard");
  const [dark, setDark] = useState(false);
  const [dateRange, setDateRange] = useState("all");
  const [customStart, setCustomStart] = useState("");
  const [customEnd, setCustomEnd] = useState("");
  const [dashboard, setDashboard] = useState({
    sales: null,
    profit: null,
    quantity: null,
    category: null,
    region: null,
    trend: null,
    products: null,
    correlation: null,
  });
  const [dashboardLoading, setDashboardLoading] = useState(false);
  const [messages, setMessages] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const resolvedDateRange = useMemo(() => {
    if (dateRange === "all") return {};
    if (dateRange === "custom") {
      if (!customStart || !customEnd) return {};
      return { startDate: customStart, endDate: customEnd };
    }
    return { startDate: `${dateRange}-01-01`, endDate: `${dateRange}-12-31` };
  }, [dateRange, customStart, customEnd]);

  const loadDashboard = async () => {
    setDashboardLoading(true);
    setError("");
    try {
      const d = await getDashboard(resolvedDateRange);
      setDashboard({
        sales: { data: { value: d.total_sales } },
        profit: { data: { value: d.total_profit } },
        quantity: { data: { value: d.total_quantity } },
        category: { data: d.category_breakdown },
        region: { data: d.region_breakdown },
        trend: { data: d.monthly_trend },
        products: { data: d.top_products },
        correlation: { data: d.correlation },
      });
    } catch (err) {
      console.error("Dashboard load failed:", err);
      setError(
        err?.response
          ? `Dashboard data could not be loaded (server error ${err.response.status}).`
          : "Dashboard data could not be loaded. Make sure the FastAPI backend is running on port 8000."
      );
    } finally {
      setDashboardLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, [dateRange, customStart, customEnd]);

  const sendQuestion = async (question) => {
    setPage("visual");
    setLoading(true);
    setError("");
    setMessages((prev) => [...prev, { id: crypto.randomUUID(), role: "user", text: question }]);
    try {
      const result = await askAnalytics(question);
      setMessages((prev) => [...prev, { id: crypto.randomUUID(), role: "assistant", result, text: result?.message || "" }]);
      setHistory((prev) => [
        {
          id: crypto.randomUUID(),
          question,
          time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        },
        ...prev,
      ].slice(0, 20));
    } catch {
      setError("I couldn't reach the analytics backend. Please check that FastAPI is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };

  const kpiMoney = (result) => dashboardLoading ? "…" : result?.data?.value == null ? "—" : formatMoney(result.data.value);
  const kpiQuantity = (result) => dashboardLoading ? "…" : result?.data?.value == null ? "—" : formatNumber(result.data.value);

  return (
    <div className={`app-shell ${dark ? "theme-dark" : ""}`}>
      <aside className="sidebar">
        <div className="brand">
          <BrandMark />
          <div><strong>AnalyticsPro</strong><span>Business Intelligence</span></div>
        </div>
        <nav className="sidebar__nav">
          <button className={page === "dashboard" ? "nav-item active" : "nav-item"} onClick={() => setPage("dashboard")}><SidebarIcon type="dashboard" />Dashboard</button>
          <button className={page === "visual" ? "nav-item active" : "nav-item"} onClick={() => setPage("visual")}><SidebarIcon type="visual" />Visualizations</button>
          <button className={page === "history" ? "nav-item active" : "nav-item"} onClick={() => setPage("history")}><SidebarIcon type="history" />History</button>
        </nav>
      </aside>

      <main className="main">
        <header className="topbar">
          <div className="topbar-spacer" />
          <div className="topbar-actions">
            <button className="theme-button" onClick={() => setDark((v) => !v)} aria-label="Toggle theme">{dark ? "☀" : "◐"}</button>
          </div>
        </header>

        <div className="page-frame">
          <section className="page-heading">
            <div>
              <h1>{page === "dashboard" ? "Dashboard" : page === "visual" ? "Visualizations" : "History"}</h1>
              <p>{page === "dashboard" ? "Overview of your business performance" : "Explore answers from your business data"}</p>
            </div>
            {page === "dashboard" && (
              <div className="heading-actions">
                <DateRange
                  value={dateRange}
                  customStart={customStart}
                  customEnd={customEnd}
                  onChange={setDateRange}
                  onCustom={(start, end) => { setCustomStart(start); setCustomEnd(end); }}
                />
              </div>
            )}
          </section>

          {error && <div className="alert">{error}</div>}

          {page === "dashboard" && (
            <div className="dashboard-main dashboard-main--full">
              <div className="kpi-grid">
                <div className="kpi-card">
                  <div><span>Total Sales</span><strong>{kpiMoney(dashboard.sales)}</strong><small>Based on selected period</small></div>
                  {/* <div className="kpi-icon sales">▣</div> */}
                </div>
                <div className="kpi-card">
                  <div><span>Total Profit</span><strong>{kpiMoney(dashboard.profit)}</strong><small>Based on selected period</small></div>
                  {/* <div className="kpi-icon profit">↗</div> */}
                </div>
                <div className="kpi-card">
                  <div><span>Total Quantity</span><strong className="quantity">{kpiQuantity(dashboard.quantity)}</strong><small>Quantity across sales records</small></div>
                  {/* <div className="kpi-icon quantity-icon">◇</div>/ */}
                </div>
              </div>

              <div className="chart-grid chart-grid--trend">
                <ResultRenderer result={{ response_type: "trend_data", data: dashboard.trend?.data }} />
              </div>

              <div className="chart-grid chart-grid--two">
                <ResultRenderer result={{ response_type: "category_data", data: dashboard.category?.data }} />
                <ResultRenderer result={{ response_type: "category_data", data: dashboard.region?.data }} />
              </div>

              <div className="chart-grid chart-grid--three">
                <ResultRenderer result={{ response_type: "category_share", data: dashboard.category?.data }} />
                <ResultRenderer result={{ response_type: "correlation_data", data: dashboard.correlation?.data }} />
                <ResultRenderer result={{ response_type: "product_data", data: dashboard.products?.data }} />
              </div>
            </div>
          )}

          {page === "visual" && (
            <div className="visual-page">
              <div className="visual-page__intro">
                <h2>Ask a Question</h2>
                <p>Ask about sales, profit, trends, customers, products, or regions. Results appear as charts, KPIs, or tables.</p>
              </div>
              {messages.map((message) => (
                <div key={message.id} className={`conversation-card ${message.role}`}>
                  {message.role === "user" ? <strong>You</strong> : <strong>Result</strong>}
                  {message.role === "user" ? <p>{message.text}</p> : <ResultRenderer result={message.result} />}
                </div>
              ))}
              <ChatInput onSend={sendQuestion} disabled={loading} />
            </div>
          )}

          {page === "history" && (
            <div className="history-page">
              <div className="visual-page__intro"><h2>Query History</h2><p>Your recent business questions.</p></div>
              {history.length
                ? history.map((item) => (
                    <button className="history-item" key={item.id} onClick={() => sendQuestion(item.question)}>
                      <span>{item.question}</span><small>{item.time}</small>
                    </button>
                  ))
                : <div className="empty-result">No questions asked yet.</div>}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
