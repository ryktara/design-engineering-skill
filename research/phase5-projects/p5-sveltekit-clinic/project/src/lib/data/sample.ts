/**
 * Deterministic sample data for ClinicBoard.
 * Generated from a seeded PRNG so every build produces the same records.
 */

export type Practitioner = { id: string; name: string; role: string };

export type Patient = {
  id: string;
  firstName: string;
  lastName: string;
  dob: string; // ISO date
  phone: string;
  email: string;
  lastVisit: string; // ISO date
  balance: number; // outstanding, in dollars
  allergies: string[];
  notes: string;
};

export type AppointmentStatus = 'scheduled' | 'checked-in' | 'in-progress' | 'done' | 'no-show';

export type Appointment = {
  id: string;
  patientId: string;
  practitionerId: string;
  start: string; // "HH:MM"
  durationMin: number;
  reason: string;
  status: AppointmentStatus;
  /** Epoch ms when the patient arrived at the front desk; set on check-in. */
  checkedInAt?: number;
  /** Epoch ms when the patient was called in to the practitioner. */
  calledInAt?: number;
};

export type Visit = {
  id: string;
  patientId: string;
  date: string;
  practitionerId: string;
  reason: string;
  summary: string;
};

export type Invoice = {
  id: string;
  patientId: string;
  date: string;
  description: string;
  amount: number;
  paid: boolean;
};

