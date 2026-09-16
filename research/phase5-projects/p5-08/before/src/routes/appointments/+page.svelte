<script lang="ts">
  import Button from '$lib/components/Button.svelte';
  import Card from '$lib/components/Card.svelte';
  import Badge from '$lib/components/Badge.svelte';
  import Modal from '$lib/components/Modal.svelte';
  import Input from '$lib/components/Input.svelte';
  import Select from '$lib/components/Select.svelte';
  import {
    practitioners,
    patients,
    patientById,
    practitionerById,
    fullName,
    type Appointment,
    type AppointmentStatus
  } from '$lib/data/sample';
  import { visibleAppointments, practitionerFilter, addAppointment } from '$lib/stores';

  const DAY_START = 8;
  const DAY_END = 18;
  const SLOT_MIN = 30;
  const PX_PER_MIN = 2; // 60px per hour

  const slots = Array.from({ length: ((DAY_END - DAY_START) * 60) / SLOT_MIN }, (_, i) => {
    const total = DAY_START * 60 + i * SLOT_MIN;
    const h = Math.floor(total / 60);
    const m = total % 60;
    return { label: `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`, minutes: total, hour: m === 0 };
  });

  const columns = $derived(
    $practitionerFilter ? practitioners.filter((p) => p.id === $practitionerFilter) : practitioners
  );

  function minutesOf(hhmm: string) {
    const [h, m] = hhmm.split(':').map(Number);
    return h * 60 + m;
  }

  function top(a: Appointment) {
    return (minutesOf(a.start) - DAY_START * 60) * PX_PER_MIN;
  }

  function height(a: Appointment) {
    return a.durationMin * PX_PER_MIN;
  }

  const statusTone: Record<AppointmentStatus, 'neutral' | 'primary' | 'success' | 'warning' | 'danger'> = {
    scheduled: 'neutral',
    'checked-in': 'primary',
    'in-progress': 'warning',
    done: 'success',
    'no-show': 'danger'
  };

  const chipStyle: Record<AppointmentStatus, string> = {
    scheduled: 'bg-white border-neutral-300',
    'checked-in': 'bg-primary-50 border-primary-300',
    'in-progress': 'bg-warning-50 border-warning-500',
    done: 'bg-success-50 border-success-500',
    'no-show': 'bg-danger-50 border-danger-500'
  };

  const practitionerOptions = practitioners.map((p) => ({ value: p.id, label: p.name }));
  const patientOptions = patients
    .map((p) => ({ value: p.id, label: fullName(p) }))
    .sort((a, b) => a.label.localeCompare(b.label));
  const durationOptions = [15, 30, 45, 60].map((n) => ({ value: String(n), label: `${n} min` }));

  let modalOpen = $state(false);
  let form = $state({ patientId: '', practitionerId: '', start: '09:00', durationMin: '30', reason: '' });
  let formError = $state('');

  function submit() {
    if (!form.patientId || !form.practitionerId || !form.start || !form.reason.trim()) {
      formError = 'All fields are required.';
      return;
    }
    addAppointment({
      patientId: form.patientId,
      practitionerId: form.practitionerId,
      start: form.start,
      durationMin: Number(form.durationMin),
      reason: form.reason.trim()
    });
    modalOpen = false;
    formError = '';
    form = { patientId: '', practitionerId: '', start: '09:00', durationMin: '30', reason: '' };
  }

  const today = new Date().toLocaleDateString('en-GB', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  });
</script>

<svelte:head><title>Appointments · ClinicBoard</title></svelte:head>

