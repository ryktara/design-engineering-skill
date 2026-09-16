import React from "react";

// Status is never colour alone: each state has a label and a distinct glyph.
const STATUS = {
  ok: { label: "Normal", glyph: "●" },   // ●
  warn: { label: "Warning", glyph: "▲" }, // ▲
  fault: { label: "Fault", glyph: "✖" },  // ✖
};

export default function MeterList({ meters }) {
  return (
    <ul className="meters">
      {meters.map((m) => {
        const s = STATUS[m.status];
        return (
          <li key={m.id} className={"meter status-" + m.status} data-status={m.status}>
            <span className="status-text">
              <span className="dot" aria-hidden="true">{s.glyph}</span>
              {s.label}
            </span>
            <span className="meter-name">{m.name}</span>
            <span className="meter-reading" data-numeric>
              {m.lastReading == null
                ? <span className="muted">No reading</span>
                : m.lastReading.toLocaleString("en-GB", { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + " " + m.unit}
            </span>
          </li>
        );
      })}
    </ul>
  );
}
