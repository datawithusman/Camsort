import backend from "./repositories/BackEnd.js";

const runtimeConfig = window.CAMBOT_CONFIG || {};

backend.configure({
  cambotBaseUrl: runtimeConfig.cambotBaseUrl || runtimeConfig.cambotApiBasePath || "/api",
  cameraSystemBaseUrl:
    runtimeConfig.cameraSystemBaseUrl ||
    runtimeConfig.cameraSystemApiBasePath ||
    "/api/camera-system",
});

window.CamBotBackend = backend;

const STORAGE_KEY = "cambot.client.prompts.v1";
const AUTH_STORAGE_KEY = "cambot.client.basicAuth.v1";

const state = {
  prompts: loadPrompts(),
  selectedPromptId: null,
  cameras: [],
  results: [],
  runningPromptIds: new Set(),
  scheduleTimers: new Map(),
  objectUrls: [],
};

const el = {
  loginView: document.getElementById("login-view"),
  dashboardView: document.getElementById("dashboard-view"),
  loginForm: document.getElementById("login-form"),
  loginUser: document.getElementById("login-user"),
  loginPass: document.getElementById("login-pass"),
  loginError: document.getElementById("login-error"),
  logoutBtn: document.getElementById("logout-btn"),
  healthPill: document.getElementById("health-pill"),
  refreshCamerasBtn: document.getElementById("refresh-cameras-btn"),
  promptForm: document.getElementById("prompt-form"),
  promptId: document.getElementById("prompt-id"),
  promptName: document.getElementById("prompt-name"),
  promptType: document.getElementById("prompt-type"),
  promptText: document.getElementById("prompt-text"),
  cameraLimit: document.getElementById("camera-limit"),
  cameraSearch: document.getElementById("camera-search"),
  resetPromptBtn: document.getElementById("reset-prompt-btn"),
  promptList: document.getElementById("prompt-list"),
  promptCount: document.getElementById("prompt-count"),
  selectedPrompt: document.getElementById("selected-prompt"),
  runScanBtn: document.getElementById("run-scan-btn"),
  scheduleBtn: document.getElementById("schedule-btn"),
  scanBanner: document.getElementById("scan-banner"),
  emptyResults: document.getElementById("empty-results"),
  resultGrid: document.getElementById("result-grid"),
  resultsTitle: document.getElementById("results-title"),
  resultsSubtitle: document.getElementById("results-subtitle"),
  cameraCount: document.getElementById("camera-count"),
  scheduledCount: document.getElementById("scheduled-count"),
  runningCount: document.getElementById("running-count"),
  activityList: document.getElementById("activity-list"),
  toast: document.getElementById("toast"),
};

installEventHandlers();
bootstrapPromptState();
renderAll();
restoreCachedLogin();

function installEventHandlers() {
  el.loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    await connect();
  });

  el.logoutBtn.addEventListener("click", () => {
    clearCachedLogin();
    backend.clearBasicAuth();
    for (const timer of state.scheduleTimers.values()) {
      window.clearInterval(timer);
    }
    state.scheduleTimers.clear();
    showLoginView();
  });

  el.refreshCamerasBtn.addEventListener("click", async () => {
    await refreshCameras();
  });

  el.promptForm.addEventListener("submit", (event) => {
    event.preventDefault();
    savePromptFromForm();
  });

  el.resetPromptBtn.addEventListener("click", () => {
    clearPromptForm();
  });

  el.selectedPrompt.addEventListener("change", () => {
    state.selectedPromptId = el.selectedPrompt.value || null;
    renderAll();
  });

  el.runScanBtn.addEventListener("click", async () => {
    await runSelectedPromptScan();
  });

  el.scheduleBtn.addEventListener("click", () => {
    toggleSelectedPromptSchedule();
  });
}

async function restoreCachedLogin() {
  const cached = readCachedLogin();
  if (!cached) {
    showLoginView();
    return;
  }

  el.loginUser.value = cached.username || "";
  el.loginPass.value = cached.password || "";

  try {
    backend.setBasicAuth(cached.username, cached.password);
    await checkHealth();
    showDashboardView();
    await refreshCameras();
  } catch (error) {
    clearCachedLogin();
    backend.clearBasicAuth();
    showLoginView();
    showLoginError(`Saved login failed: ${errorToMessage(error)}`);
  }
}

function showDashboardView() {
  el.loginView.hidden = true;
  el.dashboardView.hidden = false;
  document.body.classList.add("is-authenticated");
}

