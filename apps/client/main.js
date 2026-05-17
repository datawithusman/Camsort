const state = {
  base: '/api',
  auth: null,
  prompts: [],
  groups: [],
  bindings: [],
  operations: [],
  selectedPromptId: null,
  selectedGroupId: null,
  imageUrls: new Map(),
  showingFirstPass: false,
};

const $ = (id) => document.getElementById(id);
const esc = (s) => String(s ?? '').replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
const nowish = (v) => v ? new Date(v).toLocaleString() : '—';
const num = (v, fallback = 0) => Number.isFinite(Number(v)) ? Number(v) : fallback;
const fmtMoney = (v) => Number.isFinite(Number(v)) ? `$${Number(v).toFixed(2)}` : '—';
const normalizeId = (v) => String(v ?? '').trim();

function authHeader() {
  return state.auth ? { Authorization: 'Basic ' + btoa(`${state.auth.user}:${state.auth.pass}`) } : {};
}

async function api(path, opts = {}) {
  const headers = { ...authHeader(), ...(opts.headers || {}) };
  if (opts.body && !(opts.body instanceof FormData)) headers['Content-Type'] = 'application/json';
  const response = await fetch(state.base + path, { ...opts, headers });
  if (!response.ok) throw new Error(await response.text());
  if (response.status === 204) return null;
  return response.json();
}

function saveAuth() { localStorage.setItem('cambotAuth', JSON.stringify(state.auth)); }
function loadAuth() { try { state.auth = JSON.parse(localStorage.getItem('cambotAuth') || 'null'); } catch { state.auth = null; } }

async function login() {
  state.auth = { user: $('username').value.trim(), pass: $('password').value };
  await api('/health');
  saveAuth();
  $('login').hidden = true;
  $('dashboard').hidden = false;
  await refreshAll();
}

function logout() {
  localStorage.removeItem('cambotAuth');
  for (const url of state.imageUrls.values()) URL.revokeObjectURL(url);
  location.reload();
}

async function refreshAll() {
  await Promise.all([loadPrompts(), loadGroups(), loadOperations(), loadSettings(), loadQueue(), loadUsage()]);
  selectInitialPromptAndGroup();
  await loadBindings();
  renderPrompts();
  renderGroupSelects();
  await loadResults();
}

function selectInitialPromptAndGroup() {
  if (!state.selectedPromptId && state.prompts.length) state.selectedPromptId = state.prompts[0].id;
  if (!state.selectedGroupId && state.groups.length) state.selectedGroupId = state.groups[0].id;
}

function normalizePrompt(p) {
  return {
    ...p,
    id: p.id,
    promptText: p.promptText ?? p.prompt_text ?? '',
    createdAt: p.createdAt ?? p.created_at,
    updatedAt: p.updatedAt ?? p.updated_at,
  };
}

function normalizeGroup(g) {
  return {
    ...g,
    id: g.id,
    name: g.name || g.id,
    description: g.description || '',
    cameraIds: g.cameraIds || g.camera_ids || [],
  };
}

function normalizeBinding(b) {
  return {
    ...b,
    id: b.id,
    promptId: b.promptId ?? b.prompt_id,
    cameraGroupId: b.cameraGroupId ?? b.camera_group_id,
    lastRunAt: b.lastRunAt ?? b.last_run_at,
  };
}

function normalizeOperation(o) {
  return {
    ...o,
    id: o.id,
    promptId: o.promptId ?? o.prompt_id,
    cameraGroupId: o.cameraGroupId ?? o.camera_group_id,
    status: o.status || 'unknown',
    trigger: o.trigger || o.triggerType || o.trigger_type,
    createdAt: o.createdAt ?? o.created_at,
    startedAt: o.startedAt ?? o.started_at,
    completedAt: o.completedAt ?? o.completed_at,
  };
}

async function loadPrompts() {
  const data = await api('/saved-prompts');
  state.prompts = (data.prompts || []).map(normalizePrompt);
}

async function loadGroups() {
  const data = await api('/camera-groups');
  state.groups = (data.groups || []).map(normalizeGroup);
}

async function loadOperations() {
  try {
    const data = await api('/operations?limit=100&offset=0');
    state.operations = (data.operations || []).map(normalizeOperation);
  } catch {
    state.operations = [];
  }
}

