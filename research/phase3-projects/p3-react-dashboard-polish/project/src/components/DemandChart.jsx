import React, { useEffect, useRef, useState } from "react";

// Question the chart answers: when did demand peak today, and how does the day's shape
// compare with the selected reference period (yesterday / same day last week)?
// The viewBox width tracks the container so tick labels stay at CSS pixel size on narrow screens.
export default function DemandChart({ points, compare, titleId }) {
  const ref = useRef(null);
  const [w, setW] = useState(640);
  useEffect(() => {
    if (!ref.current || typeof ResizeObserver === "undefined") return;
    const ro = new ResizeObserver(([e]) => setW(Math.max(280, Math.round(e.contentRect.width))));
    ro.observe(ref.current);
    return () => ro.disconnect();
  }, []);
  const narrow = w < 480;
  const cmp = compare && compare.points;
  // Direct end labels replace a legend, so the right gutter widens when a second series is drawn.
  const h = narrow ? 180 : 220, padL = 44, padR = cmp ? (narrow ? 60 : 76) : 12, padT = 12, padB = 28;
  const all = cmp ? points.concat(cmp) : points;
  const max = Math.max(...points), min = Math.min(...points);
  const peakIdx = points.indexOf(max), lowIdx = points.indexOf(min);
  const avg = Math.round(points.reduce((a, b) => a + b, 0) / points.length);
  const yTop = Math.ceil(Math.max(...all) / 200) * 200, yBottom = 0;
  const x = (i) => padL + (i / (points.length - 1)) * (w - padL - padR);
  const y = (v) => padT + (1 - (v - yBottom) / (yTop - yBottom)) * (h - padT - padB);
  const line = (pts) => pts.map((v, i) => (i ? "L" : "M") + x(i).toFixed(1) + " " + y(v).toFixed(1)).join(" ");
  const hh = (i) => String(i).padStart(2, "0") + ":00";
  const ticks = [];
  for (let v = yBottom; v <= yTop; v += 200) ticks.push(v);

  let summary = `Demand peaked at ${max} kW at ${hh(peakIdx)} and was lowest at ${min} kW at ${hh(lowIdx)}; the 24-hour average was ${avg} kW.`;
  let cmpMax, cmpPeakIdx, cmpAvg, avgDelta;
  if (cmp) {
    cmpMax = Math.max(...cmp);
    cmpPeakIdx = cmp.indexOf(cmpMax);
    cmpAvg = Math.round(cmp.reduce((a, b) => a + b, 0) / cmp.length);
    avgDelta = ((avg - cmpAvg) / cmpAvg) * 100;
    const avgWord = Math.abs(avgDelta) < 0.05 ? "about the same" : `${Math.abs(avgDelta).toFixed(1)}% ${avgDelta < 0 ? "lower" : "higher"}`;
    summary += ` ${compare.label}: peak ${cmpMax} kW at ${hh(cmpPeakIdx)}, average ${cmpAvg} kW; today's average is ${avgWord}.`;
  }

  // End labels: keep the two apart when the series finish close together.
  const lastI = points.length - 1;
  let todayLabelY = y(points[lastI]), cmpLabelY = cmp ? y(cmp[lastI]) : 0;
  if (cmp && Math.abs(todayLabelY - cmpLabelY) < 14) {
    if (todayLabelY <= cmpLabelY) { todayLabelY -= 7; cmpLabelY += 7; } else { todayLabelY += 7; cmpLabelY -= 7; }
  }

  return (
    <figure className="chart-figure" role="group" aria-labelledby={titleId} aria-describedby="demand-summary" ref={ref}>
      <svg
        viewBox={`0 0 ${w} ${h}`}
        className="chart"
        role="img"
        aria-labelledby={titleId}
        aria-describedby="demand-summary"
      >
        <title>{cmp ? `Demand in kW, last 24 hours, today against ${compare.label.toLowerCase()}` : "Demand in kW, last 24 hours"}</title>
        {ticks.map((v) => (
          <g key={v}>
            <line x1={padL} x2={w - padR} y1={y(v)} y2={y(v)} className="chart-grid" />
            <text x={padL - 8} y={y(v)} className="chart-tick" textAnchor="end" dominantBaseline="middle">{v}</text>
          </g>
        ))}
        {(narrow ? [0, 12, 23] : [0, 6, 12, 18, 23]).map((i) => (
          <text key={i} x={x(i)} y={h - 8} className="chart-tick" textAnchor="middle">{hh(i)}</text>
        ))}
        {cmp && <path d={line(cmp)} className="chart-line-compare" fill="none" />}
        <path d={line(points)} className="chart-line" fill="none" />
        <circle cx={x(peakIdx)} cy={y(max)} r="4" className="chart-peak" />
        <text x={x(peakIdx)} y={y(max) - 10} className="chart-annot" textAnchor="middle">Peak {max} kW</text>
        {cmp && (
          <>
            <text x={x(lastI) + 6} y={todayLabelY} className="chart-series-label" dominantBaseline="middle">Today</text>
            <text x={x(lastI) + 6} y={cmpLabelY} className="chart-series-label compare" dominantBaseline="middle">{compare.shortLabel || compare.label}</text>
          </>
        )}
      </svg>
      <figcaption id="demand-summary" className="chart-summary">{summary}</figcaption>
      <details className="chart-data">
        <summary>Show hourly data</summary>
        <table>
          <caption className="sr-only">Hourly demand in kW{cmp ? `, today and ${compare.label.toLowerCase()}` : ""}</caption>
          <thead>
            <tr>
              <th scope="col">Hour</th>
              <th scope="col" className="num">Today kW</th>
              {cmp && <th scope="col" className="num">{compare.label} kW</th>}
              {cmp && <th scope="col" className="num">Difference</th>}
            </tr>
          </thead>
          <tbody>
            {points.map((v, i) => (
              <tr key={i}>
                <th scope="row">{hh(i)}</th>
                <td className="num" data-numeric>{v}</td>
                {cmp && <td className="num" data-numeric>{cmp[i]}</td>}
                {cmp && <td className="num" data-numeric>{(v - cmp[i] > 0 ? "+" : "") + (v - cmp[i])}</td>}
              </tr>
            ))}
          </tbody>
        </table>
      </details>
    </figure>
  );
}
