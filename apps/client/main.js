const state = {
  base: '/api',
  auth: null,
  prompts: [],
  appGroups: [],
  sourceGroups: [],
  selectedPromptId: null,
  selectedGroupKey: null,
  selectedBinding: null,
  imageUrls: new Map(),
  showingFirstPass: false,
};

const $ = (id) => document.getElementById(id);
const esc = (s) => String(s ?? '').replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
const camIds = (g) => g?.cameraIds || g?.camera_ids || [];
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

async function refreshAll() {
  await Promise.all([loadPrompts(), loadGroups(), loadSettings(), loadQueue(), loadUsage()]);
  selectInitialPromptAndGroup();
  renderPrompts();
  renderGroupSelect();
  await loadBindingStatus();
  await loadResults();
}

function selectInitialPromptAndGroup() {
  if (!state.selectedPromptId && state.prompts.length) state.selectedPromptId = state.prompts[0].id;
  if (!state.selectedGroupKey) {
    if (state.appGroups.length) state.selectedGroupKey = `app:${state.appGroups[0].id}`;
    else if (state.sourceGroups.length) state.selectedGroupKey = `source:${state.sourceGroups[0].id}`;
  }
}

function normalizePrompt(p) {
  return {
    ...p,
    promptText: p.promptText ?? p.prompt_text ?? '',
    createdAt: p.createdAt ?? p.created_at,
    updatedAt: p.updatedAt ?? p.updated_at,
  };
}

function normalizeGroup(g, source) {
  return {
    ...g,
    id: g.id,
    name: g.name || g.id,
    description: g.description || '',
    cameraIds: camIds(g),
    source,
  };
}

async function loadPrompts() {
  const data = await api('/saved-prompts');
  state.prompts = (data.prompts || []).map(normalizePrompt);
}

async function loadGroups() {
  const [appRes, sourceRes] = await Promise.allSettled([
    api('/camera-groups'),
    api('/camera-system/source-camera-groups'),
  ]);

  state.appGroups = appRes.status === 'fulfilled' ? (appRes.value.groups || []).map(g => normalizeGroup(g, 'app')) : [];
  state.sourceGroups = sourceRes.status === 'fulfilled' ? (sourceRes.value.groups || []).map(g => normalizeGroup(g, 'source')) : [];
}

function renderPrompts() {
  const selected = getSelectedPrompt();
  $('promptList').innerHTML = state.prompts.length ? state.prompts.map(p => `
    <div class="item prompt-item ${p.id === state.selectedPromptId ? 'active' : ''}" data-prompt-id="${esc(p.id)}">
      <div class="prompt-title"><span>${esc(p.name)}</span><span class="pill ${p.enabled ? 'ok' : 'danger'}">${p.enabled ? 'enabled' : 'disabled'}</span></div>
      <p class="prompt-text-preview">${esc(p.promptText || 'No prompt text yet.')}</p>
      <div class="muted small">Updated ${esc(nowish(p.updatedAt || p.createdAt))}</div>
    </div>`).join('') : '<div class="empty">No prompts yet. Create one with + New Prompt.</div>';

  document.querySelectorAll('[data-prompt-id]').forEach(el => {
    el.onclick = async () => {
      state.selectedPromptId = el.dataset.promptId;
      renderPrompts();
      fillPromptEditor();
      await loadBindingStatus();
      await loadResults();
    };
  });

  fillPromptEditor(selected);
}

function fillPromptEditor(prompt = getSelectedPrompt()) {
  if (!prompt) {
    $('editorTitle').textContent = 'New Prompt';
    $('selectedPromptPill').textContent = 'none selected';
    $('promptId').value = '';
    $('promptName').value = '';
    $('promptDescription').value = '';
    $('promptText').value = '';
    $('promptEnabled').checked = true;
    return;
  }
  $('editorTitle').textContent = 'Edit Prompt';
  $('selectedPromptPill').textContent = prompt.name || prompt.id;
  $('promptId').value = prompt.id;
  $('promptName').value = prompt.name || '';
  $('promptDescription').value = prompt.description || '';
  $('promptText').value = prompt.promptText || '';
  $('promptEnabled').checked = prompt.enabled !== false;
}

