from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from app.dtos.camera_system import (
    CameraFrameUrlResponseDto,
    CameraSnapshotDto,
    CameraStreamDto,
    CameraSystemCameraDto,
    CameraSystemCameraListDto,
    CameraSystemGroupDto,
    CameraSystemGroupListDto,
    CameraSystemStatusDto,
)


JsonObject = dict[str, Any]


class CameraSystemClientError(Exception):
    """
    Error raised when the camera-system API request fails.

    This wrapper raises CameraSystemClientError for:
      - HTTP 4xx/5xx responses
      - network failures
      - malformed/unexpected response bodies

    Attributes:
      status_code:
        HTTP status code, or None for network/client-side failures.

      body:
        Parsed JSON error body when available, otherwise text/None.

      url:
        Full URL that failed.
    """

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        body: Any = None,
        url: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.body = body
        self.url = url


@dataclass(frozen=True)
class CameraSystemClientConfig:
    """
    Configuration for internal RestApi -> CameraSystem calls.

    Important:
      This config is for internal pod-to-pod calls.

      Public browser calls go through nginx:
        https://host/camera-system/...

      Internal RestApi calls should go directly to the service:
        http://camera-system-mocker-rest-api:8080

      Because nginx owns public authentication, this internal wrapper does not
      send Basic Auth.

    Environment:
      CAMERA_SYSTEM_BASE_URL:
        Base URL for the internal camera-system service.

      CAMERA_SYSTEM_TIMEOUT_SECONDS:
        HTTP timeout for camera-system calls.
    """

    base_url: str
    timeout_seconds: float = 30.0

    @staticmethod
    def from_env() -> "CameraSystemClientConfig":
        return CameraSystemClientConfig(
            base_url=os.environ.get(
                "CAMERA_SYSTEM_BASE_URL",
                "http://camera-system-mocker-rest-api:8080",
            ),
            timeout_seconds=float(
                os.environ.get("CAMERA_SYSTEM_TIMEOUT_SECONDS", "30")
            ),
        )


