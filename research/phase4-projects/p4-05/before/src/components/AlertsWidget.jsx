import React from "react";

export default function AlertsWidget({ alerts, siteName }) {
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
  return (
    <ul className="alerts">
      {alerts.map((a) => (
        <li key={a.id}>{a.message}</li>
      ))}
    </ul>
  );
}