async function loadBindings() {
  const all = [];
  for (const group of state.groups) {
    try {
      const data = await api(`/camera-groups/${encodeURIComponent(group.id)}/prompt-bindings`);
      for (const b of (data.bindings || [])) all.push(normalizeBinding(b));
    } catch {
      // Keep UI usable even if binding endpoint is not ready.
    }
  }
  state.bindings = all;
}

function getSelectedPrompt() { return state.prompts.find(p => p.id === state.selectedPromptId) || null; }
function getSelectedGroup() { return state.groups.find(g => g.id === state.selectedGroupId) || null; }
function getPromptBindings(promptId) { return state.bindings.filter(b => b.promptId === promptId && b.enabled !== false); }
function getSelectedBinding() { return state.bindings.find(b => b.promptId === state.selectedPromptId && b.cameraGroupId === state.selectedGroupId) || null; }
function isPromptScanning(promptId) {
  return state.operations.some(o => o.promptId === promptId && ['queued', 'running', 'first_pass_running', 'second_pass_running'].includes(String(o.status).toLowerCase()));
}

function renderPrompts() {
  const list = $('promptList');
  if (!state.prompts.length) {
    list.innerHTML = '<div class="empty">No prompts yet. Create a new prompt to begin.</div>';
    return;
  }

  list.innerHTML = state.prompts.map(prompt => {
    const scheduled = getPromptBindings(prompt.id).length > 0;
    const scanning = isPromptScanning(prompt.id);
    const active = prompt.id === state.selectedPromptId;
    const groupNames = getPromptBindings(prompt.id)
      .map(b => state.groups.find(g => g.id === b.cameraGroupId)?.name || b.cameraGroupId)
      .join(', ');
    return `
      <article class="prompt-row ${active ? 'active' : ''}" data-prompt-id="${esc(prompt.id)}" tabindex="0">
        <div class="prompt-main">
          <div class="prompt-title-line">
            <strong>${esc(prompt.name || prompt.id)}</strong>
            <span class="prompt-badges">
              ${scheduled ? `<span class="pill ok" title="Scheduled on background${groupNames ? `: ${esc(groupNames)}` : ''}">Scheduled</span>` : '<span class="pill soft">Manual</span>'}
              ${scanning ? '<span class="pill warn">Scanning</span>' : ''}
              ${prompt.enabled === false ? '<span class="pill danger">Disabled</span>' : ''}
            </span>
          </div>
          <p class="prompt-preview">${esc(prompt.promptText || 'No prompt text.')}</p>
        </div>
        <button class="edit-prompt-btn secondary" data-edit-prompt-id="${esc(prompt.id)}" title="Edit prompt">Edit</button>
      </article>
    `;
  }).join('');

  document.querySelectorAll('.prompt-row').forEach(row => {
    row.onclick = async (event) => {
      if (event.target.closest('.edit-prompt-btn')) return;
      state.selectedPromptId = row.dataset.promptId;
      renderPrompts();
      await loadBindings();
      updateBindingStatus();
      await loadResults();
    };
    row.onkeydown = async (event) => {
      if (event.key !== 'Enter' && event.key !== ' ') return;
      event.preventDefault();
      state.selectedPromptId = row.dataset.promptId;
      renderPrompts();
      await loadBindings();
      updateBindingStatus();
      await loadResults();
    };
  });

  document.querySelectorAll('.edit-prompt-btn').forEach(btn => {
    btn.onclick = async (event) => {
      event.stopPropagation();
      state.selectedPromptId = btn.dataset.editPromptId;
      renderPrompts();
      await openPromptModal(getSelectedPrompt());
    };
  });
}

function renderGroupSelects() {
  const options = state.groups.map(g => `<option value="${esc(g.id)}">${esc(g.name)} · ${g.cameraIds.length} cams</option>`).join('');
  $('resultGroupSelect').innerHTML = options || '<option value="">No camera groups</option>';
  $('modalGroupSelect').innerHTML = options || '<option value="">No camera groups</option>';
  if (state.selectedGroupId && [...$('resultGroupSelect').options].some(o => o.value === state.selectedGroupId)) $('resultGroupSelect').value = state.selectedGroupId;
  if (state.selectedGroupId && [...$('modalGroupSelect').options].some(o => o.value === state.selectedGroupId)) $('modalGroupSelect').value = state.selectedGroupId;
}

