<script lang="ts">
  import { tick } from 'svelte';
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
  import { visibleAppointments, practitionerFilter, addAppointment, moveAppointment } from '$lib/stores';

  const DAY_START = 8;
  const DAY_END = 18;
  const SLOT_MIN = 30;
  const SNAP_MIN = 15; // drag / arrow-key step
  const DAY_MIN = (DAY_END - DAY_START) * 60;

  // Touch sizing: the shortest booking is 15 min, so at the pointer scale (2px/min)
  // a chip is 28px tall — below the 44px touch target the front desk needs on a
  // tablet. On coarse pointers / tablet widths the day scales to 3px/min so the
  // shortest chip is 45px. Same grid, same chips — only the minute scale changes.
  const PX_PER_MIN_FINE = 2; // 120px per hour
  const PX_PER_MIN_TOUCH = 3.2; // 192px per hour: 15 min = 48px, 44px chip + 4px gap
  const TOUCH_QUERY = '(pointer: coarse), (max-width: 1024px)';
  const MIN_DETAIL_PX = 44; // below this a chip only has room for name + time

  let touchScale = $state(false);
  $effect(() => {
    const mq = window.matchMedia(TOUCH_QUERY);
    touchScale = mq.matches;
    const onChange = (e: MediaQueryListEvent) => (touchScale = e.matches);
    mq.addEventListener('change', onChange);
    return () => mq.removeEventListener('change', onChange);
  });

  const PX_PER_MIN = $derived(touchScale ? PX_PER_MIN_TOUCH : PX_PER_MIN_FINE);
  const GRID_HEIGHT = $derived(DAY_MIN * PX_PER_MIN);
  // Inset around each chip: the gap between two back-to-back bookings. 2px on touch
  // keeps a 4px separation between adjacent 44px targets.
  const CHIP_INSET = $derived(touchScale ? 2 : 1);

  const slots = Array.from({ length: DAY_MIN / SLOT_MIN }, (_, i) => {
    const total = DAY_START * 60 + i * SLOT_MIN;
    const h = Math.floor(total / 60);
    const m = total % 60;
    return { label: `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`, minutes: total, hour: m === 0 };
  });

  const columns = $derived(
    $practitionerFilter ? practitioners.filter((p) => p.id === $practitionerFilter) : practitioners
  );

  // Bucket the day's chips per practitioner once per store change instead of
  // re-filtering the whole list inside every column. Unchanged records keep their
  // object identity, so keyed chips are left alone when one record moves.
  const byPractitioner = $derived.by(() => {
    const map: Record<string, Appointment[]> = {};
    for (const a of $visibleAppointments) (map[a.practitionerId] ??= []).push(a);
    return map;
  });

  function minutesOf(hhmm: string) {
    const [h, m] = hhmm.split(':').map(Number);
    return h * 60 + m;
  }

  function hhmm(minutes: number) {
    return `${String(Math.floor(minutes / 60)).padStart(2, '0')}:${String(minutes % 60).padStart(2, '0')}`;
  }

  function top(a: Appointment) {
    return (minutesOf(a.start) - DAY_START * 60) * PX_PER_MIN;
  }

  function height(a: Appointment) {
    return a.durationMin * PX_PER_MIN;
  }

  function clampStart(minutes: number, durationMin: number) {
    const lo = DAY_START * 60;
    const hi = DAY_END * 60 - durationMin;
    return Math.min(hi, Math.max(lo, minutes));
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

  // ---- Reschedule: drag (pointer) and arrow keys (keyboard) -------------------
  // Render-affecting drag state only. Geometry lives in `dragCtx` (not reactive) so a
  // pointermove touches the dragged chip and the drop ghost, nothing else.
  type DragView = { id: string; dx: number; dy: number; toPr: string; toTop: number; toStart: string; h: number };
  let drag = $state<DragView | null>(null);
  let dragCtx: {
    appt: Appointment;
    fromPr: string;
    startX: number;
    startY: number;
    originTop: number;
    moved: boolean;
    cols: { id: string; left: number; right: number }[];
    el: HTMLElement;
  } | null = null;
  let gridEl: HTMLElement | undefined = $state();

  /** Visible + polite-live status line for the last move; cleared after a few seconds. */
  let moveStatus = $state('');
  let statusTimer: ReturnType<typeof setTimeout> | undefined;
  async function announce(msg: string) {
    clearTimeout(statusTimer);
    moveStatus = '';
    await tick();
    moveStatus = msg;
    statusTimer = setTimeout(() => (moveStatus = ''), 6000);
  }

  function chipName(a: Appointment) {
    const p = patientById(a.patientId);
    return p ? fullName(p) : a.patientId;
  }

  async function commitMove(a: Appointment, toPr: string, toMinutes: number, restoreFocus = false) {
    const start = hhmm(clampStart(toMinutes, a.durationMin));
    if (toPr === a.practitionerId && start === a.start) return;
    moveAppointment(a.id, toPr, start);
    const pr = practitionerById(toPr);
    announce(`${chipName(a)} moved to ${start} with ${pr ? pr.name : toPr}`);
    if (restoreFocus) {
      // Moving across columns re-creates the chip in another keyed block; put focus back on it.
      await tick();
      gridEl?.querySelector<HTMLElement>(`[data-chip="${a.id}"]`)?.focus();
    }
  }

  function startDrag(e: PointerEvent, a: Appointment, prId: string) {
    if (e.button !== 0 || !gridEl) return;
    const el = e.currentTarget as HTMLElement;
    // Measure the columns once; pointermove is pure arithmetic after this.
    const cols = Array.from(gridEl.querySelectorAll<HTMLElement>('[data-col]')).map((c) => {
      const r = c.getBoundingClientRect();
      return { id: c.dataset.col as string, left: r.left, right: r.right };
    });
    dragCtx = { appt: a, fromPr: prId, startX: e.clientX, startY: e.clientY, originTop: top(a), moved: false, cols, el };
    el.setPointerCapture(e.pointerId);
  }

  function moveDrag(e: PointerEvent) {
    const ctx = dragCtx;
    if (!ctx) return;
    const dy = e.clientY - ctx.startY;
    const rawDx = e.clientX - ctx.startX;
    if (!ctx.moved && Math.abs(dy) + Math.abs(rawDx) < 4) return; // click tolerance
    ctx.moved = true;
    const from = ctx.cols.find((c) => c.id === ctx.fromPr) ?? ctx.cols[0];
    const target = ctx.cols.find((c) => e.clientX >= c.left && e.clientX < c.right) ?? (drag ? ctx.cols.find((c) => c.id === drag!.toPr) : from) ?? from;
    const minutes = clampStart(
      DAY_START * 60 + Math.round((ctx.originTop + dy) / PX_PER_MIN / SNAP_MIN) * SNAP_MIN,
      ctx.appt.durationMin
    );
    const toTop = (minutes - DAY_START * 60) * PX_PER_MIN;
    const next: DragView = {
      id: ctx.appt.id,
      dx: target.left - from.left,
      dy,
      toPr: target.id,
      toTop,
      toStart: hhmm(minutes),
      h: height(ctx.appt)
    };
    if (!drag) drag = next;
    else {
      // Assign fields individually so only the bindings that changed re-run.
      if (drag.dx !== next.dx) drag.dx = next.dx;
      drag.dy = next.dy;
      if (drag.toPr !== next.toPr) drag.toPr = next.toPr;
      if (drag.toTop !== next.toTop) drag.toTop = next.toTop;
      if (drag.toStart !== next.toStart) drag.toStart = next.toStart;
    }
  }

  function endDrag(e: PointerEvent) {
    const ctx = dragCtx;
    if (!ctx) return;
    ctx.el.releasePointerCapture(e.pointerId);
    const view = drag;
    dragCtx = null;
    drag = null;
    if (ctx.moved && view) commitMove(ctx.appt, view.toPr, minutesOf(view.toStart));
  }

  function cancelDrag() {
    if (!dragCtx) return;
    dragCtx = null;
    drag = null;
  }

  function chipKey(e: KeyboardEvent, a: Appointment, prId: string) {
    if (e.altKey || e.ctrlKey || e.metaKey) return;
    if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
      e.preventDefault();
      commitMove(a, prId, minutesOf(a.start) + (e.key === 'ArrowUp' ? -SNAP_MIN : SNAP_MIN), true);
    } else if ((e.key === 'ArrowLeft' || e.key === 'ArrowRight') && columns.length > 1) {
      e.preventDefault();
      const i = columns.findIndex((c) => c.id === prId);
      const j = i + (e.key === 'ArrowLeft' ? -1 : 1);
      if (j >= 0 && j < columns.length) commitMove(a, columns[j].id, minutesOf(a.start), true);
    }
  }

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

