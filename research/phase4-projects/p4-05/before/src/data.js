// Shapes mirror the /api/v2/sites/:id/summary payload.
export const site = { id: "site-114", name: "Northgate Logistics Hub", tz: "Europe/London" };

// Comparison periods offered by the summary endpoint (?compare=yesterday|lastweek).
export const comparePeriods = [
  { id: "yesterday", label: "Yesterday", short: "vs yesterday" },
  { id: "lastweek", label: "Same day last week", short: "vs last week" },
];

// Each KPI carries the reference value for every comparison period; deltas are derived in the UI.
export const kpis = [
  { id: "consumption", label: "Consumption today", value: 18432.7, unit: "kWh", yesterday: 19240.8, lastweek: 17690.2 },
  { id: "demand", label: "Peak demand", value: 912.4, unit: "kW", yesterday: 896.3, lastweek: 948.0 },
  { id: "cost", label: "Cost to date (month)", value: 27614.05, unit: "GBP", yesterday: 26783.8, lastweek: 24012.9 },
  { id: "carbon", label: "Carbon intensity", value: 0.19, unit: "kgCO2e/kWh", yesterday: 0.191, lastweek: 0.21 },
];

export const meters = [
  { id: "m-01", name: "Main incomer A", status: "ok", lastReading: 3120.4, unit: "kWh" },
  { id: "m-02", name: "Chiller plant", status: "warn", lastReading: 812.9, unit: "kWh" },
  { id: "m-03", name: "Cold store 2", status: "fault", lastReading: null, unit: "kWh" },
  { id: "m-04", name: "Dock lighting", status: "ok", lastReading: 46.02, unit: "kWh" },
  { id: "m-05", name: "Office HVAC", status: "ok", lastReading: 1188.33, unit: "kWh" },
];

// 24 hourly points, kW
export const hourlyDemand = [
  410, 380, 362, 355, 372, 440, 610, 780, 860, 902, 912, 890,
  871, 884, 866, 840, 795, 720, 650, 590, 540, 500, 460, 430,
];

// Same 24 hours for each comparison period, kW
export const hourlyDemandCompare = {
  yesterday: [
    420, 392, 370, 358, 380, 452, 598, 760, 842, 880, 896, 884,
    862, 870, 858, 832, 790, 730, 662, 600, 548, 508, 470, 438,
  ],
  lastweek: [
    398, 372, 350, 348, 366, 430, 640, 812, 902, 940, 948, 930,
    905, 912, 890, 860, 810, 735, 660, 596, 542, 498, 455, 425,
  ],
};

// Alerts widget: the API returned nothing for this site today.
export const alerts = [];
