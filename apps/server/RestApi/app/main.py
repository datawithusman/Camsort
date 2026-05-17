from __future__ import annotations
import os, uuid
from datetime import datetime, timezone
from typing import Any
import requests
from fastapi import FastAPI, HTTPException, Query, Response
from sqlalchemy import text
from app.db.connection import connect, row_to_dict, rows_to_dicts, check_database_connection

app = FastAPI(title="CamBot REST API")
JsonObject = dict[str, Any]

def nid(prefix): return f"{prefix}-{uuid.uuid4()}"
def now(): return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
def nf(entity, ident): raise HTTPException(404, {"error": f"{entity} not found", "details": ident})
def cam_base(): return os.getenv("CAMERA_SYSTEM_BASE_URL", "http://camera-system-mocker-rest-api:8080").rstrip("/")

def one(sql, params=None, commit=False):
    with connect() as c:
        row = c.execute(text(sql), params or {}).first()
        if commit: c.commit()
        return row_to_dict(row)

def many(sql, params=None):
    with connect() as c:
        return rows_to_dicts(c.execute(text(sql), params or {}).fetchall())

def cam(path, **params):
    url = cam_base() + path
    try:
        r = requests.get(url, params={k:v for k,v in params.items() if v is not None}, timeout=float(os.getenv("CAMERA_SYSTEM_TIMEOUT_SECONDS", "30")))
        r.raise_for_status(); return r.json() if r.content else {}
    except requests.HTTPError as e:
        raise HTTPException(e.response.status_code, {"error":"Camera system request failed", "url": url, "body": e.response.text})
    except Exception as e:
        raise HTTPException(502, {"error":"Camera system request failed", "url": url, "message": str(e)})

@app.get("/health")
def health():
    db = check_database_connection(); cs = camera_health()
    return {"status":"ok" if db.get("status") == "ok" and cs.get("status") == "ok" else "degraded", "service":"rest-api", "checkedAt": now(), "database": db, "cameraSystem": cs}

@app.get("/camera-system/health")
def camera_health():
    try: return {"status":"ok", **cam("/health")}
    except Exception as e: return {"status":"error", "error": str(e)}

@app.get("/camera-system/status")
def camera_status(): return cam("/system/status")
@app.get("/camera-system/cameras")
def cameras(group_id: str|None=Query(default=None, alias="groupId"), search: str|None=None): return cam("/cameras", groupId=group_id, search=search)
@app.get("/camera-system/cameras/{camera_id}")
def camera(camera_id: str): return cam(f"/cameras/{camera_id}")

@app.get("/camera-system/cameras/{camera_id}/snapshot")
def snapshot(camera_id: str):
    s = cam(f"/cameras/{camera_id}/snapshot"); f = s.get("frame") or {}
    fr = one("""
INSERT INTO camera_frame_refs (id,camera_id,frame_id,snapshot_id,frame_url,sequence_number,captured_at,mime_type,width,height,expires_at)
VALUES (:id,:camera_id,:frame_id,:snapshot_id,:frame_url,:sequence_number,COALESCE(CAST(:captured_at AS timestamptz),now()),COALESCE(:mime_type,'image/jpeg'),:width,:height,:expires_at)
ON CONFLICT (camera_id,frame_id) DO UPDATE SET snapshot_id=EXCLUDED.snapshot_id, frame_url=EXCLUDED.frame_url, sequence_number=EXCLUDED.sequence_number, captured_at=EXCLUDED.captured_at, mime_type=EXCLUDED.mime_type, width=EXCLUDED.width, height=EXCLUDED.height, expires_at=EXCLUDED.expires_at, updated_at=now()
RETURNING *
""", {"id": nid("frame-ref"), "camera_id": s.get("cameraId"), "frame_id": f.get("frameId"), "snapshot_id": s.get("snapshotId"), "frame_url": f.get("url"), "sequence_number": f.get("sequenceNumber"), "captured_at": f.get("capturedAt"), "mime_type": f.get("mimeType"), "width": f.get("width"), "height": f.get("height"), "expires_at": f.get("expiresAt")}, True)
    return {**s, "frameRef": fr}

@app.get("/camera-system/cameras/{camera_id}/frames/{frame_id}/url")
def frame_url(camera_id: str, frame_id: str): return cam(f"/cameras/{camera_id}/frames/{frame_id}/url")

