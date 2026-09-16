// Deterministic sample data. Uses a tiny seeded PRNG so every reload
// produces the same catalogue, which keeps screenshots and tests stable.

export type Category =
  | 'Fasteners'
  | 'Electrical'
  | 'Packaging'
  | 'Hand tools'
  | 'Safety'
  | 'Consumables'

export interface Supplier {
  id: string
  name: string
  contact: string
  email: string
  leadTimeDays: number
  city: string
}

export interface Product {
  sku: string
  name: string
  category: Category
  supplierId: string
  onHand: number
  reorderPoint: number
  unitCost: number
  location: string
}

export type AdjustmentReason = 'received' | 'cycle-count' | 'damaged' | 'returned' | 'issued'

export interface Adjustment {
  id: string
  sku: string
  quantity: number
  reason: AdjustmentReason
  notes: string
  user: string
  createdAt: string
}

function mulberry32(seed: number) {
  return function () {
    seed |= 0
    seed = (seed + 0x6d2b79f5) | 0
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed)
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}

const rand = mulberry32(20260910)
const pick = <T>(arr: readonly T[]): T => arr[Math.floor(rand() * arr.length)]
const between = (min: number, max: number) => min + Math.floor(rand() * (max - min + 1))

export const CATEGORIES: Category[] = [
  'Fasteners',
  'Electrical',
  'Packaging',
  'Hand tools',
  'Safety',
  'Consumables',
]

const CATEGORY_PREFIX: Record<Category, string> = {
  Fasteners: 'FA',
  Electrical: 'EL',
  Packaging: 'PK',
  'Hand tools': 'HT',
  Safety: 'SF',
  Consumables: 'CS',
}

const NAMES: Record<Category, string[]> = {
  Fasteners: [
    'Hex bolt M6 x 40',
    'Hex bolt M8 x 60',
    'Hex nut M6 zinc',
    'Hex nut M10 zinc',
    'Flat washer M8',
    'Spring washer M6',
    'Wood screw 4 x 40',
    'Self-tapping screw 3.5 x 25',
    'Machine screw M4 x 16',
    'Threaded rod M10 1m',
    'Rivet 4.8 x 12',
    'Anchor bolt M12',
  ],
  Electrical: [
    'Cable 2.5mm twin & earth 50m',
    'Cable tie 200mm black (100)',
    'Terminal block 12-way',
    'MCB 16A type B',
    'Socket outlet double 13A',
    'Junction box 20A',
    'Conduit 20mm 3m',
    'Fuse 13A BS1362 (10)',
    'LED batten 4ft 40W',
    'Trunking 25 x 16 3m',
    'RCD 63A 30mA',
    'Light switch 1-gang 2-way',
  ],
  Packaging: [
    'Cardboard box 300 x 200 x 200',
    'Cardboard box 450 x 350 x 300',
    'Bubble wrap 750mm x 100m',
    'Packing tape 48mm clear',
    'Stretch film 400mm 17mu',
    'Pallet wrap dispenser',
    'Mailing bag 320 x 440',
    'Void fill paper 380mm roll',
    'Edge protector 1m',
    'Label 100 x 150 (500)',
    'Strapping 12mm 2000m',
    'Corner board 50mm',
  ],
  'Hand tools': [
    'Claw hammer 16oz',
    'Screwdriver set 8pc',
    'Adjustable spanner 250mm',
    'Combination pliers 180mm',
    'Tape measure 5m',
    'Utility knife retractable',
    'Hex key set metric',
    'Hacksaw 300mm',
    'Spirit level 600mm',
    'Socket set 1/2in 24pc',
    'Wire stripper',
    'Torque wrench 40-200Nm',
  ],
  Safety: [
    'Safety glasses clear',
    'Nitrile gloves L (100)',
    'Hi-vis vest yellow L',
    'Ear defenders 27dB',
    'Hard hat white',
    'Dust mask FFP2 (20)',
    'Safety boots S3 size 10',
    'Knee pads gel',
    'First aid kit 20 person',
    'Fire extinguisher CO2 2kg',
    'Spill kit 50L',
    'Face shield visor',
  ],
  Consumables: [
    'WD-40 400ml',
    'Cutting disc 115mm (10)',
    'Sandpaper 120 grit (25)',
    'Silicone sealant clear',
    'PTFE tape 12mm',
    'Cleaning wipes (100)',
    'Marker pen black (10)',
    'Grease cartridge 400g',
    'Grinding disc 115mm',
    'Masking tape 50mm',
    'Rag bale 10kg',
    'Drill bit HSS 6mm (5)',
  ],
}

