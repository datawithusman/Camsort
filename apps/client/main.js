import backend from "./repositories/BackEnd.js";

const runtimeConfig = window.CAMBOT_CONFIG || {};
backend.configure({
  cambotBaseUrl: runtimeConfig.cambotBaseUrl || runtimeConfig.cambotApiBasePath || "/api",
  cameraSystemBaseUrl: runtimeConfig.cameraSystemBaseUrl || runtimeConfig.cameraSystemApiBasePath || "/api/camera-system",
});
window.CamBotBackend = backend;

const AUTH_STORAGE_KEY = "cambot.client.basicAuth.v2";

const state = {
  prompts: [],
  cameraGroups: [],
  settings: null,
  selectedPromptId: null,
  selectedCameraGroupId: null,
  selectedOperationId: null,
  results: [],
  queueItems: [],
  objectUrls: [],
};

const $ = (id) => document.getElementById(id);
const el = {
  loginView: $("login-view"), dashboardView: $("dashboard-view"), loginForm: $("login-form"), loginUser: $("login-user"), loginPass: $("login-pass"), loginError: $("login-error"), logoutBtn: $("logout-btn"), healthPill: $("health-pill"), refreshCamerasBtn: $("refresh-cameras-btn"), toast: $("toast"),
  promptList: $("prompt-list"), promptCount: $("prompt-count"), promptForm: $("prompt-form"), promptId: $("prompt-id"), promptName: $("prompt-name"), promptText: $("prompt-text"), resetPromptBtn: $("reset-prompt-btn"), selectedPrompt: $("selected-prompt"),
  cameraGroupSelect: $("camera-group-select"), runScanBtn: $("run-scan-btn"), scheduleBtn: $("schedule-btn"),
  resultsTitle: $("results-title"), resultsSubtitle: $("results-subtitle"), resultGrid: $("result-grid"), emptyResults: $("empty-results"), scanBanner: $("scan-banner"),
  cameraCount: $("camera-count"), scheduledCount: $("scheduled-count"), runningCount: $("running-count"), activityList: $("activity-list"),
  queueList: $("operator-queue-list"), settingsForm: $("settings-form"), continuousScanEnabled: $("continuous-scan-enabled"), continuousScanInterval: $("continuous-scan-interval"), geminiCallDelay: $("gemini-call-delay"), costSummary: $("cost-summary"),
};

installHandlers();
restoreCachedLogin();

function installHandlers() {
  el.loginForm?.addEventListener("submit", async e => { e.preventDefault(); await connect(); });
  el.logoutBtn?.addEventListener("click", logout);
  el.refreshCamerasBtn?.addEventListener("click", loadDashboardData);
  el.promptForm?.addEventListener("submit", async e => { e.preventDefault(); await savePrompt(); });
  el.resetPromptBtn?.addEventListener("click", clearPromptForm);
  el.selectedPrompt?.addEventListener("change", async () => { state.selectedPromptId = el.selectedPrompt.value || null; await loadLatestPromptResults(); renderAll(); });
  el.cameraGroupSelect?.addEventListener("change", () => { state.selectedCameraGroupId = el.cameraGroupSelect.value || null; });
  el.runScanBtn?.addEventListener("click", runManualScan);
  el.scheduleBtn?.addEventListener("click", toggleBindingForSelectedPrompt);
  el.settingsForm?.addEventListener("submit", async e => { e.preventDefault(); await saveSettings(); });
}

