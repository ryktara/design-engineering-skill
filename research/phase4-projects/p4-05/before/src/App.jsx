import React, { useEffect, useState } from "react";
import KpiGrid from "./components/KpiGrid.jsx";
import MeterList from "./components/MeterList.jsx";
import DemandChart from "./components/DemandChart.jsx";
import AlertsWidget from "./components/AlertsWidget.jsx";
import PromoBanner from "./components/PromoBanner.jsx";
import CompareSwitch from "./components/CompareSwitch.jsx";
import { site, kpis, meters, hourlyDemand, hourlyDemandCompare, comparePeriods, alerts } from "./data.js";

// The comparison period lives in the URL hash (#compare=lastweek) so a view can be shared and survives reload.
function readCompareFromHash() {
  const m = /compare=([a-z]+)/.exec(window.location.hash);
  return m && comparePeriods.some((p) => p.id === m[1]) ? m[1] : comparePeriods[0].id;
}

export default function App() {
  const [compareId, setCompareId] = useState(readCompareFromHash);
  const compare = comparePeriods.find((p) => p.id === compareId);
  useEffect(() => {
    const hash = "#compare=" + compareId;
    if (window.location.hash !== hash) window.history.replaceState(null, "", hash);
  }, [compareId]);

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">GridSense</div>
        <nav className="nav" aria-label="Primary">
          <a href="#" className="active" aria-current="page">Overview</a>
          <a href="#">Meters</a>
          <a href="#">Reports</a>
          <a href="#">Settings</a>
        </nav>
        <div className="site" title={site.name}>{site.name}</div>
      </header>

      {/* Slot height is reserved in CSS so the async banner never shifts the page. */}
      <PromoBanner />

      <main className="content">
        <div className="pagehead">
          <div>
            <h1>Overview</h1>
            <p className="pagehead-sub">{site.name} · today, updated 14:05</p>
          </div>
          <CompareSwitch periods={comparePeriods} value={compareId} onChange={setCompareId} />
          <div className="actions">
            <button type="button" className="btn secondary">Run optimisation</button>
            <button type="button" className="btn primary">Export report</button>
          </div>
        </div>
        <p className="sr-only" role="status">Comparing today with {compare.label.toLowerCase()}.</p>

        <section className="module" aria-labelledby="kpis-h">
          <h2 id="kpis-h">Today <span className="module-ctx">{compare.short}</span></h2>
          <KpiGrid items={kpis} compare={compare} />
        </section>

        <div className="row">
          <section className="module" aria-labelledby="demand-h">
            <h2 id="demand-h">Demand, last 24 hours <span className="module-ctx">{compare.short}</span></h2>
            <DemandChart
              points={hourlyDemand}
              compare={{ id: compare.id, label: compare.label, shortLabel: compare.id === "lastweek" ? "Last week" : compare.label, points: hourlyDemandCompare[compare.id] }}
              titleId="demand-h"
            />
          </section>
          <section className="module" aria-labelledby="meters-h">
            <div className="module-head">
              <h2 id="meters-h">Meters</h2>
              <button type="button" className="btn tertiary">Add meter</button>
            </div>
            <MeterList meters={meters} />
          </section>
        </div>

        <section className="module" aria-labelledby="alerts-h">
          <h2 id="alerts-h">Alerts</h2>
          <AlertsWidget alerts={alerts} siteName={site.name} />
        </section>
      </main>
    </div>
  );
}
