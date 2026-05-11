import {
  normalizeOperatorActionsResponse,
  normalizeStats,
} from "./dtos/camBotDtos.js";

async function fetchJson(url, options = {}) {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

async function updateAction(actionId, status) {
  await fetchJson(`/api/operator-actions/${actionId}`, {
    method: "PATCH",
    body: JSON.stringify({ status }),
  });
  await loadDashboard();
}

function renderStats(raw) {
  const stats = normalizeStats(raw);
  document.getElementById("stats").textContent =
    `Open: ${stats.operatorActionsOpen} · ` +
    `Acknowledged: ${stats.operatorActionsAcknowledged} · ` +
    `Resolved: ${stats.operatorActionsResolved} · ` +
    `Gemini calls today: ${stats.geminiCallsToday}`;
}

function renderActions(raw) {
  const { actions } = normalizeOperatorActionsResponse(raw);
  const container = document.getElementById("actions");

  if (actions.length === 0) {
    container.textContent = "No operator actions yet.";
    return;
  }

  container.innerHTML = "";

  for (const action of actions) {
    const card = document.createElement("article");
    card.className = "card";
    card.innerHTML = `
      <img src="${action.snapshotUrl || ""}" alt="${action.cameraId}" />
      <h3>${action.cameraId}</h3>
      <p>
        <span class="badge">${action.severity}</span>
        <span class="badge">score ${Math.round(action.score * 100)}</span>
        <span class="badge">${action.status}</span>
      </p>
      <p><strong>Classification:</strong> ${action.classification}</p>
      <p><strong>Reason:</strong> ${action.reason}</p>
      <p><strong>Recommended action:</strong> ${action.recommendedAction}</p>
      <div>
        <button data-status="acknowledged">Acknowledge</button>
        <button data-status="resolved">Resolve</button>
        <button data-status="dismissed">Dismiss</button>
      </div>
    `;

    for (const button of card.querySelectorAll("button")) {
      button.addEventListener("click", () => updateAction(action.id, button.dataset.status));
    }

    container.appendChild(card);
  }
}

async function loadDashboard() {
  try {
    const [stats, actions] = await Promise.all([
      fetchJson("/api/stats"),
      fetchJson("/api/operator-actions"),
    ]);
    renderStats(stats);
    renderActions(actions);
  } catch (err) {
    document.getElementById("actions").textContent = `Failed to load dashboard: ${err.message}`;
  }
}

document.getElementById("refreshBtn").addEventListener("click", loadDashboard);
loadDashboard();
