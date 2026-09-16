import React from "react";
import KpiGrid from "./components/KpiGrid.jsx";
import MeterList from "./components/MeterList.jsx";
import DemandChart from "./components/DemandChart.jsx";
import AlertsWidget from "./components/AlertsWidget.jsx";
import PromoBanner from "./components/PromoBanner.jsx";
import { site, kpis, meters, hourlyDemand, alerts } from "./data.js";

export default function App() {
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
          <div className="actions">
            <button type="button" className="btn secondary">Run optimisation</button>
            <button type="button" className="btn primary">Export report</button>
          </div>
        </div>

        <section className="module" aria-labelledby="kpis-h">
          <h2 id="kpis-h">Today</h2>
          <KpiGrid items={kpis} />
        </section>

        <div className="row">
          <section className="module" aria-labelledby="demand-h">
            <h2 id="demand-h">Demand, last 24 hours</h2>
            <DemandChart points={hourlyDemand} titleId="demand-h" />
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
