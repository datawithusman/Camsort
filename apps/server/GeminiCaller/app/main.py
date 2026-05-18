from __future__ import annotations

import base64
import json
import os
import re
import time
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

import requests
from sqlalchemy import create_engine, text

JsonObject = dict[str, Any]


def db_url() -> str:
    u = os.getenv("DATABASE_URL")
    if not u:
        raise RuntimeError("DATABASE_URL is required")
    return u.replace("postgresql://", "postgresql+psycopg://", 1) if u.startswith("postgresql://") else u


engine = create_engine(db_url(), pool_pre_ping=True)


def nid(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def camel(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(x[:1].upper() + x[1:] for x in parts[1:])


def val(v: Any) -> Any:
    if isinstance(v, Decimal):
        return float(v)
    if isinstance(v, datetime):
        return v.isoformat().replace("+00:00", "Z")
    return v


def rd(row: Any) -> JsonObject | None:
    return None if row is None else {camel(k): val(v) for k, v in dict(row._mapping).items()}


def one(sql: str, p: JsonObject | None = None, commit: bool = False) -> JsonObject | None:
    with engine.connect() as c:
        r = c.execute(text(sql), p or {}).first()
        if commit:
            c.commit()
        return rd(r)


def many(sql: str, p: JsonObject | None = None) -> list[JsonObject]:
    with engine.connect() as c:
        return [rd(r) for r in c.execute(text(sql), p or {}).fetchall()]


def execsql(sql: str, p: JsonObject | None = None) -> None:
    with engine.connect() as c:
        c.execute(text(sql), p or {})
        c.commit()


def rest() -> str:
    return os.getenv("REST_API_BASE_URL", "http://rest-api:8080").rstrip("/")


def cambase() -> str:
    return os.getenv("CAMERA_SYSTEM_BASE_URL", "http://camera-system-mocker-rest-api:8080").rstrip("/")


def jget(url: str) -> JsonObject:
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    return r.json() if r.content else {}


def bget(url: str) -> tuple[bytes, str]:
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    return r.content, r.headers.get("content-type", "image/jpeg")


def img_url(p: str | None) -> str:
    if not p:
        raise RuntimeError("frame image URL is missing")
    if p.startswith("http"):
        return p
    if p.startswith("/camera-system/"):
        p = p[len("/camera-system") :]
    return cambase() + p


def env_first(*names: str, default: str = "") -> str:
    for name in names:
        value = os.getenv(name)
        if value is not None and value.strip() != "":
            return value.strip()
    return default


def gemini_api_url() -> str:
    return env_first("GEMINI_API_URL", "CAM_BOT_DEFAULT_GEMINI_API_URL")


def gemini_api_key() -> str:
    return env_first("GEMINI_API_KEY", "CAM_BOT_DEFAULT_GEMINI_API_KEY")


def gemini_timeout_seconds() -> float:
    raw = env_first("GEMINI_API_TIMEOUT_SECONDS", "CAM_BOT_DEFAULT_GEMINI_API_TIMEOUT_SECONDS", default="90")
    try:
        return float(raw)
    except ValueError:
        return 90.0


def extract_gemini_text(data: Any) -> str:
    if not isinstance(data, dict):
        raise RuntimeError(f"Gemini response was not an object: {type(data).__name__}")

    candidates = data.get("candidates") or []
    if candidates:
        content = candidates[0].get("content") or {}
        parts = content.get("parts") or []
        texts = [p.get("text", "") for p in parts if isinstance(p, dict) and p.get("text")]
        if texts:
            return "\n".join(texts).strip()

    if isinstance(data.get("text"), str):
        return data["text"].strip()
    if isinstance(data.get("result"), str):
        return data["result"].strip()
    if isinstance(data.get("result"), (dict, list)):
        return json.dumps(data["result"])

    raise RuntimeError(f"Gemini response did not contain text. Keys: {sorted(data.keys())}")


def parse_json_text(s: str) -> Any:
    s = s.strip()
    if s.startswith("```"):
        s = re.sub(r"^```(?:json)?\s*", "", s, flags=re.IGNORECASE)
        s = re.sub(r"\s*```$", "", s)
        s = s.strip()

    try:
        return json.loads(s)
    except json.JSONDecodeError:
        start_obj = s.find("{")
        start_arr = s.find("[")
        starts = [x for x in [start_obj, start_arr] if x >= 0]
        if not starts:
            raise
        start = min(starts)
        end = max(s.rfind("}"), s.rfind("]"))
        if end <= start:
            raise
        return json.loads(s[start : end + 1])


def gemini_generate(payload: JsonObject) -> Any:
    url = gemini_api_url()
    key = gemini_api_key()
    if not url or not key:
        raise RuntimeError("GEMINI_API_URL and GEMINI_API_KEY are required")

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": key,
    }

    r = requests.post(url, headers=headers, json=payload, timeout=gemini_timeout_seconds())
    if r.status_code >= 400:
        raise RuntimeError(f"Gemini HTTP {r.status_code}: {r.text[:1000]}")

    data = r.json()
    text_out = extract_gemini_text(data)
    return parse_json_text(text_out)


def clamp_score(v: Any) -> float:
    try:
        n = float(v)
    except (TypeError, ValueError):
        n = 0.0
    return max(0.0, min(100.0, n))


def first_pass(cam_id: str, prompt: str, b64: str, mime: str) -> JsonObject:
    instruction = f"""
You are analyzing one security camera snapshot.

Operator prompt:
{prompt}

Return JSON only with this exact shape:
{{
  "camId": "{cam_id}",
  "include": true,
  "firstPassPromptScore": 0,
  "operatorPriorityScore": 0,
  "operatorAction": "No immediate action.",
  "reason": "brief evidence-based reason"
}}

Rules:
- include must be a boolean.
- firstPassPromptScore and operatorPriorityScore must be numbers from 0 to 100.
- operatorAction should be concise and should not exaggerate beyond the image evidence.
- reason should describe visible evidence from the image.
""".strip()

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": instruction},
                    {"inline_data": {"mime_type": mime or "image/jpeg", "data": b64}},
                ],
            }
        ],
        "generationConfig": {
            "response_mime_type": "application/json",
        },
    }

    res = gemini_generate(payload)
    if not isinstance(res, dict):
        raise RuntimeError(f"Gemini first-pass response was not an object: {type(res).__name__}")

    return {
        "camId": str(res.get("camId") or cam_id),
        "include": bool(res.get("include", False)),
        "firstPassPromptScore": clamp_score(res.get("firstPassPromptScore", res.get("promptScore", 0))),
        "operatorPriorityScore": clamp_score(res.get("operatorPriorityScore", 0)),
        "operatorAction": str(res.get("operatorAction") or "No immediate action."),
        "reason": str(res.get("reason") or "No reason returned by Gemini."),
        "raw": res,
    }