<div class="flex flex-col gap-4">
  <div class="flex items-end justify-between gap-4 flex-wrap">
    <div>
      <h2 class="text-xl font-semibold">Appointments</h2>
      <p class="text-sm text-neutral-500">{today} · {$visibleAppointments.length} booked</p>
    </div>
    <div class="flex items-end gap-3">
      <Select
        label="Practitioner"
        options={practitionerOptions}
        placeholder="All practitioners"
        bind:value={$practitionerFilter}
        class="w-56"
      />
      <Button variant="primary" onclick={() => (modalOpen = true)}>
        <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M8 3v10M3 8h10" /></svg>
        New appointment
      </Button>
    </div>
  </div>

  <Card padded={false}>
    <div class="overflow-x-auto">
      <div class="min-w-[640px]">
        <!-- Column headers -->
        <div class="grid border-b border-neutral-200 bg-neutral-50" style="grid-template-columns: 72px repeat({columns.length}, minmax(0, 1fr))">
          <div class="h-10"></div>
          {#each columns as pr (pr.id)}
            <div class="h-10 flex flex-col justify-center px-3 border-l border-neutral-200">
              <span class="text-sm font-semibold leading-tight">{pr.name}</span>
              <span class="text-xs text-neutral-500 leading-tight">{pr.role}</span>
            </div>
          {/each}
        </div>

        <!-- Time grid -->
        <div class="grid" style="grid-template-columns: 72px repeat({columns.length}, minmax(0, 1fr))">
          <div class="relative" style="height: {(DAY_END - DAY_START) * 60 * PX_PER_MIN}px">
            {#each slots as slot (slot.minutes)}
              <div
                class="absolute right-0 left-0 pr-2 text-right text-xs tabular-nums {slot.hour ? 'text-neutral-600' : 'text-neutral-400'}"
                style="top: {(slot.minutes - DAY_START * 60) * PX_PER_MIN - 7}px"
              >
                {slot.label}
              </div>
            {/each}
          </div>

          {#each columns as pr (pr.id)}
            <div class="relative border-l border-neutral-200" style="height: {(DAY_END - DAY_START) * 60 * PX_PER_MIN}px">
              {#each slots as slot (slot.minutes)}
                <div
                  class="absolute left-0 right-0 border-t {slot.hour ? 'border-neutral-200' : 'border-neutral-100'}"
                  style="top: {(slot.minutes - DAY_START * 60) * PX_PER_MIN}px"
                ></div>
              {/each}

              {#each $visibleAppointments.filter((a) => a.practitionerId === pr.id) as appt (appt.id)}
                {@const patient = patientById(appt.patientId)}
                <div
                  class="absolute left-1 right-1 rounded border px-2 py-1 overflow-hidden text-xs {chipStyle[appt.status]}"
                  style="top: {top(appt) + 1}px; height: {height(appt) - 2}px"
                  title="{appt.start} · {patient ? fullName(patient) : appt.patientId} · {appt.reason}"
                >
                  <div class="flex items-center justify-between gap-2">
                    <span class="font-semibold truncate">{patient ? fullName(patient) : appt.patientId}</span>
                    <span class="tabular-nums text-neutral-500 shrink-0">{appt.start}</span>
                  </div>
                  {#if appt.durationMin >= 30}
                    <div class="flex items-center justify-between gap-2 mt-0.5">
                      <span class="truncate text-neutral-600">{appt.reason}</span>
                      <Badge tone={statusTone[appt.status]}>{appt.status}</Badge>
                    </div>
                  {/if}
                </div>
              {/each}
            </div>
          {/each}
        </div>
      </div>
    </div>
  </Card>
</div>

<Modal bind:open={modalOpen} title="New appointment">
  <div class="flex flex-col gap-4">
    <Select label="Patient" options={patientOptions} placeholder="Select a patient" bind:value={form.patientId} />
    <Select label="Practitioner" options={practitionerOptions} placeholder="Select a practitioner" bind:value={form.practitionerId} />
    <div class="grid grid-cols-2 gap-4">
      <Input label="Start time" type="time" min="08:00" max="17:45" step="900" bind:value={form.start} />
      <Select label="Duration" options={durationOptions} bind:value={form.durationMin} />
    </div>
    <Input label="Reason" placeholder="e.g. Follow-up" bind:value={form.reason} error={formError} />
  </div>
  {#snippet footer()}
    <Button onclick={() => (modalOpen = false)}>Cancel</Button>
    <Button variant="primary" onclick={submit}>Book appointment</Button>
  {/snippet}
</Modal>