function renderGroupSelect() {
  const options = [];
  if (state.appGroups.length) {
    options.push('<optgroup label="Prompt Camera Groups">');
    for (const g of state.appGroups) options.push(`<option value="app:${esc(g.id)}">${esc(g.name)} · ${g.cameraIds.length} cams</option>`);
    options.push('</optgroup>');
  }
  if (state.sourceGroups.length) {
    options.push('<optgroup label="Source Camera System Groups">');
    for (const g of state.sourceGroups) options.push(`<option value="source:${esc(g.id)}">${esc(g.name)} · source group</option>`);
    options.push('</optgroup>');
  }
  $('groupSelect').innerHTML = options.join('') || '<option value="">No camera groups found</option>';
  if (state.selectedGroupKey && [...$('groupSelect').options].some(o => o.value === state.selectedGroupKey)) $('groupSelect').value = state.selectedGroupKey;
  else if ($('groupSelect').options.length) state.selectedGroupKey = $('groupSelect').value;
  updateGroupHelp();
}

function getSelectedPrompt() { return state.prompts.find(p => p.id === state.selectedPromptId) || null; }
function parseGroupKey(key = state.selectedGroupKey) { const [kind, ...rest] = String(key || '').split(':'); return { kind, id: rest.join(':') }; }
function getSelectedGroup() {
  const { kind, id } = parseGroupKey();
  return kind === 'source' ? state.sourceGroups.find(g => g.id === id) : state.appGroups.find(g => g.id === id);
}

function updateGroupHelp() {
  const group = getSelectedGroup();
  if (!group) {
    $('selectedGroupPill').textContent = 'no group';
    $('groupHelp').textContent = 'No group selected.';
    return;
  }
  const countText = group.source === 'app' ? `${group.cameraIds.length} cameras` : 'source group; will be imported before scan/binding';
  $('selectedGroupPill').textContent = group.name;
  $('groupHelp').innerHTML = group.source === 'source'
    ? `<span class="group-warning">${esc(group.name)} is a source camera-system group. CamBot will create/update a prompt camera group from it before scanning.</span>`
    : `${esc(group.name)} is a prompt camera group with ${esc(countText)}.`;
}

async function getSourceGroupCameraIds(sourceGroupId) {
  const data = await api(`/camera-system/source-camera-groups/${encodeURIComponent(sourceGroupId)}/cameras`);
  const cameras = data.cameras || data.cameraIds || data.camera_ids || [];
  if (Array.isArray(cameras) && cameras.length && typeof cameras[0] === 'object') return cameras.map(c => c.id || c.cameraId).filter(Boolean);
  return cameras.filter(Boolean);
}

async function ensureScanGroup() {
  const selected = getSelectedGroup();
  if (!selected) throw new Error('Select a camera group first.');
  if (selected.source === 'app') return selected.id;

  const cameraIds = selected.cameraIds.length ? selected.cameraIds : await getSourceGroupCameraIds(selected.id);
  const payload = {
    id: selected.id,
    name: selected.name || selected.id,
    description: selected.description || `Imported from source camera group ${selected.id}`,
    cameraIds,
  };

  try {
    await api('/camera-groups', { method: 'POST', body: JSON.stringify(payload) });
  } catch (err) {
    await api(`/camera-groups/${encodeURIComponent(selected.id)}`, { method: 'PUT', body: JSON.stringify({ name: payload.name, description: payload.description }) });
    await api(`/camera-groups/${encodeURIComponent(selected.id)}/cameras`, { method: 'PUT', body: JSON.stringify({ cameraIds }) });
  }

  await loadGroups();
  state.selectedGroupKey = `app:${selected.id}`;
  renderGroupSelect();
  return selected.id;
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
  state.selectedPromptId = saved.id || id;
  renderPrompts();
  await loadBindingStatus();
}

