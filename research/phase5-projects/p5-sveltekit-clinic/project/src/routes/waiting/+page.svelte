<script lang="ts">
  import Badge from '$lib/components/Badge.svelte';
  import Button from '$lib/components/Button.svelte';
  import { patientById, practitionerById, fullName, type Appointment, type AppointmentStatus } from '$lib/data/sample';
  import { appointments, setAppointmentStatus } from '$lib/stores';

  type ColumnDef = { id: AppointmentStatus; title: string; tone: 'primary' | 'warning' | 'success' };

  const columns: ColumnDef[] = [
    { id: 'checked-in', title: 'Checked-in', tone: 'primary' },
    { id: 'in-progress', title: 'With practitioner', tone: 'warning' },
    { id: 'done', title: 'Done', tone: 'success' }
  ];

  /** Wait thresholds in minutes: 15 = getting long, 30 = needs attention. */
  const WARN_AT = 15;
  const LONG_AT = 30;

  // Clock for the wait readouts; ticks every 30 s while the board is open.
  let now = $state(Date.now());
  $effect(() => {
    const t = setInterval(() => (now = Date.now()), 30_000);
    return () => clearInterval(t);
  });

  function minutesBetween(from: number | undefined, to: number | undefined): number | null {
    if (from == null || to == null) return null;
    return Math.max(0, Math.floor((to - from) / 60_000));
  }

  /** Minutes the patient has been (or was) in the waiting room. */
  function waitedMin(a: Appointment): number | null {
    if (a.status === 'checked-in') return minutesBetween(a.checkedInAt, now);
    return minutesBetween(a.checkedInAt, a.calledInAt);
  }

  function waitTone(min: number): 'neutral' | 'warning' | 'danger' {
    if (min >= LONG_AT) return 'danger';
    if (min >= WARN_AT) return 'warning';
    return 'neutral';
  }

  function waitLabel(min: number): string {
    if (min >= LONG_AT) return 'Long wait';
    if (min >= WARN_AT) return 'Getting long';
    return 'Waiting';
  }

  function clock(ms: number | undefined): string {
    if (ms == null) return '';
    return new Date(ms).toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
  }

  function isoTime(ms: number | undefined): string | undefined {
    return ms == null ? undefined : new Date(ms).toISOString();
  }

  const byStatus = $derived(
    Object.fromEntries(
      columns.map((c) => {
        const list = $appointments.filter((a) => a.status === c.id);
        // Longest wait first in the checked-in column so whoever needs attention is at the top.
        if (c.id === 'checked-in') list.sort((x, y) => (x.checkedInAt ?? now) - (y.checkedInAt ?? now));
        return [c.id, list];
      })
    ) as Record<AppointmentStatus, Appointment[]>
  );

  const scheduled = $derived($appointments.filter((a) => a.status === 'scheduled'));

  const longestWait = $derived(
    byStatus['checked-in'].reduce<number>((m, a) => Math.max(m, waitedMin(a) ?? 0), 0)
  );
  const overThreshold = $derived(
    byStatus['checked-in'].filter((a) => (waitedMin(a) ?? 0) >= LONG_AT).length
  );

  function next(status: AppointmentStatus): AppointmentStatus | null {
    if (status === 'checked-in') return 'in-progress';
    if (status === 'in-progress') return 'done';
    return null;
  }

  function prev(status: AppointmentStatus): AppointmentStatus | null {
    if (status === 'in-progress') return 'checked-in';
    if (status === 'done') return 'in-progress';
    return null;
  }
</script>

<svelte:head><title>Waiting room · ClinicBoard</title></svelte:head>