async function connect() {
  const username = el.loginUser.value.trim();
  const password = el.loginPass.value;
  if (!username || !password) return showLoginError("Enter Basic Auth credentials.");
  backend.setBasicAuth(username, password);
  try { await checkHealth(); cacheLogin(username, password); showDashboard(); await loadDashboardData(); }
  catch (e) { backend.clearBasicAuth(); clearCachedLogin(); showLoginError(errorToMessage(e)); }
}
async function restoreCachedLogin() { const c=readCachedLogin(); if(!c) return showLogin(); el.loginUser.value=c.username; el.loginPass.value=c.password; backend.setBasicAuth(c.username,c.password); try{ await checkHealth(); showDashboard(); await loadDashboardData(); }catch(e){ clearCachedLogin(); backend.clearBasicAuth(); showLogin(); } }
function logout(){ clearCachedLogin(); backend.clearBasicAuth(); showLogin(); }
function showDashboard(){ el.loginView.hidden=true; el.dashboardView.hidden=false; document.body.classList.add("is-authenticated"); }
function showLogin(){ el.dashboardView.hidden=true; el.loginView.hidden=false; document.body.classList.remove("is-authenticated"); }
function cacheLogin(username,password){ try{ localStorage.setItem(AUTH_STORAGE_KEY,JSON.stringify({username,password})); }catch{} }
function readCachedLogin(){ try{ const v=JSON.parse(localStorage.getItem(AUTH_STORAGE_KEY)||"null"); return v?.username&&v?.password?v:null; }catch{return null;} }
function clearCachedLogin(){ try{ localStorage.removeItem(AUTH_STORAGE_KEY); }catch{} }
function showLoginError(msg){ el.loginError.textContent=msg; el.loginError.hidden=false; }

async function checkHealth(){ el.healthPill.textContent="checking..."; const h=await backend.cambot.health(); el.healthPill.textContent=`api ok · db ${h?.database?.status||"?"} · camera ${h?.cameraSystem?.status||"?"}`; el.healthPill.className="health-pill ok"; return h; }
async function loadDashboardData(){ await Promise.allSettled([loadPrompts(), loadGroups(), loadSettings(), loadQueue()]); await loadLatestPromptResults(); renderAll(); }
async function loadPrompts(){ const r=await backend.cambot.savedPrompts.list(); state.prompts=Array.isArray(r?.prompts)?r.prompts:[]; if(!state.selectedPromptId) state.selectedPromptId=state.prompts[0]?.id||null; }
async function loadGroups(){ const r=await backend.cambot.cameraGroups.list(); state.cameraGroups=Array.isArray(r?.groups)?r.groups:[]; if(!state.selectedCameraGroupId) state.selectedCameraGroupId=state.cameraGroups[0]?.id||null; el.cameraCount.textContent=String(state.cameraGroups.reduce((n,g)=>n+(g.cameraIds?.length||0),0)); }
async function loadSettings(){ state.settings=await backend.cambot.settings.gemini.get(); }
async function loadQueue(){ const r=await backend.cambot.operatorQueue.list({status:"queued",limit:50,offset:0}); state.queueItems=Array.isArray(r?.items)?r.items:[]; }
async function loadLatestPromptResults(){ revokeUrls(); state.results=[]; if(!state.selectedPromptId) return; const ops=await backend.cambot.operations.list({promptId:state.selectedPromptId,status:"completed",limit:1,offset:0}); const op=ops?.operations?.[0]; state.selectedOperationId=op?.id||null; if(!op) return; const rr=await backend.cambot.operations.results(op.id); const rows=Array.isArray(rr?.results)?rr.results:[]; state.results=await Promise.all(rows.map(async row=>({...row,imageUrl: await loadProtectedImageUrl(row.frameUrl)}))); }

async function savePrompt(){ const payload={ name: el.promptName.value.trim(), promptText: el.promptText.value.trim(), enabled:true }; if(!payload.name||!payload.promptText) return showToast("Prompt name and text are required.","bad"); const id=el.promptId.value; const saved=id? await backend.cambot.savedPrompts.update(id,payload): await backend.cambot.savedPrompts.create(payload); state.selectedPromptId=saved.id; clearPromptForm(); await loadDashboardData(); showToast("Prompt saved.","good"); }
function clearPromptForm(){ el.promptId.value=""; el.promptName.value=""; el.promptText.value=""; document.querySelector(".prompt-editor")?.removeAttribute("open"); }
function editPrompt(id){ const p=state.prompts.find(x=>x.id===id); if(!p)return; el.promptId.value=p.id; el.promptName.value=p.name||""; el.promptText.value=p.promptText||""; document.querySelector(".prompt-editor")?.setAttribute("open",""); }
async function deletePrompt(id){ await backend.cambot.savedPrompts.delete(id); if(state.selectedPromptId===id) state.selectedPromptId=null; await loadDashboardData(); }

