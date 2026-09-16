import React from "react";

// Exceptions first: the highest-severity open alert sits at the top of the page in a slot whose
// height is fixed in CSS (see .exceptions), so alerts arriving later change text, never layout.
// Severity is glyph + label + tint (reusing the meter status chips), never colour alone.
// One action per strip: acknowledge the featured alert; everything else is a text link.
const SEVERITY = {
  critical: { label: "Critical", glyph: "✖", cls: "status-fault" },
  warning: { label: "Warning", glyph: "▲", cls: "status-warn" },
};
const RANK = { critical: 0, warning: 1 };

export function summarise(open) {
  if (!open.length) return "No open exceptions.";
  const c = open.filter((a) => a.severity === "critical").length;
  const w = open.length - c;
  const parts = [];
  if (c) parts.push(`${c} critical`);
  if (w) parts.push(`${w} warning${w > 1 ? "s" : ""}`);
  return `${open.length} open exception${open.length > 1 ? "s" : ""}: ${parts.join(", ")}.`;
}

export default function ExceptionStrip({ alerts, lastArrival, onAcknowledge }) {
  const open = alerts.filter((a) => !a.acknowledged).sort((a, b) => RANK[a.severity] - RANK[b.severity]);
  const featured = open[0];
  const tone = featured ? featured.severity : "clear";
  const summary = summarise(open);
  // The live text names what changed, then the totals, so a screen reader hears the new alert first.
  const live = lastArrival && !lastArrival.acknowledged
    ? `New ${SEVERITY[lastArrival.severity].label.toLowerCase()}: ${lastArrival.title}. ${summary}`
    : summary;

  return (
    <section className={"exceptions " + tone} aria-labelledby="exceptions-h">
      <h2 id="exceptions-h" className="sr-only">Exceptions</h2>
      <p className="sr-only" role="status" aria-live="polite" aria-atomic="true">{live}</p>
      {featured ? (
        <>
          <span className={"exc-chip " + SEVERITY[featured.severity].cls}>
            <span className="status-text">
              <span className="dot" aria-hidden="true">{SEVERITY[featured.severity].glyph}</span>
              {SEVERITY[featured.severity].label}
            </span>
          </span>
          <div className="exc-body">
            <p className="exc-title">{featured.title}</p>
            <p className="exc-meta">
              {featured.meter} · since {featured.since} · {featured.detail}
              {open.length > 1 && <> · <a href="#alerts-h" className="exc-link">{open.length - 1} more open</a></>}
            </p>
          </div>
          <div className="exc-actions">
            <button type="button" className="btn secondary" onClick={() => onAcknowledge(featured.id)}>Acknowledge</button>
          </div>
        </>
      ) : (
        <>
          <span className="exc-chip status-ok">
            <span className="status-text"><span className="dot" aria-hidden="true">●</span>Clear</span>
          </span>
          <div className="exc-body">
            <p className="exc-title">No open exceptions</p>
            <p className="exc-meta">Nothing is above a threshold and every meter is reporting. <a href="#alerts-h" className="exc-link">Alert history</a></p>
          </div>
        </>
      )}
    </section>
  );
}