function showLoginView() {
  el.dashboardView.hidden = true;
  el.loginView.hidden = false;
  document.body.classList.remove("is-authenticated");
}

function cacheLogin(username, password) {
  try {
    window.localStorage.setItem(
      AUTH_STORAGE_KEY,
      JSON.stringify({ username, password })
    );
  } catch {
    // Browser storage may be blocked. The session can still continue.
  }
}

function readCachedLogin() {
  try {
    const raw = window.localStorage.getItem(AUTH_STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    if (!parsed?.username || !parsed?.password) return null;
    return parsed;
  } catch {
    return null;
  }
}

function clearCachedLogin() {
  try {
    window.localStorage.removeItem(AUTH_STORAGE_KEY);
  } catch {
    // Ignore storage failures.
  }
}

async function connect() {
  const username = el.loginUser.value.trim();
  const password = el.loginPass.value;

  if (!username || !password) {
    showLoginError("Enter the same Basic Auth credentials you use with curl.");
    return;
  }

  backend.setBasicAuth(username, password);
  el.loginError.hidden = true;

  try {
    await checkHealth();
    cacheLogin(username, password);
    showDashboardView();
    await refreshCameras();
    showToast("Connected to CamBot RestApi.", "good");
  } catch (error) {
    clearCachedLogin();
    backend.clearBasicAuth();
    showLoginError(errorToMessage(error));
  }
}

async function checkHealth() {
  el.healthPill.textContent = "checking...";
  el.healthPill.className = "health-pill";

  try {
    const health = await backend.cambot.health();
    const db = health?.database?.status || "unknown";
    const camera = health?.cameraSystem?.status || "unknown";
    el.healthPill.textContent = `api ok · db ${db} · camera ${camera}`;
    el.healthPill.className = "health-pill ok";
    return health;
  } catch (error) {
    el.healthPill.textContent = "api error";
    el.healthPill.className = "health-pill bad";
    throw error;
  }
}

async function refreshCameras() {
  try {
    const response = await backend.cameraSystem.cameras.list();
    state.cameras = Array.isArray(response?.cameras) ? response.cameras : [];
    el.cameraCount.textContent = String(state.cameras.length);
    renderActivity();
    showToast(`Loaded ${state.cameras.length} cameras.`, "good");
  } catch (error) {
    showToast(`Camera refresh failed: ${errorToMessage(error)}`, "bad");
  }
}

function bootstrapPromptState() {
  if (state.prompts.length === 0) {
    const now = new Date().toISOString();
    state.prompts = [
      {
        id: crypto.randomUUID(),
        name: "Safety priority scan",
        type: "sort",
        text: "Prioritize cameras that show blocked access, unsafe walkways, spills, smoke, crowding, or anything that should be checked first.",
        status: "idle",
        createdAt: now,
        updatedAt: now,
        scheduled: false,
        lastRunAt: null,
        nextRunAt: null,
        lastResultCount: 0,
      },
    ];
    savePrompts();
  }

  state.selectedPromptId = state.prompts[0]?.id || null;
}

function loadPrompts() {
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function savePrompts() {
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state.prompts));
}

function savePromptFromForm() {
  const id = el.promptId.value || crypto.randomUUID();
  const now = new Date().toISOString();
  const existing = state.prompts.find((prompt) => prompt.id === id);

  const prompt = {
    id,
    name: el.promptName.value.trim(),
    type: el.promptType.value,
    text: el.promptText.value.trim(),
    status: existing?.status || "idle",
    createdAt: existing?.createdAt || now,
    updatedAt: now,
    scheduled: existing?.scheduled || false,
    lastRunAt: existing?.lastRunAt || null,
    nextRunAt: existing?.nextRunAt || null,
    lastResultCount: existing?.lastResultCount || 0,
  };

  if (!prompt.name || !prompt.text) {
    showToast("Prompt name and text are required.", "bad");
    return;
  }

  const index = state.prompts.findIndex((item) => item.id === id);
  if (index >= 0) {
    state.prompts[index] = prompt;
  } else {
    state.prompts.unshift(prompt);
  }

  state.selectedPromptId = prompt.id;
  savePrompts();
  clearPromptForm();
  renderAll();
  showToast("Prompt saved.", "good");
}

function clearPromptForm() {
  el.promptId.value = "";
  el.promptName.value = "";
  el.promptType.value = "sort";
  el.promptText.value = "";
  el.cameraLimit.value = "6";
  el.cameraSearch.value = "";
}

