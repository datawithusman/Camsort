from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from fastapi import FastAPI


app = FastAPI(title="CamBot REST API")

JsonObject = dict[str, Any]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def check_camera_system() -> JsonObject:
    """
    Checks whether RestApi can reach the internal camera-system service.

    This is an internal pod-to-pod call:
      RestApi -> camera-system-mocker-rest-api

    It does not go through public nginx, so no Basic Auth is needed.
    """

    base_url = os.environ.get(
        "CAMERA_SYSTEM_BASE_URL",
        "http://camera-system-mocker-rest-api:8080",
    ).rstrip("/")

    url = f"{base_url}/health"

    try:
        request = Request(
            url,
            method="GET",
            headers={"Accept": "application/json"},
        )

        with urlopen(request, timeout=5) as response:
            return {
                "status": "ok",
                "url": url,
                "httpStatus": response.status,
            }

    except HTTPError as exc:
        return {
            "status": "error",
            "url": url,
            "httpStatus": exc.code,
            "error": str(exc),
        }

    except URLError as exc:
        return {
            "status": "error",
            "url": url,
            "httpStatus": None,
            "error": str(exc.reason),
        }

    except Exception as exc:
        return {
            "status": "error",
            "url": url,
            "httpStatus": None,
            "error": str(exc),
        }


def check_database() -> JsonObject:
    """
    Checks whether RestApi can reach Postgres.

    Requires:
      DATABASE_URL

    Example:
      postgresql://cambot:cambot@postgres:5432/cambot

    This uses psycopg directly for the health check because health checks should
    stay simple. The actual RestApi routes can use generated DB code/wrappers.
    """

    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        return {
            "status": "not_configured",
            "message": "DATABASE_URL is not set.",
        }

    try:
        import psycopg

        with psycopg.connect(database_url, connect_timeout=5) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                value = cursor.fetchone()[0]

        return {
            "status": "ok",
            "result": value,
        }

    except Exception as exc:
        return {
            "status": "error",
            "error": str(exc),
        }


@app.get("/health")
def health() -> JsonObject:
    database = check_database()
    camera_system = check_camera_system()

    status = "ok"

    if database["status"] == "error":
        status = "degraded"

    if camera_system["status"] != "ok":
        status = "degraded"

    return {
        "status": status,
        "service": "rest-api",
        "checkedAt": utc_now_iso(),
        "database": database,
        "cameraSystem": camera_system,
    }


@app.get("/camera-system/health")
def camera_system_health() -> JsonObject:
    return check_camera_system()


@app.get("/debug/routes")
def debug_routes() -> JsonObject:
    return {
        "routes": [
            {
                "path": route.path,
                "name": route.name,
                "methods": sorted(route.methods or []),
            }
            for route in app.routes
        ]
    }