const SUPPLIER_SEED: Array<[string, string, string, number]> = [
  ['Northgate Fixings', 'Priya Shah', 'Leeds', 3],
  ['Kessler Electrical', 'Tom Kessler', 'Manchester', 5],
  ['Boxwell Packaging', 'Aisha Rahman', 'Birmingham', 2],
  ['Ironbridge Tools', 'Daniel Okafor', 'Telford', 7],
  ['SafeSite Supplies', 'Megan Doyle', 'Glasgow', 4],
  ['Brightline Consumables', 'Chris Adeyemi', 'Bristol', 2],
  ['Pennine Industrial', 'Laura Whitfield', 'Sheffield', 6],
  ['Harbour Trade', 'James Nolan', 'Liverpool', 5],
  ['Meridian Direct', 'Sophie Lindqvist', 'Reading', 3],
  ['Anvil & Co', 'Robert Hale', 'Derby', 10],
  ['Clearwater Wholesale', 'Hannah Byrne', 'Cardiff', 4],
  ['Redstone Supply', 'Owen Price', 'Nottingham', 8],
]

export const suppliers: Supplier[] = SUPPLIER_SEED.map(([name, contact, city, lead], i) => ({
  id: `SUP-${String(i + 1).padStart(3, '0')}`,
  name,
  contact,
  email: `${contact.split(' ')[0].toLowerCase()}@${name.split(' ')[0].toLowerCase()}.co.uk`,
  leadTimeDays: lead,
  city,
}))

const AISLES = ['A', 'B', 'C', 'D', 'E']

export const products: Product[] = []

CATEGORIES.forEach((category, ci) => {
  const base = NAMES[category]
  // 200 products / 6 categories: 34,34,33,33,33,33
  const count = ci < 2 ? 34 : 33
  for (let i = 0; i < count; i++) {
    const name = base[i % base.length]
    const variant = Math.floor(i / base.length)
    const displayName = variant === 0 ? name : `${name} (pack ${variant + 1})`
    const reorderPoint = between(10, 120)
    const onHand = rand() < 0.22 ? between(0, reorderPoint) : between(reorderPoint, reorderPoint * 6)
    products.push({
      sku: `${CATEGORY_PREFIX[category]}-${String(1000 + i).padStart(4, '0')}`,
      name: displayName,
      category,
      supplierId: suppliers[(ci * 2 + (i % 2)) % suppliers.length].id,
      onHand,
      reorderPoint,
      unitCost: Math.round(between(35, 4800)) / 100,
      location: `${pick(AISLES)}${between(1, 12)}-${between(1, 4)}`,
    })
  }
})

const USERS = ['m.patel', 'j.cole', 'r.okoro', 's.byrne']
const REASONS: AdjustmentReason[] = ['received', 'cycle-count', 'damaged', 'returned', 'issued']
const NOTES: Record<AdjustmentReason, string[]> = {
  received: ['PO 4471 delivered', 'Partial delivery', 'Backorder arrived', ''],
  'cycle-count': ['Q3 count', 'Recount after discrepancy', '', 'Bin relabelled'],
  damaged: ['Forklift damage', 'Water ingress bay C', 'Packaging split', ''],
  returned: ['Customer return', 'Wrong item shipped', ''],
  issued: ['Works order 2213', 'Maintenance draw', 'Site kit', ''],
}

export const adjustments: Adjustment[] = Array.from({ length: 30 }, (_, i) => {
  const reason = pick(REASONS)
  const negative = reason === 'damaged' || reason === 'issued'
  const qty = between(1, 60) * (negative ? -1 : 1)
  const daysAgo = Math.floor(i * 0.9)
  const date = new Date(Date.UTC(2026, 8, 10, 9, 0, 0) - daysAgo * 86_400_000 - between(0, 8) * 3_600_000)
  return {
    id: `ADJ-${String(3120 - i).padStart(5, '0')}`,
    sku: pick(products).sku,
    quantity: qty,
    reason,
    notes: pick(NOTES[reason]),
    user: pick(USERS),
    createdAt: date.toISOString(),
  }
})
