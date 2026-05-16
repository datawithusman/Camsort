from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


CameraStatus = Literal["online", "offline", "unknown"]
CameraSystemHealthStatus = Literal["healthy", "degraded", "unavailable"]
StreamType = Literal["rtsp", "hls", "webrtc", "mjpeg", "unknown"]

JsonObject = dict[str, Any]


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _optional_int(value: Any) -> int | None:
    if value is None:
        return None
    return int(value)


def _dict(value: Any) -> JsonObject:
    return value if isinstance(value, dict) else {}


def _list_of_str(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


@dataclass(frozen=True)
class CameraSystemStatusDto:
    """
    App-facing DTO for camera-system health/status.

    Expected JSON shape:

      {
        "status": "healthy",
        "checkedAt": "...",
        "cameraCount": 50,
        "onlineCameraCount": 50,
        "message": "..."
      }
    """

    status: CameraSystemHealthStatus
    checked_at: str
    camera_count: int | None = None
    online_camera_count: int | None = None
    message: str | None = None

    @staticmethod
    def from_json(data: JsonObject) -> "CameraSystemStatusDto":
        return CameraSystemStatusDto(
            status=data.get("status", "unavailable"),
            checked_at=str(data.get("checkedAt", "")),
            camera_count=_optional_int(data.get("cameraCount")),
            online_camera_count=_optional_int(data.get("onlineCameraCount")),
            message=_optional_str(data.get("message")),
        )

    def to_json(self) -> JsonObject:
        return {
            "status": self.status,
            "checkedAt": self.checked_at,
            "cameraCount": self.camera_count,
            "onlineCameraCount": self.online_camera_count,
            "message": self.message,
        }


@dataclass(frozen=True)
class CameraSystemCameraDto:
    """
    App-facing DTO for a source camera from the external camera system.

    This is not a CamBot operational camera group. This is the source camera
    exposed by the camera-system integrator/mocker.
    """

    id: str
    name: str
    description: str | None = None
    location: str | None = None
    group_ids: list[str] = field(default_factory=list)
    status: CameraStatus = "unknown"
    stream_available: bool = False
    snapshot_available: bool = False
    vendor_metadata: JsonObject = field(default_factory=dict)

    @staticmethod
    def from_json(data: JsonObject) -> "CameraSystemCameraDto":
        return CameraSystemCameraDto(
            id=str(data.get("id", "")),
            name=str(data.get("name", "")),
            description=_optional_str(data.get("description")),
            location=_optional_str(data.get("location")),
            group_ids=_list_of_str(data.get("groupIds")),
            status=data.get("status", "unknown"),
            stream_available=bool(data.get("streamAvailable", False)),
            snapshot_available=bool(data.get("snapshotAvailable", False)),
            vendor_metadata=_dict(data.get("vendorMetadata")),
        )

    def to_json(self) -> JsonObject:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "location": self.location,
            "groupIds": self.group_ids,
            "status": self.status,
            "streamAvailable": self.stream_available,
            "snapshotAvailable": self.snapshot_available,
            "vendorMetadata": self.vendor_metadata,
        }


@dataclass(frozen=True)
class CameraSystemCameraListDto:
    """
    App-facing DTO for listing source cameras.
    """

    cameras: list[CameraSystemCameraDto]

    @staticmethod
    def from_json(data: JsonObject) -> "CameraSystemCameraListDto":
        raw_cameras = data.get("cameras", [])
        if not isinstance(raw_cameras, list):
            raw_cameras = []

        return CameraSystemCameraListDto(
            cameras=[
                CameraSystemCameraDto.from_json(item)
                for item in raw_cameras
                if isinstance(item, dict)
            ]
        )

    def to_json(self) -> JsonObject:
        return {
            "cameras": [camera.to_json() for camera in self.cameras],
        }


@dataclass(frozen=True)
class CameraSystemGroupDto:
    """
    App-facing DTO for a source camera-system group.

    This is not the same thing as a CamBot operational CameraGroup.
    """

    id: str
    name: str
    description: str | None = None
    parent_group_id: str | None = None
    camera_ids: list[str] = field(default_factory=list)
    child_group_ids: list[str] = field(default_factory=list)
    vendor_metadata: JsonObject = field(default_factory=dict)

    @staticmethod
    def from_json(data: JsonObject) -> "CameraSystemGroupDto":
        return CameraSystemGroupDto(
            id=str(data.get("id", "")),
            name=str(data.get("name", "")),
            description=_optional_str(data.get("description")),
            parent_group_id=_optional_str(data.get("parentGroupId")),
            camera_ids=_list_of_str(data.get("cameraIds")),
            child_group_ids=_list_of_str(data.get("childGroupIds")),
            vendor_metadata=_dict(data.get("vendorMetadata")),
        )

    def to_json(self) -> JsonObject:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "parentGroupId": self.parent_group_id,
            "cameraIds": self.camera_ids,
            "childGroupIds": self.child_group_ids,
            "vendorMetadata": self.vendor_metadata,
        }


