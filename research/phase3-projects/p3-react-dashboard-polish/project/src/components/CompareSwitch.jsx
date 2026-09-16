import React from "react";

// Page-level comparison period. Native radios in a radiogroup: Tab enters the group,
// arrow keys move the selection, no custom key handling needed. The selected option is
// marked by weight + background + the native checked state, never colour alone.
export default function CompareSwitch({ periods, value, onChange }) {
  return (
    <div className="compare">
      <span id="compare-label" className="compare-label">Compare with</span>
      <div className="segmented" role="radiogroup" aria-labelledby="compare-label">
        {periods.map((p) => (
          <label key={p.id} className="seg">
            <input
              type="radio"
              name="compare"
              value={p.id}
              checked={value === p.id}
              onChange={() => onChange(p.id)}
            />
            <span>{p.label}</span>
          </label>
        ))}
      </div>
    </div>
  );
}
