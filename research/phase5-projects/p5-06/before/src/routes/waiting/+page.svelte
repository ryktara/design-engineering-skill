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

  const byStatus = $derived(
    Object.fromEntries(
      columns.map((c) => [c.id, $appointments.filter((a) => a.status === c.id)])
    ) as Record<AppointmentStatus, Appointment[]>
  );

  const scheduled = $derived($appointments.filter((a) => a.status === 'scheduled'));

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
      <section class="bg-neutral-100 border border-neutral-200 rounded flex flex-col min-h-[320px]">
        <header class="flex items-center justify-between px-3 h-11 border-b border-neutral-200">
          <div class="flex items-center gap-2">
            <h3 class="text-sm font-semibold">{col.title}</h3>
            <Badge tone={col.tone}>{byStatus[col.id].length}</Badge>
          </div>
        </header>
        <ul class="flex flex-col gap-2 p-2">
          {#each byStatus[col.id] as appt (appt.id)}
            {@const patient = patientById(appt.patientId)}
            {@const practitioner = practitionerById(appt.practitionerId)}
            <li class="bg-white border border-neutral-200 rounded p-3 text-sm flex flex-col gap-2">
              <div class="flex items-start justify-between gap-2">
                <div class="min-w-0">
                  <p class="font-semibold truncate">{patient ? fullName(patient) : appt.patientId}</p>
                  <p class="text-neutral-500 truncate">{appt.reason}</p>
                </div>
                <span class="tabular-nums text-neutral-500 shrink-0">{appt.start}</span>
              </div>
              <p class="text-xs text-neutral-500">{practitioner?.name}</p>
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