def second_pass(prompt: str, rows: list[JsonObject]) -> list[JsonObject]:
    compact_rows = [
        {
            "camId": r["cameraId"],
            "firstPassResultId": r["id"],
            "include": r.get("include", False),
            "firstPassPromptScore": r.get("firstPassPromptScore") or 0,
            "operatorPriorityScore": r.get("operatorPriorityScore") or 0,
            "operatorAction": r.get("operatorAction") or "No immediate action.",
            "reason": r.get("reason") or "",
        }
        for r in rows
    ]

    instruction = f"""
You are ranking first-pass camera results for an operator.

Operator prompt:
{prompt}

First-pass results:
{json.dumps(compact_rows, ensure_ascii=False)}

Return JSON only with this exact shape:
{{
  "results": [
    {{
      "camId": "camera id",
      "firstPassResultId": "first pass result id",
      "include": true,
      "globalRank": 1,
      "promptScore": 0,
      "operatorPriorityScore": 0,
      "operatorAction": "No immediate action.",
      "reason": "brief reason"
    }}
  ]
}}

Rules:
- Rank the most relevant/highest-priority included cameras first.
- Use globalRank starting at 1.
- promptScore and operatorPriorityScore must be numbers from 0 to 100.
- Keep operatorAction concise and evidence-based.
""".strip()

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": instruction}],
            }
        ],
        "generationConfig": {
            "response_mime_type": "application/json",
        },
    }

    res = gemini_generate(payload)
    if isinstance(res, dict) and isinstance(res.get("results"), list):
        out = res["results"]
    elif isinstance(res, list):
        out = res
    else:
        raise RuntimeError(f"Gemini second-pass response had unexpected shape: {type(res).__name__}")

    normalized: list[JsonObject] = []
    for i, item in enumerate(out, 1):
        if not isinstance(item, dict):
            continue
        normalized.append(
            {
                "camId": str(item.get("camId") or ""),
                "firstPassResultId": str(item.get("firstPassResultId") or ""),
                "include": bool(item.get("include", True)),
                "globalRank": int(item.get("globalRank") or i),
                "promptScore": clamp_score(item.get("promptScore", 0)),
                "operatorPriorityScore": clamp_score(item.get("operatorPriorityScore", 0)),
                "operatorAction": str(item.get("operatorAction") or "No immediate action."),
                "reason": str(item.get("reason") or "No reason returned by Gemini."),
                "raw": item,
            }
        )
    return normalized


