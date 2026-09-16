import React from "react";

const SEVERITY = {
  critical: { label: "Critical", glyph: "✖", cls: "status-fault" },
  warning: { label: "Warning", glyph: "▲", cls: "status-warn" },
};

// Full alert list (history for the day). Open alerts first; acknowledged ones stay visible, muted.
export default function AlertsWidget({ alerts, siteName, onAcknowledge }) {
  if (!alerts.length) {
    return (
      <div className="empty" data-empty>
        <p className="empty-title">No alerts today</p>
        <p className="empty-body">
          Nothing has crossed a threshold at {siteName}. Meters reporting a fault are shown in the Meters list.
        </p>
        <a href="#" className="btn tertiary flush">Alert rules</a>
      </div>
    );
  }
  const sorted = alerts.slice().sort((a, b) => Number(a.acknowledged) - Number(b.acknowledged));
  return (
    <ul className="alerts">
      {sorted.map((a) => {
        const s = SEVERITY[a.severity];
        return (
          <li key={a.id} className={"alert " + s.cls + (a.acknowledged ? " acknowledged" : "")} data-alert-id={a.id}>
            <span className="status-text">
              <span className="dot" aria-hidden="true">{s.glyph}</span>
              {s.label}
            </span>
            <div className="alert-body">
              <p className="alert-title">{a.title}</p>
              <p className="alert-meta">{a.meter} · since {a.since} · {a.detail}</p>
            </div>
            {a.acknowledged
              ? <span className="alert-state muted">Acknowledged</span>
              : <button type="button" className="btn tertiary" onClick={() => onAcknowledge(a.id)}>Acknowledge</button>}
          </li>
        );
      })}
    </ul>
  );
}