async function runManualScan(){ if(!state.selectedPromptId||!state.selectedCameraGroupId) return showToast("Select a prompt and camera group.","bad"); el.scanBanner.hidden=false; try{ const op=await backend.cambot.operations.create({promptId:state.selectedPromptId,cameraGroupId:state.selectedCameraGroupId,trigger:"manual"}); state.selectedOperationId=op.id; showToast("Manual scan queued. It will run after the current prompt operation finishes.","good"); await loadDashboardData(); }catch(e){ showToast(errorToMessage(e),"bad"); } finally{ el.scanBanner.hidden=true; } }
async function toggleBindingForSelectedPrompt(){ if(!state.selectedPromptId||!state.selectedCameraGroupId) return showToast("Select a prompt and camera group.","bad"); const bindings=await backend.cambot.promptBindings.list(state.selectedCameraGroupId); const existing=(bindings?.bindings||[]).find(b=>b.promptId===state.selectedPromptId); if(existing){ await backend.cambot.promptBindings.update(state.selectedCameraGroupId, existing.id, {enabled:!existing.enabled}); showToast(existing.enabled?"Removed from global continuous scan cycle.":"Added to global continuous scan cycle.","good"); } else { await backend.cambot.promptBindings.create(state.selectedCameraGroupId,{promptId:state.selectedPromptId,enabled:true}); showToast("Added to global continuous scan cycle.","good"); } await loadDashboardData(); }
async function saveSettings(){ const payload={ continuousScanEnabled: el.continuousScanEnabled.checked, continuousScanIntervalSeconds:Number(el.continuousScanInterval.value||900), geminiCallDelayMs:Number(el.geminiCallDelay.value||2000) }; await backend.cambot.settings.gemini.update(payload); await loadSettings(); renderSettings(); showToast("Global settings saved.","good"); }

async function loadProtectedImageUrl(frameUrl){ if(!frameUrl)return null; try{ const blob=await backend.requestUrl(frameUrl,{headers:{Accept:"image/*"}}); if(blob instanceof Blob){ const url=URL.createObjectURL(blob); state.objectUrls.push(url); return url; }}catch{} return frameUrl; }
function revokeUrls(){ for(const u of state.objectUrls) URL.revokeObjectURL(u); state.objectUrls=[]; }