@app.get("/camera-system/cameras/{camera_id}/frames/{frame_id}/image")
def frame_image(camera_id: str, frame_id: str):
    """
    Proxy frame image bytes from the camera-system mocker through RestApi.

    This makes both of these browser paths work behind nginx:
      /camera-system/cameras/{camera_id}/frames/{frame_id}/image
      /api/camera-system/cameras/{camera_id}/frames/{frame_id}/image

    The second path is useful when the frontend treats returned frame URLs as
    API assets and prefixes them with /api.
    """
    url = cam_base() + f"/cameras/{camera_id}/frames/{frame_id}/image"
    try:
        r = requests.get(
            url,
            timeout=float(os.getenv("CAMERA_SYSTEM_TIMEOUT_SECONDS", "30")),
        )
        r.raise_for_status()
        return Response(
            content=r.content,
            media_type=r.headers.get("content-type") or "image/jpeg",
            headers={"Cache-Control": "no-store"},
        )
    except requests.HTTPError as e:
        raise HTTPException(
            e.response.status_code,
            {"error": "Camera frame image request failed", "url": url, "body": e.response.text},
        )
    except Exception as e:
        raise HTTPException(
            502,
            {"error": "Camera frame image request failed", "url": url, "message": str(e)},
        )

@app.get("/camera-system/cameras/{camera_id}/stream")
def stream(camera_id: str): return cam(f"/cameras/{camera_id}/stream")
@app.get("/camera-system/source-camera-groups")
def source_groups(): return cam("/camera-groups")
@app.get("/camera-system/source-camera-groups/{group_id}")
def source_group(group_id: str): return cam(f"/camera-groups/{group_id}")
@app.get("/camera-system/source-camera-groups/{group_id}/cameras")
def source_group_cameras(group_id: str): return cam(f"/camera-groups/{group_id}/cameras")

@app.get("/camera-system/cameras/{camera_id}/frame-refs")
def frame_refs(camera_id: str, limit:int=50, offset:int=0): return {"frameRefs": many("SELECT * FROM camera_frame_refs WHERE camera_id=:id ORDER BY captured_at DESC LIMIT :limit OFFSET :offset", {"id":camera_id,"limit":limit,"offset":offset})}
@app.get("/camera-system/cameras/{camera_id}/frame-refs/latest")
def latest_frame(camera_id: str):
    r=one("SELECT * FROM camera_frame_refs WHERE camera_id=:id ORDER BY captured_at DESC LIMIT 1", {"id":camera_id})
    if not r: nf("Camera frame ref", camera_id)
    return r

@app.get("/camera-groups")
def list_groups(): return {"groups": many("SELECT * FROM camera_groups ORDER BY created_at DESC")}
@app.post("/camera-groups", status_code=201)
def create_group(p: JsonObject): return one("INSERT INTO camera_groups (id,name,description,camera_ids) VALUES (COALESCE(NULLIF(:id,''),:new),:name,:description,:camera_ids) RETURNING *", {"id":p.get("id"),"new":nid("group"),"name":p["name"],"description":p.get("description"),"camera_ids":p.get("cameraIds") or []}, True)
@app.get("/camera-groups/{group_id}")
def get_group(group_id: str):
    r=one("SELECT * FROM camera_groups WHERE id=:id", {"id":group_id})
    if not r: nf("Camera group", group_id)
    return r
@app.get("/camera-groups/{group_id}/stats")
def group_stats(group_id: str):
    g=get_group(group_id); return {"cameraCount": len(g.get("cameraIds") or [])}
@app.put("/camera-groups/{group_id}")
def update_group(group_id: str, p: JsonObject):
    r=one("UPDATE camera_groups SET name=COALESCE(:name,name), description=COALESCE(:description,description), updated_at=now() WHERE id=:id RETURNING *", {"id":group_id,"name":p.get("name"),"description":p.get("description")}, True)
    if not r: nf("Camera group", group_id)
    return r
@app.put("/camera-groups/{group_id}/cameras")
def set_group_cameras(group_id: str, p: JsonObject):
    r=one("UPDATE camera_groups SET camera_ids=:camera_ids, updated_at=now() WHERE id=:id RETURNING *", {"id":group_id,"camera_ids":p.get("cameraIds") or []}, True)
    if not r: nf("Camera group", group_id)
    return r
