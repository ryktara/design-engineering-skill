<script lang="ts">
  import '../app.css';
  import { page } from '$app/stores';
  import { clinic, currentUser } from '$lib/data/sample';
  import type { Snippet } from 'svelte';

  let { children }: { children: Snippet } = $props();

  const nav = [
    { href: '/appointments', label: 'Appointments', icon: 'calendar' },
    { href: '/patients', label: 'Patients', icon: 'users' },
    { href: '/waiting', label: 'Waiting room', icon: 'clock' },
    { href: '/reports', label: 'Reports', icon: 'chart' },
    { href: '/settings', label: 'Settings', icon: 'cog' }
  ];

  let menuOpen = $state(false);

  function isActive(href: string, pathname: string) {
    return pathname === href || pathname.startsWith(href + '/');
  }

  const initials = currentUser.name
    .split(' ')
    .map((s) => s[0])
    .join('')
    .toUpperCase();
</script>

<div class="h-screen flex bg-neutral-50 text-neutral-800">
  <!-- Left navigation rail -->
  <aside class="w-60 shrink-0 flex flex-col bg-white border-r border-neutral-200">
    <a href="/appointments" class="flex items-center gap-2 h-14 px-4 border-b border-neutral-200">
      <span class="inline-flex h-7 w-7 items-center justify-center rounded bg-primary-600 text-white">
        <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
          <path d="M8 3v10M3 8h10" />
        </svg>
      </span>
      <span class="text-base font-semibold tracking-tight">ClinicBoard</span>
    </a>

    <nav class="flex-1 overflow-y-auto p-2" aria-label="Primary">
      <ul class="flex flex-col gap-0.5">
        {#each nav as item (item.href)}
          {@const active = isActive(item.href, $page.url.pathname)}
          <li>
            <a
              href={item.href}
              aria-current={active ? 'page' : undefined}
              class="flex items-center gap-3 h-9 px-3 rounded text-sm font-medium transition-colors {active
                ? 'bg-primary-50 text-primary-700'
                : 'text-neutral-600 hover:bg-neutral-100 hover:text-neutral-800'}"
            >
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="shrink-0">
                {#if item.icon === 'calendar'}
                  <rect x="2" y="3" width="12" height="11" rx="1.5" /><path d="M2 7h12M5 1.5v3M11 1.5v3" />
                {:else if item.icon === 'users'}
                  <circle cx="6" cy="5" r="2.5" /><path d="M1.5 13.5c0-2.5 2-4 4.5-4s4.5 1.5 4.5 4M11 5.5a2 2 0 0 1 0 4M12.5 9.5c1.3.5 2 1.7 2 3.5" />
                {:else if item.icon === 'clock'}
                  <circle cx="8" cy="8" r="6.5" /><path d="M8 4.5V8l2.5 1.5" />
                {:else if item.icon === 'chart'}
                  <path d="M2 14h12M4 11V7M8 11V4M12 11V9" />
                {:else}
                  <circle cx="8" cy="8" r="2" /><path d="M8 1.5v2M8 12.5v2M1.5 8h2M12.5 8h2M3.4 3.4l1.4 1.4M11.2 11.2l1.4 1.4M3.4 12.6l1.4-1.4M11.2 4.8l1.4-1.4" />
                {/if}
              </svg>
              {item.label}
            </a>
          </li>
        {/each}
      </ul>
    </nav>

    <div class="p-4 border-t border-neutral-200 text-xs text-neutral-500">
      <p class="font-medium text-neutral-700">{clinic.name}</p>
      <p>{clinic.openingHours}</p>
    </div>
  </aside>

  <!-- Main column -->
  <div class="flex-1 min-w-0 flex flex-col">
    <header class="h-14 shrink-0 flex items-center justify-between px-6 bg-white border-b border-neutral-200">
      <div class="flex items-center gap-3">
        <h1 class="text-base font-semibold">{clinic.name}</h1>
        <span class="text-sm text-neutral-500">Front desk</span>
      </div>
      <div class="relative">
        <button
          type="button"
          class="flex items-center gap-2 h-9 pl-1 pr-3 rounded border border-transparent hover:bg-neutral-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500"
          aria-haspopup="menu"
          aria-expanded={menuOpen}
          onclick={() => (menuOpen = !menuOpen)}
        >
          <span class="inline-flex h-7 w-7 items-center justify-center rounded-full bg-primary-100 text-primary-700 text-xs font-semibold">
            {initials}
          </span>
          <span class="text-sm font-medium">{currentUser.name}</span>
          <svg width="12" height="12" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 6l4 4 4-4" />
          </svg>
        </button>
        {#if menuOpen}
          <div role="menu" class="absolute right-0 mt-1 w-48 bg-white border border-neutral-200 rounded py-1 text-sm z-40">
            <p class="px-3 py-2 text-xs text-neutral-500 border-b border-neutral-200">
              Signed in as <span class="font-medium text-neutral-700">{currentUser.role}</span>
            </p>
            <a href="/settings" role="menuitem" class="block px-3 py-2 hover:bg-neutral-100" onclick={() => (menuOpen = false)}>Settings</a>
            <button type="button" role="menuitem" class="w-full text-left px-3 py-2 hover:bg-neutral-100" onclick={() => (menuOpen = false)}>Sign out</button>
          </div>
        {/if}
      </div>
    </header>

    <main class="flex-1 min-h-0 overflow-y-auto p-6">
      {@render children()}
    </main>
  </div>
</div>
