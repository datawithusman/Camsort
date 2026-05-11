from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal

app = FastAPI(title="CamBot RestApi")

ActionStatus = Literal["open", "acknowledged", "resolved", "dismissed"]

class UpdateOperatorActionRequest(BaseModel):
    status: ActionStatus
    operatorNote: str | None = None

_now = lambda: datetime.now(timezone.utc).isoformat()

ACTIONS = [
    {
        "id": "action-001",
        "cameraId": "CAM-014",
        "promptId": "prompt-001",
        "sortRunId": "run-001",
        "rank": 1,
        "score": 0.94,
        "severity": "high",
        "classification": "obstructed_view",
        "reason": "The camera view is mostly blocked by an object near the lens.",
        "recommendedAction": "Dispatch maintenance to inspect and clear the obstruction.",
        "operatorPriority": "immediate",
        "status": "open",
        "snapshotUrl": "/cam/cameras/CAM-014/snapshot.jpg",
        "createdAt": _now(),
        "updatedAt": _now(),
    },
    {
        "id": "action-002",
        "cameraId": "CAM-006",
        "promptId": "prompt-001",
        "sortRunId": "run-001",
        "rank": 2,
        "score": 0.82,
        "severity": "medium",
        "classification": "dim_lighting",
        "reason": "The camera view appears dark and may be difficult for operators to interpret.",
        "recommendedAction": "Check lighting in this area or inspect camera night mode.",
        "operatorPriority": "urgent",
        "status": "open",
        "snapshotUrl": "/cam/cameras/CAM-006/snapshot.jpg",
        "createdAt": _now(),
        "updatedAt": _now(),
    },
]

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/operator-actions")
def list_operator_actions():
    return {"actions": ACTIONS}

@app.patch("/api/operator-actions/{action_id}")
def update_operator_action(action_id: str, body: UpdateOperatorActionRequest):
    for action in ACTIONS:
        if action["id"] == action_id:
            action["status"] = body.status
            action["updatedAt"] = _now()
            return action
    raise HTTPException(status_code=404, detail="operator action not found")

@app.get("/api/stats")
def stats():
    return {
        "operatorActionsOpen": sum(1 for a in ACTIONS if a["status"] == "open"),
        "operatorActionsAcknowledged": sum(1 for a in ACTIONS if a["status"] == "acknowledged"),
        "operatorActionsResolved": sum(1 for a in ACTIONS if a["status"] == "resolved"),
        "operatorActionsDismissed": sum(1 for a in ACTIONS if a["status"] == "dismissed"),
        "workerRunsToday": 1,
        "geminiCallsToday": 0,
        "skippedRunsDueToRateLimitToday": 0,
        "lastWorkerRunAt": None,
        "lastSuccessfulWorkerRunAt": None,
    }
