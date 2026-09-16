<script lang="ts">
  import Card from '$lib/components/Card.svelte';
  import Tabs from '$lib/components/Tabs.svelte';
  import Badge from '$lib/components/Badge.svelte';
  import Button from '$lib/components/Button.svelte';
  import Table from '$lib/components/Table.svelte';
  import {
    fullName,
    formatDate,
    formatMoney,
    practitionerById,
    type Visit,
    type Invoice
  } from '$lib/data/sample';
  import type { PageData } from './$types';

  let { data }: { data: PageData } = $props();

  const patient = $derived(data.patient);

  // Totals for the billing tab, so the amounts in the Amount column visibly add
  // up to the balance shown in the patient header.
  const billedTotal = $derived(data.invoices.reduce((sum, i) => sum + i.amount, 0));
  const outstandingTotal = $derived(
    data.invoices.filter((i) => !i.paid).reduce((sum, i) => sum + i.amount, 0)
  );

  const tabs = [
    { id: 'summary', label: 'Summary' },
    { id: 'visits', label: 'Visits' },
    { id: 'billing', label: 'Billing' }
  ];
  let active = $state('summary');

  function age(dob: string) {
    const [y, m, d] = dob.split('-').map(Number);
    const now = new Date();
    let a = now.getFullYear() - y;
    if (now.getMonth() + 1 < m || (now.getMonth() + 1 === m && now.getDate() < d)) a -= 1;
    return a;
  }

  const visitColumns = [
    { key: 'date', label: 'Date', render: (v: Visit) => formatDate(v.date), width: '130px' },
    { key: 'practitionerId', label: 'Practitioner', render: (v: Visit) => practitionerById(v.practitionerId)?.name ?? '', width: '200px' },
    { key: 'reason', label: 'Reason', width: '200px' },
    { key: 'summary', label: 'Summary' }
  ];

  const invoiceColumns = [
    { key: 'date', label: 'Date', render: (i: Invoice) => formatDate(i.date), width: '130px' },
    { key: 'description', label: 'Description' },
    { key: 'paid', label: 'Status', width: '110px' },
    { key: 'amount', label: 'Amount', align: 'right' as const, width: '120px', render: (i: Invoice) => formatMoney(i.amount) }
  ];
</script>

<svelte:head><title>{fullName(patient)} · ClinicBoard</title></svelte:head>

<div class="flex flex-col gap-4">
  <nav class="text-sm text-neutral-500" aria-label="Breadcrumb">
    <a href="/patients" class="hover:text-neutral-800 hover:underline">Patients</a>
    <span class="mx-1">/</span>
    <span class="text-neutral-800">{fullName(patient)}</span>
  </nav>

  <div class="flex items-start justify-between gap-4 flex-wrap">
    <div class="flex items-center gap-4">
      <span class="inline-flex h-12 w-12 items-center justify-center rounded-full bg-primary-100 text-primary-700 text-base font-semibold">
        {patient.firstName[0]}{patient.lastName[0]}
      </span>
      <div>
        <h2 class="text-xl font-semibold leading-tight">{fullName(patient)}</h2>
        <p class="text-sm text-neutral-500">
          {age(patient.dob)} years · DOB {formatDate(patient.dob)} · {patient.id.toUpperCase()}
        </p>
      </div>
    </div>
    <div class="flex items-center gap-2">
      {#if patient.balance > 0}
        <Badge tone="warning">Balance {formatMoney(patient.balance)}</Badge>
      {:else}
        <Badge tone="success">No balance</Badge>
      {/if}
      <Button>Edit</Button>
      <Button variant="primary">Book appointment</Button>
    </div>
  </div>

  <Card>
    <Tabs {tabs} bind:active>
      {#snippet children(tab)}
        {#if tab === 'summary'}
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <dl class="grid grid-cols-[140px_1fr] gap-y-3 text-sm">
              <dt class="text-neutral-500">Phone</dt>
              <dd class="tabular-nums">{patient.phone}</dd>
              <dt class="text-neutral-500">Email</dt>
              <dd>{patient.email}</dd>
              <dt class="text-neutral-500">Last visit</dt>
              <dd>{formatDate(patient.lastVisit)}</dd>
              <dt class="text-neutral-500">Allergies</dt>
              <dd class="flex flex-wrap gap-1">
                {#each patient.allergies as a (a)}
                  <Badge tone="danger">{a}</Badge>
                {:else}
                  <span class="text-neutral-500">None recorded</span>
                {/each}
              </dd>
            </dl>
            <div class="text-sm">
              <h3 class="font-semibold mb-2">Front desk notes</h3>
              {#if patient.notes}
                <p class="p-3 rounded border border-neutral-200 bg-neutral-50">{patient.notes}</p>
              {:else}
                <p class="text-neutral-500">No notes.</p>
              {/if}
            </div>
          </div>
        {:else if tab === 'visits'}
          <div class="-m-4 border-t border-neutral-200">
            <Table columns={visitColumns} rows={data.visits} empty="No visits recorded." />
          </div>
        {:else}
          <div class="-m-4 border-t border-neutral-200">
            <Table columns={invoiceColumns} rows={data.invoices} empty="No invoices.">
              {#snippet cell(row, col)}
                {#if col.key === 'paid'}
                  {#if row.paid}
                    <Badge tone="success">Paid</Badge>
                  {:else}
                    <Badge tone="warning">Outstanding</Badge>
                  {/if}
                {:else if col.render}
                  {col.render(row)}
                {:else}
                  {String((row as unknown as Record<string, unknown>)[col.key] ?? '')}
                {/if}
              {/snippet}
              {#snippet footer(columns)}
                <tr>
                  <th
                    scope="row"
                    colspan={columns.length - 1}
                    class="px-4 h-10 text-left text-sm font-medium text-neutral-500"
                  >
                    Total billed
                  </th>
                  <td class="px-4 h-10 text-right text-sm text-neutral-800 tabular-nums">
                    {formatMoney(billedTotal)}
                  </td>
                </tr>
                <tr class="border-t border-neutral-200">
                  <th
                    scope="row"
                    colspan={columns.length - 1}
                    class="px-4 h-10 text-left text-sm font-semibold text-neutral-800"
                  >
                    Outstanding balance
                  </th>
                  <td class="px-4 h-10 text-right text-sm font-semibold text-neutral-800 tabular-nums">
                    {formatMoney(outstandingTotal)}
                  </td>
                </tr>
              {/snippet}
            </Table>
          </div>
        {/if}
      {/snippet}
    </Tabs>
  </Card>
</div>