async function deletePrompt() {
  const prompt = getSelectedPrompt();
  if (!prompt) return;
  if (!confirm(`Delete prompt "${prompt.name}"?`)) return;
  await api(`/saved-prompts/${encodeURIComponent(prompt.id)}`, { method: 'DELETE' });
  state.selectedPromptId = null;
  await loadPrompts();
  selectInitialPromptAndGroup();
  renderPrompts();
  await loadResults();
}

function newPrompt() {
  state.selectedPromptId = null;
  document.querySelectorAll('.prompt-item.active').forEach(el => el.classList.remove('active'));
  fillPromptEditor(null);
  $('resultContext').textContent = 'Create or select a prompt.';
  $('resultList').innerHTML = '<div class="empty">No prompt selected.</div>';
}

async function runScan() {
  const prompt = getSelectedPrompt();
  if (!prompt) throw new Error('Select or save a prompt first.');
  const cameraGroupId = await ensureScanGroup();
  const operation = await api('/operations', { method: 'POST', body: JSON.stringify({ promptId: prompt.id, cameraGroupId, trigger: 'manual' }) });
  $('resultContext').textContent = `Manual scan queued: ${operation.id || 'operation created'}. Refresh results after GeminiCaller processes it.`;
}

async function loadBindingStatus() {
  const prompt = getSelectedPrompt();
  const group = getSelectedGroup();
  state.selectedBinding = null;
  if (!prompt || !group) {
    $('bindingStatus').textContent = 'Select a prompt and camera group.';
    return;
  }
  if (group.source === 'source') {
    $('bindingStatus').textContent = 'Source group selected. It will be imported before enabling continuous scan.';
    return;
  }
  try {
    const data = await api(`/camera-groups/${encodeURIComponent(group.id)}/prompt-bindings`);
    const binding = (data.bindings || []).find(b => (b.promptId || b.prompt_id) === prompt.id);
    state.selectedBinding = binding || null;
    $('bindingStatus').innerHTML = binding
      ? `Continuous scan binding: <strong>${binding.enabled ? 'enabled' : 'disabled'}</strong>. Last run: ${esc(nowish(binding.lastRunAt || binding.last_run_at))}`
      : 'No continuous scan binding for this prompt/group.';
  } catch (err) {
    $('bindingStatus').textContent = err.message;
  }
}

async function setContinuousBinding(enabled) {
  const prompt = getSelectedPrompt();
  if (!prompt) throw new Error('Select or save a prompt first.');
  const cameraGroupId = await ensureScanGroup();
  await api(`/camera-groups/${encodeURIComponent(cameraGroupId)}/prompt-bindings`, {
    method: 'POST',
    body: JSON.stringify({ promptId: prompt.id, enabled }),
  });
  await loadBindingStatus();
}

async function loadResults() {
  const prompt = getSelectedPrompt();
  const group = getSelectedGroup();
  if (!prompt || !group) {
    $('resultContext').textContent = 'Select a prompt and camera group.';
    $('resultList').innerHTML = '<div class="empty">No result context selected.</div>';
    return;
  }
  const cameraGroupId = group.source === 'app' ? group.id : group.id;
  const pass = state.showingFirstPass ? 'first-pass' : 'second-pass';
  const titlePass = state.showingFirstPass ? 'first pass/intermediate' : 'second pass/global';
  $('resultContext').textContent = `${titlePass} results for "${prompt.name}" on "${group.name}".`;

  try {
    const data = await api(`/prompt-results/latest/${pass}?promptId=${encodeURIComponent(prompt.id)}&cameraGroupId=${encodeURIComponent(cameraGroupId)}`);
    const rows = data.results || [];
    renderResults(rows, state.showingFirstPass);
  } catch (err) {
    $('resultList').innerHTML = `<div class="empty">${esc(err.message)}</div>`;
  }
}

function normalizeResult(r) {
  return {
    ...r,
    cameraId: r.cameraId ?? r.camera_id,
    frameUrl: r.frameUrl ?? r.frame_url,
    include: r.include,
    firstPassPromptScore: r.firstPassPromptScore ?? r.first_pass_prompt_score,
    promptScore: r.promptScore ?? r.prompt_score ?? r.firstPassPromptScore ?? r.first_pass_prompt_score,
    operatorPriorityScore: r.operatorPriorityScore ?? r.operator_priority_score,
    operatorAction: r.operatorAction ?? r.operator_action ?? r.recommendedAction ?? r.recommended_action,
    reason: r.reason,
    globalRank: r.globalRank ?? r.global_rank,
    updatedAt: r.updatedAt ?? r.updated_at,
  };
}

