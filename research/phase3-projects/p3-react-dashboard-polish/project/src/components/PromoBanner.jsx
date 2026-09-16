import React, { useEffect, useState } from "react";

// The banner still arrives asynchronously, but its slot is rendered immediately at final
// height (see .promo-slot in styles.css) so content below never moves. It is a quiet
// notice with a text link, not a competing primary button, and it can be dismissed.
export default function PromoBanner() {
  const [promo, setPromo] = useState(null);
  const [dismissed, setDismissed] = useState(false);
  useEffect(() => {
    const t = setTimeout(
      () => setPromo({ text: "New: GridSense Insights Pro — automated demand forecasting.", cta: "Learn more" }),
      800
    );
    return () => clearTimeout(t);
  }, []);
  if (dismissed) return <div className="promo-slot" aria-hidden="true" />;
  return (
    <div className="promo-slot">
      {promo && (
        <div className="promo" role="region" aria-label="Product notice">
          <span className="promo-text">
            {promo.text} <a href="#">{promo.cta}</a>
          </span>
          <button type="button" className="btn tertiary icon" aria-label="Dismiss notice" onClick={() => setDismissed(true)}>
            <span aria-hidden="true">✕</span>
          </button>
        </div>
      )}
    </div>
  );
}