function mulberry32(seed: number) {
  return function () {
    let t = (seed += 0x6d2b79f5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const rand = mulberry32(20240901);
const pick = <T>(arr: readonly T[]): T => arr[Math.floor(rand() * arr.length)];
const int = (min: number, max: number) => min + Math.floor(rand() * (max - min + 1));
const pad = (n: number) => String(n).padStart(2, '0');

export const practitioners: Practitioner[] = [
  { id: 'pr-1', name: 'Dr. Amara Okafor', role: 'General practitioner' },
  { id: 'pr-2', name: 'Dr. Lars Pedersen', role: 'General practitioner' },
  { id: 'pr-3', name: 'Nadia Haddad, NP', role: 'Nurse practitioner' },
  { id: 'pr-4', name: 'Tom Whitfield, RN', role: 'Practice nurse' }
];

const firstNames = [
  'Olivia', 'Noah', 'Amelia', 'Liam', 'Isla', 'Oliver', 'Ava', 'George', 'Mia', 'Arthur',
  'Freya', 'Leo', 'Grace', 'Oscar', 'Sophia', 'Harry', 'Ella', 'Jack', 'Lily', 'Henry',
  'Evie', 'Charlie', 'Rosie', 'Alfie', 'Ivy', 'Thomas', 'Poppy', 'Jacob', 'Florence', 'Freddie',
  'Willow', 'Archie', 'Isabella', 'Theo', 'Emily', 'Finley', 'Sienna', 'Lucas', 'Phoebe', 'Max'
];
const lastNames = [
  'Bennett', 'Chandra', 'Delgado', 'Fitzgerald', 'Grayson', 'Hussain', 'Iversen', 'Jankowski',
  'Kimura', 'Lindqvist', 'Moreau', 'Nakamura', 'Osei', 'Petrova', 'Quinn', 'Rahman', 'Salinas',
  'Tanaka', 'Underwood', 'Varga', 'Walsh', 'Xu', 'Yilmaz', 'Zielinski', 'Abernathy', 'Brightwater',
  'Castellano', 'Dunmore', 'Ekwueme', 'Farrow', 'Gallagher', 'Hollis', 'Ibarra', 'Jefferies',
  'Kowalczyk', 'Laurent', 'Mbeki', 'Novak', 'Oduya', 'Prescott'
];
const reasons = [
  'Annual check-up', 'Follow-up', 'Flu symptoms', 'Blood pressure review', 'Vaccination',
  'Back pain', 'Skin rash', 'Prescription renewal', 'Lab results review', 'Sore throat',
  'Physical therapy referral', 'Diabetes review', 'Ear infection', 'Sports injury', 'Migraine'
];
const allergyPool = ['Penicillin', 'Latex', 'Peanuts', 'Sulfa drugs', 'Ibuprofen', 'Shellfish'];

function isoDate(y: number, m: number, d: number) {
  return `${y}-${pad(m)}-${pad(d)}`;
}

export const patients: Patient[] = Array.from({ length: 40 }, (_, i) => {
  const firstName = firstNames[i];
  const lastName = lastNames[i];
  const year = int(1938, 2018);
  const allergyCount = rand() < 0.35 ? int(1, 2) : 0;
  const allergies = Array.from({ length: allergyCount }, () => pick(allergyPool)).filter(
    (a, idx, arr) => arr.indexOf(a) === idx
  );
  const balance = rand() < 0.55 ? 0 : int(15, 420);
  return {
    id: `p-${1000 + i}`,
    firstName,
    lastName,
    dob: isoDate(year, int(1, 12), int(1, 28)),
    phone: `(555) ${pad(int(200, 999))}-${pad(int(1000, 9999))}`,
    email: `${firstName.toLowerCase()}.${lastName.toLowerCase()}@example.com`,
    lastVisit: isoDate(2024, int(3, 8), int(1, 28)),
    balance,
    allergies,
    notes: pick([
      'Prefers morning appointments.',
      'Requires interpreter (Spanish).',
      'Hard of hearing; speak clearly.',
      'Wheelchair access needed.',
      '',
      '',
      'Insurance card on file expires this year.'
    ])
  };
});

const statuses: AppointmentStatus[] = [
  'scheduled', 'scheduled', 'scheduled', 'checked-in', 'in-progress', 'done', 'done', 'no-show'
];

export const appointments: Appointment[] = Array.from({ length: 25 }, (_, i) => {
  const hour = int(8, 17);
  const minute = pick([0, 15, 30, 45] as const);
  return {
    id: `a-${200 + i}`,
    patientId: patients[int(0, patients.length - 1)].id,
    practitionerId: practitioners[i % practitioners.length].id,
    start: `${pad(hour)}:${pad(minute)}`,
    durationMin: pick([15, 30, 30, 45] as const),
    reason: pick(reasons),
    status: statuses[i % statuses.length]
  };
}).sort((a, b) => a.start.localeCompare(b.start));

// Arrival / call-in timestamps for today's sample board, relative to app start so the
// waiting-room clock has something to count. Index-based (not PRNG) so the seeded
// patient/visit/invoice data above is unchanged.
const bootNow = Date.now();
const MIN = 60_000;
let waitingIdx = 0;
let inProgressIdx = 0;
let doneIdx = 0;
for (const a of appointments) {
  if (a.status === 'checked-in') {
    a.checkedInAt = bootNow - (7 + waitingIdx++ * 16) * MIN; // 7, 23, 39 min ago
  } else if (a.status === 'in-progress') {
    const waited = 20 + inProgressIdx * 9;
    const called = 4 + inProgressIdx++ * 3;
    a.checkedInAt = bootNow - (waited + called) * MIN;
    a.calledInAt = bootNow - called * MIN;
  } else if (a.status === 'done') {
    const waited = 5 + (doneIdx % 4) * 6;
    const ago = 30 + doneIdx++ * 15;
    a.checkedInAt = bootNow - (ago + waited) * MIN;
    a.calledInAt = bootNow - ago * MIN;
  }
}

export const visits: Visit[] = patients.flatMap((p) =>
  Array.from({ length: int(1, 4) }, (_, j) => ({
    id: `v-${p.id}-${j}`,
    patientId: p.id,
    date: isoDate(int(2022, 2024), int(1, 12), int(1, 28)),
    practitionerId: pick(practitioners).id,
    reason: pick(reasons),
    summary: pick([
      'Vitals normal. Advised rest and fluids.',
      'Prescribed course of antibiotics; review in 10 days.',
      'Referred to physiotherapy.',
      'Bloods taken; results pending.',
      'Blood pressure elevated; lifestyle advice given.',
      'Vaccination administered without complication.'
    ])
  })).sort((a, b) => b.date.localeCompare(a.date))
);

export const invoices: Invoice[] = patients.flatMap((p) => {
  const count = int(1, 3);
  const items: Invoice[] = [];
  let remaining = p.balance;
  for (let j = 0; j < count; j++) {
    const amount = int(45, 260);
    const last = j === count - 1;
    const paid = remaining <= 0 ? true : last ? false : rand() < 0.5;
    if (!paid) remaining -= amount;
    items.push({
      id: `inv-${p.id}-${j}`,
      patientId: p.id,
      date: isoDate(2024, int(1, 8), int(1, 28)),
      description: pick(['Consultation', 'Lab work', 'Vaccination', 'Procedure', 'Extended consultation']),
      amount,
      paid
    });
  }
  return items.sort((a, b) => b.date.localeCompare(a.date));
});

// A patient's balance IS the sum of their outstanding invoices. The generator
// above can round the target away (an invoice may overshoot the remaining
// balance), so reconcile it here — otherwise the balance shown in the patient
// header, the patients list and the reports totals do not line up with the
// amounts on the billing tab.
for (const p of patients) {
  p.balance = invoices
    .filter((i) => i.patientId === p.id && !i.paid)
    .reduce((sum, i) => sum + i.amount, 0);
}

export const clinic = {
  name: 'Riverside Family Clinic',
  address: '42 Harbour Street, Riverside',
  phone: '(555) 010-4200',
  openingHours: '08:00-18:00, Monday to Friday'
};

export const currentUser = { name: 'Priya Natarajan', role: 'Front desk' };

export function patientById(id: string): Patient | undefined {
  return patients.find((p) => p.id === id);
}

export function practitionerById(id: string): Practitioner | undefined {
  return practitioners.find((p) => p.id === id);
}

export function fullName(p: Pick<Patient, 'firstName' | 'lastName'>) {
  return `${p.firstName} ${p.lastName}`;
}

export function formatDate(iso: string) {
  const [y, m, d] = iso.split('-').map(Number);
  return new Date(Date.UTC(y, m - 1, d)).toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    timeZone: 'UTC'
  });
}

export function formatMoney(n: number) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(n);
}
