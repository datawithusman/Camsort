from fastapi import FastAPI, HTTPException
from fastapi.responses import Response

app = FastAPI(title="CamBot CameraSystemMockerRestApi")

CAMERAS = [
    {
        "id": "CAM-014",
        "name": "North Gate Camera",
        "location": "North Gate",
        "status": "active",
        "snapshotUrl": "/cam/cameras/CAM-014/snapshot.jpg",
        "tags": ["outdoor", "gate"],
    },
    {
        "id": "CAM-006",
        "name": "Warehouse Interior",
        "location": "Warehouse",
        "status": "active",
        "snapshotUrl": "/cam/cameras/CAM-006/snapshot.jpg",
        "tags": ["indoor", "warehouse"],
    },
]

JPEG_BYTES = bytes.fromhex(
    "ffd8ffe000104a46494600010101006000600000ffdb0043000302020302020303030304030304050805050404050a070706080c0a0c0c0b0a0b0b0d0e12100d0e110e0b0b1016101113141515150c0f171816141812141514ffdb00430103040405040509050509140d0b0d141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414ffc00011080001000103012200021101031101ffc4001400010000000000000000000000000000000000000008ffc4001410010000000000000000000000000000000000000000ffda000c03010002110311003f00b2c001ffd9"
)

@app.get("/cam/health")
def health():
    return {"status": "ok"}

@app.get("/cam/cameras")
def list_cameras():
    return {"cameras": CAMERAS}

@app.get("/cam/cameras/{camera_id}")
def get_camera(camera_id: str):
    for camera in CAMERAS:
        if camera["id"] == camera_id:
            return camera
    raise HTTPException(status_code=404, detail="camera not found")

@app.get("/cam/cameras/{camera_id}/snapshot.jpg")
def get_snapshot(camera_id: str):
    if not any(camera["id"] == camera_id for camera in CAMERAS):
        raise HTTPException(status_code=404, detail="snapshot not found")
    return Response(content=JPEG_BYTES, media_type="image/jpeg")
