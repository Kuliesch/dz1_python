const content = document.getElementById("content");
const errorBox = document.getElementById("error");
const healthEl = document.getElementById("health");
const titleEl = document.getElementById("view-title");
const subtitleEl = document.getElementById("view-subtitle");

const views = {
  overview: {
    title: "Overview",
    subtitle: "Каталог, записи player та змонтовані огляди",
    render: renderOverview,
  },
  providers: {
    title: "Providers",
    subtitle: "Провайдери з кількістю ігор у db",
    render: renderProviders,
  },
  games: {
    title: "Games",
    subtitle: "Ігри з датами релізів",
    render: renderGames,
  },
  media: {
    title: "Media",
    subtitle: "Артефакти player / mounter на спільному volume",
    render: renderMedia,
  },
};

async function api(path) {
  const res = await fetch(path);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status} ${path}: ${text}`);
  }
  return res.json();
}

function showError(err) {
  errorBox.hidden = !err;
  errorBox.textContent = err ? String(err.message || err) : "";
}

function fmtDate(value) {
  if (!value) return "—";
  return String(value).slice(0, 10);
}

function fmtBytes(n) {
  if (n == null) return "—";
  if (n < 1024) return `${n} B`;
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`;
  return `${(n / (1024 * 1024)).toFixed(1)} MB`;
}

async function refreshHealth() {
  try {
    const data = await api("/health");
    const ok = data.status === "ok";
    healthEl.textContent = ok ? "API + DB ok" : `degraded · ${data.db}`;
    healthEl.className = `status-pill ${ok ? "ok" : "bad"}`;
  } catch (err) {
    healthEl.textContent = "API unreachable";
    healthEl.className = "status-pill bad";
  }
}

async function renderOverview() {
  const data = await api("/api/summary");
  const c = data.catalog || {};
  const m = data.media || {};
  content.innerHTML = `
    <div class="grid">
      <div class="stat"><div class="label">Providers</div><div class="value">${c.providers ?? 0}</div></div>
      <div class="stat"><div class="label">Games</div><div class="value">${c.games ?? 0}</div></div>
      <div class="stat"><div class="label">With release date</div><div class="value">${c.games_with_release_date ?? 0}</div></div>
      <div class="stat"><div class="label">Mounted reviews</div><div class="value">${m.mounted ?? 0}</div></div>
    </div>
    <div class="panel">
      <div class="panel-header"><h2>Media snapshot</h2></div>
      <table>
        <thead><tr><th>Kind</th><th>Count</th></tr></thead>
        <tbody>
          <tr><td>Recordings</td><td>${m.recordings ?? 0}</td></tr>
          <tr><td>Mounted</td><td>${m.mounted ?? 0}</td></tr>
          <tr><td>Policies</td><td>${m.policies ?? 0}</td></tr>
          <tr><td>Events</td><td>${m.events ?? 0}</td></tr>
        </tbody>
      </table>
    </div>
  `;
}

async function renderProviders() {
  const rows = await api("/api/providers");
  content.innerHTML = `
    <div class="panel">
      <div class="panel-header"><h2>${rows.length} providers</h2></div>
      <table>
        <thead>
          <tr><th>Name</th><th>Slug</th><th>Country</th><th>Games</th><th>Source</th></tr>
        </thead>
        <tbody>
          ${rows
            .map(
              (p) => `
            <tr>
              <td>${p.name}</td>
              <td><span class="tag">${p.slug}</span></td>
              <td>${p.country_code || "—"}</td>
              <td>${p.games_count}</td>
              <td class="muted">${p.source}</td>
            </tr>`
            )
            .join("")}
        </tbody>
      </table>
    </div>
  `;
}

async function renderGames() {
  const rows = await api("/api/games");
  content.innerHTML = `
    <div class="panel">
      <div class="panel-header"><h2>${rows.length} games</h2></div>
      <table>
        <thead>
          <tr><th>Game</th><th>Provider</th><th>Release</th><th>RTP</th><th>Volatility</th></tr>
        </thead>
        <tbody>
          ${rows
            .map(
              (g) => `
            <tr>
              <td>${g.name}<div class="muted">${g.slug}</div></td>
              <td>${g.provider_name}</td>
              <td>${fmtDate(g.release_date)}</td>
              <td>${g.rtp_percent ?? "—"}</td>
              <td>${g.volatility || "—"}</td>
            </tr>`
            )
            .join("")}
        </tbody>
      </table>
    </div>
  `;
}

async function renderMedia() {
  const data = await api("/api/media");
  const section = (title, items, mapRow) => `
    <div class="panel" style="margin-bottom:16px">
      <div class="panel-header"><h2>${title} · ${items.length}</h2></div>
      <table>
        <thead><tr><th>Name</th><th>Size</th></tr></thead>
        <tbody>
          ${
            items.length
              ? items.map(mapRow).join("")
              : `<tr><td colspan="2" class="muted">Порожньо</td></tr>`
          }
        </tbody>
      </table>
    </div>
  `;
  const row = (f) =>
    `<tr><td>${f.name}</td><td>${fmtBytes(f.size_bytes)}</td></tr>`;
  content.innerHTML = `
    ${section("Mounted reviews", data.mounted || [], row)}
    ${section("Recordings", data.recordings || [], row)}
    ${section("Policies", data.policies || [], row)}
    ${section("Events", data.events || [], row)}
  `;
}

async function setView(name) {
  const view = views[name];
  if (!view) return;
  titleEl.textContent = view.title;
  subtitleEl.textContent = view.subtitle;
  document.querySelectorAll(".nav button").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.view === name);
  });
  showError(null);
  content.innerHTML = `<p class="muted">Loading…</p>`;
  try {
    await view.render();
  } catch (err) {
    content.innerHTML = "";
    showError(err);
  }
}

document.getElementById("nav").addEventListener("click", (event) => {
  const btn = event.target.closest("button[data-view]");
  if (!btn) return;
  setView(btn.dataset.view);
});

refreshHealth();
setView("overview");
setInterval(refreshHealth, 15000);
