from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from camera_system_integrator_dtos.api.cameras_api import CamerasApi
from camera_system_integrator_dtos.api.snapshots_api import SnapshotsApi
from camera_system_integrator_dtos.api.source_camera_groups_api import SourceCameraGroupsApi
from camera_system_integrator_dtos.api.streams_api import StreamsApi
from camera_system_integrator_dtos.api.system_api import SystemApi
from camera_system_integrator_dtos.api_client import ApiClient
from camera_system_integrator_dtos.configuration import Configuration
from camera_system_integrator_dtos.exceptions import ApiException


JsonObject = dict[str, Any]


class CameraSystemClientError(Exception):
    """
    Error raised when the camera-system API request fails.

    The FastAPI app should catch this wrapper exception instead of leaking
    generated OpenAPI-client exception types into route handlers.
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
    Configuration for internal RestApi -> Camera System calls.

    This wrapper uses the generated Python OpenAPI client from:

      backend/camera_system_integrator/camera_system_integrator_dtos

    Do not add duplicated DTO definitions in app/. The generated OpenAPI DTOs
    are the source of truth for external camera-system response shapes.
    """

    base_url: str
    timeout_seconds: float = 30.0

    @staticmethod
    def from_env() -> "CameraSystemClientConfig":
        return CameraSystemClientConfig(
            base_url=os.environ.get(
                "CAMERA_SYSTEM_BASE_URL",
                "http://camera-system-mocker-rest-api:8080",
            ).rstrip("/"),
            timeout_seconds=float(
                os.environ.get("CAMERA_SYSTEM_TIMEOUT_SECONDS", "30")
            ),
        )


def _to_json_value(value: Any) -> Any:
    """
    Convert generated OpenAPI DTOs/Pydantic models into FastAPI-safe JSON data.

    Generated DTOs stay in backend/. This wrapper normalizes those DTOs to plain
    dict/list/scalar values at the boundary so route handlers do not depend on a
    second handwritten DTO layer.
    """
    if value is None:
        return None

    if isinstance(value, (str, int, float, bool)):
        return value

    if isinstance(value, (datetime, date)):
        return value.isoformat().replace("+00:00", "Z")

    if isinstance(value, list):
        return [_to_json_value(item) for item in value]

    if isinstance(value, tuple):
        return [_to_json_value(item) for item in value]

    if isinstance(value, dict):
        return {
            str(key): _to_json_value(item)
            for key, item in value.items()
            if item is not None
        }

    if hasattr(value, "to_dict"):
        return _to_json_value(value.to_dict())

    if hasattr(value, "model_dump"):
        return _to_json_value(
            value.model_dump(by_alias=True, exclude_none=True)
        )

    return value


def _model_to_json_dict(value: Any) -> JsonObject:
    normalized = _to_json_value(value)
    if normalized is None:
        return {}
    if isinstance(normalized, dict):
        return normalized
    raise CameraSystemClientError(
        f"Expected camera-system response object, got {type(value).__name__}"
    )


