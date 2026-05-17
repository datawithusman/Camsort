const state = {
  base: '/api',
  auth: null,
  prompts: [],
  groups: [],
  cameras: [],
  bindings: [],
  operations: [],
  selectedPromptId: null,
  selectedGroupId: null,
  promptGroupFilter: '',
  promptCameraFilter: '',
  imageUrls: new Map(),
  showingFirstPass: false,
  loadingActions: new Set(),
};

const $ = (id) => document.getElementById(id);
const esc = (s) => String(s ?? '').replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
const nowish = (v) => v ? new Date(v).toLocaleString() : '—';
const num = (v, fallback = 0) => Number.isFinite(Number(v)) ? Number(v) : fallback;
const fmtMoney = (v) => Number.isFinite(Number(v)) ? `$${Number(v).toFixed(2)}` : '—';

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

function normalizePrompt(p) {
  return {
    ...p,
    id: p.id,
    name: p.name || p.id,
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

function normalizeCamera(c) {
  return {
    ...c,
    id: c.id,
    name: c.name || c.id,
    location: c.location || '',
    groupIds: c.groupIds || c.group_ids || [],
  };
}

function normalizeBinding(b) {
  return {
    ...b,
    id: b.id,
    promptId: b.promptId ?? b.prompt_id,
    cameraGroupId: b.cameraGroupId ?? b.camera_group_id,
    enabled: b.enabled !== false,
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

async function refreshAll() {
  await Promise.all([loadPrompts(), loadGroups(), loadCameras(), loadOperations(), loadSettings(), loadQueue(), loadUsage()]);
  selectInitialPromptAndGroup();
  await loadBindings();
  renderGroupSelects();
  renderPromptFilters();
  renderPrompts();
  await loadResults();
}

function selectInitialPromptAndGroup() {
  if (!state.selectedPromptId && state.prompts.length) state.selectedPromptId = state.prompts[0].id;
  if (!state.selectedGroupId && state.groups.length) state.selectedGroupId = state.groups[0].id;
}

async function loadPrompts() {
  const data = await api('/saved-prompts');
  state.prompts = (data.prompts || []).map(normalizePrompt);
}

async function loadGroups() {
  const data = await api('/camera-groups');
  state.groups = (data.groups || []).map(normalizeGroup);
}

async function loadCameras() {
  try {
    const data = await api('/camera-system/cameras');
    state.cameras = (data.cameras || []).map(normalizeCamera);
  } catch {
    state.cameras = [];
  }
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
function getPromptById(id) { return state.prompts.find(p => p.id === id) || null; }
function getModalPrompt() { const el = $('promptId'); return el?.value ? getPromptById(el.value) : null; }
function getSelectedGroup() { return state.groups.find(g => g.id === state.selectedGroupId) || null; }
function getPromptBindings(promptId) { return state.bindings.filter(b => b.promptId === promptId && b.enabled !== false); }
function getBinding(promptId, groupId) { return state.bindings.find(b => b.promptId === promptId && b.cameraGroupId === groupId && b.enabled !== false) || null; }
function getRunningOperations(promptId) {
  const activeStatuses = new Set(['queued', 'running', 'first_pass_running', 'second_pass_running', 'first_pass_queued', 'second_pass_queued']);
  return state.operations.filter(o => o.promptId === promptId && activeStatuses.has(String(o.status).toLowerCase()));
}
function isPromptScanning(promptId) { return getRunningOperations(promptId).length > 0; }

function promptMatchesFilters(prompt) {
  const bindings = getPromptBindings(prompt.id);
  if (state.promptGroupFilter && !bindings.some(b => b.cameraGroupId === state.promptGroupFilter)) return false;

  const q = state.promptCameraFilter.trim().toLowerCase();
  if (!q) return true;

  const matchingCameraIds = new Set(state.cameras
    .filter(c => [c.id, c.name, c.location].some(v => String(v || '').toLowerCase().includes(q)))
    .map(c => c.id));

  if (!matchingCameraIds.size) return false;

  const matchingGroupIds = new Set(state.groups
    .filter(g => (g.cameraIds || []).some(id => matchingCameraIds.has(id)))
    .map(g => g.id));

  return bindings.some(b => matchingGroupIds.has(b.cameraGroupId));
}

function filteredPrompts() {
  return state.prompts.filter(promptMatchesFilters);
}

function renderPromptFilters() {
  $('promptGroupFilter').innerHTML = '<option value="">All scheduled groups</option>' +
    state.groups.map(g => `<option value="${esc(g.id)}">${esc(g.name)} · ${g.cameraIds.length} cams</option>`).join('');
  $('promptGroupFilter').value = state.promptGroupFilter;
  $('promptCameraFilter').value = state.promptCameraFilter;
  updatePromptFilterSummary();
}

function updatePromptFilterSummary() {
  const parts = [];
  if (state.promptGroupFilter) {
    const group = state.groups.find(g => g.id === state.promptGroupFilter);
    parts.push(`scheduled on ${group?.name || state.promptGroupFilter}`);
  }
  if (state.promptCameraFilter.trim()) parts.push(`affecting cameras matching “${state.promptCameraFilter.trim()}”`);
  const count = filteredPrompts().length;
  $('promptFilterSummary').textContent = parts.length
    ? `Showing ${count} prompt${count === 1 ? '' : 's'} ${parts.join(' and ')}.`
    : `Showing all ${state.prompts.length} prompt${state.prompts.length === 1 ? '' : 's'}.`;
}

function renderPrompts() {
  const list = $('promptList');
  const prompts = filteredPrompts();
  updatePromptFilterSummary();
  if (!state.prompts.length) {
    list.innerHTML = '<div class="empty">No prompts yet. Create a new prompt to begin.</div>';
    return;
  }
  if (!prompts.length) {
    list.innerHTML = '<div class="empty">No prompts match the current filters.</div>';
    return;
  }

  list.innerHTML = prompts.map(prompt => {
    const bindings = getPromptBindings(prompt.id);
    const scheduled = bindings.length > 0;
    const running = isPromptScanning(prompt.id);
    const active = prompt.id === state.selectedPromptId;
    const groupNames = bindings
      .map(b => state.groups.find(g => g.id === b.cameraGroupId)?.name || b.cameraGroupId)
      .join(', ');
    const runningGroups = getRunningOperations(prompt.id)
      .map(o => state.groups.find(g => g.id === o.cameraGroupId)?.name || o.cameraGroupId)
      .filter(Boolean)
      .join(', ');
    return `
      <article class="prompt-row ${active ? 'active' : ''}" data-prompt-id="${esc(prompt.id)}" tabindex="0">
        <div class="prompt-main">
          <div class="prompt-title-line">
            <strong>${esc(prompt.name || prompt.id)}</strong>
            <span class="prompt-badges">
              ${scheduled ? `<span class="pill ok" title="Scheduled on: ${esc(groupNames)}">Scheduled · ${bindings.length}</span>` : '<span class="pill soft">Not scheduled</span>'}
              ${running ? `<span class="pill warn" title="Running: ${esc(runningGroups)}">Scanning</span>` : '<span class="pill soft">Idle</span>'}
              ${prompt.enabled === false ? '<span class="pill danger">Disabled</span>' : ''}
            </span>
          </div>
          ${scheduled ? `<p class="prompt-meta">Scheduled groups: ${esc(groupNames)}</p>` : '<p class="prompt-meta">No background schedules.</p>'}
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
      await loadResults();
    };
    row.onkeydown = async (event) => {
      if (event.key !== 'Enter' && event.key !== ' ') return;
      event.preventDefault();
      state.selectedPromptId = row.dataset.promptId;
      renderPrompts();
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
  if (state.selectedGroupId && [...$('resultGroupSelect').options].some(o => o.value === state.selectedGroupId)) $('resultGroupSelect').value = state.selectedGroupId;
}

async function openPromptModal(prompt = null) {
  if (!state.groups.length) await loadGroups();
  if (!state.selectedGroupId && state.groups.length) state.selectedGroupId = state.groups[0].id;

  const isNew = !prompt;
  $('promptModalTitle').textContent = isNew ? 'Create New Prompt' : 'Edit Prompt';
  $('modalSubtitle').textContent = isNew ? 'Create the prompt, then save it before running or scheduling.' : 'Edit the prompt and manage each camera group schedule separately.';
  $('promptId').value = prompt?.id || '';
  $('promptName').value = prompt?.name || '';
  $('promptDescription').value = prompt?.description || '';
  $('promptText').value = prompt?.promptText || '';
  $('promptEnabled').checked = prompt?.enabled !== false;
  $('deletePromptBtn').hidden = isNew;
  $('promptModal').hidden = false;
  renderModalScheduleList();
  setTimeout(() => $('promptName').focus(), 0);
}

function closePromptModal() { $('promptModal').hidden = true; setModalStatus(''); state.loadingActions.clear(); }

function actionKey(kind, groupId = '') {
  const promptId = $('promptId')?.value || state.selectedPromptId || 'none';
  return `${kind}:${promptId}:${groupId}`;
}
function isActionLoading(kind, groupId = '') { return state.loadingActions.has(actionKey(kind, groupId)); }
function anyScheduleActionLoading() { return Array.from(state.loadingActions).some(k => k.startsWith('schedule:') || k.startsWith('removeSchedule:') || k.startsWith('runScan:')); }
function setModalStatus(message = '', tone = 'info') {
  const el = $('modalStatus');
  if (!el) return;
  el.textContent = message;
  el.className = `modal-status ${message ? tone : ''}`;
  el.hidden = !message;
}
async function withLoadingAction(kind, groupId, message, fn) {
  const key = actionKey(kind, groupId);
  state.loadingActions.add(key);
  setModalStatus(message, 'loading');
  renderModalScheduleList();
  try {
    const result = await fn();
    setModalStatus('Done.', 'success');
    setTimeout(() => { if (!anyScheduleActionLoading()) setModalStatus(''); }, 1100);
    return result;
  } catch (err) {
    setModalStatus(err.message || String(err), 'error');
    throw err;
  } finally {
    state.loadingActions.delete(key);
    renderModalScheduleList();
  }
}


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
  $('promptId').value = state.selectedPromptId || '';
  $('promptModalTitle').textContent = 'Edit Prompt';
  $('modalSubtitle').textContent = 'Edit the prompt and manage each camera group schedule separately.';
  $('deletePromptBtn').hidden = false;
  await loadBindings();
  renderPrompts();
  renderModalScheduleList();
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

async function runSingleScanForGroup(groupId) {
  const prompt = getModalPrompt() || getSelectedPrompt();
  const group = state.groups.find(g => g.id === groupId);
  if (!prompt) throw new Error('Select or save a prompt first.');
  if (!group) throw new Error('Select a camera group first.');
  await withLoadingAction('runScan', group.id, `Queueing single scan for ${group.name}...`, async () => {
    const operation = await api('/operations', {
      method: 'POST',
      body: JSON.stringify({ promptId: prompt.id, cameraGroupId: group.id, trigger: 'manual' }),
    });
    state.selectedGroupId = group.id;
    $('resultGroupSelect').value = group.id;
    await loadOperations();
    renderPrompts();
    setModalStatus(`Queued single scan for ${group.name}: ${operation?.id || 'operation created'}`, 'success');
  });
}

async function enableContinuousForGroup(groupId) {
  const prompt = getModalPrompt() || getSelectedPrompt();
  const group = state.groups.find(g => g.id === groupId);
  if (!prompt) throw new Error('Select or save a prompt first.');
  if (!group) throw new Error('Select a camera group first.');
  await withLoadingAction('schedule', group.id, `Scheduling ${prompt.name || prompt.id} on ${group.name}...`, async () => {
    await api(`/camera-groups/${encodeURIComponent(group.id)}/prompt-bindings`, {
      method: 'POST',
      body: JSON.stringify({ promptId: prompt.id, enabled: true }),
    });
    await loadBindings();
    renderPrompts();
  });
}

async function disableContinuousForGroup(groupId) {
  const prompt = getModalPrompt() || getSelectedPrompt();
  const group = state.groups.find(g => g.id === groupId);
  const binding = prompt && group ? getBinding(prompt.id, group.id) : null;
  if (!binding || !group) return;
  await withLoadingAction('removeSchedule', group.id, `Removing background schedule for ${group.name}...`, async () => {
    await api(`/camera-groups/${encodeURIComponent(group.id)}/prompt-bindings/${encodeURIComponent(binding.id)}`, { method: 'DELETE' });
    await loadBindings();
    renderPrompts();
  });
}

function renderModalScheduleList() {
  const prompt = getModalPrompt();
  const list = $('modalScheduleList');
  if (!$('promptModal') || $('promptModal').hidden) return;
  if (!prompt) {
    list.innerHTML = '<div class="empty">Save this prompt before running or scheduling it.</div>';
    return;
  }
  if (!state.groups.length) {
    list.innerHTML = '<div class="empty">No camera groups are available.</div>';
    return;
  }

  list.innerHTML = state.groups.map(group => {
    const binding = getBinding(prompt.id, group.id);
    const running = state.operations.some(o => o.promptId === prompt.id && o.cameraGroupId === group.id && ['queued','running','first_pass_running','second_pass_running'].includes(String(o.status).toLowerCase()));
    const scheduling = isActionLoading('schedule', group.id);
    const removing = isActionLoading('removeSchedule', group.id);
    const queueing = isActionLoading('runScan', group.id);
    const busy = scheduling || removing || queueing;
    return `
      <article class="schedule-row ${busy ? 'busy' : ''}" data-schedule-group-id="${esc(group.id)}" aria-busy="${busy ? 'true' : 'false'}">
        <div>
          <strong>${esc(group.name)}</strong>
          <p class="muted small">${esc(group.cameraIds.length)} cameras${group.description ? ` · ${esc(group.description)}` : ''}</p>
        </div>
        <div class="schedule-status">
          ${binding ? '<span class="pill ok">Scheduled</span>' : '<span class="pill soft">Not scheduled</span>'}
          ${running ? '<span class="pill warn">Scanning</span>' : '<span class="pill soft">Idle</span>'}
          ${busy ? '<span class="pill loading-pill">Working...</span>' : ''}
          ${binding?.lastRunAt ? `<span class="pill soft">Last run ${esc(nowish(binding.lastRunAt))}</span>` : ''}
        </div>
        <div class="schedule-actions">
          ${binding
            ? `<button class="remove-schedule-btn danger" data-remove-schedule-group-id="${esc(group.id)}" ${busy ? 'disabled' : ''}>${removing ? '<span class="spinner"></span> Removing...' : 'Remove Schedule'}</button>`
            : `<button class="run-group-btn primary-action" data-run-group-id="${esc(group.id)}" ${busy ? 'disabled' : ''}>${queueing ? '<span class="spinner"></span> Queueing...' : 'Run Single Scan'}</button>
               <button class="schedule-group-btn secondary-action" data-schedule-group-id="${esc(group.id)}" ${busy ? 'disabled' : ''}>${scheduling ? '<span class="spinner"></span> Scheduling...' : 'Schedule Background'}</button>`
          }
        </div>
      </article>
    `;
  }).join('');

  document.querySelectorAll('.run-group-btn').forEach(btn => {
    btn.onclick = () => guard(() => runSingleScanForGroup(btn.dataset.runGroupId));
  });
  document.querySelectorAll('.schedule-group-btn').forEach(btn => {
    btn.onclick = () => guard(() => enableContinuousForGroup(btn.dataset.scheduleGroupId));
  });
  document.querySelectorAll('.remove-schedule-btn').forEach(btn => {
    btn.onclick = () => guard(() => disableContinuousForGroup(btn.dataset.removeScheduleGroupId));
  });
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

function on(id, event, handler) { const el = $(id); if (el) el.addEventListener(event, handler); }

function wireEvents() {
  $('loginBtn').onclick = () => guard(login);
  $('password').onkeydown = e => { if (e.key === 'Enter') guard(login); };
  $('logoutBtn').onclick = logout;
  $('refreshPromptsBtn').onclick = () => guard(async () => { await Promise.all([loadPrompts(), loadCameras(), loadOperations(), loadBindings()]); renderPromptFilters(); renderPrompts(); renderModalScheduleList(); });
  $('newPromptBtn').onclick = () => guard(async () => openPromptModal(null));
  $('closePromptModalBtn').onclick = closePromptModal;
  $('promptModal').onclick = e => { if (e.target.id === 'promptModal') closePromptModal(); };
  $('savePromptBtn').onclick = () => guard(savePrompt);
  $('deletePromptBtn').onclick = () => guard(deletePrompt);
  $('promptGroupFilter').onchange = () => { state.promptGroupFilter = $('promptGroupFilter').value; renderPrompts(); };
  $('promptCameraFilter').oninput = () => { state.promptCameraFilter = $('promptCameraFilter').value; renderPrompts(); };
  $('clearPromptFiltersBtn').onclick = () => { state.promptGroupFilter = ''; state.promptCameraFilter = ''; renderPromptFilters(); renderPrompts(); };
  $('resultGroupSelect').onchange = async () => { state.selectedGroupId = $('resultGroupSelect').value; await loadResults(); };
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