async function openPromptModal(prompt = null) {
  if (!state.groups.length) await loadGroups();
  if (!state.selectedGroupId && state.groups.length) state.selectedGroupId = state.groups[0].id;
  renderGroupSelects();

  const isNew = !prompt;
  $('promptModalTitle').textContent = isNew ? 'Create New Prompt' : 'Edit Prompt';
  $('modalSubtitle').textContent = isNew ? 'Create the prompt, then choose a camera group to run or schedule it.' : 'Edit the prompt or run/schedule it on a camera group.';
  $('promptId').value = prompt?.id || '';
  $('promptName').value = prompt?.name || '';
  $('promptDescription').value = prompt?.description || '';
  $('promptText').value = prompt?.promptText || '';
  $('promptEnabled').checked = prompt?.enabled !== false;
  $('deletePromptBtn').hidden = isNew;
  $('promptModal').hidden = false;
  updateBindingStatus();
  setTimeout(() => $('promptName').focus(), 0);
}

function closePromptModal() { $('promptModal').hidden = true; }

async function savePrompt() {
  const id = $('promptId').value.trim();
  const payload = {
    name: $('promptName').value.trim() || 'Untitled prompt',
    description: $('promptDescription').value.trim() || null,
    promptText: $('promptText').value.trim(),
    enabled: $('promptEnabled').checked,
  };
  if (!payload.promptText) throw new Error('Prompt text is required.');
  const saved = id
    ? await api(`/saved-prompts/${encodeURIComponent(id)}`, { method: 'PUT', body: JSON.stringify(payload) })
    : await api('/saved-prompts', { method: 'POST', body: JSON.stringify(payload) });
  await loadPrompts();
  state.selectedPromptId = saved?.id || id || state.prompts.find(p => p.name === payload.name)?.id || state.selectedPromptId;
  await loadBindings();
  renderPrompts();
  updateBindingStatus();
  await loadResults();
}

async function deletePrompt() {
  const prompt = getSelectedPrompt();
  if (!prompt) return;
  if (!confirm(`Delete prompt "${prompt.name}"?`)) return;
  await api(`/saved-prompts/${encodeURIComponent(prompt.id)}`, { method: 'DELETE' });
  closePromptModal();
  state.selectedPromptId = null;
  await refreshAll();
}

async function runSingleScan() {
  const prompt = getSelectedPrompt();
  const group = getSelectedGroup();
  if (!prompt) throw new Error('Select or save a prompt first.');
  if (!group) throw new Error('Select a camera group first.');
  const operation = await api('/operations', {
    method: 'POST',
    body: JSON.stringify({ promptId: prompt.id, cameraGroupId: group.id, trigger: 'manual' }),
  });
  closePromptModal();
  await loadOperations();
  renderPrompts();
  alert(`Queued single scan: ${operation?.id || 'operation created'}`);
}

async function enableContinuous() {
  const prompt = getSelectedPrompt();
  const group = getSelectedGroup();
  if (!prompt) throw new Error('Select or save a prompt first.');
  if (!group) throw new Error('Select a camera group first.');
  await api(`/camera-groups/${encodeURIComponent(group.id)}/prompt-bindings`, {
    method: 'POST',
    body: JSON.stringify({ promptId: prompt.id, enabled: true }),
  });
  await loadBindings();
  renderPrompts();
  updateBindingStatus();
}

async function disableContinuous() {
  const binding = getSelectedBinding();
  const group = getSelectedGroup();
  if (!binding || !group) return;
  await api(`/camera-groups/${encodeURIComponent(group.id)}/prompt-bindings/${encodeURIComponent(binding.id)}`, { method: 'DELETE' });
  await loadBindings();
  renderPrompts();
  updateBindingStatus();
}

function updateBindingStatus() {
  const prompt = getSelectedPrompt();
  const group = getSelectedGroup();
  const binding = getSelectedBinding();
  if (!prompt) {
    $('bindingStatus').textContent = 'Save or select a prompt before scheduling.';
    return;
  }
  if (!group) {
    $('bindingStatus').textContent = 'Select a camera group before scheduling.';
    return;
  }
  $('bindingStatus').innerHTML = binding
    ? `<span class="pill ok">Scheduled</span> ${esc(prompt.name)} runs on ${esc(group.name)} during the global continuous scan cycle. Last run: ${esc(nowish(binding.lastRunAt))}`
    : `<span class="pill soft">Not scheduled</span> ${esc(prompt.name)} is not scheduled on ${esc(group.name)}.`;
}

