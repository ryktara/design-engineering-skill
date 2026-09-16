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
  const now = Date.now();
  appointments.update((list) =>
    list.map((a) => {
      if (a.id !== id) return a;
      const next: Appointment = { ...a, status };
      // Stamp arrival on first check-in; stamp call-in when the practitioner takes them.
      // Moving back keeps the arrival time so the wait clock keeps counting from arrival.
      if (status === 'checked-in') {
        next.checkedInAt = a.checkedInAt ?? now;
        next.calledInAt = undefined;
      } else if (status === 'in-progress') {
        next.checkedInAt = a.checkedInAt ?? now;
        next.calledInAt = a.calledInAt ?? now;
      } else if (status === 'scheduled' || status === 'no-show') {
        next.checkedInAt = undefined;
        next.calledInAt = undefined;
      }
      return next;
    })
  );
}

export function addAppointment(a: Omit<Appointment, 'id' | 'status'>) {
  appointments.update((list) => [
    ...list,
    { ...a, id: `a-${Date.now()}`, status: 'scheduled' as const }
  ]);
}