function editPrompt(promptId) {
  const prompt = getPrompt(promptId);
  if (!prompt) return;

  el.promptId.value = prompt.id;
  el.promptName.value = prompt.name;
  el.promptType.value = prompt.type;
  el.promptText.value = prompt.text;
  document.querySelector(".prompt-editor")?.setAttribute("open", "");
}

function deletePrompt(promptId) {
  if (state.scheduleTimers.has(promptId)) {
    window.clearInterval(state.scheduleTimers.get(promptId));
    state.scheduleTimers.delete(promptId);
  }

  state.prompts = state.prompts.filter((prompt) => prompt.id !== promptId);
  if (state.selectedPromptId === promptId) {
    state.selectedPromptId = state.prompts[0]?.id || null;
  }
  savePrompts();
  renderAll();
}

function getPrompt(promptId = state.selectedPromptId) {
  return state.prompts.find((prompt) => prompt.id === promptId) || null;
}

async function runSelectedPromptScan() {
  const prompt = getPrompt();
  if (!prompt) {
    showToast("Select or create a prompt first.", "bad");
    return;
  }

  await runPromptScan(prompt.id);
}

async function runPromptScan(promptId) {
  const prompt = getPrompt(promptId);
  if (!prompt) return;

  state.runningPromptIds.add(promptId);
  updatePrompt(promptId, { status: "running" });
  el.scanBanner.hidden = false;
  renderAll();

  try {
    const search = el.cameraSearch.value.trim();
    const limit = clampNumber(Number(el.cameraLimit.value || 6), 1, 20);
    const cameraResponse = await backend.cameraSystem.cameras.list({ search });
    const cameras = (cameraResponse?.cameras || []).slice(0, limit);

    if (cameras.length === 0) {
      state.results = [];
      updatePrompt(promptId, {
        status: prompt.scheduled ? "scheduled" : "idle",
        lastRunAt: new Date().toISOString(),
        lastResultCount: 0,
      });
      showToast("No cameras matched the current filter.", "bad");
      return;
    }

    const results = [];

    for (let index = 0; index < cameras.length; index += 1) {
      const camera = cameras[index];
      const snapshot = await backend.cameraSystem.cameras.getSnapshot(camera.id);
      const frameRef = snapshot.frameRef || backend.cameraSystem.cameras.snapshotToFrameRef(snapshot);
      const frameUrl = backend.cameraSystem.cameras.frameImageUrl(frameRef || snapshot);
      const imageUrl = await loadProtectedImageUrl(frameUrl, snapshot.frame?.mimeType);
      const score = deterministicScore(`${prompt.id}:${camera.id}:${snapshot.frame?.frameId || index}`);

      results.push({
        camera,
        promptId,
        rank: index + 1,
        score,
        reason: buildReason(prompt, camera, score),
        snapshot,
        frameRef,
        imageUrl,
      });
    }

    results.sort((a, b) => b.score - a.score);
    results.forEach((result, index) => {
      result.rank = index + 1;
    });

    revokeResultObjectUrls();
    state.results = results;
    updatePrompt(promptId, {
      status: prompt.scheduled ? "scheduled" : "completed",
      lastRunAt: new Date().toISOString(),
      lastResultCount: results.length,
    });
    showToast(`Scan complete. Generated ${results.length} snapshot cards.`, "good");
  } catch (error) {
    updatePrompt(promptId, { status: prompt.scheduled ? "scheduled" : "idle" });
    showToast(`Scan failed: ${errorToMessage(error)}`, "bad");
  } finally {
    state.runningPromptIds.delete(promptId);
    el.scanBanner.hidden = true;
    renderAll();
  }
}

async function loadProtectedImageUrl(frameUrl, mimeType) {
  if (!frameUrl) {
    return null;
  }

  try {
    const blob = await backend.requestUrl(frameUrl, {
      headers: { Accept: mimeType || "image/*" },
    });

    if (blob instanceof Blob) {
      const objectUrl = URL.createObjectURL(blob);
      state.objectUrls.push(objectUrl);
      return objectUrl;
    }
  } catch (error) {
    console.warn("Falling back to direct image URL", error);
  }

  return frameUrl;
}

function revokeResultObjectUrls() {
  for (const objectUrl of state.objectUrls) {
    URL.revokeObjectURL(objectUrl);
  }
  state.objectUrls = [];
}