class CameraSystemClient:
    """
    Backend-facing wrapper around the Camera System Integrator API.

    This is handwritten application code. It should live under app/clients, not
    under backend/, because backend/ is generated code and may be recreated.

    Snapshot model:
      GET /cameras/{cameraId}/snapshot returns metadata for the current frame,
      including a URL pointing at the actual image resource.

      GET /cameras/{cameraId}/frames/{frameId}/url resolves a stored frameId
      back to its URL.
    """

    def __init__(self, config: CameraSystemClientConfig) -> None:
        self.config = config
        self.base_url = config.base_url.rstrip("/")

    @staticmethod
    def from_env() -> "CameraSystemClient":
        return CameraSystemClient(CameraSystemClientConfig.from_env())

    def _url(self, path: str, query: dict[str, str] | None = None) -> str:
        clean_path = path if path.startswith("/") else f"/{path}"
        url = f"{self.base_url}{clean_path}"

        if query:
            url = f"{url}?{urlencode(query)}"

        return url

    def _request_json(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, str] | None = None,
    ) -> JsonObject:
        body = self._request(
            method,
            path,
            query=query,
            accept="application/json",
        )

        if body is None:
            return {}

        if not isinstance(body, dict):
            raise CameraSystemClientError(
                "Camera system returned a non-object JSON response.",
                status_code=None,
                body=body,
                url=self._url(path, query=query),
            )

        return body

    def _request_bytes(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, str] | None = None,
        accept: str = "application/octet-stream",
    ) -> bytes:
        body = self._request(
            method,
            path,
            query=query,
            accept=accept,
        )

        if isinstance(body, bytes):
            return body

        raise CameraSystemClientError(
            "Camera system returned a non-bytes response.",
            status_code=None,
            body=body,
            url=self._url(path, query=query),
        )

    def _request(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, str] | None = None,
        accept: str = "application/json",
    ) -> Any:
        url = self._url(path, query=query)

        request = Request(
            url,
            method=method.upper(),
            headers={
                "Accept": accept,
            },
        )

        try:
            with urlopen(request, timeout=self.config.timeout_seconds) as response:
                content_type = response.headers.get("content-type", "")
                raw_body = response.read()

                if "application/json" in content_type:
                    if not raw_body:
                        return None

                    return json.loads(raw_body.decode("utf-8"))

                return raw_body

        except HTTPError as exc:
            body = self._read_error_body(exc)
            raise CameraSystemClientError(
                f"Camera system request failed: {exc.code}",
                status_code=exc.code,
                body=body,
                url=url,
            ) from exc

        except URLError as exc:
            raise CameraSystemClientError(
                f"Camera system request failed: {exc.reason}",
                status_code=None,
                body=None,
                url=url,
            ) from exc

        except json.JSONDecodeError as exc:
            raise CameraSystemClientError(
                "Camera system returned invalid JSON.",
                status_code=None,
                body=None,
                url=url,
            ) from exc

    @staticmethod
    def _read_error_body(exc: HTTPError) -> Any:
        try:
            raw = exc.read()
            if not raw:
                return None

            text = raw.decode("utf-8", errors="replace")
            content_type = exc.headers.get("content-type", "")

            if "application/json" in content_type:
                return json.loads(text)

            return text
        except Exception:
            return None

    def health(self) -> JsonObject:
        """
        Calls GET /health.

        Returns raw health JSON because this is mostly a debug/ops endpoint.
        """
        return self._request_json("GET", "/health")

    def system_status(self) -> CameraSystemStatusDto:
        """
        Calls GET /system/status.
        """
        data = self._request_json("GET", "/system/status")
        return CameraSystemStatusDto.from_json(data)

    def list_cameras(
        self,
        *,
        group_id: str | None = None,
        search: str | None = None,
    ) -> CameraSystemCameraListDto:
        """
        Calls GET /cameras.
        """
        query: dict[str, str] = {}

        if group_id:
            query["groupId"] = group_id

        if search:
            query["search"] = search

        data = self._request_json("GET", "/cameras", query=query or None)
        return CameraSystemCameraListDto.from_json(data)

    def get_camera(self, camera_id: str) -> CameraSystemCameraDto:
        """
        Calls GET /cameras/{cameraId}.
        """
        data = self._request_json(
            "GET",
            f"/cameras/{quote(camera_id, safe='')}",
        )
        return CameraSystemCameraDto.from_json(data)

    def get_snapshot(self, camera_id: str) -> CameraSnapshotDto:
        """
        Calls GET /cameras/{cameraId}/snapshot.

        Returns snapshot metadata including frame.url.
        """
        data = self._request_json(
            "GET",
            f"/cameras/{quote(camera_id, safe='')}/snapshot",
        )
        return CameraSnapshotDto.from_json(data)

    def request_snapshot(self, camera_id: str) -> CameraSnapshotDto:
        """
        Backward-compatible alias for get_snapshot().
        """
        return self.get_snapshot(camera_id)

    def get_frame_url(self, camera_id: str, frame_id: str) -> CameraFrameUrlResponseDto:
        """
        Calls GET /cameras/{cameraId}/frames/{frameId}/url.
        """
        data = self._request_json(
            "GET",
            (
                f"/cameras/{quote(camera_id, safe='')}"
                f"/frames/{quote(frame_id, safe='')}/url"
            ),
        )
        return CameraFrameUrlResponseDto.from_json(data)

    def get_frame_image(self, camera_id: str, frame_id: str) -> bytes:
        """
        Calls GET /cameras/{cameraId}/frames/{frameId}/image.
        """
        return self._request_bytes(
            "GET",
            (
                f"/cameras/{quote(camera_id, safe='')}"
                f"/frames/{quote(frame_id, safe='')}/image"
            ),
            accept="image/*",
        )

    def get_snapshot_image(self, camera_id: str) -> bytes:
        """
        Compatibility helper: requests snapshot metadata, then fetches frame bytes.
        """
        snapshot = self.get_snapshot(camera_id)
        return self.get_frame_image(camera_id, snapshot.frame.frame_id)

    def get_stream(self, camera_id: str) -> CameraStreamDto:
        """
        Calls GET /cameras/{cameraId}/stream.
        """
        data = self._request_json(
            "GET",
            f"/cameras/{quote(camera_id, safe='')}/stream",
        )
        return CameraStreamDto.from_json(data)

    def list_camera_groups(self) -> CameraSystemGroupListDto:
        """
        Calls GET /camera-groups.
        """
        data = self._request_json("GET", "/camera-groups")
        return CameraSystemGroupListDto.from_json(data)

    def get_camera_group(self, group_id: str) -> CameraSystemGroupDto:
        """
        Calls GET /camera-groups/{groupId}.
        """
        data = self._request_json(
            "GET",
            f"/camera-groups/{quote(group_id, safe='')}",
        )
        return CameraSystemGroupDto.from_json(data)

    def list_cameras_for_group(self, group_id: str) -> CameraSystemCameraListDto:
        """
        Calls GET /camera-groups/{groupId}/cameras.
        """
        data = self._request_json(
            "GET",
            f"/camera-groups/{quote(group_id, safe='')}/cameras",
        )
        return CameraSystemCameraListDto.from_json(data)
