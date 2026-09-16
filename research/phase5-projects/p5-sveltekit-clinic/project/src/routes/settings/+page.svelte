<script lang="ts">
  import Card from '$lib/components/Card.svelte';
  import Input from '$lib/components/Input.svelte';
  import Select from '$lib/components/Select.svelte';
  import Button from '$lib/components/Button.svelte';
  import { settings } from '$lib/stores';

  let draft = $state({ ...$settings });
  let saved = $state(false);

  const slotOptions = [10, 15, 20, 30].map((n) => ({ value: String(n), label: `${n} minutes` }));
  const tzOptions = ['Europe/London', 'Europe/Paris', 'America/New_York', 'America/Los_Angeles', 'Asia/Dubai'].map(
    (tz) => ({ value: tz, label: tz })
  );

  let slotLength = $state(String($settings.slotLength));

  function save(e: SubmitEvent) {
    e.preventDefault();
    settings.set({ ...draft, slotLength: Number(slotLength) });
    saved = true;
    setTimeout(() => (saved = false), 2000);
  }

  function reset() {
    draft = { ...$settings };
    slotLength = String($settings.slotLength);
  }
</script>

<svelte:head><title>Settings · ClinicBoard</title></svelte:head>

<div class="flex flex-col gap-4 max-w-2xl">
  <div>
    <h2 class="text-xl font-semibold">Settings</h2>
    <p class="text-sm text-neutral-500">Clinic details and scheduling preferences</p>
  </div>

  <form onsubmit={save} class="flex flex-col gap-4">
    <Card title="Clinic">
      <div class="flex flex-col gap-4">
        <Input label="Clinic name" bind:value={draft.clinicName} required />
        <Select label="Timezone" options={tzOptions} bind:value={draft.timezone} />
      </div>
    </Card>

    <Card title="Scheduling">
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <Select label="Default slot length" options={slotOptions} bind:value={slotLength} />
        <Input
          label="Reminder lead time"
          type="number"
          min="1"
          max="72"
          hint="Hours before the appointment"
          bind:value={draft.reminderHours}
        />
      </div>
    </Card>

    <Card title="Reminders">
      <div class="flex flex-col gap-3 text-sm">
        <label class="flex items-center gap-3">
          <input type="checkbox" class="h-4 w-4 rounded-sm border-neutral-300 accent-primary-600" bind:checked={draft.smsReminders} />
          <span>Send SMS reminders</span>
        </label>
        <label class="flex items-center gap-3">
          <input type="checkbox" class="h-4 w-4 rounded-sm border-neutral-300 accent-primary-600" bind:checked={draft.emailReminders} />
          <span>Send email reminders</span>
        </label>
      </div>
    </Card>

    <div class="flex items-center gap-2">
      <Button variant="primary" type="submit">Save changes</Button>
      <Button onclick={reset}>Reset</Button>
      {#if saved}
        <span class="text-sm text-success-700">Saved.</span>
      {/if}
    </div>
  </form>
</div>
