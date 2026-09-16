import React, { useEffect, useRef, useState } from "react";

const SEVERITY = {
  critical: { label: "Critical", glyph: "✖", cls: "status-fault" },
  warning: { label: "Warning", glyph: "▲", cls: "status-warn" },
};

// Full alert list (history for the day). Open alerts first; acknowledged ones stay visible, muted.
// Accessibility review notes (alerts panel):
//  - every Acknowledge button names its alert (visually hidden suffix), so two rows are not two identical buttons;
//  - acknowledging removes the button, so focus is moved to the row it belonged to (tabindex=-1) instead of
//    falling back to <body>; the row then reads its severity, title and the new "Acknowledged" state.
//    The state change itself is announced by the Exceptions strip's existing live region (open-count summary),
//    so no second live region is added here;
//  - the <ul> keeps list semantics with list-style:none (WebKit drops them otherwise) via role="list".
export default function AlertsWidget({ alerts, siteName, onAcknowledge }) {
  const [focusId, setFocusId] = useState(null);
  const listRef = useRef(null);
  useEffect(() => {
    if (!focusId || !listRef.current) return;
    const row = listRef.current.querySelector(`[data-alert-id="${focusId}"]`);
    if (row) row.focus();
    setFocusId(null);
  }, [focusId, alerts]);

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
  const acknowledge = (id) => {
    onAcknowledge(id);
    setFocusId(id);
  };
  return (
    <ul className="alerts" role="list" ref={listRef}>
      {sorted.map((a) => {
        const s = SEVERITY[a.severity];
        return (
          <li
            key={a.id}
            className={"alert " + s.cls + (a.acknowledged ? " acknowledged" : "")}
            data-alert-id={a.id}
            tabIndex={-1}
          >
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
              : (
                <button type="button" className="btn tertiary" onClick={() => acknowledge(a.id)}>
                  Acknowledge<span className="sr-only">: {a.title}</span>
                </button>
              )}
          </li>
        );
      })}
    </ul>
  );
}