function renderAll(){ renderPrompts(); renderControls(); renderResults(); renderQueue(); renderSettings(); }
function renderPrompts(){ el.promptCount.textContent=String(state.prompts.length); el.promptList.innerHTML=state.prompts.map(p=>`<article class="prompt-card ${p.id===state.selectedPromptId?'selected':''}" data-id="${esc(p.id)}"><div class="status-dot-row"><span class="status-dot ${p.enabled?'scheduled':'idle'}"></span><h3>${html(p.name)}</h3></div><p>${html(truncate(p.promptText,130))}</p><div class="card-actions"><button data-a="select">Select</button><button class="secondary-button" data-a="edit">Edit</button><button class="ghost-button danger" data-a="delete">Delete</button></div></article>`).join("")||`<div class="prompt-card"><p>No prompts yet.</p></div>`; el.promptList.querySelectorAll(".prompt-card").forEach(card=>{ const id=card.dataset.id; card.querySelector('[data-a="select"]')?.addEventListener("click",async()=>{state.selectedPromptId=id; await loadLatestPromptResults(); renderAll();}); card.querySelector('[data-a="edit"]')?.addEventListener("click",()=>editPrompt(id)); card.querySelector('[data-a="delete"]')?.addEventListener("click",()=>deletePrompt(id)); }); }
function renderControls(){ el.selectedPrompt.innerHTML=`<option value="">Select prompt...</option>`+state.prompts.map(p=>`<option value="${esc(p.id)}" ${p.id===state.selectedPromptId?'selected':''}>${html(p.name)}</option>`).join(""); el.cameraGroupSelect.innerHTML=`<option value="">Select camera group...</option>`+state.cameraGroups.map(g=>`<option value="${esc(g.id)}" ${g.id===state.selectedCameraGroupId?'selected':''}>${html(g.name||g.id)} (${g.cameraIds?.length||0})</option>`).join(""); el.scheduledCount.textContent="global"; el.runningCount.textContent=String(state.queueItems.length); }
function renderResults(){ const p=state.prompts.find(x=>x.id===state.selectedPromptId); el.resultsTitle.textContent=p?p.name:"No prompt selected"; el.resultsSubtitle.textContent=p?`Latest completed scan · operation ${state.selectedOperationId||'none'}`:"Create or select a prompt."; if(!state.results.length){ el.emptyResults.hidden=false; el.resultGrid.innerHTML=""; return; } el.emptyResults.hidden=true; el.resultGrid.innerHTML=state.results.map(r=>`<article class="result-card">${r.imageUrl?`<img src="${esc(r.imageUrl)}" alt="Snapshot for ${esc(r.cameraId)}" />`:""}<div class="result-card-body"><div class="result-card-top"><div><h3>${html(r.cameraId)}</h3><p>Prompt match ${num(r.promptMatchScore)} · Operator priority ${num(r.operatorPriorityScore)}</p></div><span class="rank-badge">${num(r.operatorPriorityScore)}</span></div><p><strong>Recommended:</strong> ${html(r.recommendedAction||"")}</p><p>${html(r.reason||"")}</p><div class="frame-line">frame: ${html(r.frameRefId||"")}</div></div></article>`).join(""); }
function renderQueue(){ if(!el.queueList)return; el.queueList.innerHTML=state.queueItems.map(i=>`<article class="activity-card"><h3>${html(i.cameraId)} · priority ${num(i.operatorPriorityScore)}</h3><p>${html(i.recommendedAction||"")}</p><p>${html(i.reason||"")}</p><small>${html(i.status||"")}</small></article>`).join("")||`<div class="activity-card"><p>No queued operator actions.</p></div>`; el.activityList.innerHTML=el.queueList.innerHTML; }
function renderSettings(){ if(!state.settings)return; el.continuousScanEnabled.checked=!!state.settings.continuousScanEnabled; el.continuousScanInterval.value=state.settings.continuousScanIntervalSeconds||900; el.geminiCallDelay.value=state.settings.geminiCallDelayMs||2000; const bindings='enabled prompt bindings run every '+(state.settings.continuousScanIntervalSeconds||900)+' seconds'; el.costSummary.textContent=`${bindings}. Previous/day/month cost comes from /usage/summary.`; }
function num(v){ const n=Number(v||0); return Number.isFinite(n)?n.toFixed(0):"0"; }
function truncate(v,n){ const s=String(v||""); return s.length<=n?s:s.slice(0,n-1)+"…"; }
function html(v){ return String(v??"").replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;").replaceAll("'","&#039;"); }
function esc(v){ return html(v); }
function errorToMessage(e){ return e?.body ? (typeof e.body==="string"?e.body:JSON.stringify(e.body)) : (e?.message||String(e)); }
function showToast(message,kind=""){ el.toast.textContent=message; el.toast.className=`toast ${kind}`.trim(); el.toast.hidden=false; clearTimeout(showToast.t); showToast.t=setTimeout(()=>el.toast.hidden=true,4000); }
