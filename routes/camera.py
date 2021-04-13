from fastapi import APIRouter
from controller import camera_helper
from model.camera import Configuration
from routes.root import can

router = APIRouter(prefix="/camera")


@router.get("/restart")
async def restart():
    try:
        can.stop_camera()
        can.start_camera()
        return {"message": "Camera has been restarted"}
    except Exception as e:
        return {"message": "Camera restart failed", "detail": str(e)}


@router.get("/settings")
async def get_camera_settings():
    settings = camera_helper.get_camera_settings()
    return settings


@router.patch("/settings")
async def configure_camera(configuration: Configuration = {}):
    configuration = configuration.dict(exclude_unset=True)

    if configuration:
        camera_helper.configure_camera(configuration)
    settings = camera_helper.get_camera_settings()
    return settings