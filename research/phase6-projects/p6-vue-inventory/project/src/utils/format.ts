const currency = new Intl.NumberFormat('en-GB', {
  style: 'currency',
  currency: 'GBP',
  minimumFractionDigits: 2,
})

const integer = new Intl.NumberFormat('en-GB')

export function formatMoney(value: number): string {
  return currency.format(value)
}

export function formatInt(value: number): string {
  return integer.format(value)
}

export function formatDate(iso: string): string {
  const d = new Date(iso)
  return d.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}

export function relativeDay(iso: string, now = new Date('2026-09-10T09:00:00Z')): string {
  const diff = Math.round((now.getTime() - new Date(iso).getTime()) / 86_400_000)
  if (diff <= 0) return 'Today'
  if (diff === 1) return 'Yesterday'
  return `${diff} days ago`
}