<div class="flex flex-col gap-4 h-full">
  <div class="flex items-end justify-between gap-4 flex-wrap">
    <div>
      <h2 class="text-xl font-semibold">Waiting room</h2>
      <p class="text-sm text-neutral-500">
        {byStatus['checked-in'].length} waiting · {byStatus['in-progress'].length} with practitioner · {scheduled.length} still to arrive
        {#if byStatus['checked-in'].length}
          · longest wait
          <span class="tabular-nums {longestWait >= LONG_AT ? 'text-danger-700 font-medium' : longestWait >= WARN_AT ? 'text-warning-700 font-medium' : ''}">{longestWait} min</span>
        {/if}
      </p>
    </div>
    {#if scheduled.length}
      <div class="flex items-center gap-2 text-sm">
        <span class="text-neutral-500">Check in:</span>
        {#each scheduled.slice(0, 3) as a (a.id)}
          {@const p = patientById(a.patientId)}
          <Button size="sm" onclick={() => setAppointmentStatus(a.id, 'checked-in')}>
            {a.start} · {p ? fullName(p) : a.patientId}
          </Button>
        {/each}
      </div>
    {/if}
  </div>

  <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 items-start">
    {#each columns as col (col.id)}
      <section class="bg-neutral-100 border border-neutral-200 rounded flex flex-col min-h-[320px]" aria-labelledby="col-{col.id}">
        <header class="flex items-center justify-between gap-x-3 gap-y-1 flex-wrap px-3 min-h-11 py-1.5 border-b border-neutral-200">
          <div class="flex items-center gap-2">
            <h3 id="col-{col.id}" class="text-sm font-semibold">{col.title}</h3>
            <Badge tone={col.tone}>{byStatus[col.id].length}</Badge>
          </div>
          {#if col.id === 'checked-in' && overThreshold}
            <Badge tone="danger">{overThreshold} over {LONG_AT} min</Badge>
          {/if}
        </header>
        <ul class="flex flex-col gap-2 p-2">
          {#each byStatus[col.id] as appt (appt.id)}
            {@const patient = patientById(appt.patientId)}
            {@const practitioner = practitionerById(appt.practitionerId)}
            {@const waited = waitedMin(appt)}
            <li class="bg-white border border-neutral-200 rounded p-3 text-sm flex flex-col gap-2">
              <div class="flex items-start justify-between gap-2">
                <div class="min-w-0">
                  <p class="font-semibold truncate">{patient ? fullName(patient) : appt.patientId}</p>
                  <p class="text-neutral-500 truncate">{appt.reason}</p>
                </div>
                <span class="tabular-nums text-neutral-500 shrink-0">{appt.start}</span>
              </div>
              <div class="flex items-center justify-between gap-x-2 gap-y-1 flex-wrap">
                <p class="text-xs text-neutral-500 truncate">{practitioner?.name}</p>
                {#if appt.status === 'checked-in' && waited != null}
                  <!-- Live wait readout: tone plus a text label so colour is never the only signal; fixed digit width so ticks do not reflow. -->
                  <Badge tone={waitTone(waited)}>
                    <span class="inline-flex items-center gap-1">
                      <span>{waitLabel(waited)}</span>
                      <time class="tabular-nums font-semibold inline-block min-w-[2ch] text-right" datetime={isoTime(appt.checkedInAt)} title="Checked in at {clock(appt.checkedInAt)}">{waited}</time>
                      <span>min</span>
                    </span>
                  </Badge>
                {:else if waited != null}
                  <span class="text-xs text-neutral-500 tabular-nums whitespace-nowrap">Waited {waited} min</span>
                {/if}
              </div>
              <div class="flex justify-between gap-2 pt-1 border-t border-neutral-200">
                {#if prev(appt.status)}
                  <Button size="sm" variant="ghost" onclick={() => setAppointmentStatus(appt.id, prev(appt.status)!)}>Back</Button>
                {:else}
                  <span></span>
                {/if}
                {#if next(appt.status)}
                  <Button size="sm" variant={appt.status === 'checked-in' ? 'primary' : 'secondary'} onclick={() => setAppointmentStatus(appt.id, next(appt.status)!)}>
                    {appt.status === 'checked-in' ? 'Call in' : 'Mark done'}
                  </Button>
                {/if}
              </div>
            </li>
          {:else}
            <li class="text-sm text-neutral-500 text-center py-8">Nobody here.</li>
          {/each}
        </ul>
      </section>
    {/each}
  </div>
</div>
