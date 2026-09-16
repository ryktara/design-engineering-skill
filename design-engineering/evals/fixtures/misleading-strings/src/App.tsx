// This file mentions ListView, NavigationView and isTVEnabled in comments and identifiers only.
import React from "react";
const isTVEnabled = false;   // feature flag name, not a TV platform
const darkText = "#111111";  // a text colour, not a dark theme
export function MobileSettings() { return <section className="settings-list">ListView-like settings</section>; }
export default function App() {
  return (<main><header className="site-header"><nav aria-label="Primary"><a href="/">Home</a><a href="/orders">Orders</a></nav></header>
    <MobileSettings /><p style={{color: darkText}}>NavigationView is a WinUI control we do not use here.</p></main>);
}