class CameraSystemClient:
    """
    Thin, stable wrapper over the generated Camera System Integrator client.

    Snapshot model:
      GET /cameras/{cameraId}/snapshot returns JSON metadata containing a
      frame URL. It does not return raw image bytes.

    Frame model:
      The camera-system/mocker owns image serving. RestApi stores only the
      returned frame URL/reference in Postgres when it wants auditability.
    """

    def __init__(self, config: CameraSystemClientConfig) -> None:
        self.config = config
        self.base_url = config.base_url.rstrip("/")

        generated_config = Configuration(host=self.base_url)
        self._api_client = ApiClient(generated_config)

        self._cameras = CamerasApi(self._api_client)
        self._snapshots = SnapshotsApi(self._api_client)
        self._streams = StreamsApi(self._api_client)
        self._system = SystemApi(self._api_client)
        self._groups = SourceCameraGroupsApi(self._api_client)

    @staticmethod
    def from_env() -> "CameraSystemClient":
        return CameraSystemClient(CameraSystemClientConfig.from_env())

    def _timeout(self) -> float:
        return self.config.timeout_seconds

    def _url(self, path: str) -> str:
        clean_path = path if path.startswith("/") else f"/{path}"
        return f"{self.base_url}{clean_path}"

    def _wrap_generated_error(self, exc: ApiException) -> CameraSystemClientError:
        body: Any = exc.body
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                pass

        return CameraSystemClientError(
            f"Camera system request failed: {exc.status}",
            status_code=exc.status,
            body=body,
        )

    def _call(self, callback: Callable[[], Any]) -> JsonObject:
        try:
            return _model_to_json_dict(callback())
        except CameraSystemClientError:
            raise
        except ApiException as exc:
            raise self._wrap_generated_error(exc) from exc
        except Exception as exc:
            raise CameraSystemClientError(
                f"Camera system request failed: {exc}",
                status_code=None,
                body=None,
            ) from exc

    def health(self) -> JsonObject:
        """
        Calls GET /health.

        The generated integrator OpenAPI client covers system status, but the
        mocker also has a simple /health endpoint. This remains a lightweight
        operational probe.
        """
        url = self._url("/health")

        try:
            request = Request(
                url,
                method="GET",
                headers={"Accept": "application/json"},
            )

            with urlopen(request, timeout=min(self.config.timeout_seconds, 5)) as response:
                raw = response.read()
                if raw:
                    try:
                        body = json.loads(raw.decode("utf-8"))
                    except json.JSONDecodeError:
                        body = {"body": raw.decode("utf-8", errors="replace")}
                else:
                    body = {}

                return {
                    "status": "ok",
                    "url": url,
                    "httpStatus": response.status,
                    **body,
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

    def system_status(self) -> JsonObject:
        return self._call(
            lambda: self._system.get_camera_system_status(
                _request_timeout=self._timeout(),
            )
        )

    def list_cameras(
        self,
        *,
        group_id: str | None = None,
        search: str | None = None,
    ) -> JsonObject:
        return self._call(
            lambda: self._cameras.list_integrator_cameras(
                group_id=group_id,
                search=search,
                _request_timeout=self._timeout(),
            )
        )

    def get_camera(self, camera_id: str) -> JsonObject:
        return self._call(
            lambda: self._cameras.get_integrator_camera(
                camera_id,
                _request_timeout=self._timeout(),
            )
        )

    def get_snapshot(self, camera_id: str) -> JsonObject:
        return self._call(
            lambda: self._snapshots.get_camera_snapshot(
                camera_id,
                _request_timeout=self._timeout(),
            )
        )

    def request_snapshot(self, camera_id: str) -> JsonObject:
        """
        Backward-compatible name. Returns metadata, not image bytes.
        """
        return self.get_snapshot(camera_id)

    def get_frame_url(self, camera_id: str, frame_id: str) -> JsonObject:
        return self._call(
            lambda: self._snapshots.get_camera_frame_url(
                camera_id,
                frame_id,
                _request_timeout=self._timeout(),
            )
        )

    def get_stream(self, camera_id: str) -> JsonObject:
        return self._call(
            lambda: self._streams.get_camera_stream(
                camera_id,
                _request_timeout=self._timeout(),
            )
        )

    def list_camera_groups(self) -> JsonObject:
        return self._call(
            lambda: self._groups.list_integrator_camera_groups(
                _request_timeout=self._timeout(),
            )
        )

    def get_camera_group(self, group_id: str) -> JsonObject:
        return self._call(
            lambda: self._groups.get_integrator_camera_group(
                group_id,
                _request_timeout=self._timeout(),
            )
        )

    def list_cameras_for_group(self, group_id: str) -> JsonObject:
        return self._call(
            lambda: self._groups.list_integrator_camera_group_cameras(
                group_id,
                _request_timeout=self._timeout(),
            )
        )
