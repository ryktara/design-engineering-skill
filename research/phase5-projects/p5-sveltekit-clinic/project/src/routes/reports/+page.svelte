<script lang="ts">
  import Card from '$lib/components/Card.svelte';
  import { patients, practitioners, formatMoney } from '$lib/data/sample';
  import { appointments } from '$lib/stores';

  const outstanding = patients.reduce((s, p) => s + p.balance, 0);
  const withBalance = patients.filter((p) => p.balance > 0).length;

  const perPractitioner = $derived(
    practitioners.map((pr) => ({
      ...pr,
      count: $appointments.filter((a) => a.practitionerId === pr.id).length,
      done: $appointments.filter((a) => a.practitionerId === pr.id && a.status === 'done').length,
      noShow: $appointments.filter((a) => a.practitionerId === pr.id && a.status === 'no-show').length
    }))
  );

  const maxCount = $derived(Math.max(1, ...perPractitioner.map((p) => p.count)));
</script>

<svelte:head><title>Reports · ClinicBoard</title></svelte:head>

<div class="flex flex-col gap-4">
  <div>
    <h2 class="text-xl font-semibold">Reports</h2>
    <p class="text-sm text-neutral-500">Today at a glance</p>
  </div>

  <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
    <Card>
      <p class="text-xs uppercase tracking-wide text-neutral-500">Appointments</p>
      <p class="text-2xl font-semibold tabular-nums mt-1">{$appointments.length}</p>
    </Card>
    <Card>
      <p class="text-xs uppercase tracking-wide text-neutral-500">No-shows</p>
      <p class="text-2xl font-semibold tabular-nums mt-1 text-danger-700">{$appointments.filter((a) => a.status === 'no-show').length}</p>
    </Card>
    <Card>
      <p class="text-xs uppercase tracking-wide text-neutral-500">Outstanding balance</p>
      <p class="text-2xl font-semibold tabular-nums mt-1 text-warning-700">{formatMoney(outstanding)}</p>
    </Card>
    <Card>
      <p class="text-xs uppercase tracking-wide text-neutral-500">Patients with balance</p>
      <p class="text-2xl font-semibold tabular-nums mt-1">{withBalance} <span class="text-sm font-normal text-neutral-500">of {patients.length}</span></p>
    </Card>
  </div>

  <Card title="Appointments by practitioner">
    <ul class="flex flex-col gap-3">
      {#each perPractitioner as pr (pr.id)}
        <li class="grid grid-cols-[200px_1fr_120px] items-center gap-4 text-sm">
          <span class="font-medium truncate">{pr.name}</span>
          <div class="h-3 bg-neutral-100 rounded-sm overflow-hidden">
            <div class="h-full bg-primary-500" style="width: {(pr.count / maxCount) * 100}%"></div>
          </div>
          <span class="text-neutral-500 tabular-nums text-right">{pr.count} booked · {pr.done} done</span>
        </li>
      {/each}
    </ul>
  </Card>
</div>