function renderResults(rows, firstPass) {
  const normalized = rows.map(normalizeResult);
  if (!normalized.length) {
    $('resultList').innerHTML = `<div class="empty">No ${firstPass ? 'first-pass' : 'second-pass'} results yet.</div>`;
    return;
  }
  $('resultList').innerHTML = normalized.map((r, idx) => `
    <article class="result-card">
      ${r.frameUrl ? `<img data-frame-url="${esc(r.frameUrl)}" alt="snapshot for ${esc(r.cameraId)}">` : ''}
      <div class="score-row">
        <div><span class="muted small">${firstPass ? 'First-pass score' : 'Prompt score'}</span><div class="big-score">${Math.round(num(r.promptScore))}</div></div>
        <div><span class="muted small">Operator priority</span><div class="priority-score">${Math.round(num(r.operatorPriorityScore))}</div></div>
      </div>
      <div>
        <span class="pill">${esc(r.cameraId)}</span>
        ${r.globalRank ? `<span class="pill ok">rank ${esc(r.globalRank)}</span>` : `<span class="pill soft">#${idx + 1}</span>`}
        ${r.include === false ? '<span class="pill danger">excluded</span>' : '<span class="pill ok">included</span>'}
      </div>
      <p><strong>Operator action:</strong> ${esc(r.operatorAction || 'Review this camera.')}</p>
      <p class="muted">${esc(r.reason || '')}</p>
      <p class="muted small">Updated ${esc(nowish(r.updatedAt))}</p>
    </article>
  `).join('');
  hydrateImages();
}

async function hydrateImages() {
  const imgs = [...document.querySelectorAll('img[data-frame-url]')];
  for (const img of imgs) {
    const frameUrl = img.dataset.frameUrl;
    if (!frameUrl) continue;
    if (state.imageUrls.has(frameUrl)) { img.src = state.imageUrls.get(frameUrl); continue; }
    try {
      const response = await fetch(frameUrl.startsWith('http') ? frameUrl : frameUrl, { headers: authHeader() });
      if (!response.ok) throw new Error(`image ${response.status}`);
      const blob = await response.blob();
      const objectUrl = URL.createObjectURL(blob);
      state.imageUrls.set(frameUrl, objectUrl);
      img.src = objectUrl;
    } catch (err) {
      img.replaceWith(Object.assign(document.createElement('div'), { className: 'empty', textContent: `Could not load snapshot: ${err.message}` }));
    }
  }
}

async function loadQueue() {
  try {
    const data = await api('/operator-queue');
    renderQueue(data.items || []);
  } catch (err) {
    $('queueList').innerHTML = `<div class="empty">${esc(err.message)}</div>`;
  }
}

function normalizeQueueItem(i) {
  return {
    ...i,
    cameraId: i.cameraId ?? i.camera_id,
    status: i.status,
    promptScore: i.promptScore ?? i.prompt_score,
    operatorPriorityScore: i.operatorPriorityScore ?? i.operator_priority_score,
    operatorAction: i.operatorAction ?? i.operator_action,
    reason: i.reason,
    createdAt: i.createdAt ?? i.created_at,
  };
}

function renderQueue(items) {
  const normalized = items.map(normalizeQueueItem);
  if (!normalized.length) {
    $('queueList').innerHTML = '<div class="empty">Operator queue is empty.</div>';
    return;
  }
  $('queueList').innerHTML = normalized.map(i => `
    <div class="item queue-item">
      <div>
        <strong>${esc(i.operatorAction || 'Review camera')}</strong>
        <p class="muted">${esc(i.reason || '')}</p>
        <span class="pill">${esc(i.cameraId)}</span><span class="pill ${i.status === 'queued' ? 'warn' : 'soft'}">${esc(i.status)}</span>
      </div>
      <div class="queue-meta">
        <div class="priority-score">${Math.round(num(i.operatorPriorityScore))}</div>
        <div class="muted small">prompt ${Math.round(num(i.promptScore))}</div>
        <div class="muted small">${esc(nowish(i.createdAt))}</div>
      </div>
    </div>
  `).join('');
}

async function loadSettings() {
  try {
    const s = await api('/settings/gemini');
    $('continuousEnabled').checked = !!(s.continuousScanEnabled ?? s.continuous_scan_enabled);
    $('continuousInterval').value = s.continuousScanIntervalSeconds ?? s.continuous_scan_interval_seconds ?? 900;
    $('geminiDelay').value = s.geminiCallDelayMs ?? s.gemini_call_delay_ms ?? 2000;
    $('maxCostDay').value = s.maxCostPerDay ?? s.max_cost_per_day ?? 10;
    $('nextScanAt').textContent = nowish(s.nextContinuousScanAt ?? s.next_continuous_scan_at);
  } catch (err) {
    $('usageSummary').textContent = err.message;
  }
}

async function saveSettings() {
  await api('/settings/gemini', {
    method: 'PUT',
    body: JSON.stringify({
      continuousScanEnabled: $('continuousEnabled').checked,
      continuousScanIntervalSeconds: Number($('continuousInterval').value),
      geminiCallDelayMs: Number($('geminiDelay').value),
      maxCostPerDay: Number($('maxCostDay').value),
    }),
  });
  await loadSettings();
}

async function loadUsage() {
  try {
    const u = await api('/usage/summary');
    $('usageSummary').textContent = JSON.stringify(u, null, 2);
    $('prevDayCost').textContent = fmtMoney(u.previousDayCost ?? u.previous_day_cost ?? u.yesterdayCost ?? u.yesterday_cost);
    $('monthCost').textContent = fmtMoney(u.monthToDateCost ?? u.month_to_date_cost ?? u.monthlyCost ?? u.monthly_cost);
    $('projectedCost').textContent = fmtMoney(u.projectedCostPerDay ?? u.projected_cost_per_day);
  } catch (err) {
    $('usageSummary').textContent = err.message;
  }
}

function wire() {
  $('loginBtn').onclick = () => login().catch(e => $('loginMsg').textContent = e.message);
  $('logoutBtn').onclick = logout;
  $('newPromptBtn').onclick = newPrompt;
  $('refreshPromptsBtn').onclick = () => loadPrompts().then(renderPrompts).catch(alert);
  $('savePromptBtn').onclick = () => savePrompt().catch(e => alert(e.message));
  $('deletePromptBtn').onclick = () => deletePrompt().catch(e => alert(e.message));
  $('runBtn').onclick = () => runScan().catch(e => alert(e.message));
  $('enableContinuousBtn').onclick = () => setContinuousBinding(true).catch(e => alert(e.message));
  $('disableContinuousBtn').onclick = () => setContinuousBinding(false).catch(e => alert(e.message));
  $('refreshResultsBtn').onclick = () => loadResults().catch(e => alert(e.message));
  $('showFirstPassBtn').onclick = () => { state.showingFirstPass = !state.showingFirstPass; $('showFirstPassBtn').textContent = state.showingFirstPass ? 'Show Second Pass' : 'Show First Pass'; loadResults().catch(alert); };
  $('refreshQueueBtn').onclick = () => loadQueue().catch(e => alert(e.message));
  $('saveSettingsBtn').onclick = () => saveSettings().then(loadUsage).catch(e => alert(e.message));
  $('groupSelect').onchange = async () => { state.selectedGroupKey = $('groupSelect').value; updateGroupHelp(); await loadBindingStatus(); await loadResults(); };
}

wire();
loadAuth();
if (state.auth) {
  $('login').hidden = true;
  $('dashboard').hidden = false;
  refreshAll().catch(err => {
    console.error(err);
    localStorage.removeItem('cambotAuth');
    $('login').hidden = false;
    $('dashboard').hidden = true;
    $('loginMsg').textContent = err.message;
  });
}