function toggleSelectedPromptSchedule() {
  const prompt = getPrompt();
  if (!prompt) {
    showToast("Select a prompt first.", "bad");
    return;
  }

  if (state.scheduleTimers.has(prompt.id)) {
    window.clearInterval(state.scheduleTimers.get(prompt.id));
    state.scheduleTimers.delete(prompt.id);
    updatePrompt(prompt.id, {
      scheduled: false,
      status: "idle",
      nextRunAt: null,
    });
    showToast("Local schedule stopped.", "good");
  } else {
    const intervalMs = 60_000;
    const timer = window.setInterval(() => runPromptScan(prompt.id), intervalMs);
    state.scheduleTimers.set(prompt.id, timer);
    updatePrompt(prompt.id, {
      scheduled: true,
      status: "scheduled",
      nextRunAt: new Date(Date.now() + intervalMs).toISOString(),
    });
    showToast("Local demo schedule started. Backend queue hookup can replace this later.", "good");
  }

  savePrompts();
  renderAll();
}

function updatePrompt(promptId, patch) {
  const index = state.prompts.findIndex((prompt) => prompt.id === promptId);
  if (index < 0) return;
  state.prompts[index] = {
    ...state.prompts[index],
    ...patch,
    updatedAt: new Date().toISOString(),
  };
  savePrompts();
}

function renderAll() {
  renderPromptList();
  renderPromptSelect();
  renderResults();
  renderActivity();
}

function renderPromptList() {
  el.promptCount.textContent = String(state.prompts.length);

  if (state.prompts.length === 0) {
    el.promptList.innerHTML = `<div class="prompt-card"><p>No prompts yet.</p></div>`;
    return;
  }

  el.promptList.innerHTML = state.prompts.map((prompt) => `
    <article class="prompt-card ${prompt.id === state.selectedPromptId ? "selected" : ""}" data-prompt-id="${escapeAttr(prompt.id)}">
      <div class="status-dot-row">
        <span class="status-dot ${escapeAttr(prompt.status)}"></span>
        <h3>${escapeHtml(prompt.name)}</h3>
      </div>
      <p>${escapeHtml(truncate(prompt.text, 115))}</p>
      <div class="meta-row">
        <span class="meta-chip">${escapeHtml(prompt.type)}</span>
        <span class="meta-chip">${escapeHtml(prompt.status)}</span>
        <span class="meta-chip">${prompt.lastResultCount || 0} results</span>
      </div>
      <div class="card-actions">
        <button type="button" data-action="select">Select</button>
        <button type="button" class="secondary-button" data-action="edit">Edit</button>
        <button type="button" class="ghost-button danger" data-action="delete">Delete</button>
      </div>
    </article>
  `).join("");

  el.promptList.querySelectorAll(".prompt-card").forEach((card) => {
    const promptId = card.dataset.promptId;
    card.querySelector('[data-action="select"]').addEventListener("click", () => {
      state.selectedPromptId = promptId;
      renderAll();
    });
    card.querySelector('[data-action="edit"]').addEventListener("click", () => editPrompt(promptId));
    card.querySelector('[data-action="delete"]').addEventListener("click", () => deletePrompt(promptId));
  });
}

function renderPromptSelect() {
  const selected = state.selectedPromptId || "";
  el.selectedPrompt.innerHTML = [
    `<option value="">Select prompt...</option>`,
    ...state.prompts.map((prompt) => `
      <option value="${escapeAttr(prompt.id)}" ${prompt.id === selected ? "selected" : ""}>${escapeHtml(prompt.name)}</option>
    `),
  ].join("");

  const prompt = getPrompt();
  el.scheduleBtn.textContent = prompt?.scheduled ? "Unschedule" : "Schedule";
}

