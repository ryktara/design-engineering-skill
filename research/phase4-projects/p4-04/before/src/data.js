// Shapes mirror the /api/v2/sites/:id/summary payload.
export const site = { id: "site-114", name: "Northgate Logistics Hub", tz: "Europe/London" };

export const kpis = [
  { id: "consumption", label: "Consumption today", value: 18432.7, unit: "kWh", delta: -4.2 },
  { id: "demand", label: "Peak demand", value: 912.4, unit: "kW", delta: 1.8 },
  { id: "cost", label: "Cost to date (month)", value: 27614.05, unit: "GBP", delta: 3.1 },
  { id: "carbon", label: "Carbon intensity", value: 0.19, unit: "kgCO2e/kWh", delta: -0.7 },
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

// Alerts widget: the API returned nothing for this site today.
export const alerts = [];
