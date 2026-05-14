from __future__ import annotations

import base64
import json
import os
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


JsonObject = dict[str, Any]


class CameraSystemClientError(Exception):
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
    base_url: str
    username: str | None = None
    password: str | None = None
    timeout_seconds: float = 30.0

    @staticmethod
    def from_env() -> "CameraSystemClientConfig":
        return CameraSystemClientConfig(
            base_url=os.environ.get("CAMERA_SYSTEM_BASE_URL", "http://camera-system-mocker-rest-api:8080"),
            username=os.environ.get("CAMERA_SYSTEM_USERNAME"),
            password=os.environ.get("CAMERA_SYSTEM_PASSWORD"),
            timeout_seconds=float(os.environ.get("CAMERA_SYSTEM_TIMEOUT_SECONDS", "30")),
        )


class CameraSystemClient:
    """
    Small backend-facing wrapper for the external camera-system API.

    This wrapper intentionally hides generated-client/fetch/HTTP details from
    RestApi business logic.

    The camera-system mocker/current contract uses:

      GET /health
      GET /system/status
      GET /cameras
      GET /cameras/{cameraId}
      GET /cameras/{cameraId}/snapshot
      GET /cameras/{cameraId}/snapshot/image
      GET /cameras/{cameraId}/stream
      GET /camera-groups
      GET /camera-groups/{groupId}
      GET /camera-groups/{groupId}/cameras

    Snapshot behavior:
      - request_snapshot(camera_id) advances/selects the current snapshot.
      - get_latest_snapshot_image(camera_id) returns the current/latest image.
      - Historical snapshot lookup is intentionally not implemented.
    """

    def __init__(self, config: CameraSystemClientConfig) -> None:
        self.config = config
        self.base_url = config.base_url.rstrip("/")

    @staticmethod
    def from_env() -> "CameraSystemClient":
        return CameraSystemClient(CameraSystemClientConfig.from_env())

    def _auth_header(self) -> str | None:
        if not self.config.username or not self.config.password:
            return None

        raw = f"{self.config.username}:{self.config.password}".encode("utf-8")
        token = base64.b64encode(raw).decode("ascii")
        return f"Basic {token}"

    def _url(self, path: str, query: dict[str, str] | None = None) -> str:
        clean_path = path if path.startswith("/") else f"/{path}"
        url = f"{self.base_url}{clean_path}"

        if query:
            url = f"{url}?{urlencode(query)}"

        return url

    def _request(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, str] | None = None,
        accept: str = "application/json",
    ) -> Any:
        url = self._url(path, query=query)

        headers = {
            "Accept": accept,
        }

        auth_header = self._auth_header()
        if auth_header:
            headers["Authorization"] = auth_header

        request = Request(
            url,
            method=method.upper(),
            headers=headers,
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
        return self._request("GET", "/health")

    def system_status(self) -> JsonObject:
        return self._request("GET", "/system/status")

    def list_cameras(
        self,
        *,
        group_id: str | None = None,
        search: str | None = None,
    ) -> JsonObject:
        query: dict[str, str] = {}

        if group_id:
            query["groupId"] = group_id

        if search:
            query["search"] = search

        return self._request("GET", "/cameras", query=query or None)

    def get_camera(self, camera_id: str) -> JsonObject:
        return self._request("GET", f"/cameras/{quote(camera_id, safe='')}")

    def request_snapshot(self, camera_id: str) -> JsonObject:
        """
        Requests/advances the current snapshot for a camera.

        Returns CameraSnapshot metadata, including imageUrl.
        """
        return self._request("GET", f"/cameras/{quote(camera_id, safe='')}/snapshot")

    def get_latest_snapshot_image(self, camera_id: str) -> bytes:
        """
        Returns the current/latest snapshot image bytes.

        Call request_snapshot(camera_id) first if you want to advance the mocker
        before retrieving the image.
        """
        return self._request(
            "GET",
            f"/cameras/{quote(camera_id, safe='')}/snapshot/image",
            accept="image/*",
        )

    def get_stream(self, camera_id: str) -> JsonObject:
        return self._request("GET", f"/cameras/{quote(camera_id, safe='')}/stream")

    def list_camera_groups(self) -> JsonObject:
        return self._request("GET", "/camera-groups")

    def get_camera_group(self, group_id: str) -> JsonObject:
        return self._request("GET", f"/camera-groups/{quote(group_id, safe='')}")

    def list_cameras_for_group(self, group_id: str) -> JsonObject:
        return self._request("GET", f"/camera-groups/{quote(group_id, safe='')}/cameras")