def settings() -> JsonObject:
    return one("SELECT * FROM gemini_caller_settings WHERE id=true") or {}


def next_op() -> JsonObject | None:
    op = one("SELECT * FROM operations WHERE status='queued' AND trigger='manual' ORDER BY created_at ASC LIMIT 1")
    if op:
        return op

    op = one("SELECT * FROM operations WHERE status='queued' AND trigger='scheduled' ORDER BY created_at ASC LIMIT 1")
    if op:
        return op

    s = settings()
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    if s.get("enabled") and s.get("continuousScanEnabled") and (
        not s.get("nextContinuousScanAt") or str(s.get("nextContinuousScanAt")) <= now
    ):
        for b in many("SELECT * FROM prompt_bindings WHERE enabled=true ORDER BY created_at"):
            g = one("SELECT * FROM camera_groups WHERE id=:id", {"id": b["cameraGroupId"]}) or {}
            cams = g.get("cameraIds") or []
            one(
                """
                INSERT INTO operations
                  (id,prompt_id,camera_group_id,prompt_binding_id,trigger,status,total_cameras,estimated_gemini_calls)
                VALUES
                  (:id,:pid,:gid,:bid,'scheduled','queued',:n,:calls)
                RETURNING *
                """,
                {
                    "id": nid("operation"),
                    "pid": b["promptId"],
                    "gid": b["cameraGroupId"],
                    "bid": b["id"],
                    "n": len(cams),
                    "calls": len(cams) + 1,
                },
                True,
            )
        execsql(
            """
            UPDATE gemini_caller_settings
            SET last_continuous_scan_at=now(),
                next_continuous_scan_at=now()+make_interval(secs=>continuous_scan_interval_seconds),
                updated_at=now()
            WHERE id=true
            """
        )
        return one("SELECT * FROM operations WHERE status='queued' AND trigger='scheduled' ORDER BY created_at ASC LIMIT 1")

    return None


def fail_operation(opid: str, message: str) -> None:
    execsql(
        """
        UPDATE operations
        SET status='failed',
            first_pass_status=CASE WHEN first_pass_status='running' THEN 'failed' ELSE first_pass_status END,
            second_pass_status=CASE WHEN second_pass_status='running' THEN 'failed' ELSE second_pass_status END,
            error_message=:msg,
            completed_at=now()
        WHERE id=:id
        """,
        {"id": opid, "msg": message[:2000]},
    )