@dataclass(frozen=True)
class CameraSystemGroupListDto:
    """
    App-facing DTO for listing source camera-system groups.
    """

    groups: list[CameraSystemGroupDto]

    @staticmethod
    def from_json(data: JsonObject) -> "CameraSystemGroupListDto":
        raw_groups = data.get("groups", [])
        if not isinstance(raw_groups, list):
            raw_groups = []

        return CameraSystemGroupListDto(
            groups=[
                CameraSystemGroupDto.from_json(item)
                for item in raw_groups
                if isinstance(item, dict)
            ]
        )

    def to_json(self) -> JsonObject:
        return {
            "groups": [group.to_json() for group in self.groups],
        }


@dataclass(frozen=True)
class CameraStreamDto:
    """
    App-facing DTO for a source camera stream descriptor.

    The current mocker does not provide a real stream, but the wrapper supports
    the endpoint so RestApi can consume a real camera system later.
    """

    camera_id: str
    stream_type: StreamType | None = None
    stream_url: str | None = None
    expires_at: str | None = None

    @staticmethod
    def from_json(data: JsonObject) -> "CameraStreamDto":
        return CameraStreamDto(
            camera_id=str(data.get("cameraId", "")),
            stream_type=_optional_str(data.get("streamType")),
            stream_url=_optional_str(data.get("streamUrl")),
            expires_at=_optional_str(data.get("expiresAt")),
        )

    def to_json(self) -> JsonObject:
        return {
            "cameraId": self.camera_id,
            "streamType": self.stream_type,
            "streamUrl": self.stream_url,
            "expiresAt": self.expires_at,
        }


@dataclass(frozen=True)
class CameraFrameMetadataDto:
    """
    Metadata for a frame owned by the camera-system mocker/integrator.

    The URL points to the image resource. The raw image bytes are not embedded
    in the snapshot response and should not be stored in Postgres.
    """

    frame_id: str
    sequence_number: int
    captured_at: str
    url: str
    mime_type: str = "image/jpeg"
    width: int | None = None
    height: int | None = None
    expires_at: str | None = None

    @staticmethod
    def from_json(data: JsonObject) -> "CameraFrameMetadataDto":
        return CameraFrameMetadataDto(
            frame_id=str(data.get("frameId", "")),
            sequence_number=int(data.get("sequenceNumber", 0) or 0),
            captured_at=str(data.get("capturedAt", "")),
            url=str(data.get("url", "")),
            mime_type=str(data.get("mimeType", "image/jpeg")),
            width=_optional_int(data.get("width")),
            height=_optional_int(data.get("height")),
            expires_at=_optional_str(data.get("expiresAt")),
        )

    def to_json(self) -> JsonObject:
        return {
            "frameId": self.frame_id,
            "sequenceNumber": self.sequence_number,
            "capturedAt": self.captured_at,
            "url": self.url,
            "mimeType": self.mime_type,
            "width": self.width,
            "height": self.height,
            "expiresAt": self.expires_at,
        }


@dataclass(frozen=True)
class CameraSnapshotDto:
    """
    Snapshot metadata response for GET /cameras/{cameraId}/snapshot.
    """

    snapshot_id: str
    camera_id: str
    frame: CameraFrameMetadataDto

    @staticmethod
    def from_json(data: JsonObject) -> "CameraSnapshotDto":
        frame = data.get("frame")
        if not isinstance(frame, dict):
            frame = {}

        return CameraSnapshotDto(
            snapshot_id=str(data.get("snapshotId", "")),
            camera_id=str(data.get("cameraId", "")),
            frame=CameraFrameMetadataDto.from_json(frame),
        )

    def to_json(self) -> JsonObject:
        return {
            "snapshotId": self.snapshot_id,
            "cameraId": self.camera_id,
            "frame": self.frame.to_json(),
        }


@dataclass(frozen=True)
class CameraFrameUrlResponseDto:
    """
    Response for GET /cameras/{cameraId}/frames/{frameId}/url.
    """

    camera_id: str
    frame_id: str
    url: str
    mime_type: str = "image/jpeg"
    expires_at: str | None = None

    @staticmethod
    def from_json(data: JsonObject) -> "CameraFrameUrlResponseDto":
        return CameraFrameUrlResponseDto(
            camera_id=str(data.get("cameraId", "")),
            frame_id=str(data.get("frameId", "")),
            url=str(data.get("url", "")),
            mime_type=str(data.get("mimeType", "image/jpeg")),
            expires_at=_optional_str(data.get("expiresAt")),
        )

    def to_json(self) -> JsonObject:
        return {
            "cameraId": self.camera_id,
            "frameId": self.frame_id,
            "url": self.url,
            "mimeType": self.mime_type,
            "expiresAt": self.expires_at,
        }