<svelte:window onkeydown={(e) => e.key === 'Escape' && dragCtx && cancelDrag()} />

<div class="flex flex-col gap-4">
  <div class="flex items-end justify-between gap-4 flex-wrap">
    <!-- min-w-0 + flex-1: the block's width comes from the row, not from the status text,
         so a status appearing or clearing never rewraps the date line above the grid -->
    <div class="min-w-0 flex-1">
      <h2 class="text-xl font-semibold">Appointments</h2>
      <p class="text-sm text-neutral-500">
        {today} · {$visibleAppointments.length} booked
        <span class="text-neutral-400"> · Drag a chip or use the arrow keys to reschedule</span>
      </p>
      <!-- Fixed one-line height so the grid never shifts when the status appears or clears -->
      <p class="text-sm text-primary-700 h-5 truncate" aria-live="polite" data-move-status title={moveStatus}>{moveStatus}</p>
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
        <div
          class="grid {drag ? 'select-none' : ''}"
          style="grid-template-columns: 72px repeat({columns.length}, minmax(0, 1fr))"
          bind:this={gridEl}
        >
          <div class="relative" style="height: {GRID_HEIGHT}px">
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
            <div class="relative border-l border-neutral-200" style="height: {GRID_HEIGHT}px" data-col={pr.id}>
              {#each slots as slot (slot.minutes)}
                <div
                  class="absolute left-0 right-0 border-t {slot.hour ? 'border-neutral-200' : 'border-neutral-100'}"
                  style="top: {(slot.minutes - DAY_START * 60) * PX_PER_MIN}px"
                ></div>
              {/each}

              <!-- Drop target: where the dragged chip will land, with the snapped time -->
              {#if drag && drag.toPr === pr.id}
                <div
                  aria-hidden="true"
                  data-drop-ghost
                  class="absolute left-1 right-1 rounded border-2 border-dashed border-primary-500 bg-primary-50/70 pointer-events-none z-10"
                  style="top: {drag.toTop + CHIP_INSET}px; height: {drag.h - 2 * CHIP_INSET}px"
                >
                  <span class="absolute top-0.5 left-1 px-1 rounded-sm bg-primary-600 text-white text-[11px] leading-4 tabular-nums">
                    {drag.toStart}
                  </span>
                </div>
              {/if}

              {#each byPractitioner[pr.id] ?? [] as appt (appt.id)}
                {@const name = chipName(appt)}
                {@const dragging = drag?.id === appt.id}
                <div
                  role="button"
                  tabindex="0"
                  data-chip={appt.id}
                  aria-label="{name}, {appt.start}, {appt.durationMin} minutes, {pr.name}. Arrow keys move the appointment."
                  class="absolute left-1 right-1 rounded border pl-1 pr-2 py-1 overflow-hidden text-xs flex gap-1 cursor-grab select-none touch-none
                    focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:z-20 {chipStyle[appt.status]}
                    {dragging ? 'cursor-grabbing shadow-md z-30 will-change-transform' : ''}"
                  style="top: {top(appt) + CHIP_INSET}px; height: {height(appt) - 2 * CHIP_INSET}px;{dragging ? ` transform: translate(${drag!.dx}px, ${drag!.dy}px);` : ''}"
                  title="{appt.start} · {name} · {appt.reason} — drag or use the arrow keys to reschedule"
                  onpointerdown={(e) => startDrag(e, appt, pr.id)}
                  onpointermove={moveDrag}
                  onpointerup={endDrag}
                  onpointercancel={cancelDrag}
                  onkeydown={(e) => chipKey(e, appt, pr.id)}
                >
                  <!-- Grip: always visible (no hover reveal), quiet -->
                  <svg aria-hidden="true" width="6" height="10" viewBox="0 0 6 10" class="shrink-0 mt-0.5 text-neutral-400" fill="currentColor">
                    <circle cx="1.5" cy="1.5" r="1" /><circle cx="4.5" cy="1.5" r="1" />
                    <circle cx="1.5" cy="5" r="1" /><circle cx="4.5" cy="5" r="1" />
                    <circle cx="1.5" cy="8.5" r="1" /><circle cx="4.5" cy="8.5" r="1" />
                  </svg>
                  <div class="min-w-0 flex-1">
                    <div class="flex items-center justify-between gap-2">
                      <span class="font-semibold truncate">{name}</span>
                      <span class="tabular-nums text-neutral-500 shrink-0">{appt.start}</span>
                    </div>
                    {#if height(appt) - 2 * CHIP_INSET >= MIN_DETAIL_PX}
                      <div class="flex items-center justify-between gap-2 mt-0.5">
                        <span class="truncate text-neutral-600">{appt.reason}</span>
                        <Badge tone={statusTone[appt.status]}>{appt.status}</Badge>
                      </div>
                    {/if}
                  </div>
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