async function imageObjectUrl(frameUrl) {
  if (!frameUrl) return null;
  if (state.imageUrls.has(frameUrl)) return state.imageUrls.get(frameUrl);
  const response = await fetch(frameUrl.startsWith('http') ? frameUrl : frameUrl, { headers: authHeader() });
  if (!response.ok) return null;
  const blob = await response.blob();
  const url = URL.createObjectURL(blob);
  state.imageUrls.set(frameUrl, url);
  return url;
}

function normalizeResult(r) {
  return {
    id: r.id,
    cameraId: r.cameraId ?? r.camera_id,
    frameUrl: r.frameUrl ?? r.frame_url,
    promptScore: r.promptScore ?? r.prompt_score ?? r.firstPassPromptScore ?? r.first_pass_prompt_score,
    operatorPriorityScore: r.operatorPriorityScore ?? r.operator_priority_score,
    operatorAction: r.operatorAction ?? r.operator_action ?? r.recommendedAction ?? r.recommended_action,
    reason: r.reason,
    globalRank: r.globalRank ?? r.global_rank,
    createdAt: r.createdAt ?? r.created_at ?? r.updatedAt ?? r.updated_at,
  };
}

async function loadResults() {
  const prompt = getSelectedPrompt();
  const group = getSelectedGroup();
  $('resultContext').textContent = prompt && group
    ? `${prompt.name} · ${group.name} · ${state.showingFirstPass ? 'first pass/intermediate' : 'second pass/global'} results`
    : 'Select a prompt and camera group.';
  if (!prompt || !group) {
    $('resultList').innerHTML = '<div class="empty">Select a prompt and camera group to see results.</div>';
    return;
  }
  const pass = state.showingFirstPass ? 'first' : 'second';
  try {
    const data = await api(`/prompt-results/latest/${pass}?promptId=${encodeURIComponent(prompt.id)}&cameraGroupId=${encodeURIComponent(group.id)}`);
    const results = (data.results || []).map(normalizeResult);
    await renderResults(results);
  } catch (err) {
    $('resultList').innerHTML = `<div class="empty">Could not load results yet.<br><small>${esc(err.message || err)}</small></div>`;
  }
}