def process(op: JsonObject) -> None:
    opid = op["id"]
    try:
        pr = one("SELECT * FROM saved_prompts WHERE id=:id", {"id": op["promptId"]})
        gr = one("SELECT * FROM camera_groups WHERE id=:id", {"id": op["cameraGroupId"]})
        if not pr or not gr:
            fail_operation(opid, "Missing prompt or group")
            return

        cams = gr.get("cameraIds") or []
        execsql(
            """
            UPDATE operations
            SET status='running',
                first_pass_status='running',
                started_at=COALESCE(started_at,now()),
                total_cameras=:n
            WHERE id=:id
            """,
            {"id": opid, "n": len(cams)},
        )

        delay = int(settings().get("geminiCallDelayMs") or 2000)
        rows: list[JsonObject] = []
        calls = 0
        errors: list[str] = []

        for i, cam_id in enumerate(cams, 1):
            try:
                snap = jget(f"{rest()}/camera-system/cameras/{cam_id}/snapshot")
                fr = snap.get("frameRef") or {}
                frame = snap.get("frame") or {}
                frame_url = frame.get("url") or fr.get("frameUrl")
                data, mime = bget(img_url(frame_url))

                res = first_pass(cam_id, pr["promptText"], base64.b64encode(data).decode(), mime)
                calls += 1

                row = one(
                    """
                    INSERT INTO operation_first_pass_results
                      (id,operation_id,camera_id,camera_group_id,prompt_id,frame_ref_id,frame_url,include,
                       first_pass_prompt_score,operator_priority_score,operator_action,reason,raw_model_json)
                    VALUES
                      (:id,:op,:cam,:gid,:pid,:fr,:url,:inc,:score,:prio,:act,:reason,CAST(:raw AS jsonb))
                    RETURNING *
                    """,
                    {
                        "id": nid("first-pass"),
                        "op": opid,
                        "cam": cam_id,
                        "gid": op["cameraGroupId"],
                        "pid": op["promptId"],
                        "fr": fr["id"],
                        "url": fr.get("frameUrl") or frame.get("url"),
                        "inc": res.get("include", False),
                        "score": res.get("firstPassPromptScore", res.get("promptScore", 0)),
                        "prio": res.get("operatorPriorityScore", 0),
                        "act": res.get("operatorAction") or "No immediate action.",
                        "reason": res.get("reason") or "",
                        "raw": json.dumps(res.get("raw", res)),
                    },
                    True,
                )
                if row is None:
                    raise RuntimeError("first-pass insert returned no row")
                rows.append(row)

                one(
                    """
                    INSERT INTO latest_first_pass_results
                      (prompt_id,camera_group_id,camera_id,operation_id,first_pass_result_id,frame_ref_id,frame_url,
                       include,first_pass_prompt_score,operator_priority_score,operator_action,reason)
                    VALUES
                      (:pid,:gid,:cam,:op,:rid,:fr,:url,:inc,:score,:prio,:act,:reason)
                    ON CONFLICT (prompt_id,camera_group_id,camera_id) DO UPDATE SET
                      operation_id=EXCLUDED.operation_id,
                      first_pass_result_id=EXCLUDED.first_pass_result_id,
                      frame_ref_id=EXCLUDED.frame_ref_id,
                      frame_url=EXCLUDED.frame_url,
                      include=EXCLUDED.include,
                      first_pass_prompt_score=EXCLUDED.first_pass_prompt_score,
                      operator_priority_score=EXCLUDED.operator_priority_score,
                      operator_action=EXCLUDED.operator_action,
                      reason=EXCLUDED.reason,
                      updated_at=now()
                    RETURNING prompt_id
                    """,
                    {
                        "pid": op["promptId"],
                        "gid": op["cameraGroupId"],
                        "cam": cam_id,
                        "op": opid,
                        "rid": row["id"],
                        "fr": row["frameRefId"],
                        "url": row["frameUrl"],
                        "inc": row["include"],
                        "score": row["firstPassPromptScore"],
                        "prio": row["operatorPriorityScore"],
                        "act": row["operatorAction"],
                        "reason": row["reason"],
                    },
                    True,
                )
            except Exception as e:
                msg = f"first pass error {cam_id} {e}"
                errors.append(msg)
                print(msg, flush=True)

            execsql(
                """
                UPDATE operations
                SET processed_cameras=:p,
                    first_pass_result_count=:c,
                    actual_gemini_calls=:calls
                WHERE id=:id
                """,
                {"p": i, "c": len(rows), "calls": calls, "id": opid},
            )
            if delay:
                time.sleep(delay / 1000)

        if not rows:
            fail_operation(opid, "; ".join(errors[-10:]) if errors else "No first-pass results were created")
            return

        execsql(
            "UPDATE operations SET first_pass_status='completed', second_pass_status='running' WHERE id=:id",
            {"id": opid},
        )

        ranked = second_pass(pr["promptText"], rows)
        calls += 1
        count = 0
        matched = 0

        for item in ranked:
            fp = next(
                (
                    r
                    for r in rows
                    if r["id"] == item.get("firstPassResultId") or r["cameraId"] == item.get("camId")
                ),
                None,
            )
            if not fp:
                continue

            inc = bool(item.get("include", True))
            matched += 1 if inc else 0
            row = one(
                """
                INSERT INTO operation_second_pass_results
                  (id,operation_id,camera_id,camera_group_id,prompt_id,first_pass_result_id,frame_ref_id,frame_url,
                   include,global_rank,prompt_score,operator_priority_score,operator_action,reason,raw_model_json)
                VALUES
                  (:id,:op,:cam,:gid,:pid,:fpid,:fr,:url,:inc,:rank,:score,:prio,:act,:reason,CAST(:raw AS jsonb))
                RETURNING *
                """,
                {
                    "id": nid("second-pass"),
                    "op": opid,
                    "cam": fp["cameraId"],
                    "gid": op["cameraGroupId"],
                    "pid": op["promptId"],
                    "fpid": fp["id"],
                    "fr": fp["frameRefId"],
                    "url": fp["frameUrl"],
                    "inc": inc,
                    "rank": item.get("globalRank"),
                    "score": item.get("promptScore", fp["firstPassPromptScore"]),
                    "prio": item.get("operatorPriorityScore", fp["operatorPriorityScore"]),
                    "act": item.get("operatorAction", fp["operatorAction"]),
                    "reason": item.get("reason", fp["reason"]),
                    "raw": json.dumps(item.get("raw", item)),
                },
                True,
            )
            if row is None:
                continue
            count += 1

            one(
                """
                INSERT INTO latest_second_pass_results
                  (prompt_id,camera_group_id,camera_id,operation_id,second_pass_result_id,first_pass_result_id,
                   frame_ref_id,frame_url,include,global_rank,prompt_score,operator_priority_score,operator_action,reason)
                VALUES
                  (:pid,:gid,:cam,:op,:rid,:fpid,:fr,:url,:inc,:rank,:score,:prio,:act,:reason)
                ON CONFLICT (prompt_id,camera_group_id,camera_id) DO UPDATE SET
                  operation_id=EXCLUDED.operation_id,
                  second_pass_result_id=EXCLUDED.second_pass_result_id,
                  first_pass_result_id=EXCLUDED.first_pass_result_id,
                  frame_ref_id=EXCLUDED.frame_ref_id,
                  frame_url=EXCLUDED.frame_url,
                  include=EXCLUDED.include,
                  global_rank=EXCLUDED.global_rank,
                  prompt_score=EXCLUDED.prompt_score,
                  operator_priority_score=EXCLUDED.operator_priority_score,
                  operator_action=EXCLUDED.operator_action,
                  reason=EXCLUDED.reason,
                  updated_at=now()
                RETURNING prompt_id
                """,
                {
                    "pid": op["promptId"],
                    "gid": op["cameraGroupId"],
                    "cam": row["cameraId"],
                    "op": opid,
                    "rid": row["id"],
                    "fpid": row["firstPassResultId"],
                    "fr": row["frameRefId"],
                    "url": row["frameUrl"],
                    "inc": row["include"],
                    "rank": row["globalRank"],
                    "score": row["promptScore"],
                    "prio": row["operatorPriorityScore"],
                    "act": row["operatorAction"],
                    "reason": row["reason"],
                },
                True,
            )

            if inc:
                one(
                    """
                    INSERT INTO operator_queue_items
                      (id,second_pass_result_id,operation_id,camera_id,camera_group_id,prompt_id,frame_ref_id,
                       frame_url,prompt_score,operator_priority_score,operator_action,reason,status)
                    VALUES
                      (:id,:rid,:op,:cam,:gid,:pid,:fr,:url,:score,:prio,:act,:reason,'queued')
                    ON CONFLICT (second_pass_result_id) DO UPDATE SET
                      prompt_score=EXCLUDED.prompt_score,
                      operator_priority_score=EXCLUDED.operator_priority_score,
                      operator_action=EXCLUDED.operator_action,
                      reason=EXCLUDED.reason,
                      updated_at=now()
                    RETURNING id
                    """,
                    {
                        "id": nid("queue"),
                        "rid": row["id"],
                        "op": opid,
                        "cam": row["cameraId"],
                        "gid": row["cameraGroupId"],
                        "pid": row["promptId"],
                        "fr": row["frameRefId"],
                        "url": row["frameUrl"],
                        "score": row["promptScore"],
                        "prio": row["operatorPriorityScore"],
                        "act": row["operatorAction"],
                        "reason": row["reason"],
                    },
                    True,
                )

        if count == 0:
            fail_operation(opid, "No second-pass results were created")
            return

        execsql(
            """
            UPDATE operations
            SET status='completed',
                second_pass_status='completed',
                second_pass_result_count=:c,
                matched_cameras=:m,
                actual_gemini_calls=:calls,
                completed_at=now()
            WHERE id=:id
            """,
            {"c": count, "m": matched, "calls": calls, "id": opid},
        )

        if op.get("promptBindingId"):
            execsql(
                "UPDATE prompt_bindings SET last_run_at=now(), updated_at=now() WHERE id=:id",
                {"id": op["promptBindingId"]},
            )

    except Exception as e:
        print("operation error", opid, e, flush=True)
        fail_operation(opid, str(e))


def main() -> None:
    print("GeminiCaller two-pass worker starting", flush=True)
    poll = float(env_first("WORKER_POLL_INTERVAL_SECONDS", "CAM_BOT_DEFAULT_BACKGROUND_WORKER_INTERVAL_S", default="5"))
    while True:
        try:
            op = next_op()
            process(op) if op else time.sleep(poll)
        except Exception as e:
            print("worker error", e, flush=True)
            time.sleep(poll)


if __name__ == "__main__":
    main()