@app.delete("/camera-groups/{group_id}", status_code=204)
def delete_group(group_id: str):
    with connect() as c:
        res=c.execute(text("DELETE FROM camera_groups WHERE id=:id"), {"id":group_id}); c.commit()
        if res.rowcount==0: nf("Camera group", group_id)
    return Response(status_code=204)

@app.get("/saved-prompts")
def prompts(): return {"prompts": many("SELECT * FROM saved_prompts ORDER BY created_at DESC")}
@app.post("/saved-prompts", status_code=201)
def create_prompt(p: JsonObject): return one("INSERT INTO saved_prompts (id,name,description,prompt_text,enabled) VALUES (COALESCE(NULLIF(:id,''),:new),:name,:description,:prompt_text,COALESCE(:enabled,true)) RETURNING *", {"id":p.get("id"),"new":nid("prompt"),"name":p["name"],"description":p.get("description"),"prompt_text":p.get("promptText") or "","enabled":p.get("enabled", True)}, True)
@app.get("/saved-prompts/{prompt_id}")
def get_prompt(prompt_id: str):
    r=one("SELECT * FROM saved_prompts WHERE id=:id", {"id":prompt_id})
    if not r: nf("Saved prompt", prompt_id)
    return r
@app.put("/saved-prompts/{prompt_id}")
def update_prompt(prompt_id: str, p: JsonObject):
    r=one("UPDATE saved_prompts SET name=COALESCE(:name,name), description=COALESCE(:description,description), prompt_text=COALESCE(:prompt_text,prompt_text), enabled=COALESCE(:enabled,enabled), updated_at=now() WHERE id=:id RETURNING *", {"id":prompt_id,"name":p.get("name"),"description":p.get("description"),"prompt_text":p.get("promptText"),"enabled":p.get("enabled")}, True)
    if not r: nf("Saved prompt", prompt_id)
    return r