function renderResults() {
  const prompt = getPrompt();

  el.resultsTitle.textContent = prompt ? prompt.name : "No prompt selected";
  el.resultsSubtitle.textContent = prompt
    ? `${prompt.type} · ${prompt.lastRunAt ? `last run ${formatTime(prompt.lastRunAt)}` : "not run yet"}`
    : "Create or select a prompt, then run a scan.";

  if (state.results.length === 0) {
    el.emptyResults.hidden = false;
    el.resultGrid.innerHTML = "";
    return;
  }

  el.emptyResults.hidden = true;
  el.resultGrid.innerHTML = state.results.map((result) => {
    const frameId = result.frameRef?.frameId || result.snapshot?.frame?.frameId || "n/a";
    const capturedAt = result.frameRef?.capturedAt || result.snapshot?.frame?.capturedAt;
    const imageUrl = result.imageUrl || "";

    return `
      <article class="result-card">
        ${imageUrl ? `<img src="${escapeAttr(imageUrl)}" alt="Snapshot for ${escapeAttr(result.camera.name || result.camera.id)}" />` : ""}
        <div class="result-card-body">
          <div class="result-card-top">
            <div>
              <h3>${escapeHtml(result.camera.name || result.camera.id)}</h3>
              <p>${escapeHtml(result.camera.id)} · ${escapeHtml(result.camera.location || "unknown location")}</p>
            </div>
            <span class="rank-badge">#${result.rank}</span>
          </div>
          <p>${escapeHtml(result.reason)}</p>
          <div class="meta-row">
            <span class="meta-chip score-chip">score ${result.score}</span>
            <span class="meta-chip">${escapeHtml(result.camera.status || "unknown")}</span>
            <span class="meta-chip">${capturedAt ? escapeHtml(formatTime(capturedAt)) : "no capture time"}</span>
          </div>
          <div class="frame-line">frame: ${escapeHtml(frameId)}</div>
        </div>
      </article>
    `;
  }).join("");
}

function renderActivity() {
  const scheduled = state.prompts.filter((prompt) => prompt.scheduled).length;
  el.scheduledCount.textContent = String(scheduled);
  el.runningCount.textContent = String(state.runningPromptIds.size);
  el.cameraCount.textContent = String(state.cameras.length);

  if (state.prompts.length === 0) {
    el.activityList.innerHTML = `<div class="activity-card"><p>No prompt activity yet.</p></div>`;
    return;
  }

  el.activityList.innerHTML = state.prompts.map((prompt) => `
    <article class="activity-card">
      <div class="status-dot-row">
        <span class="status-dot ${escapeAttr(prompt.status)}"></span>
        <h3>${escapeHtml(prompt.name)}</h3>
      </div>
      <p>Status: ${escapeHtml(prompt.status)}${prompt.scheduled ? " · local schedule every 60s" : ""}</p>
      <p>Last run: ${prompt.lastRunAt ? escapeHtml(formatTime(prompt.lastRunAt)) : "never"}</p>
      <p>Next run: ${prompt.nextRunAt ? escapeHtml(formatTime(prompt.nextRunAt)) : "not scheduled"}</p>
    </article>
  `).join("");
}

function deterministicScore(seed) {
  let hash = 0;
  for (let index = 0; index < seed.length; index += 1) {
    hash = (hash * 31 + seed.charCodeAt(index)) >>> 0;
  }
  return 55 + (hash % 45);
}

function buildReason(prompt, camera, score) {
  const cameraName = camera.name || camera.id;
  if (prompt.type === "find") {
    return `${cameraName} is included as a prompt match candidate. Real Gemini analysis can replace this placeholder score.`;
  }
  if (prompt.type === "classify") {
    return `${cameraName} captured a snapshot for classification. Placeholder confidence is ${score}.`;
  }
  return `${cameraName} was ranked using the saved prompt and the captured snapshot frame. Placeholder priority score is ${score}.`;
}

function showLoginError(message) {
  el.loginError.textContent = message;
  el.loginError.hidden = false;
}

function showToast(message, kind = "") {
  el.toast.textContent = message;
  el.toast.className = `toast ${kind}`.trim();
  el.toast.hidden = false;
  window.clearTimeout(showToast.timer);
  showToast.timer = window.setTimeout(() => {
    el.toast.hidden = true;
  }, 4200);
}

function errorToMessage(error) {
  if (!error) return "Unknown error";
  if (error.body && typeof error.body === "string") return error.body;
  if (error.body && typeof error.body === "object") return JSON.stringify(error.body);
  return error.message || String(error);
}

function truncate(value, maxLength) {
  const text = String(value || "");
  return text.length <= maxLength ? text : `${text.slice(0, maxLength - 1)}…`;
}

function formatTime(value) {
  try {
    return new Intl.DateTimeFormat(undefined, {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      month: "short",
      day: "2-digit",
    }).format(new Date(value));
  } catch {
    return value;
  }
}

function clampNumber(value, min, max) {
  if (!Number.isFinite(value)) return min;
  return Math.max(min, Math.min(max, value));
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function escapeAttr(value) {
  return escapeHtml(value);
}
