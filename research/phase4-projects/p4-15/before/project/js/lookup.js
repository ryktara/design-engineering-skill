// Patient lookup against the static fixture (stands in for the pharmacy API).
let cache = null;
async function load() {
  if (cache) return cache;
  const res = await fetch('data/prescriptions.json');
  cache = (await res.json()).patients;
  return cache;
}

// dob comes in as MMDDYYYY digits; the fixture stores ISO dates.
function isoFromDigits(d) {
  if (!/^\d{8}$/.test(d)) return null;
  return `${d.slice(4, 8)}-${d.slice(0, 2)}-${d.slice(2, 4)}`;
}

export async function findPatient({ dob, lastName, code }) {
  const patients = await load();
  await new Promise((r) => setTimeout(r, 350)); // network-ish latency so the busy state is real
  if (code) return patients.find((p) => p.pickupCode.replace(/\s/g, '').toUpperCase() === code.replace(/\s/g, '').toUpperCase()) ?? null;
  const iso = isoFromDigits(dob);
  if (!iso) return null;
  return patients.find((p) => p.dob === iso && p.lastName.toLowerCase() === lastName.toLowerCase()) ?? null;
}

// "Okafor" -> "O••••r": keep first and last letter so the patient can recognise it, onlookers cannot.
export function maskName(n) {
  if (n.length <= 2) return n[0] + '•';
  return n[0] + '•'.repeat(n.length - 2) + n[n.length - 1];
}
// "Atorvastatin 20 mg" -> "Ator•••••••• 20 mg": keep the first 4 letters of the drug and the strength.
export function maskDrug(d) {
  const [name, ...rest] = d.split(' ');
  const shown = name.slice(0, 4);
  return `${shown}${'•'.repeat(Math.max(0, name.length - 4))} ${rest.join(' ')}`.trim();
}
