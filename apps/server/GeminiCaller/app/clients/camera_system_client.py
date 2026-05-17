from __future__ import annotations

import os
from typing import Any

import requests


class CameraSystemClientError(RuntimeError):
    def __init__(self, message: str, *, url: str | None = None, status_code: int | None = None, body: Any = None):
        super().__init__(message)
        self.url = url
        self.status_code = status_code
        self.body = body


class CameraSystemClient:
    def __init__(self, base_url: str, timeout_seconds: float = 20.0):
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    @classmethod
    def from_env(cls) -> "CameraSystemClient":
        return cls(
            base_url=os.environ.get("CAMERA_SYSTEM_BASE_URL", "http://camera-system-mocker-rest-api:8080"),
            timeout_seconds=float(os.environ.get("CAMERA_SYSTEM_TIMEOUT_SECONDS", "20")),
        )

    def _request_json(self, method: str, path: str, **kwargs) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        try:
            response = requests.request(method, url, timeout=self.timeout_seconds, **kwargs)
        except requests.RequestException as exc:
            raise CameraSystemClientError(str(exc), url=url) from exc

        if response.status_code >= 400:
            try:
                body = response.json()
            except Exception:
                body = response.text
            raise CameraSystemClientError(
                f"Camera system returned HTTP {response.status_code}",
                url=url,
                status_code=response.status_code,
                body=body,
            )

        try:
            return response.json()
        except ValueError as exc:
            raise CameraSystemClientError("Camera system returned non-JSON response", url=url, body=response.text) from exc

    def _request_bytes(self, method: str, path: str, **kwargs) -> tuple[bytes, str]:
        url = f"{self.base_url}{path}"
        try:
            response = requests.request(method, url, timeout=self.timeout_seconds, **kwargs)
        except requests.RequestException as exc:
            raise CameraSystemClientError(str(exc), url=url) from exc

        if response.status_code >= 400:
            raise CameraSystemClientError(
                f"Camera system returned HTTP {response.status_code}",
                url=url,
                status_code=response.status_code,
                body=response.text,
            )
        return response.content, response.headers.get("content-type", "image/jpeg")

    def get_snapshot(self, camera_id: str) -> dict[str, Any]:
        return self._request_json("GET", f"/cameras/{camera_id}/snapshot")

    def get_frame_image(self, frame_url: str) -> tuple[bytes, str]:
        # Snapshot frame URLs are intentionally path-only, such as
        # /camera-system/cameras/cam01/frames/... when exposed through nginx.
        # Internally the camera system service serves the same resource without
        # the /camera-system reverse-proxy prefix.
        path = frame_url
        if path.startswith("/camera-system/"):
            path = path[len("/camera-system"):]
        if not path.startswith("/"):
            path = f"/{path}"
        return self._request_bytes("GET", path)
