import React from "react";

// One precision per unit so the column of values reads consistently.
const PRECISION = { kWh: 1, kW: 1, GBP: 2, "kgCO2e/kWh": 2 };

function formatValue(v, unit) {
  const digits = PRECISION[unit] ?? 1;
  const n = v.toLocaleString("en-GB", { minimumFractionDigits: digits, maximumFractionDigits: digits });
  return unit === "GBP" ? { value: "£" + n, unit: "" } : { value: n, unit };
}

// For energy, a decrease is the good direction; colour is paired with arrow + sign + text.
function Delta({ delta }) {
  const down = delta < 0;
  const tone = down ? "good" : "bad";
  const arrow = down ? "▼" : "▲"; // ▼ ▲
  return (
    <div className={"kpi-delta " + tone}>
      <span aria-hidden="true">{arrow} </span>
      <span data-numeric>{(down ? "" : "+") + delta.toFixed(1)}%</span>
      <span className="kpi-delta-ctx"> vs yesterday</span>
    </div>
  );
}

export default function KpiGrid({ items }) {
  return (
    <dl className="kpis">
      {items.map((k, i) => {
        const f = formatValue(k.value, k.unit);
        return (
          <div className={"kpi" + (i === 0 ? " kpi-lead" : "")} key={k.id}>
            <dt className="kpi-label">{k.label}</dt>
            <dd className="kpi-body">
              <div className="kpi-value">
                <span data-numeric>{f.value}</span>
                {f.unit && <span className="kpi-unit"> {f.unit}</span>}
              </div>
              <Delta delta={k.delta} />
            </dd>
          </div>
        );
      })}
    </dl>
  );
}
