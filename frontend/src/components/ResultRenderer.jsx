import {
  BarChart, Bar, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer,
  LineChart, Line, ScatterChart, Scatter, ZAxis, PieChart, Pie, Cell, Legend,
} from "recharts";

const PIE_COLORS = ["#2F6BFF", "#6E45D8", "#F59E0B", "#16A085", "#E85D75"];

function money(value) {
  const number = Number(value ?? 0);
  return `$${number.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

function compactMoney(value) {
  const number = Number(value ?? 0);
  if (Math.abs(number) >= 1_000_000) return `$${(number / 1_000_000).toFixed(1)}M`;
  if (Math.abs(number) >= 1_000) return `$${(number / 1_000).toFixed(0)}K`;
  return money(number);
}

function normalizeRows(data) {
  if (Array.isArray(data)) return data;
  if (data && typeof data === "object") {
    return Object.entries(data).map(([group_label, value]) => ({ group_label, value }));
  }
  return [];
}

function ResultShell({ title, subtitle, children, className = "" }) {
  return (
    <section className={`result-card ${className}`}>
      <div className="result-card__head">
        <div>
          <h3>{title}</h3>
          {subtitle && <p>{subtitle}</p>}
        </div>
      </div>
      {children}
    </section>
  );
}

function MoneyTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="chart-tooltip">
      <strong>{label}</strong>
      <span>{compactMoney(payload[0].value)}</span>
    </div>
  );
}

export function BarResult({ result, title = "Sales by category", subtitle = "Contribution by group" }) {
  const rows = normalizeRows(result?.data);
  return (
    <ResultShell title={title} subtitle={subtitle}>
      <div className="chart-wrap">
        <ResponsiveContainer width="100%" height={235}>
          <BarChart data={rows} margin={{ top: 10, right: 12, left: 0, bottom: 8 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="group_label" interval={0} tickLine={false} axisLine={false} tickMargin={8} tick={{ fontSize: 10 }} />
            <YAxis tickLine={false} axisLine={false} tickFormatter={compactMoney} />
            <Tooltip content={<MoneyTooltip />} />
            <Bar dataKey="value" fill="#2F6BFF" radius={[7, 7, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </ResultShell>
  );
}

export function TrendResult({ result }) {
  const rows = normalizeRows(result?.data);
  return (
    <ResultShell title="Sales over time" subtitle="Monthly business trend">
      <div className="chart-wrap">
        <ResponsiveContainer width="100%" height={235}>
          <LineChart data={rows} margin={{ top: 10, right: 12, left: 0, bottom: 8 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="group_label" tickLine={false} axisLine={false} />
            <YAxis tickLine={false} axisLine={false} tickFormatter={compactMoney} />
            <Tooltip content={<MoneyTooltip />} />
            <Line type="monotone" dataKey="value" stroke="#2F6BFF" strokeWidth={3} dot={false} activeDot={{ r: 5 }} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </ResultShell>
  );
}

export function CorrelationResult({ result }) {
  const rows = Array.isArray(result?.data) ? result.data : [];
  const points = rows.map((row) => ({ x: Number(row.x ?? row.sales ?? 0), y: Number(row.y ?? row.profit ?? 0) }));
  return (
    <ResultShell title="Sales vs profit" subtitle="Relationship between the two metrics">
      <div className="chart-wrap">
        <ResponsiveContainer width="100%" height={235}>
          <ScatterChart margin={{ top: 10, right: 18, left: 0, bottom: 8 }}>
            <CartesianGrid />
            <XAxis type="number" dataKey="x" name="Sales" tickLine={false} />
            <YAxis type="number" dataKey="y" name="Profit" tickLine={false} />
            <ZAxis range={[35, 35]} />
            <Tooltip cursor={{ strokeDasharray: "3 3" }} />
            <Scatter data={points} fill="#6E45D8" />
          </ScatterChart>
        </ResponsiveContainer>
      </div>
    </ResultShell>
  );
}

export function PieResult({ result }) {
  const rows = normalizeRows(result?.data);
  return (
    <ResultShell title="Sales by category (share)" subtitle="Category contribution">
      <div className="chart-wrap chart-wrap--small">
        <ResponsiveContainer width="100%" height={235}>
          <PieChart>
            <Pie data={rows} dataKey="value" nameKey="group_label" innerRadius={58} outerRadius={82} paddingAngle={3}>
              {rows.map((_, index) => <Cell key={index} fill={PIE_COLORS[index % PIE_COLORS.length]} />)}
            </Pie>
            <Tooltip formatter={(value) => money(value)} />
            <Legend iconType="circle" />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </ResultShell>
  );
}

export function ProductResult({ result }) {
  const rows = normalizeRows(result?.data).slice(0, 5);
  return (
    <ResultShell title="Top products by sales" subtitle="Highest-selling products">
      <div className="product-list">
        {rows.map((row, index) => (
          <div className="product-row" key={`${row.group_label}-${index}`}>
            <div className="product-rank">{index + 1}</div>
            <div className="product-main">
              <strong title={row.group_label}>{row.group_label}</strong>
              <div className="product-bar"><span style={{ width: `${Math.max(10, Math.min(100, (Number(row.value) / Math.max(1, Number(rows[0]?.value))) * 100))}%` }} /></div>
            </div>
            <b>{money(row.value)}</b>
          </div>
        ))}
      </div>
    </ResultShell>
  );
}

export default function ResultRenderer({ result }) {
  if (!result) return null;
  const type = result.response_type;
  const data = result.data;

  if (type === "aggregate_data") {
    const value = typeof data === "object" ? data?.value : data;
    return (
      <div className="result-grid result-grid--kpi">
        <div className="kpi-card kpi-card--featured">
          <span className="kpi-card__label">Analytics result</span>
          <strong>{typeof value === "number" ? value.toLocaleString() : value ?? "—"}</strong>
          <span className="kpi-card__hint">{result.message || "Calculated from business data"}</span>
        </div>
      </div>
    );
  }

  if (type === "category_data") return <BarResult result={result} />;
  if (type === "trend_data") return <TrendResult result={result} />;
  if (type === "correlation_data") return <CorrelationResult result={result} />;
  if (type === "category_share") return <PieResult result={result} />;
  if (type === "product_data") return <ProductResult result={result} />;

  if (type === "list_query") {
    const rows = Array.isArray(data) ? data : [];
    if (!rows.length) {
      return <ResultShell title="Orders" subtitle="No matching records"><div className="empty-result">No data found for the requested criteria.</div></ResultShell>;
    }
    const columns = ["order_id", "order_date", "product", "category", "city", "sales", "profit"];
    return (
      <ResultShell title="Order details" subtitle={`${rows.length} record${rows.length === 1 ? "" : "s"}`}>
        <div className="table-scroll">
          <table className="data-table">
            <thead><tr>{columns.map((column) => <th key={column}>{column.replaceAll("_", " ")}</th>)}</tr></thead>
            <tbody>
              {rows.map((row, index) => (
                <tr key={`${row.order_id}-${index}`}>
                  <td>{row.order_id ?? "—"}</td>
                  <td>{row.order_date ?? "—"}</td>
                  <td className="data-table__product">{row.product ?? "—"}</td>
                  <td>{row.category ?? "—"}</td>
                  <td>{row.city ?? "—"}</td>
                  <td>{money(row.sales)}</td>
                  <td className={Number(row.profit) < 0 ? "negative" : ""}>{money(row.profit)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </ResultShell>
    );
  }

  return <ResultShell title="Analytics result"><div className="empty-result">{result.message || "No visualization is available for this result."}</div></ResultShell>;
}

export function DashboardPie({ data }) {
  return <PieResult result={{ data }} />;
}