async function renderResults(results) {
  if (!results.length) {
    $('resultList').innerHTML = '<div class="empty">No results yet. Run a single scan or wait for the background scanner.</div>';
    return;
  }
  $('resultList').innerHTML = results.map((r, index) => `
    <article class="result-card" data-frame-url="${esc(r.frameUrl || '')}">
      <div class="image-slot"><span>Loading snapshot...</span></div>
      <div class="score-row">
        <div><span class="muted small">Prompt Score</span><div class="big-score">${esc(num(r.promptScore, 0).toFixed(0))}</div></div>
        <div><span class="muted small">Operator Priority</span><div class="priority-score">${esc(num(r.operatorPriorityScore, 0).toFixed(0))}</div></div>
      </div>
      <h3>${esc(r.cameraId || `Camera ${index + 1}`)} ${r.globalRank ? `<span class="pill soft">#${esc(r.globalRank)}</span>` : ''}</h3>
      <p><strong>Action:</strong> ${esc(r.operatorAction || 'Review this camera.')}</p>
      <p class="muted"><strong>Reason:</strong> ${esc(r.reason || 'No reason provided.')}</p>
      <p class="muted small">Updated: ${esc(nowish(r.createdAt))}</p>
    </article>
  `).join('');
  for (const card of document.querySelectorAll('.result-card')) {
    const frameUrl = card.dataset.frameUrl;
    const slot = card.querySelector('.image-slot');
    const url = await imageObjectUrl(frameUrl);
    slot.innerHTML = url ? `<img src="${esc(url)}" alt="camera snapshot">` : '<span>No snapshot image</span>';
  }
}

async function loadQueue() {
  try {
    const data = await api('/operator-queue');
    const items = data.items || [];
    $('queueList').innerHTML = items.length ? items.map(item => {
      const cameraId = item.cameraId ?? item.camera_id;
      const action = item.operatorAction ?? item.operator_action ?? item.recommendedAction ?? item.recommended_action;
      const score = item.operatorPriorityScore ?? item.operator_priority_score;
      const status = item.status || 'queued';
      return `
        <article class="item queue-item">
          <div>
            <strong>${esc(cameraId)} · ${esc(action || 'Operator action')}</strong>
            <p class="muted">${esc(item.reason || '')}</p>
          </div>
          <div class="queue-meta">
            <span class="pill ${status === 'queued' ? 'warn' : 'soft'}">${esc(status)}</span>
            <div class="priority-score">${esc(num(score, 0).toFixed(0))}</div>
          </div>
        </article>
      `;
    }).join('') : '<div class="empty">No operator actions yet.</div>';
  } catch (err) {
    $('queueList').innerHTML = `<div class="empty">Could not load queue.<br><small>${esc(err.message || err)}</small></div>`;
  }
}

async function loadSettings() {
  try {
    const s = await api('/settings/gemini');
    $('continuousEnabled').checked = Boolean(s.continuousScanEnabled ?? s.continuous_scan_enabled);
    $('continuousInterval').value = s.continuousScanIntervalSeconds ?? s.continuous_scan_interval_seconds ?? 900;
    $('geminiDelay').value = s.geminiCallDelayMs ?? s.gemini_call_delay_ms ?? 2000;
    $('maxCostDay').value = s.maxEstimatedCostPerDay ?? s.max_estimated_cost_per_day ?? '';
    $('nextScanAt').textContent = nowish(s.nextContinuousScanAt ?? s.next_continuous_scan_at);
  } catch {
    // Settings endpoint may not be ready during early dev.
  }
}

async function saveSettings() {
  await api('/settings/gemini', {
    method: 'PUT',
    body: JSON.stringify({
      continuousScanEnabled: $('continuousEnabled').checked,
      continuousScanIntervalSeconds: Number($('continuousInterval').value || 900),
      geminiCallDelayMs: Number($('geminiDelay').value || 2000),
      maxEstimatedCostPerDay: Number($('maxCostDay').value || 0),
    }),
  });
  await loadSettings();
}

async function loadUsage() {
  try {
    const u = await api('/usage/summary');
    $('prevDayCost').textContent = fmtMoney(u.previousDayCost ?? u.previous_day_cost);
    $('monthCost').textContent = fmtMoney(u.monthToDateCost ?? u.month_to_date_cost);
    $('projectedCost').textContent = fmtMoney(u.projectedCostPerDay ?? u.projected_cost_per_day);
    $('usageSummary').textContent = JSON.stringify(u, null, 2);
  } catch {
    $('usageSummary').textContent = 'Usage summary unavailable.';
  }
}

async function guard(fn) {
  try { await fn(); }
  catch (err) { alert(err.message || String(err)); }
}

function wireEvents() {
  $('loginBtn').onclick = () => guard(login);
  $('password').onkeydown = e => { if (e.key === 'Enter') guard(login); };
  $('logoutBtn').onclick = logout;
  $('refreshPromptsBtn').onclick = () => guard(async () => { await loadPrompts(); await loadOperations(); await loadBindings(); renderPrompts(); });
  $('newPromptBtn').onclick = () => guard(async () => openPromptModal(null));
  $('closePromptModalBtn').onclick = closePromptModal;
  $('promptModal').onclick = e => { if (e.target.id === 'promptModal') closePromptModal(); };
  $('savePromptBtn').onclick = () => guard(savePrompt);
  $('deletePromptBtn').onclick = () => guard(deletePrompt);
  $('runBtn').onclick = () => guard(runSingleScan);
  $('enableContinuousBtn').onclick = () => guard(enableContinuous);
  $('disableContinuousBtn').onclick = () => guard(disableContinuous);
  $('modalGroupSelect').onchange = async () => { state.selectedGroupId = $('modalGroupSelect').value; $('resultGroupSelect').value = state.selectedGroupId; updateBindingStatus(); await loadResults(); };
  $('resultGroupSelect').onchange = async () => { state.selectedGroupId = $('resultGroupSelect').value; $('modalGroupSelect').value = state.selectedGroupId; await loadBindings(); updateBindingStatus(); await loadResults(); };
  $('refreshResultsBtn').onclick = () => guard(loadResults);
  $('showFirstPassBtn').onclick = () => guard(async () => {
    state.showingFirstPass = !state.showingFirstPass;
    $('showFirstPassBtn').textContent = state.showingFirstPass ? 'Show Second Pass' : 'Show First Pass';
    await loadResults();
  });
  $('refreshQueueBtn').onclick = () => guard(loadQueue);
  $('saveSettingsBtn').onclick = () => guard(saveSettings);
}

async function boot() {
  wireEvents();
  loadAuth();
  if (state.auth) {
    try {
      await api('/health');
      $('login').hidden = true;
      $('dashboard').hidden = false;
      await refreshAll();
    } catch {
      localStorage.removeItem('cambotAuth');
    }
  }
}

boot();
