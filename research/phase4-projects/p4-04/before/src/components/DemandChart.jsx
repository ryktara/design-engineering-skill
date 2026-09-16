import React, { useEffect, useRef, useState } from "react";

// Question the chart answers: when did demand peak today and how far off the low was it?
// The viewBox width tracks the container so tick labels stay at CSS pixel size on narrow screens.
export default function DemandChart({ points, titleId }) {
  const ref = useRef(null);
  const [w, setW] = useState(640);
  useEffect(() => {
    if (!ref.current || typeof ResizeObserver === "undefined") return;
    const ro = new ResizeObserver(([e]) => setW(Math.max(280, Math.round(e.contentRect.width))));
    ro.observe(ref.current);
    return () => ro.disconnect();
  }, []);
  const h = w < 480 ? 180 : 220, padL = 44, padR = 12, padT = 12, padB = 28;
  const max = Math.max(...points), min = Math.min(...points);
  const peakIdx = points.indexOf(max), lowIdx = points.indexOf(min);
  const avg = Math.round(points.reduce((a, b) => a + b, 0) / points.length);
  const yTop = Math.ceil(max / 200) * 200, yBottom = 0;
  const x = (i) => padL + (i / (points.length - 1)) * (w - padL - padR);
  const y = (v) => padT + (1 - (v - yBottom) / (yTop - yBottom)) * (h - padT - padB);
  const d = points.map((v, i) => (i ? "L" : "M") + x(i).toFixed(1) + " " + y(v).toFixed(1)).join(" ");
  const hh = (i) => String(i).padStart(2, "0") + ":00";
  const ticks = [];
  for (let v = yBottom; v <= yTop; v += 200) ticks.push(v);

  const summary = `Demand peaked at ${max} kW at ${hh(peakIdx)} and was lowest at ${min} kW at ${hh(lowIdx)}; the 24-hour average was ${avg} kW.`;

  return (
    <figure className="chart-figure" role="group" aria-labelledby={titleId} aria-describedby="demand-summary" ref={ref}>
      <svg
        viewBox={`0 0 ${w} ${h}`}
        className="chart"
        role="img"
        aria-labelledby={titleId}
        aria-describedby="demand-summary"
      >
        <title>Demand in kW, last 24 hours</title>
        {ticks.map((v) => (
          <g key={v}>
            <line x1={padL} x2={w - padR} y1={y(v)} y2={y(v)} className="chart-grid" />
            <text x={padL - 8} y={y(v)} className="chart-tick" textAnchor="end" dominantBaseline="middle">{v}</text>
          </g>
        ))}
        {(w < 480 ? [0, 12, 23] : [0, 6, 12, 18, 23]).map((i) => (
          <text key={i} x={x(i)} y={h - 8} className="chart-tick" textAnchor="middle">{hh(i)}</text>
        ))}
        <path d={d} className="chart-line" fill="none" />
        <circle cx={x(peakIdx)} cy={y(max)} r="4" className="chart-peak" />
        <text x={x(peakIdx)} y={y(max) - 10} className="chart-annot" textAnchor="middle">Peak {max} kW</text>
      </svg>
      <figcaption id="demand-summary" className="chart-summary">{summary}</figcaption>
      <details className="chart-data">
        <summary>Show hourly data</summary>
        <table>
          <caption className="sr-only">Hourly demand in kW</caption>
          <thead><tr><th scope="col">Hour</th><th scope="col" className="num">kW</th></tr></thead>
          <tbody>
            {points.map((v, i) => (
              <tr key={i}><th scope="row">{hh(i)}</th><td className="num" data-numeric>{v}</td></tr>
            ))}
          </tbody>
        </table>
      </details>
    </figure>
  );
}