@app.delete("/saved-prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    with connect() as c:
        res=c.execute(text("DELETE FROM saved_prompts WHERE id=:id"), {"id":prompt_id}); c.commit()
        if res.rowcount==0: nf("Saved prompt", prompt_id)
    return Response(status_code=204)

@app.get("/camera-groups/{group_id}/prompt-bindings")
def bindings(group_id: str): return {"bindings": many("SELECT * FROM prompt_bindings WHERE camera_group_id=:id ORDER BY created_at DESC", {"id":group_id})}
@app.post("/camera-groups/{group_id}/prompt-bindings", status_code=201)
def create_binding(group_id: str, p: JsonObject):
    get_group(group_id); get_prompt(p["promptId"])
    return one("INSERT INTO prompt_bindings (id,camera_group_id,prompt_id,enabled) VALUES (COALESCE(NULLIF(:id,''),:new),:gid,:pid,COALESCE(:enabled,true)) ON CONFLICT (camera_group_id,prompt_id) DO UPDATE SET enabled=EXCLUDED.enabled, updated_at=now() RETURNING *", {"id":p.get("id"),"new":nid("binding"),"gid":group_id,"pid":p["promptId"],"enabled":p.get("enabled", True)}, True)
@app.put("/camera-groups/{group_id}/prompt-bindings/{binding_id}")
def update_binding(group_id: str, binding_id: str, p: JsonObject):
    r=one("UPDATE prompt_bindings SET enabled=COALESCE(:enabled,enabled), updated_at=now() WHERE id=:id AND camera_group_id=:gid RETURNING *", {"id":binding_id,"gid":group_id,"enabled":p.get("enabled")}, True)
    if not r: nf("Prompt binding", binding_id)
    return r
@app.delete("/camera-groups/{group_id}/prompt-bindings/{binding_id}", status_code=204)
def delete_binding(group_id: str, binding_id: str):
    with connect() as c:
        res=c.execute(text("DELETE FROM prompt_bindings WHERE id=:id AND camera_group_id=:gid"), {"id":binding_id,"gid":group_id}); c.commit()
        if res.rowcount==0: nf("Prompt binding", binding_id)
    return Response(status_code=204)

def estimate(prompt_id, camera_group_id):
    get_prompt(prompt_id); g=get_group(camera_group_id); n=len(g.get("cameraIds") or [])
    return {"allowed":True,"restrictionReason":None,"estimatedCameraCount":n,"estimatedGeminiCalls":n+1,"estimatedTokenCount":n*1024,"estimatedCost":0.0}
@app.post("/operations/estimate")
def estimate_operation(p: JsonObject): return estimate(p["promptId"], p["cameraGroupId"])
@app.get("/operations")
def list_operations(prompt_id: str|None=Query(default=None, alias="promptId"), camera_group_id: str|None=Query(default=None, alias="cameraGroupId"), status: str|None=None, limit:int=50, offset:int=0):
    return {"operations": many("SELECT * FROM operations WHERE (:pid IS NULL OR prompt_id=:pid) AND (:gid IS NULL OR camera_group_id=:gid) AND (:status IS NULL OR status=:status) ORDER BY created_at DESC LIMIT :limit OFFSET :offset", {"pid":prompt_id,"gid":camera_group_id,"status":status,"limit":limit,"offset":offset})}
@app.post("/operations", status_code=201)
def create_operation(p: JsonObject):
    e=estimate(p["promptId"], p["cameraGroupId"])
    return one("INSERT INTO operations (id,prompt_id,camera_group_id,prompt_binding_id,trigger,status,total_cameras,estimated_gemini_calls,estimated_token_count,estimated_cost) VALUES (COALESCE(NULLIF(:id,''),:new),:pid,:gid,:bid,COALESCE(:trigger,'manual'),COALESCE(:status,'queued'),:total,:calls,:tokens,:cost) RETURNING *", {"id":p.get("id"),"new":nid("operation"),"pid":p["promptId"],"gid":p["cameraGroupId"],"bid":p.get("promptBindingId"),"trigger":p.get("trigger","manual"),"status":p.get("status","queued"),"total":e["estimatedCameraCount"],"calls":e["estimatedGeminiCalls"],"tokens":e["estimatedTokenCount"],"cost":e["estimatedCost"]}, True)
@app.get("/operations/{operation_id}")
def get_operation(operation_id: str):
    r=one("SELECT * FROM operations WHERE id=:id", {"id":operation_id})
    if not r: nf("Operation", operation_id)
    return r
@app.get("/operations/{operation_id}/first-pass-results")
def first_results(operation_id: str, include: bool|None=Query(default=None)):
    get_operation(operation_id); return {"results": many("SELECT * FROM operation_first_pass_results WHERE operation_id=:id AND (:include IS NULL OR include=:include) ORDER BY first_pass_prompt_score DESC, operator_priority_score DESC", {"id":operation_id,"include":include})}
@app.get("/operations/{operation_id}/second-pass-results")
def second_results(operation_id: str, include: bool|None=Query(default=None)):
    get_operation(operation_id); return {"results": many("SELECT * FROM operation_second_pass_results WHERE operation_id=:id AND (:include IS NULL OR include=:include) ORDER BY global_rank ASC NULLS LAST, prompt_score DESC", {"id":operation_id,"include":include})}
@app.get("/prompt-results/latest/first-pass")
def latest_first(prompt_id: str=Query(alias="promptId"), camera_group_id: str=Query(alias="cameraGroupId")): return {"results": many("SELECT * FROM latest_first_pass_results WHERE prompt_id=:pid AND camera_group_id=:gid ORDER BY first_pass_prompt_score DESC", {"pid":prompt_id,"gid":camera_group_id})}
@app.get("/prompt-results/latest/second-pass")
def latest_second(prompt_id: str=Query(alias="promptId"), camera_group_id: str=Query(alias="cameraGroupId")): return {"results": many("SELECT * FROM latest_second_pass_results WHERE prompt_id=:pid AND camera_group_id=:gid ORDER BY global_rank ASC NULLS LAST, prompt_score DESC", {"pid":prompt_id,"gid":camera_group_id})}

@app.get("/operator-queue")
def queue(status: str|None=None, limit:int=50, offset:int=0): return {"items": many("SELECT * FROM operator_queue_items WHERE (:status IS NULL OR status=:status) ORDER BY CASE status WHEN 'queued' THEN 0 WHEN 'acknowledged' THEN 1 WHEN 'completed' THEN 2 WHEN 'dismissed' THEN 3 ELSE 4 END, operator_priority_score DESC, prompt_score DESC, created_at ASC LIMIT :limit OFFSET :offset", {"status":status,"limit":limit,"offset":offset})}
@app.post("/operator-queue", status_code=201)
def create_queue_item(p: JsonObject):
    rid=p.get("secondPassResultId")
    if not rid: raise HTTPException(400, "secondPassResultId is required")
    r=one("INSERT INTO operator_queue_items (id,second_pass_result_id,operation_id,camera_id,camera_group_id,prompt_id,frame_ref_id,frame_url,prompt_score,operator_priority_score,operator_action,reason,status) SELECT COALESCE(NULLIF(:id,''),:new), id, operation_id, camera_id, camera_group_id, prompt_id, frame_ref_id, frame_url, prompt_score, operator_priority_score, operator_action, reason, COALESCE(:status,'queued') FROM operation_second_pass_results WHERE id=:rid ON CONFLICT (second_pass_result_id) DO UPDATE SET prompt_score=EXCLUDED.prompt_score, operator_priority_score=EXCLUDED.operator_priority_score, operator_action=EXCLUDED.operator_action, reason=EXCLUDED.reason, updated_at=now() RETURNING *", {"id":p.get("id"),"new":nid("queue"),"rid":rid,"status":p.get("status","queued")}, True)
    if not r: nf("Second pass result", rid)
    return r
@app.put("/operator-queue/{queue_item_id}")
def update_queue(queue_item_id: str, p: JsonObject):
    r=one("UPDATE operator_queue_items SET status=COALESCE(:status,status), operator_note=COALESCE(:note,operator_note), updated_at=now() WHERE id=:id RETURNING *", {"id":queue_item_id,"status":p.get("status"),"note":p.get("operatorNote")}, True)
    if not r: nf("Operator queue item", queue_item_id)
    return r

@app.get("/settings/gemini")
def gemini_settings(): return one("SELECT * FROM gemini_caller_settings WHERE id=true") or {}
@app.put("/settings/gemini")
def update_gemini_settings(p: JsonObject):
    return one("UPDATE gemini_caller_settings SET enabled=COALESCE(:enabled,enabled), continuous_scan_enabled=COALESCE(:cse,continuous_scan_enabled), continuous_scan_interval_seconds=COALESCE(:csis,continuous_scan_interval_seconds), gemini_call_delay_ms=COALESCE(:delay,gemini_call_delay_ms), max_cost_per_day=COALESCE(:day,max_cost_per_day), max_cost_per_month=COALESCE(:mon,max_cost_per_month), updated_at=now() WHERE id=true RETURNING *", {"enabled":p.get("enabled"),"cse":p.get("continuousScanEnabled"),"csis":p.get("continuousScanIntervalSeconds"),"delay":p.get("geminiCallDelayMs"),"day":p.get("maxCostPerDay"),"mon":p.get("maxCostPerMonth")}, True)
@app.get("/settings/usage-limits")
def usage_limits(): return one("SELECT * FROM usage_limit_settings WHERE id=true") or {}
@app.put("/settings/usage-limits")
def update_usage_limits(p: JsonObject): return one("UPDATE usage_limit_settings SET max_scans_per_day=COALESCE(:d,max_scans_per_day), max_scans_per_month=COALESCE(:m,max_scans_per_month), max_estimated_cost_per_day=COALESCE(:cd,max_estimated_cost_per_day), max_estimated_cost_per_month=COALESCE(:cm,max_estimated_cost_per_month), updated_at=now() WHERE id=true RETURNING *", {"d":p.get("maxScansPerDay"),"m":p.get("maxScansPerMonth"),"cd":p.get("maxEstimatedCostPerDay"),"cm":p.get("maxEstimatedCostPerMonth")}, True)
@app.get("/usage/summary")
def usage_summary(): return {"previousDay": one("SELECT COALESCE(sum(estimated_cost),0) AS cost, count(*) AS events FROM usage_events WHERE created_at >= now() - interval '1 day'") or {}, "monthToDate": one("SELECT COALESCE(sum(estimated_cost),0) AS cost, count(*) AS events FROM usage_events WHERE created_at >= now() - interval '30 days'") or {}}
@app.get("/debug/routes")
def routes(): return {"routes":[{"path":r.path,"name":r.name,"methods":sorted(r.methods or [])} for r in app.routes]}
