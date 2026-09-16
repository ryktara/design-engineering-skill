import { writable, derived } from 'svelte/store';
import { appointments as seed, type Appointment, type AppointmentStatus } from '$lib/data/sample';

/** In-memory appointment list. Mutations affect the running session only. */
export const appointments = writable<Appointment[]>(seed.map((a) => ({ ...a })));

/** Practitioner filter for the day view; empty string means "all". */
export const practitionerFilter = writable<string>('');

/** Free-text search on the patients list. */
export const patientSearch = writable<string>('');

/** Settings form values. */
export const settings = writable({
  clinicName: 'Riverside Family Clinic',
  slotLength: 15,
  reminderHours: 24,
  timezone: 'Europe/London',
  smsReminders: true,
  emailReminders: true
});

export const visibleAppointments = derived(
  [appointments, practitionerFilter],
  ([$appointments, $filter]) =>
    $filter ? $appointments.filter((a) => a.practitionerId === $filter) : $appointments
);

export function setAppointmentStatus(id: string, status: AppointmentStatus) {
  appointments.update((list) => list.map((a) => (a.id === id ? { ...a, status } : a)));
}

export function addAppointment(a: Omit<Appointment, 'id' | 'status'>) {
  appointments.update((list) => [
    ...list,
    { ...a, id: `a-${Date.now()}`, status: 'scheduled' as const }
  ]);
}
